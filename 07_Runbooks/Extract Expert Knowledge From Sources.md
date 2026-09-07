---
type: runbook
status: active
tags: [runbook, extraction, domain-knowledge, books, reports, images]
reliability: medium
---

# Extract Expert Knowledge From Sources

## One-line Summary

Use this runbook to turn books, pictures, reports, transcripts, and internal data into expert-usable Obsidian notes.

## When To Use

Use this whenever raw material needs to become retrievable knowledge for an expert agent.

Do not skip this for long PDFs, books, images, diagrams, charts, screenshots, scanned pages, internal reports, database exports, or any material that a human must audit later.

## Output

- Source note with provenance.
- Extracted concept, case, claim, checklist, or failure-mode notes.
- Links back to original source note.
- Knowledge pack inclusion decision.
- Golden retrieval questions.

## Extraction Gate

Keep a unit only when it helps the expert:

- Make a better decision.
- Diagnose a situation.
- Ask a high-impact question.
- Apply a framework.
- Avoid a failure mode.
- Cite a source-backed claim.
- State a caveat.
- Detect an evidence gap.

Drop or defer anything that is duplicate, motivational, vague, unsupported, too broad, or not decision-changing.

## Source Type Checklist

| Source Type | Must Extract | Must Verify |
| --- | --- | --- |
| Book | frameworks, definitions, examples, counterexamples, durable claims | chapter/page reference, copyright-safe summary |
| Report | findings, methodology, dates, tables, charts, limitations | source authority, date, method, sample |
| Article | core claim, evidence, author, date, caveat | original source when possible |
| Picture or screenshot | OCR text, visible facts, UI state, labels | OCR/caption accuracy |
| Diagram or chart | entities, relationships, axes, quantitative takeaways | whether the visual supports the conclusion |
| Transcript | firsthand observation, decision, result, caveat | anecdotal scope and speaker identity |
| Database export | schema, field meaning, aggregate pattern, freshness | permission, privacy, sample bias |
| Internal doc | owner, version, workflow, policy, exception | authority and active status |

## Process

1. Put rough material in `00_Inbox`.
2. Create a source note in `02_Domain-Knowledge/Sources`.
3. Fill metadata: `type`, `source_type`, `domain`, `status`, `reliability`, `updated`, source title, author, URL/path, and source date.
4. Summarize the source in one line.
5. Extract candidate units.
6. Apply the extraction gate.
7. Create extracted notes in the correct folder.
8. Link every extracted note to the source note.
9. Add useful notes to a knowledge pack.
10. Add golden retrieval questions.
11. Run retrieval smoke tests.
12. Mark unresolved issues as `needs-source`, `needs-human-review`, or `needs-vision`.

## Retrieval Smoke Test

```bash
python3 tools/agent_retrieve.py \
  "question this expert should answer" \
  --domain your-domain \
  --reliability-floor medium \
  --json
```

Pass when the expected extracted notes appear, the evidence pack includes Obsidian links, and unsupported questions return `partial` or `gap`.

## Related

- [[../09_Module-System/Domain Knowledge Retrieval Design Spec|Domain Knowledge Retrieval Design Spec]]
- [[../09_Module-System/Domain Knowledge Retrieval v1 Pipeline|Domain Knowledge Retrieval v1 Pipeline]]
- [[../09_Module-System/Source Trust and Certainty Standard|Source Trust and Certainty Standard]]
- [[Build Knowledge Pack For Expert]]
