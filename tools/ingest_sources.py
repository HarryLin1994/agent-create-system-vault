#!/usr/bin/env python3
"""Create source manifests for raw files before extraction."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


RAW_DEFAULT = Path("00_Inbox") / "Raw Sources"
MANIFEST_DEFAULT = Path("00_Inbox") / "Source Manifests"

EXTENSION_TYPES = {
    ".csv": "data-export",
    ".doc": "document",
    ".docx": "document",
    ".htm": "web-page",
    ".html": "web-page",
    ".jpeg": "image",
    ".jpg": "image",
    ".json": "data-export",
    ".md": "markdown",
    ".pdf": "pdf",
    ".png": "image",
    ".ppt": "presentation",
    ".pptx": "presentation",
    ".rtf": "document",
    ".txt": "text",
    ".xml": "structured-data",
    ".xlsx": "spreadsheet",
}


@dataclass(frozen=True)
class RawSource:
    path: Path
    display_path: str
    source_id: str
    source_type: str
    extension: str
    sha256: str
    size_bytes: int
    modified_at: str
    source_url: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan raw source files and create Obsidian source manifests."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Scan raw folder and write manifests.")
    scan.add_argument(
        "--vault",
        default=str(Path(__file__).resolve().parents[1]),
        help="Path to the Obsidian vault.",
    )
    scan.add_argument(
        "--raw-dir",
        default=str(RAW_DEFAULT),
        help="Raw source folder, relative to vault unless absolute.",
    )
    scan.add_argument(
        "--manifest-dir",
        default=str(MANIFEST_DEFAULT),
        help="Manifest output folder, relative to vault unless absolute.",
    )
    scan.add_argument("--domain", default="", help="Default domain for new manifests.")
    scan.add_argument(
        "--permission",
        default="needs-review",
        help="Default permission label for new manifests.",
    )
    scan.add_argument(
        "--sensitivity",
        default="unknown",
        help="Default sensitivity label for new manifests.",
    )
    scan.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing manifest notes for unchanged source ids.",
    )
    scan.add_argument("--json", action="store_true", help="Emit JSON report.")
    return parser.parse_args()


def resolve_under_vault(vault: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else vault / path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def slugify(value: str) -> str:
    lowered = value.lower()
    lowered = re.sub(r"[^a-z0-9]+", "-", lowered)
    return lowered.strip("-") or "source"


def iso_mtime(path: Path) -> str:
    timestamp = path.stat().st_mtime
    return datetime.fromtimestamp(timestamp, timezone.utc).replace(microsecond=0).isoformat()


def source_type(path: Path) -> str:
    return EXTENSION_TYPES.get(path.suffix.lower(), "unknown")


def display_path(path: Path, vault: Path) -> str:
    try:
        return str(path.relative_to(vault))
    except ValueError:
        return str(path)


def iter_raw_files(raw_dir: Path) -> list[Path]:
    if not raw_dir.exists():
        return []
    paths: list[Path] = []
    for path in sorted(raw_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.name.startswith("."):
            continue
        if path.name == "README.md":
            continue
        paths.append(path)
    return paths


def inspect_file(path: Path, vault: Path, raw_dir: Path) -> RawSource:
    digest = sha256_file(path)
    stem = slugify(path.stem)
    source_id = f"{stem}-{digest[:12]}"
    return RawSource(
        path=path,
        display_path=display_path(path, vault),
        source_id=source_id,
        source_type=source_type(path),
        extension=path.suffix.lower(),
        sha256=digest,
        size_bytes=path.stat().st_size,
        modified_at=iso_mtime(path),
    )


def manifest_path(manifest_dir: Path, source: RawSource) -> Path:
    return manifest_dir / f"{source.source_id}.md"


def quote_yaml(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def render_manifest(
    source: RawSource,
    domain: str,
    permission: str,
    sensitivity: str,
) -> str:
    updated = datetime.now(timezone.utc).date().isoformat()
    title = source.path.stem.replace("_", " ").replace("-", " ").strip()
    return f"""---
