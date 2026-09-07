---
type: internal-module
status: active
tags: [module-system, domain-retrieval, obsidian, human-checkpoint, ai-review]
reliability: high
updated: 2026-09-07
---

# 11 - Obsidian Human Checkpoint Interface

## One-line Summary

Make every important retrieval artifact understandable and checkpointable in Obsidian.

## Purpose

Let humans confirm inputs, outputs, and performance while AI reviews source, extraction, citation, and confidence quality.

## Trigger

Use whenever the pipeline creates source notes, extracted notes, knowledge packs, evidence packs, evals, or tool specs.

## Inputs

- Markdown notes.
- Obsidian wiki links.
- Evidence pack result paths.
- Source references.
- AI review flags and human checkpoint flags.

## Outputs

- Obsidian-readable indexes.
- Wiki links between source, extracted notes, packs, tools, and evals.
- `obsidian_uri` links in evidence packs.
- Review statuses such as `draft`, `needs-source`, `needs-vision`, `needs-ai-review`, `ai-reviewed`, `needs-human-checkpoint`, and `active`.
- Human checkpoint fields for input, output, and performance acceptance.

## Dependencies

- Obsidian Properties and Internal Links docs captured in [[../../02_Domain-Knowledge/Sources/Source - Retrieval and Tooling Best Practices|Retrieval and Tooling Best Practices]]
- [[../AI Self-Review and Human Checkpoint Standard]]
- [[04 - Knowledge Note Writer]]
- [[09 - Evidence Pack Builder]]

## Runtime Instructions

- Keep Obsidian as the canonical human-readable vault.
- Use flat YAML frontmatter for metadata.
- Use wiki links for all system relationships.
- Every retrieved result should include an Obsidian URI.
- Index pages should show what exists and where to start.
- AI review flags should be visible in note metadata and body text.
- Human checkpoint fields should be limited to input acceptance, output acceptance, and performance acceptance.

## Failure Modes

- Machine artifacts are not readable by humans.
- JSON results do not link back to notes.
- Notes exist but are disconnected from source, pack, tool, or eval.
- Human checkpoint owner cannot tell what input, output, or performance effect needs acceptance.
- AI reviewer does not record confidence, citation, or extraction checks.

## Eval Coverage

- Evidence pack includes Obsidian links.
- Human checkpoint and AI self-review checklist in extraction and knowledge pack runbooks.
