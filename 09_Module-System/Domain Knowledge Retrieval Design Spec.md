---
type: module-design-spec
status: active
tags: [module-system, domain-knowledge, retrieval, rag, design-spec]
reliability: high
updated: 2026-09-07
---

# Domain Knowledge Retrieval Design Spec

## One-line Summary

Design domain knowledge retrieval as a source-backed evidence system: trusted material is transformed into Obsidian-readable knowledge packs, retrieved through scoped tools, and returned to expert agents as evidence packs with answerability, reliability, caveats, and human-review links.

## Goal

Give each expert agent the domain knowledge, tools, and review surface it needs to answer like a specialist without hardcoding books, notes, or raw source dumps into a giant prompt.

The system must serve two users at the same time:

- Expert agent: needs precise, structured, scoped evidence.
- Human maintainer: needs Obsidian notes, links, source provenance, and review paths that are easy to understand.

## Does This Need A Pipeline?

Yes, if any of these are true:

- The source is larger than one short note.
- The source has structure that matters: chapters, sections, figures, tables, appendices, forms, or slide pages.
- The source is visual or scanned: screenshots, pictures, diagrams, charts, whiteboards, or scanned PDFs.
- More than one expert agent will reuse the knowledge.
- A human needs to audit why the expert made a claim.
- The answer has material risk if retrieval cites weak, stale, or irrelevant evidence.
- The corpus will grow and bad retrieval needs to be debugged.

No, or not yet, if the expert has only a tiny handwritten note set, low-risk output, and no need for repeatable evaluation. Even then, the notes should still use source metadata and Obsidian links so they can enter the pipeline later.

## Pipeline Requirement Decision

| Corpus Type | Pipeline Required | Reason |
| --- | --- | --- |
| One small handwritten note | Optional | Manual retrieval can be enough if risk is low. |
| Book or long PDF | Required | Needs source registration, chapter/section extraction, chunking, and provenance. |
| Report with charts and tables | Required | Needs table/figure extraction plus text summary. |
| Screenshots, diagrams, scanned pages, photos | Required | Needs OCR/vision captioning and human verification. |
| Internal docs or database exports | Required | Needs permission, schema, freshness, and row/field provenance. |
| Multi-agent reusable domain corpus | Required | Needs knowledge packs, filters, evals, and versioning. |

## Non-goals

- Do not let every expert search the whole vault by default.
- Do not treat embeddings as a substitute for source quality, metadata, or evals.
- Do not paste full books, articles, or documents into prompts.
- Do not cite retrieval results that are only keyword-related.
- Do not make machine-only JSON that humans cannot inspect in Obsidian.

## Definitions

| Term | Meaning |
| --- | --- |
| Raw source | Original book, PDF, article, transcript, database export, screenshot, diagram, or internal note. |
| Source note | Obsidian note that records provenance, summary, useful claims, caveats, and references. |
| Knowledge unit | A concept, case, claim, checklist, warning, failure mode, or visual insight extracted from a source. |
| Knowledge pack | Scoped bundle of source notes and extracted knowledge for one expert domain or decision area. |
| Retrieval index | Machine-readable searchable view of notes, headings, metadata, and chunks. |
| Evidence pack | Structured retrieval output consumed by the expert agent and reviewable by humans. |
| Answerability | Whether retrieved evidence supports an answer: `supported`, `partial`, `gap`, or `conflict`. |

## Trusted And Known Standard

Use [[Source Trust and Certainty Standard]].

For this system:

- `known`: directly observed in this vault, source code, or a trusted source.
- `trusted`: primary or official source when available, such as official API docs, protocol specs, source code, original reports, legal text, or reviewed academic/institutional material.
- `uncertain`: not directly observed, rapidly changing, weakly sourced, stale, or outside the current corpus.

When the builder or expert does not know whether a claim is current or trustworthy, it must retrieve from the vault first and use web search only against trusted sources for external verification. Search findings should become source notes if they affect future expert behavior.

## System Shape

```text
Raw Sources
  -> Source Notes
  -> Extracted Knowledge Units
  -> Knowledge Packs
  -> Retrieval Index
  -> Evidence Pack
  -> Expert Answer
  -> Retrieval Feedback / Evals
```

This follows the common RAG data-pipeline shape from trusted guidance: ingest documents or media, chunk into semantically meaningful parts, enrich chunks with metadata, index them, retrieve at runtime, and evaluate retrieval quality.

## Required Note Metadata

All notes that should participate in retrieval need simple frontmatter that Obsidian and scripts can both read.

