---
type: eval
status: active
tags: [eval, retrieval, domain-knowledge, evidence-pack]
reliability: medium
---

# Eval - Domain Retrieval Relevance

## One-line Summary

This eval checks whether retrieval returns relevant, source-backed notes and exposes gaps instead of giving unsupported certainty.

## Purpose

Protect the domain knowledge retrieval module from returning popular but irrelevant notes, weak sources, or evidence packs that cannot support the expert's answer.

## Test Inputs

Use golden retrieval questions from a knowledge pack.

Each test case should include:

- User question or expert task.
- Knowledge pack name or retrieval filters.
- Expected note paths.
- Notes that should not be cited.
- Minimum reliability level.
- Expected answerability: supported, partial, or gap.

Run all available pack cases:

```bash
python3 tools/eval_retrieval.py --all
```

By default, the runner evaluates only knowledge packs with `status: active`.
Draft or `needs-source` packs can keep golden questions during intake without
failing the active retrieval suite. To intentionally test non-active packs:

```bash
python3 tools/eval_retrieval.py --all --include-draft
```

## Passing Behavior

- Top results include the expected notes for supported questions.
- Evidence pack includes note path, title, type, reliability, excerpt, and source reference when available.
- The expert uses evidence only when it is relevant to the question.
- Partial support is labeled as partial.
- Missing support is labeled as a gap.
- Human-readable output includes Obsidian links so AI can self-review citations and humans can checkpoint outputs.

## Failing Behavior

- Cites a note that is only keyword-related but not decision-relevant.
- Treats a low-reliability or stale source as decisive.
- Hides gaps by giving generic advice.
- Returns raw source dumps instead of concise evidence.
- Omits note paths or Obsidian links.

## Example Case

```yaml
question: "What should this domain expert answer when evidence is incomplete?"
filters:
  type: ["capability-module", "concept", "case"]
  tag: ["evidence", "retrieval"]
expected_notes:
  - 03_Capability-Modules/Capability - Evidence Grounding.md
  - 02_Domain-Knowledge/Concepts/Concept - Evidence Hierarchy.md
answerability: partial
must_not:
  - claim certainty without retrieved support
```

## Related

- [[../03_Capability-Modules/Capability - Domain Knowledge Retrieval|Domain Knowledge Retrieval]]
- [[../03_Capability-Modules/Capability - Evidence Grounding|Evidence Grounding]]
- [[../02_Domain-Knowledge/Packs/Pack - Agent Create System Retrieval|Pack - Agent Create System Retrieval]]
- [[../04_Tool-Specs/Tool Spec - Vault Retrieval|Vault Retrieval]]
- [[Eval - Refuse Unsupported Certainty]]
