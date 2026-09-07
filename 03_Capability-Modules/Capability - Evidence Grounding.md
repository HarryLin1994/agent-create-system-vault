---
type: capability-module
status: active
tags: [capability, evidence, retrieval, grounding]
reliability: medium
---

# Capability - Evidence Grounding

## One-line Summary

This module makes an agent tie recommendations to retrieved notes, explicit assumptions, and confidence levels.

## Purpose

Prevent unsupported claims by grounding recommendations in retrieved notes, user-provided facts, and explicit assumptions.

## Trigger

Use when the agent has access to a knowledge base, source library, RAG retrieval layer, or any source material that should affect the answer.

## Inputs

- User request.
- Retrieved notes.
- Source reliability labels.
- Current agent blueprint and scope.

## Outputs

- Evidence used.
- Assumptions.
- Recommendation.
- Confidence level.
- What would change the recommendation.

## Dependencies

- [[../02_Domain-Knowledge/Concepts/Concept - Evidence Hierarchy|Evidence Hierarchy]]
- [[../04_Tool-Specs/Tool Spec - Vault Retrieval|Vault Retrieval]]

## Runtime Instructions

- Retrieve relevant notes before producing a final answer.
- Prefer high-reliability notes when conflicts exist.
- Use specific cases or concepts instead of broad claims.
- Mark unsupported claims as assumptions.
- Mention uncertainty when sources are weak or context-specific.

## Failure Modes

- Listing sources without using them.
- Citing irrelevant notes.
- Treating source summaries as universal rules.

## Eval Coverage

- [[../06_Evals/Eval - Refuse Unsupported Certainty|Refuse Unsupported Certainty]]

## Related

- [[../02_Domain-Knowledge/Concepts/Concept - Evidence Hierarchy|Evidence Hierarchy]]
- [[../04_Tool-Specs/Tool Spec - Vault Retrieval|Vault Retrieval]]