```yaml
type: source | concept | case | claim | checklist | failure-mode | knowledge-pack | capability-module | tool-spec | eval
status: draft | active | deprecated
domain: startup | agent-create-system | other-domain
tags: [domain-knowledge, retrieval]
reliability: draft | low | medium | high
updated: YYYY-MM-DD
```

Recommended metadata for source-backed notes:

```yaml
source_type: book | article | official-docs | spec | paper | internal-doc | interview | visual
title: ""
author: ""
source_url: ""
source_date: YYYY-MM-DD
packs: []
applies_to: []
limitations: ""
```

Keep metadata flat. Nested frontmatter makes Obsidian and simple scripts harder to maintain.

## Knowledge Pack Contract

A knowledge pack is the normal boundary for expert retrieval.

Required sections:

- Scope: domain, target user, supported decisions, out-of-scope decisions.
- Retrieval filters: domain, tags, note types, reliability floor, freshness rule.
- Included sources: table with reliability, use, caveat.
- Included concepts and cases: links to Obsidian notes.
- Included tools: retrieval, calculators, APIs, file readers, or other allowed tools.
- Agent usage: how the expert should use this pack.
- Unsupported areas: gaps the expert must not pretend to know.
- Golden retrieval questions: expected notes and acceptance rules.
- Related evals.

## Ingestion Pipeline

1. Register raw source identity before extraction.
2. Create or update a source note from [[../_templates/Knowledge Source Template|Knowledge Source Template]].
3. Extract only material that can change expert behavior:
   - reusable concepts
   - concrete cases
   - decision-relevant claims
   - checklists
   - warnings and exceptions
   - failure modes
   - visual explanations, OCR, or captions
4. Apply keep/drop criteria from [[Domain Knowledge Retrieval v1 Pipeline]].
5. Assign reliability using [[Source Trust and Certainty Standard]].
6. Link extracted units back to source notes.
7. Attach relevant units to a knowledge pack.
8. Add or update golden retrieval questions.

## How To Find Expert-Usable Knowledge

Raw material becomes expert-usable only if it passes the extraction gate.

Keep a unit when it can help the expert:

- Diagnose a user's situation.
- Choose between options.
- Ask a better question.
- Warn about a failure mode.
- Apply a framework or checklist.
- Compare cases.
- Cite a source-backed claim.
- State a caveat or limitation.
- Decide that evidence is insufficient.

Drop or defer a unit when it is:

- Motivational filler.
- Duplicate.
- Too broad to retrieve precisely.
- Interesting but not decision-changing.
- Missing provenance.
- Not understandable without more context.
- A long raw excerpt that should remain in the source, not the expert prompt.

## Media-Specific Extraction Matrix

| Source Type | Extract | Output Notes | Required Human Check |
| --- | --- | --- | --- |
| Book | thesis, chapter-level frameworks, definitions, durable claims, examples, counterexamples, checklists | source note, concept notes, case notes, claim notes | Confirm page/chapter reference and avoid copying long text. |
| PDF report | executive findings, methodology, data definitions, tables, charts, limitations, dates | source note, claim notes, table/figure notes, concept notes | Check report date, methodology, sample, and whether claims are current. |
| Article or web page | core argument, evidence, author/source, publication date, caveats | source note, claim notes, failure-mode notes | Prefer original/official source over commentary when factual accuracy matters. |
| Transcript or interview | firsthand observations, decisions, constraints, outcomes, quotes, caveats | source note, case notes, claim notes | Mark anecdotal evidence and avoid overgeneralizing. |
| Screenshot or picture | OCR text, visible facts, UI state, diagram labels, factual observations | visual source note, claim notes, case notes | Human verifies OCR/caption accuracy. |
| Chart or diagram | axes, labels, relationships, process flow, quantitative takeaways, visual caveats | visual source note, concept notes, claim notes | Check whether the visual supports the claimed conclusion. |
| Scanned document | OCR text, page identity, signatures/stamps if relevant, tables/forms | source note, claim notes, form/table notes | Human verifies OCR errors and page provenance. |
| Database export | schema, field definitions, row-level examples, aggregate patterns, data freshness | source note, data dictionary note, claim notes | Check permission, privacy, sample bias, and freshness. |
| Internal docs | policies, workflows, owners, exceptions, decision rules | source note, checklist notes, failure-mode notes | Check authority, version, and whether the policy is active. |

## Extraction Workflow For Humans

1. Put raw source or rough notes in `00_Inbox`.
2. Create a source note in `02_Domain-Knowledge/Sources`.
3. Fill provenance: title, author, URL/path, date, source type, reliability.
4. Extract candidate knowledge units.
5. Apply the extraction gate.
6. Create or update concept, case, claim, checklist, or failure-mode notes.
7. Link each extracted note back to the source note.
8. Add extracted notes to a knowledge pack.
9. Write golden retrieval questions that should find those notes.
10. Run retrieval and inspect Obsidian links.

