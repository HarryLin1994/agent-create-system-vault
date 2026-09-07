---
type: knowledge-pack
pack_name: Evidence-Based Startup Methodology
domain: evidence-based-startup-methodology
status: needs-source
owner: Harry Lin
tags: [knowledge-pack, domain-knowledge, startup, customer-discovery, mvp, pmf, go-to-market, pivot]
reliability: draft
source_reliability_floor: medium
updated: 2026-09-07
---

# Pack - Evidence-Based Startup Methodology

## One-line Summary

Use this pack to build a startup execution advisor grounded in customer evidence, MVP experiments, business model validation, PMF signals, go-to-market learning, and pivot/persevere decisions.

## Scope

- Domain: 證據導向創業方法論，涵蓋創業想法、customer discovery、MVP、商業模式、PMF、go-to-market，以及 pivot / persevere 的執行方法。
- Target expert: 創業執行顧問。
- Target users: founders, product builders, early startup operators, and human reviewers.
- Decisions this pack supports: whether to start a startup idea, which assumptions to validate first, how much MVP to build, which business model risks matter, whether to pivot/persevere/continue experiments, whether the team is scaling too early, and what the next 1-2 week sprint should do.
- Out of scope: legal, tax, accounting, investment advice, fundraising guarantees, valuation judgment, final business decisions for the founder, unsupported certainty without customer evidence, and regulated-industry compliance judgment.

## Priority Book Targets

| Book | Author | Priority | Public Source Rule | Use For |
| --- | --- | --- | --- | --- |
| The Lean Startup | Eric Ries | high | Use official book site, publisher metadata, legal previews, or user-provided files with processing permission. Do not download unauthorized full text. | Validated learning, MVP, build-measure-learn, pivot/persevere |
| Company of One: Why Staying Small Is the Next Big Thing for Business | Paul Jarvis | high | Use official author/publisher pages, bookstore metadata, legal previews, or user-provided files with processing permission. Do not download unauthorized full text. | Staying small, scale restraint, sustainable solo/small-company operating model |
| The 4-Hour Workweek | Tim Ferriss | high | Use official author/publisher pages, bookstore metadata, legal previews, or user-provided files with processing permission. Do not download unauthorized full text. | Automation, delegation, lifestyle-business assumptions, productivity experiments |

Book content rule: do not search for, queue, download, or ingest pirated PDFs, unauthorized ebook mirrors, torrents, or full-book downloads. Use only legal public metadata, official pages, licensed subscription access, legal previews, or user-provided files that the user has permission to process.

## Retrieval Filters

- Required domain: evidence-based-startup-methodology
- Preferred note types: knowledge-source, concept, case, checklist, eval, source-manifest, tool-spec
- Required tags: startup, customer-discovery, mvp, pmf, go-to-market, pivot
- Excluded tags: confidential unless the user has permission and a need to know
- Permission rule: public methodology can be used directly; founder notes, customer interviews, pitch decks, financial models, investor feedback, and customer lists need review before retrieval or citation.
- Sensitivity rule: avoid exposing customer names, internal metrics, fundraising terms, private strategy, or personally identifiable details.
- Reliability floor: medium
- Freshness rule: verify current provider guidance, market statistics, and failure-rate reports before using them as current factual claims.

## Included Sources

