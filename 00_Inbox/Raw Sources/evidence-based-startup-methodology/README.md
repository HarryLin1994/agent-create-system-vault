---
type: index
status: active
tags: [inbox, raw-sources, startup, user-provided-source]
reliability: medium
updated: 2026-09-07
---

# Raw Sources - Evidence-Based Startup Methodology

Put user-provided files for the startup execution advisor here.

## Current Source Mode

- Use user-provided local files only.
- Do not use public source search for this domain unless the human explicitly re-enables it.
- Public-source discovery is paused to avoid false-positive source judgments.
- Raw files remain ignored by git.

## Good Inputs

- Notes from books you own or have permission to process.
- Your own summaries, highlights, and chapter notes.
- Founder notes and startup operating notes.
- Customer interview notes after sensitive names and identifiers are reviewed.
- Pitch decks, financial models, investor feedback, and customer lists only when marked confidential and intentionally included.
- PDF, DOC/DOCX, TXT, Markdown, PPT/PPTX, JPG/PNG, CSV, JSON, and XLSX files.

## Sensitivity Defaults

- Permission: needs-review
- Sensitivity: mixed
- Treat founder notes, customer interviews, pitch decks, financial models, investor feedback, and customer lists as confidential unless reviewed.
- Avoid exposing customer names, internal metrics, fundraising terms, or non-public strategy in extracted notes.

## Next Step

After adding files here, run:

```bash
python3 tools/ingest_sources.py scan \
  --raw-dir "00_Inbox/Raw Sources/evidence-based-startup-methodology" \
  --domain evidence-based-startup-methodology \
  --permission needs-review \
  --sensitivity mixed
```

Then review generated manifests in [[../../Source Manifests/README|Source Manifests]] before extracting knowledge notes.
