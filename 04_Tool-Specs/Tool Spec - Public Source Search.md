---
type: tool-spec
tool_name: source_search
status: active
tags: [tool, web-sources, search, public-source, ingestion]
reliability: medium
domain: agent-create-system
---

# Tool Spec - Public Source Search

## One-line Summary

Find public source candidates for a domain knowledge pack, score them for trust and public accessibility, and optionally queue them for download/review.

## Command

Search explicit queries:

```bash
python3 tools/source_search.py search "customer discovery startup official source" --domain evidence-based-startup-methodology
```

Generate queries from a knowledge pack:

```bash
python3 tools/source_search.py from-pack "Evidence-Based Startup Methodology" --report
```

Find book metadata/access candidates:

```bash
python3 tools/source_search.py books \
  --book "The Lean Startup | Eric Ries" \
  --book "Company of One: Why Staying Small Is the Next Big Thing for Business | Paul Jarvis" \
  --book "The 4-Hour Workweek | Tim Ferriss" \
  --domain evidence-based-startup-methodology \
  --report
```

Queue recommended candidates:

```bash
python3 tools/source_search.py from-pack "Evidence-Based Startup Methodology" --queue
```

Use Brave Search API:

```bash
BRAVE_SEARCH_API_KEY=... python3 tools/source_search.py search "NSF I-Corps customer discovery" --provider brave
```

Use only bookstore/library connectors, without generic web search:

```bash
python3 tools/source_search.py books \
  --book "The Lean Startup | Eric Ries" \
  --connector openlibrary \
  --connector google-books \
  --connector oreilly \
  --connector amazon \
  --no-web-queries
```

## Inputs

- Search query text or knowledge pack path/title/`pack_name`.
- Book targets as `Title | Author`.
- Optional domain slug for queue rows.
- Optional search provider: `auto`, `brave`, or `queries-only`.
- Optional book connectors: `web`, `openlibrary`, `google-books`, `oreilly`, `amazon`.
- Optional site filters, trusted hosts, result count, score threshold, and queue limit.
- Optional `BRAVE_SEARCH_API_KEY` environment variable for Brave Search API.
- Optional `GOOGLE_BOOKS_API_KEY` for Google Books API quota.
- Optional `OREILLY_API_TOKEN` and `OREILLY_AUTH_SCHEME` for authenticated O'Reilly Learning API search.
- Optional `AMAZON_PARTNER_TAG` for Amazon bookstore search URLs. Full Amazon SearchItems API support requires Amazon onboarding and partner credentials.
- Optional `--insecure-skip-tls-verify` for local development machines with broken Python CA configuration. Do not use this in production.
- Optional report output directory.

## Outputs

- Ranked source candidates with URL, title, snippet, host, source kind, public-likelihood label, trust score, and recommendation.
- Manual search URLs when no API key is configured.
- Optional rows appended to `00_Inbox/Web Source Queue.md`.
- Optional human-review Markdown report under `00_Inbox/Public Source Searches/`.

## Dependencies

- Python 3.10 or newer.
- Python standard library: `argparse`, `urllib`, `json`, `html`, `re`, `pathlib`.
- Optional Brave Search API key via `BRAVE_SEARCH_API_KEY`.
- Optional Google Books API key via `GOOGLE_BOOKS_API_KEY`.
- Optional O'Reilly Learning API token via `OREILLY_API_TOKEN`.
- Optional Amazon partner tag via `AMAZON_PARTNER_TAG`.
- No browser automation, crawler dependency, or SDK dependency.

## Connector Model

| Connector | What It Returns | Auth | Ingestion Rule |
| --- | --- | --- | --- |
| `web` | Search-engine candidates from Brave API or manual search URLs | Optional `BRAVE_SEARCH_API_KEY` | Queue candidates for review, then use `source_download` only on explicit approved URLs |
| `openlibrary` | Public library metadata and Open Library work pages | None | Treat as metadata, not replacement for book content |
| `google-books` | Public Google Books metadata and preview/info links | Optional `GOOGLE_BOOKS_API_KEY` | Treat previews as metadata/legal excerpts only |
| `oreilly` | O'Reilly Learning search results when token exists; otherwise public O'Reilly search page | `OREILLY_API_TOKEN` for API | Treat as subscription/owned-source candidate unless public page is explicitly accessible |
| `amazon` | Amazon Books search URLs, optionally tagged with `AMAZON_PARTNER_TAG` | Optional partner tag | Treat as bookstore metadata candidate, not source text |

## Provider References

- [Brave Web Search API](https://api-dashboard.search.brave.com/app/documentation/web-search/get-started)
- [Open Library Search API](https://openlibrary.org/dev/docs/api/search)
- [Google Books Volumes list API](https://developers.google.com/books/docs/v1/reference/volumes/list)
- [O'Reilly Platform Search API](https://www.oreilly.com/online-learning/integration-docs/search.html)
- [Amazon Creators API SearchItems](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/search-items)

## Safety Limits

- Prefers official, government, academic, known-primary, and primary framework sources.
- Flags login, signup, subscription, checkout, captcha, and paywall-like URLs as restricted.
- Does not download pages; hand off explicit URLs to `source_download`.
- Does not download copyrighted books or subscription content.
- Does not queue pirated PDFs, unauthorized full-book downloads, torrents, or suspicious ebook mirrors.
- Does not treat discovered candidates as trusted evidence until ingestion and source-note review.
- Defaults queued candidates to `permission: needs-review`.
- Verifies TLS by default; `--insecure-skip-tls-verify` is a local development workaround only.

## Failure Handling

- If no API key is available, return generated manual search queries instead of failing.
- If the provider request fails, report the query-level error and keep any pack-listed URL candidates.
- If a pack cannot be resolved, fail without changing queue files.
- If a candidate already exists in the Web Source Queue, skip the duplicate.
- If a candidate appears to be a pirated PDF, unauthorized full-book download, torrent, or suspicious ebook mirror, label it `copyright-risk` and `skip`.
- If a candidate has weak trust score or restricted access markers, label it `skip`.

## Related

- [[../00_Inbox/Web Source Queue|Web Source Queue]]
- [[Tool Spec - Web Source Download]]
- [[Tool Spec - Source Ingestion]]
- [[Tool Spec - Vault Retrieval]]
