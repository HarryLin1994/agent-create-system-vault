---
type: internal-module
status: active
tags: [module-system, domain-retrieval, ranking]
reliability: high
updated: 2026-09-07
---

# 08 - Retrieval Ranker

## One-line Summary

Rank candidate chunks by relevance, metadata match, reliability, and result diversity.

## Purpose

Return the evidence most likely to support the expert's answer while avoiding irrelevant keyword matches and duplicate note flooding.

## Trigger

Use after [[06 - Retrieval Index Builder]] creates candidates and [[07 - Query Scope Router]] provides query filters.

## Inputs

- Query tokens.
- Candidate chunks.
- Note metadata.
- Knowledge pack filters.
- Reliability floor.

## Outputs

- Ranked candidate results.
- Score per result.
- Best matching heading per note.
- Diverse top-k evidence candidates.

## Dependencies

- [[06 - Retrieval Index Builder]]
- [[07 - Query Scope Router]]
- [[../Source Trust and Certainty Standard]]
- `tools/agent_retrieve.py`

## Runtime Instructions

- Boost title, heading, tag, type, and domain matches.
- Penalize or filter below the reliability floor.
- Keep only the best chunk per note by default.
- Prefer scoped pack matches over global matches.
- Do not let popularity or repeated terms override source relevance.
- Keep lexical ranking in V1; add hybrid semantic retrieval only after eval failures justify it.

## Failure Modes

- Top-k contains many chunks from one note.
- Relevant source notes are buried under generic module notes.
- High keyword score masks low source quality.
- Ranking weights are changed without eval evidence.

## Eval Coverage

- Expected note in top 3 for supported golden questions.
- Negative tests for irrelevant keyword matches.
