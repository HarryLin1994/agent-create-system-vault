---
type: module-standard
status: active
tags: [module-system, source-quality, certainty, reliability]
reliability: medium
---

# Source Trust and Certainty Standard

## One-line Summary

Use this standard when deciding whether the agent can rely on a source, claim certainty, or must label an answer as partial or unsupported.

## Trusted Source Rule

A source is trusted only for the claims it can actually support. Prefer sources with clear authority, provenance, recency, accuracy, and purpose.

## Source Tiers

| Tier | Use | Examples |
| --- | --- | --- |
| Primary | Strongest for facts about a system, API, policy, law, or event | Official docs, specs, original datasets, source code, published standards, legal text |
| Secondary | Useful for interpretation when sourced and current | Academic reviews, institutional guides, expert analysis with citations |
| Tertiary | Useful for orientation, not decisive support | Summaries, encyclopedic pages, unsourced explainers |
| Anecdotal | Useful as examples, not general rules | Interviews, conversations, forum posts, personal notes |

## Reliability Labels

| Label | Meaning |
| --- | --- |
| high | Primary or strongly sourced material directly supports the claim and is current enough for the decision. |
| medium | Credible but indirect, older, or interpretive material supports the claim with caveats. |
| low | Weak, anecdotal, stale, or hard-to-verify material. Use only as a lead or example. |
| draft | Not yet reviewed. Do not use as decisive evidence. |

## Certainty Labels

| Label | Meaning |
| --- | --- |
| supported | Retrieved evidence directly supports the answer. |
| partial | Evidence is relevant but incomplete, indirect, stale, or context-dependent. |
| gap | Retrieval found no adequate support. The expert should ask for more facts, search a trusted source, or state the gap. |
| conflict | Credible sources disagree. The expert should compare sources and avoid a single confident conclusion. |

## AI Self-Review Checklist

- Authority: Who produced the source, and are they qualified for this claim?
- Accuracy: Does the source show evidence, methodology, or traceable references?
- Currency: Is the source current enough for this domain?
- Relevance: Does it answer this exact question, not just nearby keywords?
- Purpose: Is the source trying to inform, persuade, sell, or speculate?
- Provenance: Can the claim be traced back to the source?

## Human Checkpoints

Humans only confirm:

- Input: the right source batch, domain, permission, sensitivity, and target expert scope are being processed.
- Output: the produced notes and evidence are understandable and useful.
- Performance: golden questions and real usage show acceptable behavior.

## Runtime Rule

When certainty is not supported, the expert must say what is missing and what would change the answer.

## Related

- [[Domain Knowledge Retrieval v1 Pipeline]]
- [[AI Self-Review and Human Checkpoint Standard]]
- [[../03_Capability-Modules/Capability - Evidence Grounding|Evidence Grounding]]
- [[../02_Domain-Knowledge/Concepts/Concept - Evidence Hierarchy|Evidence Hierarchy]]
