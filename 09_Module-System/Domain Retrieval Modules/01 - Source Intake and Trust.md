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
- Access/permission status.
- Intended expert domain.
- Human reviewer when available.

## Outputs

- Source note in `02_Domain-Knowledge/Sources`.
- Reliability label: `draft`, `low`, `medium`, or `high`.
- Source trust tier.
- `needs-source`, `needs-human-review`, or `active` status.
- Obsidian links to downstream extracted notes.

## Dependencies

- [[../Source Trust and Certainty Standard]]
- [[../../_templates/Knowledge Source Template|Knowledge Source Template]]
- [[../../02_Domain-Knowledge/Sources/README|Sources]]

## Runtime Instructions

- Never extract expert knowledge before recording source identity.
- Prefer primary and official sources for factual or technical claims.
- Mark unclear source authority as `draft` or `low`.
- Record source date and freshness caveat when the domain changes over time.
- Record permission and privacy constraints for internal or database sources.

## Failure Modes

- Source note is created without provenance.
- Weak source is labeled as high reliability.
- Stale source is used for current claims.
- Internal or private data enters retrieval without permission notes.

## Eval Coverage

- [[../../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]]
- `tools/validate_vault.py` source metadata checks.
