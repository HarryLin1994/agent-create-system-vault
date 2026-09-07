---
type: module-standard
status: active
tags: [module-system, ai-review, human-checkpoint, quality]
reliability: medium
updated: 2026-09-07
---

# AI Self-Review and Human Checkpoint Standard

## One-line Summary

Use AI self-review for source, extraction, citation, and confidence quality; use human checkpoints only for input acceptance, output acceptance, and observed performance.

## Purpose

Keep the knowledge pipeline moving without asking humans to manually inspect every source note, chunk, and citation. Human attention should be spent where it has the highest leverage: whether the right material entered the system, whether the produced artifact is useful, and whether the expert performs well on real tasks.

## Review Ownership

| Area | Owner | Required Output |
| --- | --- | --- |
| Source identity and provenance consistency | AI reviewer | Source title/path/hash/domain/permission/sensitivity check |
| Extraction accuracy and structure | AI reviewer | Kept/dropped units, caveats, and source references |
| Citation and evidence alignment | AI reviewer | Evidence supports the claim or answerability is downgraded |
| Confidence and certainty label | AI reviewer | `supported`, `partial`, `gap`, or `conflict` with reason |
| Input acceptance | Human checkpoint | The source batch and domain intent are correct enough to process |
| Output acceptance | Human checkpoint | The generated notes/evidence are understandable and useful |
| Performance acceptance | Human checkpoint | Golden questions and real usage produce acceptable behavior |

## AI Self-Review Checklist

- Provenance: source path, hash, URL, author, date, and version are recorded when available.
- Permission and sensitivity: source handling matches the declared permission and sensitivity.
- Extraction fit: kept material changes expert decisions, questions, frameworks, warnings, or eval behavior.
- Source alignment: every extracted claim can be traced to a source note or marked as an assumption.
- Caveat handling: weak, anecdotal, stale, or context-dependent evidence is not overstated.
- Citation precision: cited notes directly support the answer, not just nearby keywords.
- Confidence: answerability and reliability labels match the retrieved evidence.
- Gap reporting: missing evidence creates a concrete gap or next-action recommendation.

## Human Checkpoints

Humans only need to confirm:

- Input: this is the right source batch, domain, permission, sensitivity, and target expert scope.
- Output: the produced source notes, extracted notes, evidence packs, or prompts are readable and practically useful.
- Performance: golden questions, smoke tests, and real tasks show acceptable answer quality.

Humans do not need to manually inspect every extracted unit unless an output or performance checkpoint fails.

## Status Guidance

| Status | Meaning |
| --- | --- |
| `needs-ai-review` | AI must review extraction, citations, confidence, or metadata before the artifact is trusted. |
| `ai-reviewed` | AI self-review passed, but the artifact is not necessarily active yet. |
| `needs-human-checkpoint` | Human input/output/performance acceptance is needed. |
| `active` | The artifact can be used by the expert within its stated scope and reliability. |

## Runtime Rule

AI review can increase process confidence, not truth beyond the evidence. If evidence is incomplete, the output must stay `partial`, `gap`, or `conflict` even when the AI review passes.

## Related

- [[Source Trust and Certainty Standard]]
- [[Domain Knowledge Retrieval v1 Pipeline]]
- [[Domain Retrieval Modules/11 - Obsidian Human Review Interface|Obsidian Human Checkpoint Interface]]
- [[../07_Runbooks/Extract Expert Knowledge From Sources|Extract Expert Knowledge From Sources]]
