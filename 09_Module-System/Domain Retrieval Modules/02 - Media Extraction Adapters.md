---
type: internal-module
status: active
tags: [module-system, domain-retrieval, extraction, media]
reliability: high
updated: 2026-09-07
---

# 02 - Media Extraction Adapters

## One-line Summary

Choose the correct extraction path for each source type instead of treating every input as plain text.

## Purpose

Preserve expert-relevant structure from books, reports, tables, charts, screenshots, diagrams, scanned documents, transcripts, and database exports.

## Trigger

Use after source intake and before deciding which extracted material should become knowledge units.

## Inputs

- Source note from [[01 - Source Intake and Trust]].
- Raw source type.
- File path, URL, or source reference.
- Human notes about what matters.

## Outputs

- Candidate extracted units.
- OCR text or visual caption when relevant.
- Table, chart, schema, or layout summaries.
- Extraction caveats and `needs-human-review` flags.

## Dependencies

- [[../Domain Knowledge Retrieval Design Spec]]
- [[01 - Source Intake and Trust]]
- Trusted document extraction references in [[../../02_Domain-Knowledge/Sources/Source - Retrieval and Tooling Best Practices|Retrieval and Tooling Best Practices]]

## Runtime Instructions

- Book: extract thesis, chapter frameworks, definitions, examples, counterexamples, durable claims, and checklists.
- Report: extract findings, methodology, dates, limitations, tables, figures, and charts.
- Article: extract core claim, evidence, author, publication date, and caveats.
- Picture or screenshot: extract OCR text, visible entities, UI state, labels, and factual observations.
- Chart or diagram: extract entities, relationships, axes, values, process flow, and visual caveats.
- Transcript: extract decisions, context, speaker, outcome, quote snippets, and caveats.
- Database export: extract schema, field definitions, row-level examples, aggregate patterns, freshness, and privacy constraints.
- Mark uncertain OCR or visual interpretation as `needs-human-review`.

## Failure Modes

- Treating image/chart/table evidence as ordinary text.
- Losing page, slide, row, or figure provenance.
- Overinterpreting a visual without human verification.
- Extracting only summaries and losing methodology or limitations.

## Eval Coverage

- Media extraction checklist in [[../../07_Runbooks/Extract Expert Knowledge From Sources|Extract Expert Knowledge From Sources]]
- Retrieval relevance checks for expected extracted notes.
