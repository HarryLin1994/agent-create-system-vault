---
type: internal-module
status: active
tags: [module-system, domain-retrieval, knowledge-pack]
reliability: high
updated: 2026-09-07
---

# 05 - Knowledge Pack Builder

## One-line Summary

Bundle source-backed notes into scoped expert memory for one domain or decision area.

## Purpose

Prevent experts from searching the entire vault and give them a known boundary for what they can rely on.

## Trigger

Use when an expert agent needs domain knowledge or when extracted notes should become reusable memory.

## Inputs

- Expert domain.
- Target user and supported decisions.
- Source notes.
- Concept, case, claim, checklist, and failure-mode notes.
- Required tools.
- Unsupported areas.
- Golden retrieval questions.

## Outputs

- Knowledge pack note in `02_Domain-Knowledge/Packs`.
- Retrieval filters.
- Reliability floor.
- Included source/concept/case/tool/eval links.
- Unsupported areas.
- Golden retrieval question table.

## Dependencies

- [[../../_templates/Knowledge Pack Template|Knowledge Pack Template]]
- [[01 - Source Intake and Trust]]
- [[04 - Knowledge Note Writer]]
- [[../../07_Runbooks/Build Knowledge Pack For Expert|Build Knowledge Pack For Expert]]

## Runtime Instructions

- Keep a pack focused on one expert domain or decision class.
- Define what the expert can and cannot answer from the pack.
- Include enough source diversity for important claims.
- Prefer `medium` or `high` reliability for decisive advice.
- Add golden questions before considering the pack trustworthy.
- Record excluded tags or domains when confusion is likely.

## Failure Modes

- Pack scope is too broad.
- Pack contains notes with weak provenance.
- Unsupported areas are missing.
- No golden questions exist, so retrieval quality cannot be measured.

## Eval Coverage

- [[../../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]]
- `tools/validate_vault.py` pack contract checks.
- `tools/eval_retrieval.py` golden question checks.
