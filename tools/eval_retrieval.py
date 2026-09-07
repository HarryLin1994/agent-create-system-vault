#!/usr/bin/env python3
"""Run golden-question retrieval evals from knowledge pack notes."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

from agent_retrieve import (
    RELIABILITY_RANK,
    retrieve,
    split_frontmatter,
)


TABLE_ROW_RE = re.compile(r"^\s*\|(?P<cells>.+)\|\s*$")
SPLIT_RE = re.compile(r"\s*(?:,|;|<br\s*/?>)\s*", re.IGNORECASE)


@dataclass(frozen=True)
class EvalCase:
    pack_path: Path
    question: str
    expected_notes: list[str]
    acceptance_rule: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run retrieval evals from knowledge pack golden questions."
    )
    parser.add_argument(
        "--vault",
        default=str(Path(__file__).resolve().parents[1]),
        help="Path to the Obsidian vault.",
    )
    parser.add_argument(
        "--pack",
        action="append",
        default=[],
        help="Knowledge pack path, title, or pack_name. May be repeated.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Evaluate all knowledge pack notes under 02_Domain-Knowledge/Packs.",
    )
    parser.add_argument(
        "--include-draft",
        action="store_true",
        help=(
            "Also evaluate non-active packs, such as draft or needs-source packs. "
            "By default only active packs are evaluated."
        ),
    )
    parser.add_argument("--top-k", type=int, default=3, help="Expected-note cutoff.")
    parser.add_argument("--json", action="store_true", help="Emit JSON report.")
    return parser.parse_args()


def markdown_body(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    return split_frontmatter(text)


def raw_section(body: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(?P<section>.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(body)
    return match.group("section") if match else ""


def normalize_cell(value: str) -> str:
    value = re.sub(r"<br\s*/?>", ";", value, flags=re.IGNORECASE)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def table_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        match = TABLE_ROW_RE.match(line)
        if not match:
            continue
        cells = [normalize_cell(cell) for cell in match.group("cells").split("|")]
        if not cells:
            continue
        if all(set(cell) <= {"-", " "} for cell in cells):
            continue
        if cells[0].lower() == "question":
            continue
        if any(cells):
            rows.append(cells)
    return rows


def strip_wikilink(value: str) -> str:
    value = value.strip()
    if value.startswith("[[") and value.endswith("]]"):
        value = value[2:-2].split("|", 1)[0].split("#", 1)[0].strip()
    return value


def split_expected_notes(value: str) -> list[str]:
    notes: list[str] = []
    for item in SPLIT_RE.split(value):
        clean = strip_wikilink(item.strip())
        if clean:
            notes.append(clean)
    return notes


def parse_cases(pack_path: Path, include_draft: bool = False) -> list[EvalCase]:
    metadata, body = markdown_body(pack_path)
    if metadata.get("type") != "knowledge-pack":
        return []
    status = str(metadata.get("status", "")).strip().lower()
    if not include_draft and status != "active":
        return []
    section = raw_section(body, "Golden Retrieval Questions")
    cases: list[EvalCase] = []
    for row in table_rows(section):
        question = row[0].strip()
        if not question:
            continue
        expected_notes = split_expected_notes(row[1]) if len(row) > 1 else []
        acceptance_rule = row[2].strip() if len(row) > 2 else ""
        cases.append(
            EvalCase(
                pack_path=pack_path,
                question=question,
                expected_notes=expected_notes,
                acceptance_rule=acceptance_rule,
            )
        )
    return cases


def all_pack_paths(vault: Path) -> list[Path]:
    pack_root = vault / "02_Domain-Knowledge" / "Packs"
    if not pack_root.exists():
        return []
    return [
        path
        for path in sorted(pack_root.rglob("*.md"))
        if path.name.lower() != "readme.md"
    ]


def resolve_pack(vault: Path, value: str) -> Path | None:
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = vault / candidate
    if candidate.exists() and candidate.is_file():
        return candidate.resolve()

    target = value.strip().lower()
    for path in all_pack_paths(vault):
        metadata, body = markdown_body(path)
        title = first_heading(body) or path.stem
        aliases = {
            path.stem.lower(),
            title.lower(),
            str(metadata.get("pack_name", "")).strip().lower(),
        }
        if target in aliases:
            return path.resolve()
    return None


def first_heading(body: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", body, re.MULTILINE)
    return match.group(1).strip() if match else ""


def normalized_expected(value: str, pack_path: Path, vault: Path) -> str:
    raw = strip_wikilink(value)
    candidate = Path(raw)
    if raw.startswith("./") or raw.startswith("../"):
        resolved = (pack_path.parent / candidate).resolve()
        with_suffix = resolved if resolved.suffix == ".md" else resolved.with_suffix(".md")
        for path in (resolved, with_suffix):
            try:
                return str(path.relative_to(vault)).lower().removesuffix(".md")
            except ValueError:
                continue

    value = raw.lower()
    if value.endswith(".md"):
        value = value[:-3]
    return value


def matches_expected(
    expected: str,
    result_path: str,
    title: str,
    pack_path: Path,
    vault: Path,
) -> bool:
    expected_norm = normalized_expected(expected, pack_path, vault)
    result_norm = result_path.lower()
    result_without_suffix = result_norm[:-3] if result_norm.endswith(".md") else result_norm
    title_norm = title.lower()
    stem_norm = Path(result_path).stem.lower()
    return expected_norm in {
        result_norm,
        result_without_suffix,
        title_norm,
        stem_norm,
    } or result_without_suffix.endswith(expected_norm)


def expected_answerability(rule: str) -> str:
    lower = rule.lower()
    for label in ("conflict", "supported", "partial", "gap"):
        if label in lower:
            return label
    return ""


def reliability_floor(metadata: dict[str, object]) -> str:
    raw = str(
        metadata.get("source_reliability_floor")
        or metadata.get("reliability_floor")
        or "medium"
    ).strip().lower()
    return raw if raw in RELIABILITY_RANK else "medium"


def run_case(vault: Path, case: EvalCase, top_k: int) -> dict[str, object]:
    metadata, _ = markdown_body(case.pack_path)
    domain = str(metadata.get("domain", "")).strip().lower()
    floor = reliability_floor(metadata)
    evidence = retrieve(
        vault=vault,
        query=case.question,
        top_k=top_k,
        domain_filter={domain} if domain else set(),
        reliability_floor=floor,
    )
    results = evidence["results"]
    found: list[str] = []
    missing: list[str] = []
    for expected in case.expected_notes:
        hit = False
        for item in results:
            if matches_expected(
                expected,
                str(item.get("path", "")),
                str(item.get("title", "")),
                case.pack_path,
                vault,
            ):
                hit = True
                break
        if hit:
            found.append(expected)
        else:
            missing.append(expected)

    expected_label = expected_answerability(case.acceptance_rule)
    answerability_ok = (
        not expected_label
        or str(evidence["answerability"]) == expected_label
        or (
            expected_label == "conflict"
            and str(evidence["answerability"]) in {"partial", "gap"}
        )
    )
    expected_ok = not missing
    ok = expected_ok and answerability_ok
    return {
        "ok": ok,
        "pack": str(case.pack_path.relative_to(vault)),
        "question": case.question,
        "expected_notes": case.expected_notes,
        "found_expected": found,
        "missing_expected": missing,
        "acceptance_rule": case.acceptance_rule,
        "expected_answerability": expected_label,
        "actual_answerability": evidence["answerability"],
        "failure_category": failure_category(missing, expected_label, evidence),
        "top_results": [
            {
                "path": item["path"],
                "title": item["title"],
                "score": item["score"],
                "reliability": item["reliability"],
            }
            for item in results
        ],
    }


def failure_category(
    missing: list[str],
    expected_label: str,
    evidence: dict[str, object],
) -> str:
    if not missing and not expected_label:
        return ""
    if not evidence["results"]:
        return "source missing or query routing wrong"
    if missing:
        return "metadata, extraction, chunking, or ranking wrong"
    if expected_label and evidence["answerability"] != expected_label:
        return "gap/conflict label wrong"
    return ""


def collect_cases(
    vault: Path,
    pack_values: list[str],
    include_all: bool,
    include_draft: bool,
) -> tuple[list[EvalCase], list[str]]:
    paths: list[Path] = []
    unresolved: list[str] = []
    if include_all or not pack_values:
        paths.extend(all_pack_paths(vault))
    for value in pack_values:
        resolved = resolve_pack(vault, value)
        if resolved:
            paths.append(resolved)
        else:
            unresolved.append(value)

    deduped = sorted(set(paths))
    cases: list[EvalCase] = []
    for path in deduped:
        cases.extend(parse_cases(path, include_draft=include_draft))
    return cases, unresolved


def main() -> int:
    args = parse_args()
    vault = Path(args.vault).resolve()
    cases, unresolved = collect_cases(vault, args.pack, args.all, args.include_draft)
    results = [run_case(vault, case, args.top_k) for case in cases]
    failures = [result for result in results if not result["ok"]]
    report = {
        "vault": str(vault),
        "ok": not unresolved and not failures,
        "status": "skipped" if not cases and not unresolved else "complete",
        "case_count": len(cases),
        "pass_count": len(results) - len(failures),
        "fail_count": len(failures),
        "unresolved_packs": unresolved,
        "results": results,
    }

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(
            f"Retrieval eval: {report['pass_count']} passed, "
            f"{report['fail_count']} failed, {report['case_count']} cases"
        )
        if report["status"] == "skipped":
            print("No knowledge pack golden questions found.")
        for pack in unresolved:
            print(f"UNRESOLVED PACK: {pack}")
        for result in results:
            label = "PASS" if result["ok"] else "FAIL"
            print(f"{label}: {result['pack']}: {result['question']}")
            if result["missing_expected"]:
                print(f"  missing: {', '.join(result['missing_expected'])}")
            if result["failure_category"]:
                print(f"  category: {result['failure_category']}")

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
