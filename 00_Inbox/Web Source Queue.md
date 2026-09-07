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
| https://www.ycombinator.com/library/4D-yc-s-essential-startup-advice | evidence-based-startup-methodology | Startup execution defaults: launch early, talk to users, and avoid premature scaling. | public | queued |
| https://steveblank.com/category/customer-development-manifesto/ | evidence-based-startup-methodology | Primary Steve Blank customer development material for outside-the-building validation. | public | queued |
| https://hbr.org/2013/05/why-the-lean-start-up-changes-everything | evidence-based-startup-methodology | Original HBR article explaining why lean startup changes product development and venture launch practice. | needs-review | queued |
| https://www.nsf.gov/funding/initiatives/i-corps | evidence-based-startup-methodology | Official NSF I-Corps source for customer discovery and evidence-based commercialization context. | public | queued |
| https://theleanstartup.com/principles | evidence-based-startup-methodology | Primary Lean Startup principles for validated learning and build-measure-learn framing. | public | queued |
| https://theleanstartup.com/book | evidence-based-startup-methodology | Official book page for The Lean Startup priority source target. | public | queued |
| https://www.penguin.co.uk/books/312524/company-of-one-by-jarvis-paul/9780241380239 | evidence-based-startup-methodology | Publisher page for Company of One priority source target. | public | queued |
| https://www.penguinrandomhouse.com/books/49081/the-4-hour-workweek-expanded-and-updated-by-timothy-ferriss/ | evidence-based-startup-methodology | Publisher page for The 4-Hour Workweek priority source target. | public | queued |
| https://www.strategyzer.com/library/the-business-model-canvas | evidence-based-startup-methodology | Strategyzer source for business model hypothesis structure. | public | queued |
| https://www.strategyzer.com/library/the-value-proposition-canvas | evidence-based-startup-methodology | Strategyzer source for customer jobs, pains, gains, and value proposition fit. | public | queued |
| https://www.cbinsights.com/research/report/startup-failure-reasons-top/ | evidence-based-startup-methodology | Startup failure-risk source for no market need, cash runway, team, pricing, and scaling risk patterns. | public | queued |

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
