---
type: tool-spec
tool_name: expert_vault_interface
status: active
tags: [tool, vault, obsidian, retrieval, mcp, expert-agent]
reliability: medium
---

# Tool Spec - Expert Vault Interface

## One-line Summary

Expose the Obsidian vault to expert agents as scoped retrieval tools, readable resources, and reusable prompts without making the agent search raw files blindly.

## Purpose

Give each expert the minimum tool and knowledge surface it needs:

- Search the right knowledge pack.
- Inspect source-backed evidence.
- Open Obsidian notes for human review.
- Report gaps when evidence is missing.
- Reuse runbooks and templates as prompts.

## Interface Model

| Surface | Owner | Examples | Agent Control |
| --- | --- | --- | --- |
| Tools | `04_Tool-Specs` and `tools/` | `vault_retrieve`, `retrieval_gap_report`, `eval_retrieval` | Model-invoked |
| Resources | Obsidian Markdown notes | sources, concepts, cases, knowledge packs, diagrams | Application-provided |
| Prompts | `05_Prompts`, `07_Runbooks`, `_templates` | system prompt templates, build runbooks | User-selected or builder-selected |

This mirrors the MCP split between tools, resources, and prompts while keeping V1 local and dependency-free.

## V1 Tools

### `vault_retrieve`

Implemented by:

```bash
python3 tools/agent_retrieve.py "query" --json
```

Use for scoped search across Markdown notes.

### `vault_open_note`

Implemented by evidence pack `obsidian_uri` fields.

Use when the expert cites or relies on a note and the human needs to inspect it in Obsidian.

### `knowledge_pack_inspect`

V1 implementation:

```bash
python3 tools/agent_retrieve.py "pack name or domain" --type knowledge-pack --json
```

Use before answering when the expert has a known domain or pack.

### `retrieval_gap_report`

V1 implementation: read the `answerability` and `gaps` fields returned by `vault_retrieve`.

Use when retrieved evidence is partial or missing.

### `eval_retrieval`

V1 implementation: manual eval using [[../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]] and the pack's golden retrieval questions.

Future implementation can automate golden question checks.

## Approval Policy

For this project version, approval gates are auto-approved.

The expert may call read-only vault tools without interrupting the user. Write tools, source ingestion, web fetching, or destructive actions still need a documented tool spec and audit trail before being trusted in production.

## Runtime Rules

- Retrieve from a knowledge pack when one is available.
- Use `--domain`, `--type`, `--tag`, and `--reliability-floor` filters when the scope is known.
- Treat notes as evidence, not as final answers.
- Include Obsidian links for cited evidence.
- Do not cite notes that are not directly relevant.
- If `answerability` is `partial` or `gap`, say what is missing.
- Prefer official, primary, or high-reliability sources for claims that can change user decisions.

## Failure Modes

- Giving the expert whole-vault access without pack boundaries.
- Returning raw Markdown without answerability, reliability, or source fields.
- Treating Obsidian links as proof instead of review paths.
- Auto-approving write tools without logging or eval coverage.
- Mixing reusable prompts with retrieved evidence.

## Eval Coverage

- [[../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]]
- [[../06_Evals/Eval - Refuse Unsupported Certainty|Refuse Unsupported Certainty]]

## Related

- [[Tool Spec - Vault Retrieval]]
- [[../09_Module-System/Domain Knowledge Retrieval v1 Pipeline|Domain Knowledge Retrieval v1 Pipeline]]
- [[../09_Module-System/Source Trust and Certainty Standard|Source Trust and Certainty Standard]]
- [[../02_Domain-Knowledge/Packs/README|Knowledge Packs]]
