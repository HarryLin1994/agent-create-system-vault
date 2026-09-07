#!/usr/bin/env python3
"""Gradio UI for source intake questions and raw-file upload."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import gradio as gr

from ingest_sources import display_path, scan, slugify
from source_download import download_urls


VAULT = Path(__file__).resolve().parents[1]
RAW_ROOT = VAULT / "00_Inbox" / "Raw Sources"
MANIFEST_ROOT = VAULT / "00_Inbox" / "Source Manifests"
QUEUE_PATH = VAULT / "00_Inbox" / "Source Intake Queue.md"
WEB_QUEUE_PATH = VAULT / "00_Inbox" / "Web Source Queue.md"

PERMISSION_OPTIONS = [
    "needs-review",
    "owned",
    "public",
    "licensed",
    "internal-approved",
    "restricted",
]

SENSITIVITY_OPTIONS = [
    "unknown",
    "public",
    "internal",
    "confidential",
    "personal-data",
    "regulated",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the source intake Gradio UI.")
    parser.add_argument("--host", default="127.0.0.1", help="Server host.")
    parser.add_argument("--port", type=int, default=7862, help="Server port.")
    parser.add_argument(
        "--share",
        action="store_true",
        help="Create a public Gradio share URL.",
    )
    return parser.parse_args()


def today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def quote_yaml(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def lines(value: str) -> list[str]:
    return [line.strip(" -\t") for line in value.splitlines() if line.strip(" -\t")]


def table_value(value: str) -> str:
    compact = " ".join(line.strip() for line in value.splitlines() if line.strip())
    return compact.replace("|", "\\|")


def batch_slug(batch_name: str, domain: str) -> str:
    return slugify(batch_name or domain or "source-batch")


def uploaded_paths(files: Any) -> list[Path]:
    if not files:
        return []
    if not isinstance(files, list):
        files = [files]

    paths: list[Path] = []
    for item in files:
        if isinstance(item, str):
            paths.append(Path(item))
        elif isinstance(item, dict) and item.get("path"):
            paths.append(Path(str(item["path"])))
        elif hasattr(item, "name"):
            paths.append(Path(str(item.name)))
        elif hasattr(item, "path"):
            paths.append(Path(str(item.path)))
    return paths


def unique_destination(directory: Path, filename: str) -> Path:
    target = directory / filename
    if not target.exists():
        return target
    stem = target.stem
    suffix = target.suffix
    index = 2
    while True:
        candidate = directory / f"{stem}-{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def copy_uploads(files: Any, batch_name: str, domain: str) -> list[Path]:
    paths = uploaded_paths(files)
    if not paths:
        return []
    destination_dir = RAW_ROOT / batch_slug(batch_name, domain)
    destination_dir.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for source in paths:
        if not source.exists():
            continue
        destination = unique_destination(destination_dir, source.name)
        shutil.copy2(source, destination)
        copied.append(destination)
    return copied


def markdown_bullets(items: list[str]) -> str:
    if not items:
        return "- "
    return "\n".join(f"- {item}" for item in items)


def render_queue(
    batch_name: str,
    domain: str,
    target_expert: str,
    supported_decisions: str,
    out_of_scope: str,
    permission: str,
    sensitivity: str,
    reviewer: str,
    golden_questions: str,
    copied_files: list[Path],
    web_urls: str,
) -> str:
    golden_rows = []
    for question in lines(golden_questions):
        safe_question = question.replace("|", "\\|")
        golden_rows.append(f"| {safe_question} |  | supported / partial / gap |")
    if not golden_rows:
        golden_rows.append("|  |  | supported / partial / gap |")

    file_rows = []
    for path in copied_files:
        file_rows.append(f"- `{display_path(path, VAULT)}`")
    if not file_rows:
        file_rows.append("- ")

    url_rows = []
    for url in lines(web_urls):
        url_rows.append(f"- {url}")
    if not url_rows:
        url_rows.append("- ")

    return f"""---
type: source-intake-queue
status: active
tags: [inbox, raw-sources, ingestion, domain-retrieval]
reliability: medium
updated: {quote_yaml(today())}
---

# Source Intake Queue

## One-line Summary

Use this queue to tell the ingestion pipeline what domain a source batch belongs to and what expert behavior the sources should support.

## Current Batch

| Field | Value |
| --- | --- |
| Batch name | {table_value(batch_name)} |
| Domain | {table_value(domain)} |
| Target expert | {table_value(target_expert)} |
| Supported decisions | {table_value(supported_decisions)} |
| Out of scope | {table_value(out_of_scope)} |
| Permission | {permission} |
| Sensitivity | {sensitivity} |
| Human reviewer | {table_value(reviewer)} |