type: source-manifest
source_id: {quote_yaml(source.source_id)}
source_type: {quote_yaml(source.source_type)}
status: draft
domain: {quote_yaml(domain)}
tags: [source-manifest, ingestion, raw-source]
reliability: draft
raw_path: {quote_yaml(source.display_path)}
sha256: {quote_yaml(source.sha256)}
size_bytes: {source.size_bytes}
modified_at: {quote_yaml(source.modified_at)}
extension: {quote_yaml(source.extension)}
title: {quote_yaml(title)}
author: ""
source_date: ""
source_url: {quote_yaml(source.source_url)}
version: ""
permission: {quote_yaml(permission)}
sensitivity: {quote_yaml(sensitivity)}
reviewer: ""
updated: {quote_yaml(updated)}
---

# Source Manifest - {source.source_id}

## One-line Summary

Review this raw source before extraction.

## Source Identity

| Field | Value |
| --- | --- |
| Source ID | `{source.source_id}` |
| Raw path | `{source.display_path}` |
| SHA-256 | `{source.sha256}` |
| Source type | `{source.source_type}` |
| Extension | `{source.extension}` |
| Size bytes | `{source.size_bytes}` |
| Modified at | `{source.modified_at}` |
| Domain | {domain or "needs-domain"} |
| Title | {title} |
| Author |  |
| Source date |  |
| Source URL | {source.source_url or ""} |
| Version |  |
| Permission | {permission} |
| Sensitivity | {sensitivity} |

## Extraction Plan

- Extraction adapter: {adapter_for(source.source_type)}
- Expected outputs:
- Human review required: yes

## Human Inputs Needed

- Confirm domain.
- Confirm permission and sensitivity.
- Confirm source title, author, version, and source date when available.
- Add the expert questions this source should help answer.

## Processing Notes

- Raw files are not committed to git.
- Do not treat this manifest as evidence until a source note exists.

## Related Source Note

-
"""


def adapter_for(kind: str) -> str:
    return {
        "data-export": "schema/table extraction",
        "document": "digital document text and structure extraction",
        "image": "OCR or vision caption with human review",
        "markdown": "direct Markdown section extraction",
        "pdf": "PDF text extraction or OCR if scanned",
        "presentation": "slide text, speaker-note, image, and table extraction",
        "spreadsheet": "sheet/table schema extraction",
        "text": "plain text section extraction",
    }.get(kind, "manual inspection")


def scan(args: argparse.Namespace) -> dict[str, object]:
    vault = Path(args.vault).resolve()
    raw_dir = resolve_under_vault(vault, args.raw_dir).resolve()
    manifest_dir = resolve_under_vault(vault, args.manifest_dir).resolve()
    manifest_dir.mkdir(parents=True, exist_ok=True)

    raw_files = iter_raw_files(raw_dir)
    created: list[str] = []
    skipped: list[str] = []
    manifests: list[dict[str, object]] = []
    for path in raw_files:
        source = inspect_file(path, vault, raw_dir)
        output_path = manifest_path(manifest_dir, source)
        if output_path.exists() and not args.force:
            skipped.append(display_path(output_path, vault))
        else:
            output_path.write_text(
                render_manifest(
                    source=source,
                    domain=args.domain,
                    permission=args.permission,
                    sensitivity=args.sensitivity,
                ),
                encoding="utf-8",
            )
            created.append(display_path(output_path, vault))
        manifests.append(
            {
                "source_id": source.source_id,
                "source_type": source.source_type,
                "raw_path": source.display_path,
                "manifest_path": display_path(output_path, vault),
                "sha256": source.sha256,
                "size_bytes": source.size_bytes,
            }
        )

    return {
        "ok": True,
        "vault": str(vault),
        "raw_dir": display_path(raw_dir, vault),
        "manifest_dir": display_path(manifest_dir, vault),
        "raw_file_count": len(raw_files),
        "created_count": len(created),
        "skipped_count": len(skipped),
        "created": created,
        "skipped": skipped,
        "manifests": manifests,
    }


def main() -> int:
    args = parse_args()
    if args.command == "scan":
        report = scan(args)
    else:
        raise ValueError(f"Unknown command: {args.command}")

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(
            f"Source scan: {report['raw_file_count']} raw files, "
            f"{report['created_count']} manifests created, "
            f"{report['skipped_count']} skipped"
        )
        for path in report["created"]:
            print(f"CREATED: {path}")
        for path in report["skipped"]:
            print(f"SKIPPED: {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
