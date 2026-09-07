---
type: knowledge-pack
pack_name: Agent Create System Retrieval
domain: agent-create-system
status: active
owner: Harry Lin
tags: [knowledge-pack, domain-knowledge, retrieval, module-system, agent-create-system]
reliability: high
source_reliability_floor: medium
updated: 2026-09-07
---

# Pack - Agent Create System Retrieval

## One-line Summary

Use this pack when building or reviewing the domain knowledge retrieval module system inside this vault.

## Scope

- Domain: agent-create-system
- Target users: agent builder, module designer, human reviewer
- Decisions this pack supports: how domain knowledge retrieval should ingest sources, write notes, scope retrieval, return evidence, and evaluate quality
- Out of scope: production OCR provider choice, production vector database choice, and the first external expert domain

## Retrieval Filters

- Required domain: agent-create-system
- Preferred note types: architecture-note, module-design-spec, tool-spec, knowledge-source, eval, internal-module
- Required tags: retrieval
- Excluded tags: draft-only
- Reliability floor: medium
- Freshness rule: verify external provider behavior before changing implementation details

## Included Sources

| Source | Type | Reliability | Use For | Caveat |
| --- | --- | --- | --- | --- |
| [[../Sources/Source - Retrieval and Tooling Best Practices]] | knowledge-source | high | Best-practice basis for retrieval, chunking, tool boundaries, extraction, and Obsidian metadata | Provider docs can change; recheck before production integration |

## Included Concepts

- [[../../09_Module-System/Domain Knowledge Retrieval Design Spec]]
- [[../../09_Module-System/Domain Retrieval Modules/System Architecture - 12 Module Pipeline]]
- [[../../09_Module-System/Source Trust and Certainty Standard]]

## Included Cases

- [[../Cases/Case - Unsupported Certainty Failure]]

## Included Tools

- [[../../04_Tool-Specs/Tool Spec - Vault Retrieval]]
- [[../../04_Tool-Specs/Tool Spec - Expert Vault Interface]]
- `tools/agent_retrieve.py`
- `tools/validate_vault.py`
- `tools/eval_retrieval.py`

## Agent Usage

Use this pack when the expert or builder needs to:

- Explain the 12-module domain retrieval pipeline.
- Identify each module's input/output contract.
- Run local retrieval with Obsidian links and answerability labels.
- Validate vault metadata and module contracts.
- Run golden-question retrieval evals.

When retrieved evidence is partial, the expert should:

- Say which source, note, metadata, chunk, ranking, or eval gap prevents a supported answer.
- Prefer a specific upstream fix over prompt-only patching.

## Unsupported Areas

- Production-grade OCR/vision extraction is designed but not implemented.
- Production vector search or embedding retrieval is intentionally deferred until V1 eval failures justify it.
- A first external expert domain has not been selected yet.

## Golden Retrieval Questions

| Question | Expected Notes | Acceptance Rule |
| --- | --- | --- |
| What is the 12 module pipeline for domain knowledge retrieval and its inputs and outputs? | [[../../09_Module-System/Domain Retrieval Modules/System Architecture - 12 Module Pipeline]] | Expected note appears in top 3; answerability supported. |
| How should vault retrieval return evidence with Obsidian links and answerability? | [[../../04_Tool-Specs/Tool Spec - Vault Retrieval]] | Expected note appears in top 3; answerability supported. |
| Which trusted sources justify metadata filtering, chunking, document extraction, and Obsidian links? | [[../Sources/Source - Retrieval and Tooling Best Practices]] | Expected note appears in top 3; answerability supported. |

## Related Evals

- [[../../06_Evals/Eval - Domain Retrieval Relevance]]
