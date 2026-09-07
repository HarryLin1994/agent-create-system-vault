---
type: internal-module
status: active
tags: [module-system, domain-retrieval, obsidian, note-writing]
reliability: high
updated: 2026-09-07
---

# 04 - Knowledge Note Writer

## One-line Summary

Convert kept knowledge units into Obsidian notes that are both human-readable and machine-retrievable.

## Purpose

Make extracted knowledge durable, linkable, reviewable, and searchable without turning the vault into raw source dumps.

## Trigger

Use after [[03 - Knowledge Unit Extraction Gate]] accepts a unit.

## Inputs

- Kept knowledge unit.
- Source note link.
- Domain.
- Reliability label.
- Caveat or limitation.
- Target knowledge pack.

## Outputs

- Markdown note in the right folder.
- Flat frontmatter metadata.
- One-line summary.
- Source reference.
- Agent usage guidance.
- Caveat or limitation.
- Obsidian links to source, pack, capabilities, tools, or evals.

## Dependencies

- [[../../_templates/Knowledge Source Template|Knowledge Source Template]]
- [[../../02_Domain-Knowledge/README|Domain Knowledge]]
- [[../../02_Domain-Knowledge/Packs/README|Knowledge Packs]]

## Runtime Instructions

- Write one note per durable concept, case, claim, checklist, or failure mode.
- Keep source references short and traceable.
- Do not copy long copyrighted source text.
- Include `type`, `status`, `domain`, `tags`, `reliability`, and `updated`.
- Include `packs` when the note belongs to a knowledge pack.
- Link back to the source note.
- Write "Agent Usage" so an expert knows when to use the note.

## Failure Modes

- Creating notes without metadata.
- Creating notes that are too broad to retrieve.
- Copying raw source text instead of extracting expert-usable knowledge.
- Making machine-readable notes that humans cannot understand.

## Eval Coverage

- `tools/validate_vault.py` metadata and Obsidian-link checks.
- AI self-review and human checkpoint checklist in [[11 - Obsidian Human Review Interface]].
