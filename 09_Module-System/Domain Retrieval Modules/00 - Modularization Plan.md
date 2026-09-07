---
type: module-plan
status: active
tags: [module-system, domain-retrieval, planning]
reliability: high
updated: 2026-09-07
---

# 00 - Modularization Plan

## One-line Summary

Build domain knowledge retrieval as a chain of small modules, each with clear inputs, outputs, failure modes, and eval coverage.

## Planning

| Order | Module | Job | Done When |
| --- | --- | --- | --- |
| 1 | [[01 - Source Intake and Trust]] | Register source identity and source trust before extraction. | Every source has provenance, source type, reliability, and review status. |
| 2 | [[02 - Media Extraction Adapters]] | Choose extraction path for books, reports, images, charts, transcripts, and data. | Each media type maps to expected extracted fields and human checks. |
| 3 | [[03 - Knowledge Unit Extraction Gate]] | Decide what raw material is expert-usable. | Keep/drop decisions are explicit and auditable. |
| 4 | [[04 - Knowledge Note Writer]] | Convert kept units into Obsidian notes. | Notes have metadata, links, summaries, caveats, and source references. |
| 5 | [[05 - Knowledge Pack Builder]] | Bundle notes into scoped expert memory. | Pack has domain, scope, filters, sources, unsupported areas, and golden questions. |
| 6 | [[06 - Retrieval Index Builder]] | Build searchable chunks and metadata views. | Index includes heading chunks, metadata, source refs, and Obsidian paths. |
| 7 | [[07 - Query Scope Router]] | Route query to pack and filters. | Query has domain, intent, filters, and reliability floor. |
| 8 | [[08 - Retrieval Ranker]] | Rank candidate chunks. | Results are diverse, scoped, and not dominated by one note. |
| 9 | [[09 - Evidence Pack Builder]] | Normalize results into agent-facing evidence. | Evidence pack schema is stable and includes Obsidian review links. |
| 10 | [[10 - Gap and Conflict Detector]] | Label support quality. | Output says `supported`, `partial`, `gap`, or `conflict`. |
| 11 | [[11 - Obsidian Human Review Interface]] | Make the pipeline understandable to humans. | Humans can inspect sources, packs, evidence, and evals in Obsidian. |
| 12 | [[12 - Retrieval Eval Feedback Loop]] | Test and improve retrieval quality. | Golden questions catch relevance, citation, gap, and conflict failures. |

## Build Rule

Implement in this order. Do not improve ranking before source metadata and knowledge-unit extraction are clean.

## V1 Completion Target

V1 is complete when:

- Each module has an active spec.
- The existing CLI retrieval tool maps to modules 6 through 10.
- Humans have a runbook for modules 1 through 5 and 11.
- Evals exist for module 12.
- Obsidian links connect planning, specs, runbooks, tool specs, and evals.
- [[System Architecture - 12 Module Pipeline]] documents the full module input/output contract.
- `tools/validate_vault.py` checks metadata, module contracts, and Obsidian links.
- `tools/eval_retrieval.py` runs knowledge-pack golden retrieval questions.

## Related

- [[../Domain Knowledge Retrieval Design Spec]]
- [[../../07_Runbooks/Extract Expert Knowledge From Sources|Extract Expert Knowledge From Sources]]
- [[../../07_Runbooks/Build Knowledge Pack For Expert|Build Knowledge Pack For Expert]]