| Source | Type | Reliability Target | Status | Use For |
| --- | --- | --- | --- | --- |
| [YC's Essential Startup Advice](https://www.ycombinator.com/library/4D-yc-s-essential-startup-advice) | Primary startup accelerator guidance | high | queued | Early execution defaults, launch discipline, user focus, premature scaling risk |
| [Steve Blank Customer Development Manifesto](https://steveblank.com/category/customer-development-manifesto/) | Primary methodology source | high | queued | Customer development and outside-the-building validation |
| [Why the Lean Start-Up Changes Everything](https://hbr.org/2013/05/why-the-lean-start-up-changes-everything) | Original article by Steve Blank | high | queued | Lean startup framing for hypothesis testing and customer feedback loops |
| [NSF I-Corps](https://www.nsf.gov/funding/initiatives/i-corps) | Official program source | high | queued | Customer discovery and evidence-based commercialization |
| [The Lean Startup Principles](https://theleanstartup.com/principles) | Primary methodology source | high | queued | Validated learning, MVP framing, build-measure-learn |
| [The Lean Startup book page](https://theleanstartup.com/book) | Official book page | high | queued | Priority book metadata and legal public context |
| [Company of One publisher page](https://www.penguin.co.uk/books/312524/company-of-one-by-jarvis-paul/9780241380239) | Publisher page | medium | queued | Priority book metadata and legal public context |
| [The 4-Hour Workweek publisher page](https://www.penguinrandomhouse.com/books/49081/the-4-hour-workweek-expanded-and-updated-by-timothy-ferriss/) | Publisher page | medium | queued | Priority book metadata and legal public context |
| [Strategyzer Business Model Canvas](https://www.strategyzer.com/library/the-business-model-canvas) | Primary framework source | high | queued | Business model assumptions and model structure |
| [Strategyzer Value Proposition Canvas](https://www.strategyzer.com/library/the-value-proposition-canvas) | Primary framework source | high | queued | Customer jobs, pains, gains, and value proposition fit |
| [CB Insights: Why Startups Fail](https://www.cbinsights.com/research/report/startup-failure-reasons-top/) | Research report | medium | queued | Failure modes, no-market-need risk, cash/runway and scaling signals |

## Included Concepts

- Pending extraction: falsifiable startup hypotheses.
- Pending extraction: customer discovery and customer development.
- Pending extraction: MVP as minimum validated-learning mechanism.
- Pending extraction: business model assumptions.
- Pending extraction: value proposition fit.
- Pending extraction: product-market fit evidence.
- Pending extraction: pivot, persevere, or continue experimenting.
- Pending extraction: premature scaling risk.
- Pending extraction: go-to-market experiments.
- Pending extraction: 1-2 week evidence sprint planning.

## Included Cases

- Pending extraction: founder has idea but no customer evidence.
- Pending extraction: users say they like the product but retention and willingness to pay are weak.
- Pending extraction: MVP scope is growing before validation.
- Pending extraction: team is scaling hiring, product, sales, or fundraising before PMF signals are strong.
- Pending extraction: business model assumptions are untested.

## Included Tools

- [[../../04_Tool-Specs/Tool Spec - Vault Retrieval|Vault Retrieval]]
- [[../../04_Tool-Specs/Tool Spec - Public Source Search|Public Source Search]]
- [[../../04_Tool-Specs/Tool Spec - Web Source Download|Web Source Download]]
- [[../../04_Tool-Specs/Tool Spec - Source Ingestion|Source Ingestion]]
- `tools/source_search.py`
- `tools/source_download.py`
- `tools/ingest_sources.py`
- `tools/agent_retrieve.py`
- `tools/eval_retrieval.py`

## Agent Usage

Use this pack when a founder asks for execution advice that should be grounded in evidence instead of generic encouragement.

The expert should:

- Ask what customer evidence exists before giving strong direction.
- Turn an idea into explicit hypotheses, risks, experiments, and decision thresholds.
- Separate interview signal, behavioral signal, retention signal, payment signal, and sales pipeline signal.
- Prefer the smallest next experiment that can reduce the highest-risk uncertainty.
- Cite source notes after ingestion, including file name, section, page, URL, or chunk id when available.
- Label answers as supported, partial, or gap when the current knowledge base cannot support the requested conclusion.
- Keep confidential founder and customer material out of answers unless permission and relevance are explicit.

## Unsupported Areas

- Legal, tax, accounting, securities, valuation, or investment advice.
- Guarantees about fundraising success, market outcome, or startup success.
- Founder final decision ownership.
- Claims that a product will succeed without customer evidence.
- Highly regulated industry compliance judgment, including medical, finance, insurance, and similar domains.
- Use of confidential founder notes, customer interviews, pitch decks, financial models, investor feedback, or customer lists before review.

## Golden Retrieval Questions

| Question | Expected Notes | Acceptance Rule |
| --- | --- | --- |
| 我有一個創業點子，還沒做產品，第一步應該驗證什麼？ | Steve Blank Customer Development Manifesto; NSF I-Corps | Expected sources appear in top results after ingestion; answerability supported. |
| 我的 MVP 應該做到什麼程度才可以 launch？ | YC's Essential Startup Advice; The Lean Startup Principles | Expected sources appear in top results after ingestion; answerability supported. |
| 使用者說喜歡，但留存和付費都很弱，我該 pivot 還是繼續做？ | The Lean Startup Principles; YC's Essential Startup Advice | Expected sources appear in top results after ingestion; answerability supported. |
| 我怎麼知道現在有沒有 product-market fit？ | YC's Essential Startup Advice; Strategyzer Value Proposition Canvas | Expected sources appear in top results after ingestion; answerability partial until PMF-specific source notes are added. |
| 我們是不是太早 scale？ | YC's Essential Startup Advice; CB Insights: Why Startups Fail | Expected sources appear in top results after ingestion; answerability supported. |

## Related Evals

- [[../../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]]
