#!/usr/bin/env python3
"""Simple dependency-free retrieval for the agent creation vault."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import quote


TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_+.-]*", re.IGNORECASE)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
SECTION_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
RELIABILITY_RANK = {
    "draft": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
}
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "from",
    "how",
    "i",
    "in",
    "is",
    "it",
    "my",
    "of",
    "on",
    "or",
    "our",
    "should",
    "the",
    "to",
    "what",
    "when",
    "with",
}

NON_EVIDENCE_SECTIONS = {
    "knowledge-pack": {"Golden Retrieval Questions", "Related Evals"},
}

ALIASES = {
    "agent": ["agent"],
    "agents": ["agent"],
    "\u667a\u80fd\u9ad4": ["agent"],
    "\u667a\u80fd\u4f53": ["agent"],
    "\u4ee3\u7406": ["agent"],
    "\u7cfb\u7d71": ["system"],
    "\u7cfb\u7edf": ["system"],
    "\u5efa\u7acb": ["create", "build"],
    "\u5efa\u7acb\u7cfb\u7d71": ["create", "system", "builder"],
    "\u521b\u5efa": ["create", "build"],
    "\u80fd\u529b": ["capability", "module"],
    "\u6a21\u7d44": ["module"],
    "\u6a21\u5757": ["module"],
    "\u63d0\u793a\u8a5e": ["prompt"],
    "\u63d0\u793a\u8bcd": ["prompt"],
    "\u7cfb\u7d71\u63d0\u793a": ["system", "prompt"],
    "\u7cfb\u7edf\u63d0\u793a": ["system", "prompt"],
    "\u8a55\u6e2c": ["eval", "test"],
    "\u8bc4\u6d4b": ["eval", "test"],
    "\u6e2c\u8a66": ["eval", "test"],
    "\u6d4b\u8bd5": ["eval", "test"],
    "\u5de5\u5177": ["tool"],
    "\u77e5\u8b58": ["knowledge"],
    "\u77e5\u8bc6": ["knowledge"],
    "\u89d2\u8272": ["role"],
    "\u85cd\u5716": ["blueprint"],
    "\u84dd\u56fe": ["blueprint"],
    "\u6aa2\u7d22": ["retrieval", "search"],
    "\u68c0\u7d22": ["retrieval", "search"],
    "\u7522\u54c1\u5e02\u5834\u5951\u5408": ["product", "market", "fit", "pmf"],
    "\u4ea7\u54c1\u5e02\u573a\u5951\u5408": ["product", "market", "fit", "pmf"],
    "\u52df\u8cc7": ["fundraising", "raise", "capital"],
    "\u878d\u8d44": ["fundraising", "raise", "capital"],
    "\u6210\u9577": ["growth"],
    "\u589e\u957f": ["growth"],
    "\u5b9a\u50f9": ["pricing"],
    "\u5b9a\u4ef7": ["pricing"],
    "\u5931\u6557": ["failure", "failed", "risk"],
    "\u5931\u8d25": ["failure", "failed", "risk"],
    "\u6210\u529f": ["success", "worked"],
    "\u6848\u4f8b": ["case"],
    "\u51b7\u555f\u52d5": ["cold", "start", "cold-start"],
    "\u51b7\u542f\u52a8": ["cold", "start", "cold-start"],
    "\u5275\u696d": ["startup", "founder"],
    "\u521b\u4e1a": ["startup", "founder"],
    "\u55ae\u4f4d\u7d93\u6fdf": ["unit", "economics"],
    "\u5355\u4f4d\u7ecf\u6d4e": ["unit", "economics"],
}


@dataclass(frozen=True)
class Note:
    path: Path
    title: str
    note_type: str
    tags: list[str]
    metadata: dict[str, object]
    status: str
    domain: str
    reliability: str
    summary: str
    text: str
    tokens: list[str]


@dataclass(frozen=True)
class Chunk:
    note: Note
    heading: str
    text: str
    tokens: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Retrieve evidence packs from the agent creation vault."
    )
    parser.add_argument("query", help="User request, expert task, or search query")
    parser.add_argument(
        "--vault",
        default=str(Path(__file__).resolve().parents[1]),
        help="Path to the Obsidian vault",
    )
    parser.add_argument("--top-k", type=int, default=5, help="Number of notes to return")
    parser.add_argument(
        "--type",
        action="append",
        default=[],
        help="Filter by note type. May be repeated or comma-separated.",
    )
    parser.add_argument(
        "--tag",
        action="append",
        default=[],
        help="Filter by tag. May be repeated or comma-separated.",
    )
    parser.add_argument(
        "--domain",
        action="append",
        default=[],
        help="Filter by domain. May be repeated or comma-separated.",
    )
    parser.add_argument(
        "--status",
        action="append",
        default=[],
        help="Filter by status. May be repeated or comma-separated.",
    )
    parser.add_argument(
        "--reliability-floor",
        choices=sorted(RELIABILITY_RANK),
        default="draft",
        help="Minimum reliability label to return.",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    return parser.parse_args()


def parse_scalar(value: str) -> object:
    stripped = value.strip().strip('"').strip("'")
    if stripped.startswith("[") and stripped.endswith("]"):
        items = [item.strip().strip('"').strip("'") for item in stripped[1:-1].split(",")]
        return [item for item in items if item]
    if stripped.lower() == "true":
        return True
    if stripped.lower() == "false":
        return False
    return stripped


def split_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text

    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, text

    raw_meta = parts[1]
    body = parts[2]
    metadata: dict[str, object] = {}
    current_list_key = ""
    for line in raw_meta.splitlines():
        if line.startswith("  - ") or line.startswith("- "):
            if current_list_key:
                value = line.split("-", 1)[1].strip().strip('"').strip("'")
                existing = metadata.setdefault(current_list_key, [])
                if isinstance(existing, list) and value:
                    existing.append(value)
            continue
        if ":" not in line:
            current_list_key = ""
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if value:
            metadata[key] = parse_scalar(value)
            current_list_key = ""
        else:
            metadata[key] = []
            current_list_key = key
    return metadata, body


def as_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [str(item).strip() for item in value.split(",") if str(item).strip()]
    return []


def csv_args(values: list[str]) -> set[str]:
    selected: set[str] = set()
    for raw_value in values:
        for item in raw_value.split(","):
            normalized = item.strip().lower()
            if normalized:
                selected.add(normalized)
    return selected


def normalize_tokens(text: str) -> list[str]:
    expanded = text.lower().replace("-", " ").replace("/", " ")
    tokens = [token.lower() for token in TOKEN_RE.findall(expanded)]
    tokens.extend(token.lower() for token in TOKEN_RE.findall(text.lower()))
    for phrase, additions in ALIASES.items():
        if phrase in text:
            tokens.extend(additions)
    return [token for token in tokens if token not in STOPWORDS and len(token) > 1]


def extract_title(metadata: dict[str, object], body: str, path: Path) -> str:
    title = metadata.get("title")
    if isinstance(title, str) and title:
        return title
    match = HEADING_RE.search(body)
    if match:
        return match.group(1).strip()
    return path.stem


def extract_section(body: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(?P<section>.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(body)
    if not match:
        return ""
    lines = [
        line.strip().strip("- ").strip()
        for line in match.group("section").splitlines()
        if line.strip()
    ]
    return " ".join(lines)


def extract_summary(body: str) -> str:
    for heading in ("One-line Summary", "Summary", "Advisor Usage"):
        section = extract_section(body, heading)
        if section:
            return section[:280]
    return ""


def normalized_reliability(value: object) -> str:
    label = str(value or "draft").strip().lower()
    return label if label in RELIABILITY_RANK else "draft"


def load_notes(vault: Path) -> list[Note]:
    notes: list[Note] = []
    for path in sorted(vault.rglob("*.md")):
        relative_parts = path.relative_to(vault).parts
        if any(part.startswith(".") for part in relative_parts):
            continue
        if relative_parts[0] in {"_templates", "tools"}:
            continue

        text = path.read_text(encoding="utf-8")
        metadata, body = split_frontmatter(text)
        tags = as_list(metadata.get("tags", []))
        note_type = str(metadata.get("type", "note"))
        title = extract_title(metadata, body, path)
        searchable = " ".join([title, note_type, " ".join(tags), body])
        notes.append(
            Note(
                path=path,
                title=title,
                note_type=note_type,
                tags=tags,
                metadata=metadata,
                status=str(metadata.get("status", "")).strip().lower(),
                domain=str(metadata.get("domain", "")).strip().lower(),
                reliability=normalized_reliability(metadata.get("reliability", "draft")),
                summary=extract_summary(body),
                text=body,
                tokens=normalize_tokens(searchable),
            )
        )
    return notes


def chunk_notes(notes: list[Note]) -> list[Chunk]:
    chunks: list[Chunk] = []
    for note in notes:
        matches = list(SECTION_HEADING_RE.finditer(note.text))
        if not matches:
            chunks.append(Chunk(note=note, heading="", text=note.text, tokens=note.tokens))
            continue

        preface = note.text[: matches[0].start()].strip()
        if preface:
            searchable = " ".join([note.title, note.note_type, " ".join(note.tags), preface])
            chunks.append(
                Chunk(
                    note=note,
                    heading="",
                    text=preface,
                    tokens=normalize_tokens(searchable),
                )
            )

        for index, match in enumerate(matches):
            heading = match.group(2).strip()
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(note.text)
            text = note.text[start:end].strip()
            if heading in NON_EVIDENCE_SECTIONS.get(note.note_type, set()):
                continue
            if not text:
                continue
            searchable = " ".join(
                [note.title, note.note_type, " ".join(note.tags), heading, text]
            )
            chunks.append(
                Chunk(
                    note=note,
                    heading=heading,
                    text=text,
                    tokens=normalize_tokens(searchable),
                )
            )
    return chunks


def score_chunk(query_tokens: list[str], chunk: Chunk) -> float:
    if not query_tokens:
        return 0.0

    token_counts: dict[str, int] = {}
    for token in chunk.tokens:
        token_counts[token] = token_counts.get(token, 0) + 1

    title_tokens = set(normalize_tokens(chunk.note.title))
    heading_tokens = set(normalize_tokens(chunk.heading))
    tag_tokens = set(token for tag in chunk.note.tags for token in normalize_tokens(str(tag)))
    type_tokens = set(normalize_tokens(chunk.note.note_type))

    score = 0.0
    for token in query_tokens:
        count = token_counts.get(token, 0)
        if count:
            score += min(count, 8)
        if token in title_tokens:
            score += 6
        if token in heading_tokens:
            score += 5
        if token in tag_tokens:
            score += 8
        if token in type_tokens:
            score += 4

    if chunk.note.note_type in {"case", "framework", "playbook", "checklist", "knowledge-pack"}:
        score *= 1.15

    return round(score, 2)


def extract_excerpt(text: str, fallback: str, query_tokens: Iterable[str]) -> str:
    query_set = set(query_tokens)
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]
    best_block = ""
    best_hits = 0
    for block in blocks:
        block_tokens = set(normalize_tokens(block))
        hits = len(query_set.intersection(block_tokens))
        if hits > best_hits:
            best_hits = hits
            best_block = block
    if not best_block:
        best_block = fallback or (blocks[0] if blocks else "")
    return re.sub(r"\s+", " ", best_block).strip()[:500]


def passes_filters(
    note: Note,
    type_filter: set[str],
    tag_filter: set[str],
    domain_filter: set[str],
    status_filter: set[str],
    reliability_floor: str,
) -> bool:
    if type_filter and note.note_type.lower() not in type_filter:
        return False
    note_tags = {tag.lower() for tag in note.tags}
    if tag_filter and not tag_filter.issubset(note_tags):
        return False
    if domain_filter and note.domain not in domain_filter:
        return False
    if status_filter and note.status not in status_filter:
        return False
    if RELIABILITY_RANK[note.reliability] < RELIABILITY_RANK[reliability_floor]:
        return False
    return True


def obsidian_uri(path: Path) -> str:
    return "obsidian://open?path=" + quote(str(path.resolve()))


def source_reference(note: Note) -> str:
    fields = [
        str(note.metadata.get("source", "") or "").strip(),
        str(note.metadata.get("url", "") or "").strip(),
        str(note.metadata.get("author", "") or "").strip(),
    ]
    compact = [field for field in fields if field]
    if compact:
        return "; ".join(compact)
    section = extract_section(note.text, "Source References")
    return section[:280]


def usage_guidance(note: Note) -> str:
    for heading in ("Agent Usage", "Use When", "Runtime Instructions", "Advisor Usage"):
        section = extract_section(note.text, heading)
        if section:
            return section[:280]
    return ""


def caveat(note: Note) -> str:
    for heading in ("Caveat", "Limitations", "Failure Modes", "Unsupported Areas"):
        section = extract_section(note.text, heading)
        if section:
            return section[:280]
    return ""


def answerability(results: list[dict[str, object]]) -> str:
    if not results:
        return "gap"
    best = results[0]
    best_score = float(best["score"])
    best_reliability = str(best["reliability"])
    if best_score >= 12 and RELIABILITY_RANK[best_reliability] >= RELIABILITY_RANK["medium"]:
        return "supported"
    return "partial"


def filter_payload(
    type_filter: set[str],
    tag_filter: set[str],
    domain_filter: set[str],
    status_filter: set[str],
    reliability_floor: str,
) -> dict[str, object]:
    return {
        "type": sorted(type_filter),
        "tag": sorted(tag_filter),
        "domain": sorted(domain_filter),
        "status": sorted(status_filter),
        "reliability_floor": reliability_floor,
    }


def retrieve(
    vault: Path,
    query: str,
    top_k: int,
    type_filter: set[str] | None = None,
    tag_filter: set[str] | None = None,
    domain_filter: set[str] | None = None,
    status_filter: set[str] | None = None,
    reliability_floor: str = "draft",
) -> dict[str, object]:
    type_filter = type_filter or set()
    tag_filter = tag_filter or set()
    domain_filter = domain_filter or set()
    status_filter = status_filter or set()
    query_tokens = normalize_tokens(query)
    results: list[dict[str, object]] = []
    notes = [
        note
        for note in load_notes(vault)
        if passes_filters(
            note,
            type_filter,
            tag_filter,
            domain_filter,
            status_filter,
            reliability_floor,
        )
    ]
    best_by_note: dict[str, dict[str, object]] = {}
    for chunk in chunk_notes(notes):
        note = chunk.note
        score = score_chunk(query_tokens, chunk)
        if score <= 0:
            continue
        relative_path = str(note.path.relative_to(vault))
        item = {
            "path": relative_path,
            "obsidian_uri": obsidian_uri(note.path),
            "title": note.title,
            "type": note.note_type,
            "heading": chunk.heading,
            "tags": note.tags,
            "domain": note.domain,
            "status": note.status,
            "reliability": note.reliability,
            "summary": note.summary,
            "excerpt": extract_excerpt(chunk.text, note.summary, query_tokens),
            "source_reference": source_reference(note),
            "how_to_use": usage_guidance(note),
            "caveat": caveat(note),
            "score": score,
        }
        existing = best_by_note.get(relative_path)
        if existing is None or score > float(existing["score"]):
            best_by_note[relative_path] = item
    results.extend(best_by_note.values())
    results.sort(key=lambda item: (-float(item["score"]), str(item["path"])))
    results = results[:top_k]
    gaps = []
    if not results:
        gaps.append(
            "No matching notes met the query and filters. Broaden terms, check metadata, or create a source/concept/case note."
        )
    elif answerability(results) == "partial":
        gaps.append(
            "Retrieval found related notes but not enough medium-or-better evidence for a fully supported answer."
        )
    return {
        "query": query,
        "vault": str(vault),
        "filters": filter_payload(
            type_filter,
            tag_filter,
            domain_filter,
            status_filter,
            reliability_floor,
        ),
        "answerability": answerability(results),
        "results": results,
        "gaps": gaps,
    }


def main() -> int:
    args = parse_args()
    vault = Path(args.vault).resolve()
    pack = retrieve(
        vault=vault,
        query=args.query,
        top_k=args.top_k,
        type_filter=csv_args(args.type),
        tag_filter=csv_args(args.tag),
        domain_filter=csv_args(args.domain),
        status_filter=csv_args(args.status),
        reliability_floor=args.reliability_floor,
    )

    if args.json:
        print(json.dumps(pack, indent=2))
        return 0

    print(f"Query: {args.query}")
    print(f"Vault: {vault}")
    print(f"Answerability: {pack['answerability']}")
    filters = pack["filters"]
    if isinstance(filters, dict) and any(
        value for key, value in filters.items() if key != "reliability_floor"
    ):
        print(f"Filters: {json.dumps(filters, sort_keys=True)}")
    print("")
    results = pack["results"]
    if not results:
        print("No matching notes found.")
        for gap in pack["gaps"]:
            print(f"Gap: {gap}")
        return 1

    for index, item in enumerate(results, start=1):
        tags = ", ".join(str(tag) for tag in item["tags"])
        heading = f" > {item['heading']}" if item["heading"] else ""
        print(
            f"{index}. {item['title']}{heading} "
            f"({item['type']}, reliability={item['reliability']}, score={item['score']})"
        )
        print(f"   path: {item['path']}")
        print(f"   obsidian: {item['obsidian_uri']}")
        if tags:
            print(f"   tags: {tags}")
        if item["summary"]:
            print(f"   summary: {item['summary']}")
        if item["source_reference"]:
            print(f"   source: {item['source_reference']}")
        if item["how_to_use"]:
            print(f"   use: {item['how_to_use']}")
        if item["caveat"]:
            print(f"   caveat: {item['caveat']}")
        print(f"   excerpt: {item['excerpt']}")
        print("")
    for gap in pack["gaps"]:
        print(f"Gap: {gap}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
