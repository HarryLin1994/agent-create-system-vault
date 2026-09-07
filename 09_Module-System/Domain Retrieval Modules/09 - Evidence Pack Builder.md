---
type: internal-module
status: active
tags: [module-system, domain-retrieval, evidence-pack]
reliability: high
updated: 2026-09-07
---

# 09 - Evidence Pack Builder

## One-line Summary

Normalize ranked retrieval results into a stable evidence pack for expert agents and human review.

## Purpose

Give the expert enough structured context to use evidence correctly without dumping raw notes into the prompt.

## Trigger

Use after retrieval ranking and before the expert produces an answer.

## Inputs

- Ranked results from [[08 - Retrieval Ranker]].
- Query and filters from [[07 - Query Scope Router]].
- Source references.
- Usage guidance and caveats.
- Obsidian paths.

## Outputs

- Evidence pack JSON.
- Human-readable evidence list.
- Answerability field placeholder or final label.
- Obsidian URI for every result.
- Gaps list when evidence is missing.

## Dependencies

- [[08 - Retrieval Ranker]]
- [[10 - Gap and Conflict Detector]]
- [[../../04_Tool-Specs/Tool Spec - Vault Retrieval|Vault Retrieval]]
- [[11 - Obsidian Human Review Interface]]

## Runtime Instructions

- Include query, vault, filters, answerability, results, and gaps.
- Each result must include path, Obsidian URI, title, type, heading, tags, domain, status, reliability, summary, excerpt, source reference, usage guidance, caveat, and score.
- Keep excerpts concise and source-backed.
- Never hide `partial`, `gap`, or `conflict` status.
- Make JSON stable so tools and evals can depend on it.

## Failure Modes

- Evidence pack omits source or reliability.
- Results cannot be opened in Obsidian.
- Excerpts are too long or copyright unsafe.
- The evidence pack looks like a final answer and the expert stops reasoning.

## Eval Coverage

- JSON schema validation in V1.1.
- [[../../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]]
