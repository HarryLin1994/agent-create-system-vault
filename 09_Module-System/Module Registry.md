---
type: module-registry
status: active
tags: [module-system, registry]
reliability: medium
---

# Module Registry

Track reusable modules here.

| Module | Type | Status | Primary Trigger | Eval Coverage |
| --- | --- | --- | --- | --- |
| [[../03_Capability-Modules/Capability - Diagnostic Interview|Diagnostic Interview]] | capability | active | User request is underspecified | [[../06_Evals/Eval - Refuse Unsupported Certainty|Refuse Unsupported Certainty]] |
| [[../03_Capability-Modules/Capability - Evidence Grounding|Evidence Grounding]] | capability | active | Answer depends on retrieved knowledge or source material | [[../06_Evals/Eval - Refuse Unsupported Certainty|Refuse Unsupported Certainty]] |
| [[Domain Knowledge Retrieval Design Spec]] | design-spec | active | Need to design or change retrieval architecture | [[../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]] |
| [[Domain Retrieval Modules/README|Domain Retrieval Modules]] | internal-module-set | active | Need to build retrieval pipeline one module at a time | [[../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]] |
| [[../03_Capability-Modules/Capability - Domain Knowledge Retrieval|Domain Knowledge Retrieval]] | capability | active | Skill needs domain expertise from local sources | [[../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]] |
| [[../02_Domain-Knowledge/Packs/README|Knowledge Packs]] | knowledge | active | Expert needs scoped domain memory | [[../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]] |
| [[../04_Tool-Specs/Tool Spec - Vault Retrieval|Vault Retrieval]] | tool | active | Need to search vault notes | [[../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]] |
| [[../04_Tool-Specs/Tool Spec - Expert Vault Interface|Expert Vault Interface]] | tool | active | Expert needs vault retrieval plus Obsidian review links | [[../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]] |
| [[Source Trust and Certainty Standard]] | standard | active | Need to judge whether a source can support certainty | [[../06_Evals/Eval - Refuse Unsupported Certainty|Refuse Unsupported Certainty]] |
| [[AI Self-Review and Human Checkpoint Standard]] | standard | active | Need to separate AI content review from human input/output/performance checkpoints | [[../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]] |

## Registry Rules

- Add a module here only after it follows [[Module Contract]].
- Every module should eventually have eval coverage.
- Prefer fewer, stronger modules over many overlapping modules.
