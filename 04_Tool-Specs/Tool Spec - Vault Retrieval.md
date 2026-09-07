---
type: tool-spec
tool_name: vault_retrieval
status: active
tags: [tool, retrieval, rag, markdown]
reliability: medium
---

# Tool Spec - Vault Retrieval

## One-line Summary

Use local Markdown retrieval to find relevant vault notes before creating, revising, or running an agent.

## Command

```bash
python3 agent-create-system-vault/tools/agent_retrieve.py "your query"
```

Common filtered examples:

```bash
python3 agent-create-system-vault/tools/agent_retrieve.py \
  "evidence grounding unsupported certainty" \
  --type capability-module \
  --reliability-floor medium

python3 agent-create-system-vault/tools/agent_retrieve.py \
  "startup pricing retention expansion" \
  --domain startup \
  --tag pricing \
  --json
```

## Inputs

- Query: user request, agent requirement, failure mode, domain question, or eval target.
- Optional `--top-k`: number of matching notes.
- Optional `--type`: filter by note type.
- Optional `--tag`: require matching tags.
- Optional `--domain`: filter by domain.
- Optional `--status`: filter by status.
- Optional `--reliability-floor`: minimum reliability label: `draft`, `low`, `medium`, or `high`.
- Optional `--json`: emit machine-readable output.

## Outputs

The tool returns an evidence pack, not just a search result list.

Human-readable output includes:

- Answerability: `supported`, `partial`, or `gap`.
- Matching note title and best matching heading.
- Note type, reliability, score, tags, and relative path.
- Obsidian URI for human review.
- Summary, source reference, usage guidance, caveat, and excerpt when available.
- Gap messages when retrieval cannot support the answer.

JSON output uses this stable shape:

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
  "answerability": "supported | partial | gap",
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

## Use When

- Building a new agent blueprint.
- Selecting capability modules.
- Finding domain knowledge.
- Writing or refining prompts.
- Creating eval cases.
- Inspecting whether a knowledge pack supports an expert answer.
- Producing links a human can inspect in Obsidian.

## Expert Tool Policy

For this project version, approval gates are auto-approved at the product workflow level. The expert may run this read-only retrieval tool without asking the user each time.

The expert must still:

- Use filters when a knowledge pack or domain is known.
- Prefer `medium` or `high` reliability for decisive answers.
- Return `partial` or `gap` instead of pretending weak retrieval is enough.
- Show Obsidian links for notes it relies on.
- Avoid citing retrieved notes that are keyword-related but not decision-relevant.

## Failure Handling

- If no notes are found, search broader terms.
- If the top note is irrelevant, add better tags or improve the note summary.
- If too many duplicate concepts appear, create or refine a knowledge pack.
- If a source lacks provenance, mark the result as partial or gap.
- If retrieval is too shallow, move to embeddings later.

## Related

- [[../09_Module-System/Domain Knowledge Retrieval v1 Pipeline|Domain Knowledge Retrieval v1 Pipeline]]
- [[../09_Module-System/Source Trust and Certainty Standard|Source Trust and Certainty Standard]]
- [[../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]]
