---
type: runbook
status: active
tags: [runbook, knowledge-pack, domain-knowledge, expert-agent]
reliability: medium
---

# Build Knowledge Pack For Expert

## One-line Summary

Use this runbook to turn source material into a scoped knowledge pack that an expert agent can retrieve from and a human can inspect in Obsidian.

## Inputs

- Expert domain.
- Target user and decisions.
- Source notes, books, articles, internal docs, cases, or diagrams.
- Tool requirements.
- Known risks and unsupported areas.

## Output

- One knowledge pack note in `02_Domain-Knowledge/Packs`.
- Linked source, concept, case, checklist, and failure-mode notes.
- Retrieval filters.
- Reliability floor.
- Golden retrieval questions.
- Related evals.

## Process

1. Define the expert's supported decisions.
2. Add or review source notes in `02_Domain-Knowledge/Sources`.
3. Extract reusable concepts into `02_Domain-Knowledge/Concepts`.
4. Extract concrete cases into `02_Domain-Knowledge/Cases`.
5. Drop trivia, duplicate claims, and material that does not change expert behavior.
6. Create a knowledge pack from [[../_templates/Knowledge Pack Template|Knowledge Pack Template]].
7. Add `domain`, `status`, `tags`, and `reliability` metadata.
8. Link included notes with Obsidian wiki links.
9. Add unsupported areas and caveats.
10. Add three to five golden retrieval questions.
11. Run retrieval smoke tests.
12. Attach [[../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]].

## Retrieval Smoke Test

```bash
python3 tools/agent_retrieve.py \
  "domain question here" \
  --domain your-domain \
  --reliability-floor medium \
  --json
```

Pass when:

- Expected notes appear in top results.
- `answerability` is correct.
- Results include Obsidian links.
- Weak or missing support appears as `partial` or `gap`.

## Related

- [[../02_Domain-Knowledge/Packs/README|Knowledge Packs]]
- [[../04_Tool-Specs/Tool Spec - Expert Vault Interface|Expert Vault Interface]]
- [[../04_Tool-Specs/Tool Spec - Vault Retrieval|Vault Retrieval]]
- [[../09_Module-System/Source Trust and Certainty Standard|Source Trust and Certainty Standard]]
