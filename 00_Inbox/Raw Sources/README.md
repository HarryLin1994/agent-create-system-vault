---
type: index
status: active
tags: [inbox, raw-sources, ingestion]
reliability: medium
updated: 2026-09-07
---

# Raw Sources

Put original source files here when testing the ingestion pipeline.

## What To Put Here

- PDF, DOC, DOCX, TXT, Markdown, PPTX
- JPG, JPEG, PNG screenshots or scans
- CSV, JSON, XLSX exports
- Small batches of related files in a subfolder

## Git Policy

Raw files in this folder are ignored by git because they may be large, private, or copyrighted. The tracked outputs are source manifests, source notes, extracted knowledge notes, chunks, packs, and evals.

## Required Human Context

For every batch, also update [[../Source Intake Queue]] with:

- Domain name.
- What expert you want to build.
- What questions the expert should answer.
- Permission/sensitivity level.
- Whether images or scans need human verification.

## Next Step

After adding files, run:

```bash
python3 tools/ingest_sources.py scan
```
