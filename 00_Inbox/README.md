---
type: index
tags: [inbox, workflow]
---

# Inbox

Use this folder for raw material before it is converted into the agent creation system.

## Intake Steps

1. Add raw agent ideas, user requirements, prompt fragments, eval failures, or tool ideas here.
2. Put original source files in [[Raw Sources/README|Raw Sources]].
3. Describe the batch in [[Source Intake Queue]].
4. Run `python3 tools/ingest_sources.py scan` to create source manifests.
5. Review generated manifests in [[Source Manifests/README|Source Manifests]].
6. Create a structured note from one of the templates in `_templates`.
7. Extract reusable material into blueprints, modules, knowledge, tool specs, prompts, or evals.
8. Link the processed note back to its source.
9. Move stale or duplicate raw notes to `90_Archive` when an archive folder is added.

## Definition of Done

A processed item has:

- A `type` in frontmatter.
- A one-line summary.
- Clear owner: blueprint, capability, knowledge, tool, prompt, eval, or runbook.
- Applicability and limits.
- Related links to at least one other system component.

## Raw Source Folder

Use `00_Inbox/Raw Sources/` for PDFs, Word files, images, scans, text files, and data exports. Raw files are ignored by git; manifests and extracted notes are tracked.
