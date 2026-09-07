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

## Human Fields

- `domain`
- `title`
- `author`
- `source_date`
- `version`
- `permission`
- `sensitivity`
- `reviewer`

## Next Step

After reviewing a manifest, create or update a source note in `02_Domain-Knowledge/Sources`.
