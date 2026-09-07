---
type: diagram-note
status: active
tags: [module-system, domain-knowledge, retrieval, pipeline]
reliability: medium
---

# Domain Knowledge Retrieval v1 Pipeline

## One-line Summary

This dataflow shows how books, web material, database exports, and notes become retrievable evidence packs for expert skills.

## Diagram Files

- HTML: [Domain Knowledge Retrieval v1 Pipeline.html](Domain%20Knowledge%20Retrieval%20v1%20Pipeline.html)
- Source JSON: [Domain Knowledge Retrieval v1 Pipeline.dataflow.json](Domain%20Knowledge%20Retrieval%20v1%20Pipeline.dataflow.json)

## Accepted Inputs

- Books: PDF, EPUB, text, Markdown.
- Web: articles, reports, transcripts, saved pages.
- Internal: database exports, docs, notes, conversations.
- Visual: images, screenshots, charts, diagrams, scanned pages, whiteboard photos.

## V1 Dataflow

1. Preserve the raw source identity.
2. Convert useful material into source notes.
3. Extract decision-relevant concepts, cases, claims, checklists, and failure modes.
4. Attach frontmatter metadata that both Obsidian and retrieval can use.
5. Bundle scoped material into a knowledge pack.
6. Retrieve from the pack or vault using keyword, metadata, and heading-level chunks.
7. Return an evidence pack with answerability, sources, excerpts, caveats, usage guidance, and Obsidian links.
8. Feed bad retrieval examples back into metadata, chunking, source extraction, or evals.

## Keep Criteria

Keep material that affects decisions, skill behavior, or eval criteria:

- Reusable concepts or frameworks.
- Cases with context, action, result, and lesson.
- Claims that affect professional advice.
- Warnings, failure modes, exceptions.
- Checklist items.
- Useful source references.

Drop or defer duplicates, vague claims, trivia, unsupported filler, and material that is interesting but does not change agent behavior.

## Evidence Pack Output

The retrieval module should return:

- Relevant note or chunk.
- Best matching heading.
- Source reference.
- Excerpt.
- Visual caption or OCR text when available.
- Tags and metadata.
- Reliability or confidence.
- How the consuming skill should use the result.
- Gaps when the corpus does not support an expert answer.
- Obsidian link for human review.

## Knowledge Pack Boundary

A domain expert should normally retrieve from a knowledge pack, not from the entire vault.

A knowledge pack defines:

- Domain and supported decisions.
- Included source, concept, case, claim, checklist, and failure-mode notes.
- Retrieval filters.
- Source reliability floor.
- Unsupported areas.
- Golden retrieval questions.
- Related tools and evals.

## Runtime Rule

The consuming expert should treat the evidence pack as input evidence, not as the final answer. It must compare evidence with the user's facts, label uncertainty, and avoid citing notes that do not directly support the answer.

## Source Quality

Use [[Source Trust and Certainty Standard]] to decide whether retrieval is `supported`, `partial`, `gap`, or `conflict`.

## Related

- [[../02_Domain-Knowledge/Packs/README|Knowledge Packs]]
- [[../04_Tool-Specs/Tool Spec - Vault Retrieval|Vault Retrieval]]
- [[../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]]