## Extraction Workflow For Agents

1. Read the target expert blueprint or domain request.
2. Retrieve existing module-system and source-trust rules.
3. Identify source type and extraction path.
4. Propose candidate source metadata.
5. Extract candidate units with provenance.
6. Classify each unit as concept, case, claim, checklist, warning, or failure mode.
7. Apply keep/drop criteria.
8. Produce Obsidian-ready Markdown notes.
9. Add retrieval filters and golden questions to the knowledge pack.
10. Run `vault_retrieve` smoke tests.

The agent should not silently convert raw media into expert knowledge when OCR, visual interpretation, provenance, or source authority is uncertain. It should mark the note as `draft`, `needs-vision`, `needs-source`, or `needs-human-review`.

## Chunking Rules

V1 chunks by note and Markdown heading.

Chunk text should keep enough context to be useful:

- note title
- note type
- tags
- domain
- reliability
- heading
- local section text
- source reference when available

If a section is too broad, split the note. If the same note matches too often, improve headings, tags, or pack filters before moving to embeddings.

Best-practice implication:

- Chunking is not just for token limits. It also prevents irrelevant material from entering the expert answer.
- Chunks that are too small lose context.
- Chunks that are too large create false positives and confuse answer generation.
- Structured sources should preserve their natural boundaries: chapter, section, heading, table, figure, transcript segment, or record group.

## Retrieval Pipeline

1. Understand the user question or expert task.
2. Select a knowledge pack when a domain is known.
3. Convert the pack into filters: `domain`, `type`, `tag`, `status`, `reliability_floor`.
4. Search heading-level chunks with keyword, alias, title, tag, type, and metadata boosts.
5. Return only the best chunk per note by default.
6. Rank results by relevance, source reliability, and scope match.
7. Label answerability:
   - `supported`: directly supported by medium-or-better evidence.
   - `partial`: related evidence exists but is incomplete, stale, indirect, or weak.
   - `gap`: no adequate support.
   - `conflict`: credible sources disagree.
8. Return an evidence pack.
9. If results are bad, feed the failure into metadata fixes, chunking fixes, source extraction, or evals.

## Evidence Pack Schema

```json
{
  "query": "string",
  "vault": "string",
  "filters": {
    "type": [],
    "tag": [],
    "domain": [],
    "status": [],
    "reliability_floor": "medium"
  },
  "answerability": "supported | partial | gap | conflict",
  "results": [
    {
      "path": "string",
      "obsidian_uri": "string",
      "title": "string",
      "type": "string",
      "heading": "string",
      "tags": [],
      "domain": "string",
      "status": "string",
      "reliability": "draft | low | medium | high",
      "summary": "string",
      "excerpt": "string",
      "source_reference": "string",
      "how_to_use": "string",
      "caveat": "string",
      "score": 0
    }
  ],
  "gaps": []
}
```

## Expert Tool Surface

Minimum V1 expert tools:

| Tool | Purpose | Current Implementation |
| --- | --- | --- |
| `vault_retrieve` | Retrieve scoped evidence from the vault. | `python3 tools/agent_retrieve.py "query" --json` |
| `knowledge_pack_inspect` | Inspect available knowledge for the expert's domain. | `--type knowledge-pack --domain <domain> --json` |
| `vault_open_note` | Give humans a review link for evidence. | `obsidian_uri` in evidence pack results |
| `retrieval_gap_report` | Explain what the corpus cannot support. | `answerability` and `gaps` fields |
| `eval_retrieval` | Test golden questions. | [[../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]] |

Approval gates are auto-approved for this project version. That is a product workflow decision, not a reason to skip tool specs, boundaries, or auditability.

## MCP Direction

V1 is local CLI plus Obsidian. Future MCP integration should map the vault this way:

| MCP Surface | Vault Mapping |
| --- | --- |
| Tools | `vault_retrieve`, `knowledge_pack_inspect`, `eval_retrieval`, source ingestion tools |
| Resources | Markdown notes, knowledge packs, diagrams, source references |
| Prompts | Runbooks, prompt templates, agent assembly templates |

The expert should not receive every resource automatically. The client or retrieval layer should provide selected resources based on pack scope and query.

## Obsidian Human Loop

Every important machine output must point back to human-readable notes.

Required Obsidian behavior:

