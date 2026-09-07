---
type: capability-module
status: active
tags: [capability, domain-knowledge, retrieval, rag]
reliability: medium
---

# Capability - Domain Knowledge Retrieval

## One-line Summary

This module turns books, web material, internal notes, images, diagrams, and database exports into retrievable evidence packs for expert skills.

## Purpose

Give a generated skill access to relevant domain knowledge without hardcoding all knowledge into `SKILL.md`.

## Trigger

Use when a skill or agent needs domain-specific expertise from a local corpus, source library, book notes, images, diagrams, cases, concepts, or internal business data.

## Inputs

- Business need or user question.
- Accepted source files or source notes, including visual assets.
- Domain scope.
- Metadata fields such as source type, domain, reliability, tags, date, author, and status.
- Retrieval settings such as top-k, filters, and preferred note types.

## Outputs

- Evidence pack.
- Ranked notes or chunks.
- Source references.
- Confidence and reliability labels.
- Usage guidance for the consuming skill.
- Gaps when retrieval cannot support an expert answer.
- Obsidian links for AI review traceability and human input/output/performance checkpoints.

## Dependencies

- [[../09_Module-System/Domain Knowledge Retrieval v1 Pipeline|Domain Knowledge Retrieval v1 Pipeline]]
- [[../09_Module-System/Source Trust and Certainty Standard|Source Trust and Certainty Standard]]
- [[../02_Domain-Knowledge/Packs/README|Knowledge Packs]]
- [[../02_Domain-Knowledge/Concepts/Concept - Evidence Hierarchy|Evidence Hierarchy]]
- [[../04_Tool-Specs/Tool Spec - Vault Retrieval|Vault Retrieval]]

## Runtime Instructions

- Accept common personal corpus types first: PDF, EPUB, text, Markdown, saved web pages, article notes, transcripts, database exports, internal docs, screenshots, diagrams, scanned pages, and whiteboard photos.
- Preserve raw source identity before extraction.
- Parse source material into source notes, concepts, cases, claims, examples, OCR text, and visual descriptions.
- If an image cannot be interpreted locally, create a `needs-vision` note instead of silently dropping it.
- Keep only material that can affect a decision, answer quality, skill behavior, or eval criteria.
- Drop duplicate, vague, unsupported, trivia-level, or non-actionable material.
- Index retained notes by frontmatter, headings, tags, source type, reliability, and chunk text.
- Prefer scoped knowledge packs over whole-vault retrieval when the expert domain is known.
- Retrieve with keyword and metadata matching first; add embeddings after failure cases show the limit.
- Return evidence with source, excerpt, confidence, and how the consuming skill should use it.
- Include Obsidian links in evidence output so AI can self-review citations and humans can checkpoint outputs when needed.
- Mark answerability as `supported`, `partial`, `gap`, or `conflict`.
- Ask humans only for input acceptance, output acceptance, or performance acceptance.

## Retention Criteria

Keep a knowledge unit when it has at least one of:

- A reusable concept or framework.
- A concrete case with context, action, result, and lesson.
- A claim that affects professional advice.
- A warning, failure mode, or exception.
- A checklist item that changes execution.
- A useful source reference for later verification.
- A visual explanation, diagram, chart, or screenshot that changes the skill's answer.

Drop or defer when:

- It is duplicated elsewhere.
- It is motivational filler.
- The claim has no source or useful context.
- It is interesting but does not affect the skill's decisions.
- It is too broad to retrieve precisely.

## Failure Modes

- Treating raw book text as directly usable expertise.
- Retrieving popular but irrelevant notes.
- Keeping too much low-signal content.
- Losing source provenance during extraction.
- Ignoring diagrams, charts, screenshots, or scanned pages because they are not plain text.
- Returning evidence without explaining how the skill should use it.
- Moving to embeddings before the metadata and note structure are clear.

## Eval Coverage

- Retrieval returns relevant notes for known domain questions.
- Retrieval exposes gaps when the corpus lacks support.
- Evidence packs include source, confidence, and usage guidance.
- AI self-review checks source alignment, caveats, and answerability before use.
- Bad retrieval results create feedback for metadata, chunking, or retention rules.
- [[../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]]

## Related

- [[../09_Module-System/Expert Skill Factory v1 Pipeline|Expert Skill Factory v1 Pipeline]]
- [[../09_Module-System/Module Contract|Module Contract]]
