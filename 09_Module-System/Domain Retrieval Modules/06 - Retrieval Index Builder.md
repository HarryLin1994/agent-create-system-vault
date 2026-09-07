---
type: internal-module
status: active
tags: [module-system, domain-retrieval, indexing, chunks]
reliability: high
updated: 2026-09-07
---

# 06 - Retrieval Index Builder

## One-line Summary

Build a searchable representation of notes, headings, metadata, source references, and Obsidian paths.

## Purpose

Give retrieval a structured index instead of repeatedly scanning unstructured raw files.

## Trigger

Use after notes or knowledge packs change, or on demand for local CLI retrieval.

## Inputs

- Obsidian Markdown notes.
- Frontmatter metadata.
- Headings and section text.
- Source references.
- Knowledge pack filters.

## Outputs

- Searchable note records.
- Heading-level chunks.
- Metadata fields for filtering.
- Obsidian URI for each note.
- Source reference and usage guidance fields.

## Dependencies

- [[04 - Knowledge Note Writer]]
- [[05 - Knowledge Pack Builder]]
- [[../../04_Tool-Specs/Tool Spec - Vault Retrieval|Vault Retrieval]]
- `tools/agent_retrieve.py`

## Runtime Instructions

- Parse frontmatter before body text.
- Skip `.obsidian`, templates when inappropriate, hidden folders, and tool internals.
- Chunk by Markdown heading in V1.
- Include title, type, tags, domain, reliability, heading, and source reference in searchable text.
- Skip knowledge-pack eval metadata sections such as `Golden Retrieval Questions` and `Related Evals` when building runtime evidence chunks.
- Return only the best chunk per note by default to avoid duplicate result flooding.
- Defer embeddings until metadata and eval failures show lexical search is insufficient.

## Failure Modes

- Broken frontmatter makes filters unreliable.
- Chunks are too large or too small.
- One note dominates all results.
- Index loses Obsidian paths or source references.

## Eval Coverage

- Retrieval smoke tests using `tools/agent_retrieve.py`.
- `tools/validate_vault.py` metadata and Obsidian-link checks.
- `tools/eval_retrieval.py` expected-note ranking checks.
