---
type: internal-module
status: active
tags: [module-system, domain-retrieval, extraction-gate, knowledge-unit]
reliability: high
updated: 2026-09-07
---

# 03 - Knowledge Unit Extraction Gate

## One-line Summary

Decide which extracted material is useful enough to become expert knowledge.

## Purpose

Keep the corpus dense, decision-relevant, and retrievable by filtering out trivia, duplicates, motivational filler, unsupported claims, and vague summaries.

## Trigger

Use after media-specific extraction and before writing knowledge notes.

## Inputs

- Candidate extracted units from [[02 - Media Extraction Adapters]].
- Expert domain and supported decisions.
- Source reliability and caveats.
- Existing notes for duplicate detection.

## Outputs

- Kept knowledge units.
- Dropped or deferred units with reasons.
- Unit type: concept, case, claim, checklist, warning, failure mode, visual insight, or data definition.
- Suggested destination folder and knowledge pack.

## Dependencies

- [[../Domain Knowledge Retrieval Design Spec]]
- [[../Source Trust and Certainty Standard]]
- [[../../02_Domain-Knowledge/Packs/README|Knowledge Packs]]

## Runtime Instructions

Keep a unit when it helps the expert:

- Diagnose a situation.
- Choose between options.
- Ask a better question.
- Warn about a failure mode.
- Apply a framework or checklist.
- Compare cases.
- Cite a source-backed claim.
- State a caveat or limitation.
- Identify insufficient evidence.

Drop or defer a unit when it is duplicate, motivational, vague, unsupported, too broad, not decision-changing, or missing provenance.

## Failure Modes

- Keeping too much low-signal material.
- Dropping caveats and limitations.
- Keeping broad claims that cannot be retrieved precisely.
- Treating extracted text as expert knowledge without a use case.

## Eval Coverage

- Golden retrieval questions must find kept units.
- Bad retrieval examples should identify whether extraction gate was too loose or too strict.
