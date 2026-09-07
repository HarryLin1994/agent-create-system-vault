---
type: index
status: active
tags: [module-system, domain-retrieval, module-set, index]
reliability: high
updated: 2026-09-07
---

# Domain Retrieval Modules

This folder splits domain knowledge retrieval into internal modules that can be designed, built, tested, and replaced independently.

## Module Order

1. [[00 - Modularization Plan]]
2. [[01 - Source Intake and Trust]]
3. [[02 - Media Extraction Adapters]]
4. [[03 - Knowledge Unit Extraction Gate]]
5. [[04 - Knowledge Note Writer]]
6. [[05 - Knowledge Pack Builder]]
7. [[06 - Retrieval Index Builder]]
8. [[07 - Query Scope Router]]
9. [[08 - Retrieval Ranker]]
10. [[09 - Evidence Pack Builder]]
11. [[10 - Gap and Conflict Detector]]
12. [[11 - Obsidian Human Review Interface]]
13. [[12 - Retrieval Eval Feedback Loop]]

## Boundary

These are system-internal retrieval modules. Runtime agents should normally use the public capability and tool specs:

- [[../../03_Capability-Modules/Capability - Domain Knowledge Retrieval|Domain Knowledge Retrieval]]
- [[../../04_Tool-Specs/Tool Spec - Vault Retrieval|Vault Retrieval]]
- [[../../04_Tool-Specs/Tool Spec - Expert Vault Interface|Expert Vault Interface]]

## Related

- [[../Domain Knowledge Retrieval Design Spec]]
- [[../Domain Knowledge Retrieval v1 Pipeline]]
- [[../Source Trust and Certainty Standard]]