- Use wiki links between blueprints, modules, packs, tools, and evals.
- Return `obsidian_uri` for every evidence result.
- Keep source notes readable without running code.
- Put reusable design rules in `09_Module-System`.
- Put runtime behavior in `03_Capability-Modules`.
- Put actual domain material in `02_Domain-Knowledge`.
- Put tool boundaries in `04_Tool-Specs`.
- Put regression checks in `06_Evals`.

## Eval Plan

Retrieval must be tested before an expert is trusted.

Required eval types:

- Relevance: expected notes appear in top results.
- Citation precision: the expert cites only notes that support the answer.
- Gap detection: unsupported questions produce `gap` or `partial`.
- Conflict handling: conflicting credible sources produce `conflict`.
- Metadata health: active packs have domain, reliability floor, sources, and golden questions.

Minimum acceptance for a knowledge pack:

- Three to five golden retrieval questions.
- Expected note appears in top 3 for supported questions.
- Unsupported question produces `gap` or `partial`.
- Evidence pack includes Obsidian links.
- Human reviewer can inspect cited notes without reading JSON only.

## Version Roadmap

### V1 - Current Local Design

- Obsidian vault is canonical.
- Markdown frontmatter is metadata.
- Knowledge packs define retrieval scope.
- Local script returns evidence packs.
- Retrieval is lexical plus metadata and heading chunks.
- Approval gates are auto-approved.

### V1.1 - Quality Tools

- Add metadata validator.
- Add automated golden retrieval eval runner.
- Add source note ingestion checklist.
- Add conflict detection using reliability and source date.
- Add pack health report.
- Add media-specific extraction templates for book, report, image, chart, transcript, and database export.

### V2 - Hybrid Retrieval

- Add local BM25 or equivalent lexical index.
- Add embeddings for semantic recall.
- Combine lexical and semantic ranking.
- Add reranking for final top-k.
- Add OCR/vision ingestion for screenshots, diagrams, charts, and scanned pages.

### V3 - MCP Server

- Expose vault retrieval as MCP tools.
- Expose notes and packs as MCP resources.
- Expose runbooks and prompt templates as MCP prompts.
- Add structured output schemas and audit logs.

## Design Decisions

| Decision | Rationale |
| --- | --- |
| Start with metadata and lexical retrieval | The corpus is still small and human-maintained; metadata quality must exist before embeddings help. |
| Make knowledge packs first-class | Experts need scoped memory, not whole-vault search. |
| Return evidence packs | Agents need reliability, usage guidance, caveats, and gaps, not just snippets. |
| Keep Obsidian canonical | Humans must be able to read, maintain, and trust the system. |
| Use trusted-source standard | Expert confidence must be tied to provenance and source quality. |
| Defer MCP until interface stabilizes | CLI and Markdown are enough to validate the contract before adding server complexity. |

## Trusted Sources Used

- [[../02_Domain-Knowledge/Sources/Source - Retrieval and Tooling Best Practices|Retrieval and Tooling Best Practices]]
- OpenAI File Search docs: https://developers.openai.com/api/docs/guides/tools-file-search
- OpenAI Vector Store Search API: https://developers.openai.com/api/reference/python/resources/vector_stores/methods/search
- Anthropic Contextual Retrieval: https://www.anthropic.com/engineering/contextual-retrieval
- Microsoft Azure RAG design guide: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-solution-design-and-evaluation-guide
- Microsoft Azure chunking guide: https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents
- Google Cloud Document AI extraction overview: https://docs.cloud.google.com/document-ai/docs/extracting-overview
- MCP Tools spec: https://modelcontextprotocol.io/specification/2025-06-18/server/tools
- MCP Resources spec: https://modelcontextprotocol.io/specification/2025-06-18/server/resources
- MCP Prompts spec: https://modelcontextprotocol.io/specification/2025-06-18/server/prompts
- Obsidian Properties docs: https://help.obsidian.md/Properties
- Obsidian Internal Links docs: https://help.obsidian.md/Linking+notes+and+files/Internal+links

## Related

- [[Domain Knowledge Retrieval v1 Pipeline]]
- [[Source Trust and Certainty Standard]]
- [[../03_Capability-Modules/Capability - Domain Knowledge Retrieval|Domain Knowledge Retrieval]]
- [[../04_Tool-Specs/Tool Spec - Vault Retrieval|Vault Retrieval]]
- [[../04_Tool-Specs/Tool Spec - Expert Vault Interface|Expert Vault Interface]]
- [[../02_Domain-Knowledge/Packs/README|Knowledge Packs]]
- [[../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]]
- [[../07_Runbooks/Extract Expert Knowledge From Sources|Extract Expert Knowledge From Sources]]
