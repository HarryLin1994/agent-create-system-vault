---
type: index
status: active
tags: [domain-knowledge, knowledge-pack, index]
reliability: medium
---

# Knowledge Packs

Knowledge packs are scoped bundles of sources, concepts, cases, claims, tools, and evals that can be attached to an expert agent.

## Purpose

Use a knowledge pack when an agent needs domain expertise without searching the whole vault or hardcoding domain content into the system prompt.

## What A Pack Owns

- Domain and user scope.
- Included sources, concepts, cases, checklists, and failure modes.
- Retrieval filters for this domain.
- Tool specs that the expert can use.
- Evidence rules and citation expectations.
- Known gaps and unsupported claims.
- Retrieval and answer-quality evals.

## Pack Rules

- Keep one pack focused on one domain or decision area.
- Link to source notes instead of copying long source text.
- Prefer high-reliability sources when notes conflict.
- Record why each note belongs in the pack.
- Include exclusion rules so the expert knows what not to retrieve.
- Include at least three golden retrieval questions before trusting the pack.

## Human Readability

Every pack should be useful inside Obsidian:

- Use wiki links for all included notes.
- Keep short tables for sources, concepts, cases, tools, and evals.
- Include an "Agent Usage" section that explains how the expert should use the pack.
- Include an "Unsupported Areas" section for gaps.

## Related

- [[../README|Domain Knowledge]]
- [[../../09_Module-System/Domain Knowledge Retrieval v1 Pipeline|Domain Knowledge Retrieval v1 Pipeline]]
- [[../../04_Tool-Specs/Tool Spec - Vault Retrieval|Vault Retrieval]]

## Current Packs

- [[Pack - Agent Create System Retrieval]]
