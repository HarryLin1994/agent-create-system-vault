---
type: tool-spec
tool_name: source_intake_ui
status: active
tags: [tool, ui, gradio, ingestion, raw-sources]
reliability: medium
domain: agent-create-system
---

# Tool Spec - Source Intake UI

## One-line Summary

Run a local Gradio form for domain, expert scope, permissions, raw-file upload, URLs, and golden retrieval questions.

## Command

```bash
python3 tools/source_intake_ui.py --port 7862
```

## Inputs

- Batch name.
- Domain.
- Target expert.
- Supported decisions.
- Out-of-scope questions.
- Permission and sensitivity labels.
- Human reviewer.
- Three to five golden questions.
- Optional raw files.
- Optional web URLs.

## Outputs

- Updated `00_Inbox/Source Intake Queue.md`.
- Uploaded files copied into ignored raw source folders.
- Source manifests generated when the scan option is enabled.
- Updated `00_Inbox/Web Source Queue.md` when URLs are provided.
- JSON report shown in the UI.

## Dependencies

- Python 3.10 or newer.
- Gradio, tested locally with `gradio 6.24.0`.
- `tools/ingest_sources.py`.
- `tools/source_download.py` when URL download is enabled.

## Safety Limits

- Runs on `127.0.0.1` by default.
- Raw files remain ignored by git.
- URL download is opt-in and defaults to dry-run.
- The UI does not OCR, embed, summarize, or rate source reliability.
- Public Gradio share URLs should not be used for private source intake.

## Failure Handling

- If required fields are missing, the UI returns a missing-field message and writes nothing.
- If fewer than three golden questions are provided, the UI blocks save.
- If file copy fails, inspect the JSON report and raw folder.
- If URL download fails, keep URLs in the queue and run `tools/source_download.py` separately.
- If generated manifests are wrong, edit them before creating source notes.

## Related

- [[../00_Inbox/Source Intake Queue|Source Intake Queue]]
- [[../00_Inbox/Raw Sources/README|Raw Sources]]
- [[../00_Inbox/Source Manifests/README|Source Manifests]]
- [[Tool Spec - Source Ingestion]]
- [[Tool Spec - Web Source Download]]
