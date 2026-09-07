---
type: capability-module
status: active
tags: [capability, diagnostic-interview, requirements]
reliability: medium
---

# Capability - Diagnostic Interview

## One-line Summary

This module helps an agent ask only the questions needed to turn an underspecified request into a usable decision problem.

## Purpose

Turn an underspecified request into a clearer decision problem without forcing a long intake process.

## Trigger

Use when the user asks for advice, strategy, planning, diagnosis, or agent design and missing facts could change the answer.

## Inputs

- User request.
- Known user constraints.
- Retrieved blueprint, knowledge, or eval notes when available.
- Risk level of making assumptions.

## Outputs

- Current read of the user's situation.
- Missing facts that would change the recommendation.
- Reasonable assumptions when safe.
- A short set of high-impact questions or a provisional recommendation.

## Dependencies

- [[Capability - Evidence Grounding|Evidence Grounding]] when retrieved knowledge is available.
- [[../06_Evals/Eval - Refuse Unsupported Certainty|Refuse Unsupported Certainty]]

## Runtime Instructions

- Identify the decision the user is trying to make.
- Identify missing facts that would change the recommendation.
- Ask a small number of high-impact questions.
- Make a reasonable assumption only when the risk is low.
- If answering immediately, state assumptions clearly.

## Failure Modes

- Asking too many questions.
- Asking questions that do not affect the answer.
- Pretending the context is complete.

## Eval Coverage

- [[../06_Evals/Eval - Refuse Unsupported Certainty|Refuse Unsupported Certainty]]

## Related

- [[Capability - Evidence Grounding|Evidence Grounding]]
- [[../02_Domain-Knowledge/Cases/Case - Unsupported Certainty Failure|Unsupported Certainty Failure]]