## Golden Questions Draft

Write questions the expert should answer after ingestion.

| Question | Expected source or note | Answerability |
| --- | --- | --- |
{chr(10).join(golden_rows)}

## Uploaded Raw Files

{chr(10).join(file_rows)}

## Web URLs

{chr(10).join(url_rows)}

## Source Notes

- Put raw files in [[Raw Sources/README|Raw Sources]].
- Source manifests will be generated in [[Source Manifests/README|Source Manifests]].

## Related

- [[../07_Runbooks/Extract Expert Knowledge From Sources|Extract Expert Knowledge From Sources]]
- [[../09_Module-System/Domain Retrieval Modules/System Architecture - 12 Module Pipeline|System Architecture - 12 Module Pipeline]]
"""


def render_web_queue(web_urls: str, domain: str, permission: str) -> str:
    rows = []
    for url in lines(web_urls):
        rows.append(f"| {url.replace('|', '%7C')} | {domain} | source intake | {permission} | queued |")
    if not rows:
        rows.append("|  |  |  | needs-review | queued |")
    return f"""---
type: web-source-queue
status: active
tags: [inbox, web-sources, crawler, ingestion]
reliability: medium
updated: {quote_yaml(today())}
---

# Web Source Queue

## One-line Summary

Use this queue for URLs that should enter the source ingestion pipeline through the download assistant.

## Rules

- Prefer official, primary, open-access, or owned sources.
- Do not crawl login-only, paywalled, personal, or sensitive sites without explicit permission.
- Keep crawl scope small: same host, low page limit, low depth.
- Use downloaded web pages as raw sources, then create source notes and extracted knowledge notes.

## URL Queue

| URL | Domain | Reason | Permission | Status |
| --- | --- | --- | --- | --- |
{chr(10).join(rows)}

## Commands

Download explicit URLs:

```bash
python3 tools/source_download.py download "https://example.com/page" --domain your-domain
```

Crawl a small same-host area:

```bash
python3 tools/source_download.py crawl "https://example.com/docs/" --domain your-domain --max-pages 10 --max-depth 1
```

## Related

