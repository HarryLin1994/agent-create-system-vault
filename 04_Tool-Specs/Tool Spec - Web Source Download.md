---
type: tool-spec
tool_name: source_download
status: active
tags: [tool, web-sources, download, crawler, ingestion]
reliability: medium
domain: agent-create-system
---

# Tool Spec - Web Source Download

## One-line Summary

Download explicit URLs or crawl a small same-host area into raw source intake while checking robots rules and creating source manifests.

## Command

Download explicit URLs:

```bash
python3 tools/source_download.py download "https://example.com/page" --domain your-domain
```

Crawl a small same-host area:

```bash
python3 tools/source_download.py crawl "https://example.com/docs/" --domain your-domain --max-pages 10 --max-depth 1
```

## Inputs

- One or more HTTP/HTTPS URLs.
- Optional URL file.
- Raw output folder.
- Manifest output folder.
- Domain, permission, and sensitivity defaults.
- User agent.
- Request delay, timeout, max bytes, depth, and page limit.
- Optional dry-run mode.

## Outputs

- Downloaded raw files under `00_Inbox/Raw Sources/_downloads`.
- One source manifest per downloaded URL.
- `source_id`, SHA-256 hash, content type, source URL, size, raw path, and manifest path.
- JSON or human-readable download report.

## Dependencies

- Python 3.10 or newer.
- Python standard library: `urllib`, `urllib.robotparser`, `html.parser`, `hashlib`, `mimetypes`.
- No search engine scraping dependency.

## Safety Limits

- Checks `robots.txt` before downloading.
- Uses same-host crawl by default.
- Uses a low default request rate.
- Uses a default response size limit.
- Does not bypass logins, paywalls, captchas, or access controls.
- Does not treat downloaded content as trusted evidence until source notes are reviewed.

## Failure Handling

- If a URL is blocked by robots rules, skip it and report `blocked-by-robots`.
- If a URL exceeds `--max-bytes`, skip it and report the size failure.
- If a host is unavailable, report the exception per URL.
- If a crawl sees cross-host links, skip them unless `--cross-host` is set.
- If a content type is unknown, save it with a safe extension and require manual review.

## Related

- [[../00_Inbox/Web Source Queue|Web Source Queue]]
- [[../00_Inbox/Raw Sources/README|Raw Sources]]
- [[../00_Inbox/Source Manifests/README|Source Manifests]]
- [[Tool Spec - Source Ingestion]]
