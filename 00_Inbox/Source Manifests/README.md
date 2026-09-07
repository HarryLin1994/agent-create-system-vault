---
type: index
status: active
tags: [inbox, source-manifest, ingestion]
reliability: medium
updated: 2026-09-07
---

# Source Manifests

This folder stores one manifest note per raw source file.

## Purpose

The manifest is the bridge between raw files and retrievable Obsidian knowledge. It records file identity before extraction so later chunks and notes can cite a stable `source_id`.

## Generated Fields

- `source_id`
- `source_type`
- `raw_path`
- `sha256`
- `size_bytes`
- `modified_at`
- `extension`

## AI Review Fields

- `ai_reviewer`
- `ai_review_status`
- provenance check
- permission/sensitivity check
- extraction fit check
- citation/confidence check

## Human Checkpoint Fields

Humans only need to confirm:

- Input acceptance: source batch, domain, permission, sensitivity, and intended expert questions.
- Output acceptance: generated notes/evidence are understandable and useful.
- Performance acceptance: golden questions or real tasks behave acceptably.

## Next Step

After AI self-review passes the manifest, create or update a source note in `02_Domain-Knowledge/Sources`. Use human checkpoints only for input, output, and performance acceptance.
