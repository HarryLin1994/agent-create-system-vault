---
type: internal-module
status: active
tags: [module-system, domain-retrieval, source-intake, reliability]
reliability: high
updated: 2026-09-07
---

# 01 - Source Intake and Trust

## One-line Summary

Register source identity, permission, provenance, and reliability before extracting knowledge.

## Purpose

Prevent the retrieval system from producing expert claims from unknown, stale, weak, or unreviewed material.

## Trigger

Use when new raw material enters the vault: book, PDF, report, article, screenshot, diagram, transcript, database export, or internal document.

## Inputs

- Raw source path, URL, or reference.
- Source type.
- Author or owner.
- Publication or update date.
- File hash when the source is a local file.
- Access/permission status.
- Intended expert domain.
- AI reviewer and human checkpoint owner when available.

## Outputs

- Source note in `02_Domain-Knowledge/Sources`.
- Source manifest in `00_Inbox/Source Manifests` for local files.
- Reliability label: `draft`, `low`, `medium`, or `high`.
- Source trust tier.
- `needs-source`, `needs-ai-review`, `needs-human-checkpoint`, `ai-reviewed`, or `active` status.
- Obsidian links to downstream extracted notes.

## Dependencies

- [[../Source Trust and Certainty Standard]]
- [[../AI Self-Review and Human Checkpoint Standard]]
- [[../../_templates/Knowledge Source Template|Knowledge Source Template]]
- [[../../02_Domain-Knowledge/Sources/README|Sources]]

## Runtime Instructions

- Never extract expert knowledge before recording source identity.
- Prefer primary and official sources for factual or technical claims.
- Mark unclear source authority as `draft` or `low`.
- Record source date and freshness caveat when the domain changes over time.
- Record permission and privacy constraints for internal or database sources.
- Use `tools/ingest_sources.py scan` to assign stable `source_id` and `sha256` before extraction.
- Let AI review source identity, provenance, permission/sensitivity consistency, and reliability before extraction.
- Ask humans only for input acceptance when the source batch, domain, permission, sensitivity, or intended expert questions are unclear.

## Failure Modes

- Source note is created without provenance.
- Weak source is labeled as high reliability.
- Stale source is used for current claims.
- Internal or private data enters retrieval without permission notes.
- Humans are asked to do line-by-line content review instead of input/output/performance checkpoints.

## Eval Coverage

- [[../../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]]
- `tools/validate_vault.py` source metadata checks.
