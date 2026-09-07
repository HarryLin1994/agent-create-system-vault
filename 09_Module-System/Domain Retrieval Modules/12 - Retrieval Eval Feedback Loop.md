---
type: internal-module
status: active
tags: [module-system, domain-retrieval, eval, feedback-loop]
reliability: high
updated: 2026-09-07
---

# 12 - Retrieval Eval Feedback Loop

## One-line Summary

Use golden questions and failure cases to improve extraction, metadata, chunking, ranking, and knowledge packs.

## Purpose

Prove whether retrieval works for the expert's real questions instead of assuming the design is good.

## Trigger

Use before trusting a knowledge pack, after adding sources, after changing ranking, or when the expert cites bad evidence.

## Inputs

- Golden retrieval questions.
- Expected note paths.
- Negative notes that should not be cited.
- Retrieval output.
- AI self-review result.
- Human performance checkpoint when needed.

## Outputs

- Pass/fail result per question.
- Retrieval failure category.
- Fix recommendation.
- Updated metadata, notes, chunks, pack filters, ranking, or evals.
- Human-readable performance checkpoint summary.

## Dependencies

- [[../../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]]
- [[05 - Knowledge Pack Builder]]
- [[08 - Retrieval Ranker]]
- [[10 - Gap and Conflict Detector]]

## Runtime Instructions

- Every knowledge pack needs three to five golden questions before use.
- Expected note should appear in top 3 for supported questions.
- Unsupported questions should produce `partial` or `gap`.
- Citation tests should ensure the expert does not cite irrelevant notes.
- Each failure should be classified:
  - source missing
  - extraction missing
  - metadata wrong
  - chunk too broad
  - query routing wrong
  - ranking wrong
  - evidence pack missing field
  - gap/conflict label wrong
- AI should self-review whether failures belong to source intake, extraction, metadata, chunking, ranking, pack scope, or eval design before asking for human input.
- Humans should only be asked whether the observed behavior is acceptable or what performance target changed.

## Failure Modes

- Retrieval is judged by intuition instead of test cases.
- Ranking changes have no regression check.
- Golden questions are too easy or do not match expert usage.
- Failures are patched in prompts instead of fixed in source, metadata, or retrieval.

## Eval Coverage

- This module owns [[../../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]].
- `tools/eval_retrieval.py` runs knowledge-pack golden retrieval questions.
