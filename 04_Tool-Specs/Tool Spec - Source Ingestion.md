---
type: tool-spec
tool_name: source_ingestion_scan
status: active
tags: [tool, ingestion, raw-sources, domain-retrieval]
reliability: medium
domain: agent-create-system
---

# Tool Spec - Source Ingestion

## One-line Summary

Scan raw source files, compute stable identity metadata, and create Obsidian source manifests before extraction.

## Command

```bash
python3 tools/ingest_sources.py scan
```

With batch defaults:

```bash
python3 tools/ingest_sources.py scan \
  --domain your-domain \
  --permission needs-review \
  --sensitivity unknown
```

## Inputs

- Raw source folder, default `00_Inbox/Raw Sources`.
- Manifest output folder, default `00_Inbox/Source Manifests`.
- Optional default domain.
- Optional permission label.
- Optional sensitivity label.
- Optional `--force` flag to regenerate manifests.

## Outputs

- One Markdown source manifest per raw file.
- Stable `source_id` derived from filename and SHA-256 hash.
- File metadata: raw path, extension, source type, file size, modified time, and hash.
- Human-review fields for domain, title, author, source date, permission, sensitivity, and reviewer.

## Use When

- New PDFs, Word files, text files, slides, images, scans, or data exports are added.
- A source batch needs provenance before extraction.
- A human needs to verify what entered the knowledge pipeline.

## Safety Limits

- Raw files are ignored by git.
- The scan does not upload files.
- The scan does not OCR, caption, embed, summarize, or rewrite source content.
- The scan does not mark a source as reliable; generated manifests start as `draft`.
- `--force` can overwrite generated manifest notes and should be used only after review.

## Failure Handling

- If the raw folder is empty, report zero files and do nothing.
- If a file extension is unknown, mark `source_type: unknown` and require manual inspection.
- If a manifest already exists, skip it unless `--force` is set.
- If permission or sensitivity is unknown, keep `needs-review` and `unknown`.
- If a manifest is created for the wrong domain, edit the manifest before creating source notes.

## Related

- [[../00_Inbox/Raw Sources/README|Raw Sources]]
- [[../00_Inbox/Source Intake Queue|Source Intake Queue]]
- [[../00_Inbox/Source Manifests/README|Source Manifests]]
- [[../07_Runbooks/Extract Expert Knowledge From Sources|Extract Expert Knowledge From Sources]]
- [[../09_Module-System/Domain Retrieval Modules/01 - Source Intake and Trust|Source Intake and Trust]]
- [[Tool Spec - Source Intake UI]]
- [[Tool Spec - Web Source Download]]
- [[Tool Spec - Vault Retrieval]]
