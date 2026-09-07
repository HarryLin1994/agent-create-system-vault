#!/usr/bin/env python3
"""Validate Obsidian vault structure for retrieval modules."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from agent_retrieve import RELIABILITY_RANK, as_list, split_frontmatter


WIKI_LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)

VALID_STATUSES = {
    "active",
    "archived",
    "deprecated",
    "draft",
    "failure-pattern",
    "needs-human-review",
    "needs-source",
    "needs-vision",
    "unprocessed",
}

RETRIEVAL_CRITICAL_TYPES = {
    "agent-blueprint",
    "capability-module",
    "case",
    "checklist",
    "claim",
    "concept",
    "eval",
    "eval-case",
    "failure-mode",
    "internal-module",
    "knowledge-pack",
    "knowledge-source",
    "module-contract",
    "module-design-spec",
    "module-pipeline",
    "module-plan",
    "module-registry",
    "module-standard",
    "module-taxonomy",
    "prompt",
    "runbook",
    "tool-spec",
}

REQUIRED_SECTIONS = {
    "internal-module": {
        "One-line Summary",
        "Purpose",
        "Trigger",
        "Inputs",
        "Outputs",
        "Dependencies",
        "Runtime Instructions",
        "Failure Modes",
        "Eval Coverage",
    },
    "knowledge-source": {
        "One-line Summary",
        "Claims Worth Using",
        "Agent Usage",
        "Source References",
    },
    "knowledge-pack": {
        "One-line Summary",
        "Scope",
        "Retrieval Filters",
        "Included Sources",
        "Agent Usage",
        "Unsupported Areas",
        "Golden Retrieval Questions",
    },
    "module-plan": {
        "One-line Summary",
        "Planning",
        "V1 Completion Target",
    },
    "tool-spec": {
        "One-line Summary",
        "Inputs",
        "Outputs",
        "Failure Handling",
        "Related",
    },
}

REQUIRED_FIELDS = {
    "knowledge-source": {"source_type", "title", "status", "tags", "reliability"},
    "knowledge-pack": {"pack_name", "domain", "status", "tags", "reliability"},
    "internal-module": {"type", "status", "tags", "reliability", "updated"},
    "tool-spec": {"type", "tool_name", "status", "tags", "reliability"},
}


@dataclass(frozen=True)
class Finding:
    level: str
    path: str
    code: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate metadata, module contracts, and Obsidian links."
    )
    parser.add_argument(
        "--vault",
        default=str(Path(__file__).resolve().parents[1]),
        help="Path to the Obsidian vault.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Promote warnings to errors for CI-style checks.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON report.")
    return parser.parse_args()


def markdown_files(vault: Path) -> list[Path]:
    paths: list[Path] = []
    for path in sorted(vault.rglob("*.md")):
        relative_parts = path.relative_to(vault).parts
        if any(part.startswith(".") for part in relative_parts):
            continue
        if relative_parts[0] in {"_templates", "tools"}:
            continue
        paths.append(path)
    return paths


def heading_set(body: str) -> set[str]:
    return {match.group(1).strip() for match in HEADING_RE.finditer(body)}


def severity(default: str, strict: bool) -> str:
    if strict and default == "warning":
        return "error"
    return default


def add(
    findings: list[Finding],
    level: str,
    path: Path,
    vault: Path,
    code: str,
    message: str,
    strict: bool = False,
) -> None:
    findings.append(
        Finding(
            level=severity(level, strict),
            path=str(path.relative_to(vault)),
            code=code,
            message=message,
        )
    )


def normalize_link_target(raw_target: str) -> str:
    target = raw_target.split("|", 1)[0].split("#", 1)[0].strip()
    return target.strip()


def candidate_paths(vault: Path, source_path: Path, target: str) -> Iterable[Path]:
    raw = Path(target)
    if target.startswith("./") or target.startswith("../"):
        candidate = (source_path.parent / raw).resolve()
        yield candidate
        if candidate.suffix != ".md":
            yield candidate.with_suffix(".md")
        return

    candidate = vault / raw
    yield candidate
    if candidate.suffix != ".md":
        yield candidate.with_suffix(".md")


def build_link_index(paths: list[Path], vault: Path) -> dict[str, set[Path]]:
    index: dict[str, set[Path]] = {}
    for path in paths:
        rel = path.relative_to(vault)
        keys = {
            path.stem.lower(),
            str(rel).lower(),
            str(rel.with_suffix("")).lower(),
        }
        for key in keys:
            index.setdefault(key, set()).add(path)
    return index


def link_resolves(
    vault: Path,
    source_path: Path,
    target: str,
    link_index: dict[str, set[Path]],
) -> bool:
    if not target:
        return True
    if "://" in target:
        return True

    for candidate in candidate_paths(vault, source_path, target):
        try:
            if candidate.exists() and candidate.is_file():
                return True
        except OSError:
            pass

    key = target.lower()
    if key in link_index:
        return True
    if key.endswith(".md") and key[:-3] in link_index:
        return True
    return Path(target).stem.lower() in link_index


def check_links(
    path: Path,
    body: str,
    vault: Path,
    link_index: dict[str, set[Path]],
    findings: list[Finding],
    strict: bool,
) -> None:
    for match in WIKI_LINK_RE.finditer(body):
        target = normalize_link_target(match.group(1))
        if not link_resolves(vault, path, target, link_index):
            add(
                findings,
                "warning",
                path,
                vault,
                "broken-wiki-link",
                f"Wiki link does not resolve: [[{target}]]",
                strict,
            )


def check_metadata(
    path: Path,
    metadata: dict[str, object],
    body: str,
    vault: Path,
    findings: list[Finding],
    strict: bool,
) -> None:
    note_type = str(metadata.get("type", "")).strip()
    tags = as_list(metadata.get("tags", []))
    status = str(metadata.get("status", "")).strip()
    reliability = str(metadata.get("reliability", "")).strip()

    if not note_type:
        add(
            findings,
            "warning",
            path,
            vault,
            "missing-type",
            "Missing frontmatter field: type",
            strict,
        )
        return

    if not tags:
        add(
            findings,
            "warning",
            path,
            vault,
            "missing-tags",
            "Missing or empty frontmatter field: tags",
            strict,
        )

    if note_type in RETRIEVAL_CRITICAL_TYPES and not status:
        add(
            findings,
            "warning",
            path,
            vault,
            "missing-status",
            "Retrieval-critical note is missing status.",
            strict,
        )
    if status and status not in VALID_STATUSES:
        add(
            findings,
            "warning",
            path,
            vault,
            "unknown-status",
            f"Unknown status: {status}",
            strict,
        )

    if note_type in RETRIEVAL_CRITICAL_TYPES and not reliability:
        add(
            findings,
            "warning",
            path,
            vault,
            "missing-reliability",
            "Retrieval-critical note is missing reliability.",
            strict,
        )
    if reliability and reliability not in RELIABILITY_RANK:
        add(
            findings,
            "error",
            path,
            vault,
            "invalid-reliability",
            f"Invalid reliability label: {reliability}",
            strict,
        )

    for field in REQUIRED_FIELDS.get(note_type, set()):
        value = metadata.get(field)
        if value is None or value == "" or value == []:
            add(
                findings,
                "error",
                path,
                vault,
                "missing-required-field",
                f"{note_type} is missing required field: {field}",
                strict,
            )

    headings = heading_set(body)
    for heading in sorted(REQUIRED_SECTIONS.get(note_type, set()) - headings):
        add(
            findings,
            "error",
            path,
            vault,
            "missing-required-section",
            f"{note_type} is missing required section: {heading}",
            strict,
        )

    if note_type == "knowledge-pack":
        golden = re.search(
            r"^##\s+Golden Retrieval Questions\s*$\n(?P<section>.*?)(?=^##\s+|\Z)",
            body,
            re.MULTILINE | re.DOTALL,
        )
        if golden and not has_table_data(golden.group("section")):
            add(
                findings,
                "warning",
                path,
                vault,
                "empty-golden-questions",
                "Knowledge pack has no runnable golden retrieval questions.",
                strict,
            )


def has_table_data(section: str) -> bool:
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or cells[0].lower() == "question":
            continue
        if all(set(cell) <= {"-", " "} for cell in cells):
            continue
        if any(cells):
            return True
    return False


def validate(vault: Path, strict: bool) -> dict[str, object]:
    paths = markdown_files(vault)
    link_index = build_link_index(paths, vault)
    findings: list[Finding] = []

    for path in paths:
        text = path.read_text(encoding="utf-8")
        metadata, body = split_frontmatter(text)
        if not metadata:
            add(
                findings,
                "warning",
                path,
                vault,
                "missing-frontmatter",
                "Markdown file has no frontmatter metadata.",
                strict,
            )
            continue
        check_metadata(path, metadata, body, vault, findings, strict)
        check_links(path, body, vault, link_index, findings, strict)

    errors = [finding for finding in findings if finding.level == "error"]
    warnings = [finding for finding in findings if finding.level == "warning"]
    return {
        "vault": str(vault),
        "ok": not errors,
        "strict": strict,
        "note_count": len(paths),
        "errors": len(errors),
        "warnings": len(warnings),
        "findings": [finding.__dict__ for finding in findings],
    }


def main() -> int:
    args = parse_args()
    vault = Path(args.vault).resolve()
    report = validate(vault, args.strict)

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(
            f"Vault validation: {report['errors']} errors, "
            f"{report['warnings']} warnings across {report['note_count']} notes"
        )
        for finding in report["findings"]:
            print(
                f"{finding['level'].upper()}: {finding['path']}: "
                f"{finding['code']}: {finding['message']}"
            )

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
