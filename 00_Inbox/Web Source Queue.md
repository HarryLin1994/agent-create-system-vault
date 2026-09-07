---
type: web-source-queue
status: active
tags: [inbox, web-sources, crawler, ingestion]
reliability: medium
updated: 2026-09-07
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
|  |  |  | needs-review | queued |

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
