---
type: internal-module
status: active
tags: [module-system, domain-retrieval, gaps, conflict]
reliability: high
updated: 2026-09-07
---

# 10 - Gap and Conflict Detector

## One-line Summary

Decide whether retrieved evidence supports an expert answer, partially supports it, exposes a gap, or contains conflict.

## Purpose

Stop the expert from converting weak or conflicting retrieval into confident advice.

## Trigger

Use after retrieval ranking and before final expert answer generation.

## Inputs

- Evidence candidates.
- Source reliability labels.
- Source dates and caveats.
- Knowledge pack unsupported areas.
- User question.

## Outputs

- Answerability: `supported`, `partial`, `gap`, or `conflict`.
- Gap messages.
- Conflict notes.
- Recommendation on whether to answer, ask a question, retrieve more, or use web verification.

## Dependencies

- [[../Source Trust and Certainty Standard]]
- [[09 - Evidence Pack Builder]]
- [[../../03_Capability-Modules/Capability - Evidence Grounding|Evidence Grounding]]

## Runtime Instructions

- Use `supported` only when evidence directly answers the question with medium-or-better reliability.
- Use `partial` when evidence is relevant but incomplete, stale, indirect, or context-dependent.
- Use `gap` when retrieval cannot support the answer.
- Use `conflict` when credible sources disagree.
- If answerability is not supported, the expert must state what is missing and what would change the answer.

## Failure Modes

- Low-reliability evidence is treated as decisive.
- Missing context is hidden.
- Conflicts are averaged into a false single answer.
- The expert claims certainty because a note was retrieved.

## Eval Coverage

- [[../../06_Evals/Eval - Refuse Unsupported Certainty|Refuse Unsupported Certainty]]
- [[../../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]]