- [[Raw Sources/README|Raw Sources]]
- [[Source Manifests/README|Source Manifests]]
- [[../04_Tool-Specs/Tool Spec - Web Source Download|Tool Spec - Web Source Download]]
"""


def scan_raw(batch_name: str, domain: str, permission: str, sensitivity: str) -> dict[str, Any]:
    raw_dir = RAW_ROOT / batch_slug(batch_name, domain)
    if not raw_dir.exists():
        raw_dir = RAW_ROOT
    args = SimpleNamespace(
        vault=str(VAULT),
        raw_dir=str(raw_dir),
        manifest_dir=str(MANIFEST_ROOT),
        domain=domain,
        permission=permission,
        sensitivity=sensitivity,
        force=False,
        json=True,
    )
    return scan(args)


def download_web_sources(
    web_urls: str,
    domain: str,
    permission: str,
    sensitivity: str,
    dry_run: bool,
) -> dict[str, Any]:
    url_items = lines(web_urls)
    if not url_items:
        return {"ok": True, "downloaded_count": 0, "skipped_count": 0, "downloads": [], "skipped": []}
    args = SimpleNamespace(
        vault=str(VAULT),
        raw_dir=str(RAW_ROOT / "_downloads"),
        manifest_dir=str(MANIFEST_ROOT),
        domain=domain,
        permission=permission,
        sensitivity=sensitivity,
        user_agent="agent-create-system-vault/0.1 (+local knowledge ingestion)",
        delay=2.0,
        timeout=20.0,
        max_bytes=25 * 1024 * 1024,
        dry_run=dry_run,
        force=False,
        json=True,
    )
    return download_urls(args, url_items)


def save_intake(
    batch_name: str,
    domain: str,
    target_expert: str,
    supported_decisions: str,
    out_of_scope: str,
    permission: str,
    sensitivity: str,
    reviewer: str,
    golden_questions: str,
    files: Any,
    web_urls: str,
    run_scan: bool,
    download_urls_now: bool,
    download_dry_run: bool,
) -> tuple[str, str]:
    missing = []
    if not domain.strip():
        missing.append("Domain")
    if not target_expert.strip():
        missing.append("Target expert")
    if not supported_decisions.strip():
        missing.append("Supported decisions")
    if len(lines(golden_questions)) < 3:
        missing.append("3-5 golden questions")
    if missing:
        return (
            "Missing required fields: " + ", ".join(missing),
            "{}",
        )

    RAW_ROOT.mkdir(parents=True, exist_ok=True)
    MANIFEST_ROOT.mkdir(parents=True, exist_ok=True)
    copied_files = copy_uploads(files, batch_name, domain)
    QUEUE_PATH.write_text(
        render_queue(
            batch_name=batch_name,
            domain=domain,
            target_expert=target_expert,
            supported_decisions=supported_decisions,
            out_of_scope=out_of_scope,
            permission=permission,
            sensitivity=sensitivity,
            reviewer=reviewer,
            golden_questions=golden_questions,
            copied_files=copied_files,
            web_urls=web_urls,
        ),
        encoding="utf-8",
    )
    if web_urls.strip():
        WEB_QUEUE_PATH.write_text(
            render_web_queue(web_urls, domain, permission),
            encoding="utf-8",
        )

    reports: dict[str, Any] = {
        "queue_path": display_path(QUEUE_PATH, VAULT),
        "copied_files": [display_path(path, VAULT) for path in copied_files],
    }
    if run_scan:
        reports["scan"] = scan_raw(batch_name, domain, permission, sensitivity)
    if download_urls_now:
        reports["download"] = download_web_sources(
            web_urls=web_urls,
            domain=domain,
            permission=permission,
            sensitivity=sensitivity,
            dry_run=download_dry_run,
        )

    message_parts = [
        f"Saved queue: `{display_path(QUEUE_PATH, VAULT)}`",
        f"Uploaded files: {len(copied_files)}",
    ]
    if run_scan:
        scan_report = reports["scan"]
        message_parts.append(
            f"Manifests created: {scan_report['created_count']}, skipped: {scan_report['skipped_count']}"
        )
    if download_urls_now:
        download_report = reports["download"]
        message_parts.append(
            f"Downloaded URLs: {download_report['downloaded_count']}, skipped: {download_report['skipped_count']}"
        )
    return "\n".join(message_parts), json.dumps(reports, indent=2, sort_keys=True)


def build_app() -> gr.Blocks:
    with gr.Blocks(title="Source Intake") as demo:
        gr.Markdown("# Source Intake")

        with gr.Row():
            with gr.Column(scale=1):
                batch_name = gr.Textbox(label="Batch name", placeholder="startup-strategy-books")
                domain = gr.Textbox(label="Domain", placeholder="startup-strategy")
                target_expert = gr.Textbox(
                    label="Target expert",
                    placeholder="Startup strategy advisor",
                )
                permission = gr.Dropdown(
                    label="Permission",
                    choices=PERMISSION_OPTIONS,
                    value="needs-review",
                )
                sensitivity = gr.Dropdown(
                    label="Sensitivity",
                    choices=SENSITIVITY_OPTIONS,
                    value="unknown",
                )
                reviewer = gr.Textbox(label="Human reviewer", placeholder="Harry")

            with gr.Column(scale=2):
                supported_decisions = gr.Textbox(
                    label="Supported decisions",
                    lines=4,
                    placeholder="What decisions should this expert help with?",
                )
                out_of_scope = gr.Textbox(
                    label="Out of scope",
                    lines=3,
                    placeholder="What should this expert refuse or mark as unsupported?",
                )
                golden_questions = gr.Textbox(
                    label="3-5 golden questions",
                    lines=6,
                    placeholder="One question per line.",
                )

        with gr.Row():
            files = gr.File(
                label="Raw files",
                file_count="multiple",
                type="filepath",
            )
            web_urls = gr.Textbox(
                label="Web URLs",
                lines=6,
                placeholder="Optional. One URL per line.",
            )

        with gr.Row():
            run_scan = gr.Checkbox(label="Generate manifests", value=True)
            download_urls_now = gr.Checkbox(label="Download URLs now", value=False)
            download_dry_run = gr.Checkbox(label="URL dry run", value=True)

        save = gr.Button("Save intake", variant="primary")
        status = gr.Markdown()
        report = gr.Code(label="Report", language="json")

        save.click(
            fn=save_intake,
            inputs=[
                batch_name,
                domain,
                target_expert,
                supported_decisions,
                out_of_scope,
                permission,
                sensitivity,
                reviewer,
                golden_questions,
                files,
                web_urls,
                run_scan,
                download_urls_now,
                download_dry_run,
            ],
            outputs=[status, report],
        )

    return demo


def main() -> int:
    args = parse_args()
    demo = build_app()
    demo.launch(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
        prevent_thread_lock=False,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
