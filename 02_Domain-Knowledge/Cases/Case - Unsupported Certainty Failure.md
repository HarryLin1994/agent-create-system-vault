---
type: case
status: failure-pattern
tags: [case, failure-pattern, hallucination, certainty]
reliability: medium
---

# Case - Unsupported Certainty Failure

## One-line Summary

An agent fails when it gives confident strategic advice without enough facts, sources, or context.

## Context

The user asks a broad question. The agent answers with a strong recommendation before knowing the user's goals, constraints, evidence, or available options.

## Failure Pattern

- Treats a vague question as fully specified.
- Uses generic best practices as if they are evidence.
- Does not ask for missing facts.
- Does not state assumptions.
- Does not explain what would change the recommendation.

## Prevention

- Use a diagnostic interview when missing facts affect the answer.
- Retrieve relevant knowledge before recommending.
- Separate evidence from assumptions.
- Include what would change the recommendation.

## Related

- [[../Concepts/Concept - Evidence Hierarchy|Evidence Hierarchy]]
- [[../../03_Capability-Modules/Capability - Diagnostic Interview|Diagnostic Interview]]
- [[../../06_Evals/Eval - Refuse Unsupported Certainty|Refuse Unsupported Certainty]]

