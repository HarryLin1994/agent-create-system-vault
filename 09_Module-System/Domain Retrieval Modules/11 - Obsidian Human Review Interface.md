---
type: internal-module
status: active
tags: [module-system, domain-retrieval, obsidian, human-review]
reliability: high
updated: 2026-09-07
---

# 11 - Obsidian Human Review Interface

## One-line Summary

Make every important retrieval artifact understandable and inspectable in Obsidian.

## Purpose

Let a human maintain, review, and debug expert knowledge without reading only JSON or code.

## Trigger

Use whenever the pipeline creates source notes, extracted notes, knowledge packs, evidence packs, evals, or tool specs.

## Inputs

- Markdown notes.
- Obsidian wiki links.
- Evidence pack result paths.
- Source references.
- Human review flags.

## Outputs

- Obsidian-readable indexes.
- Wiki links between source, extracted notes, packs, tools, and evals.
- `obsidian_uri` links in evidence packs.
- Review statuses such as `draft`, `active`, `needs-source`, `needs-vision`, and `needs-human-review`.

## Dependencies

- Obsidian Properties and Internal Links docs captured in [[../../02_Domain-Knowledge/Sources/Source - Retrieval and Tooling Best Practices|Retrieval and Tooling Best Practices]]
- [[04 - Knowledge Note Writer]]
- [[09 - Evidence Pack Builder]]

## Runtime Instructions

- Keep Obsidian as the canonical human-readable vault.
- Use flat YAML frontmatter for metadata.
- Use wiki links for all system relationships.
- Every retrieved result should include an Obsidian URI.
- Index pages should show what exists and where to start.
- Human review flags should be visible in note metadata and body text.

## Failure Modes

- Machine artifacts are not readable by humans.
- JSON results do not link back to notes.
- Notes exist but are disconnected from source, pack, tool, or eval.
- Human reviewer cannot tell why the expert cited something.

## Eval Coverage

- Evidence pack includes Obsidian links.
- Human review checklist in extraction and knowledge pack runbooks.
