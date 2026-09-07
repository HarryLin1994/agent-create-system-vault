---
type: index
tags: [evals, index]
---

# Evals

Evals define whether an agent behaves correctly. Every serious agent should have evals before it is trusted.

Use [[../_templates/Eval Case Template|Eval Case Template]].

## Eval Types

- Golden answer: expected shape and required points.
- Rubric: score the answer against criteria.
- Adversarial: make sure the agent avoids unsafe or low-quality behavior.
- Regression: protect behavior that already works.

## Current Evals

- [[Eval - Refuse Unsupported Certainty|Refuse Unsupported Certainty]]
- [[Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]]
