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

## Inputs

- Expert or user question.
- Agent blueprint and known domain.
- Optional knowledge pack name.
- Required reliability level or freshness constraint.
- Human review need when the answer cites vault evidence.

## Outputs

- Scoped retrieval query and filters.
- Evidence pack with answerability, source references, caveats, and Obsidian links.
- Vault validation report when module or pack structure changed.
- Retrieval eval report when golden questions exist.
- Gap or conflict report when evidence is insufficient.

## Interface Model

| Surface | Owner | Examples | Agent Control |
| --- | --- | --- | --- |
| Tools | `04_Tool-Specs` and `tools/` | `source_ingestion_scan`, `source_search`, `source_download`, `vault_retrieve`, `vault_validate`, `retrieval_gap_report`, `eval_retrieval` | Builder-invoked or model-invoked |
| Resources | Obsidian Markdown notes | sources, concepts, cases, knowledge packs, diagrams | Application-provided |
| Prompts | `05_Prompts`, `07_Runbooks`, `_templates` | system prompt templates, build runbooks | User-selected or builder-selected |

This mirrors the MCP split between tools, resources, and prompts while keeping V1 local and dependency-free.

## V1 Tools

### `source_ingestion_scan`

Implemented by:

```bash
python3 tools/ingest_sources.py scan
```

Use before extraction when raw local files enter the vault. It creates source manifests with `source_id`, hash, source type, permission, and review fields.

### `source_download`

Implemented by:

```bash
python3 tools/source_download.py download "https://example.com/page" --domain your-domain
```

Use only for explicit URLs or small same-host crawls. It checks robots rules and creates raw files plus source manifests.

### `source_search`

Implemented by:

```bash
python3 tools/source_search.py from-pack "Evidence-Based Startup Methodology" --report
```

Use before download when a domain needs public source candidates. It scores official, government, academic, and known-primary sources, then can write candidates into the Web Source Queue for review.

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

### `vault_validate`

Implemented by:

```bash
python3 tools/validate_vault.py
```

Use before trusting a module or knowledge-pack change. It checks metadata, required sections, and Obsidian links.

### `retrieval_gap_report`

V1 implementation: read the `answerability` and `gaps` fields returned by `vault_retrieve`.

Use when retrieved evidence is partial or missing.

### `eval_retrieval`

Implemented by:

```bash
python3 tools/eval_retrieval.py --all
```

Use after source, pack, metadata, chunking, or ranking changes. It runs knowledge-pack golden questions and reports failure categories.

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

## Failure Handling

- If no scoped evidence is found, broaden terms once, then report the gap.
- If a cited note lacks source metadata, treat the answer as partial until the source is fixed.
- If Obsidian links fail, run `tools/validate_vault.py` and fix links before trusting review output.
- If golden questions fail, route the failure to source intake, extraction, metadata, chunking, ranking, pack scope, or gap labeling.
- If a tool would write, fetch, or delete data, require a separate tool spec and audit trail before production use.

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
- [[Tool Spec - Source Ingestion]]
- [[Tool Spec - Public Source Search]]
- [[Tool Spec - Web Source Download]]
- [[../09_Module-System/Domain Retrieval Modules/System Architecture - 12 Module Pipeline|System Architecture - 12 Module Pipeline]]
- [[../09_Module-System/Domain Knowledge Retrieval v1 Pipeline|Domain Knowledge Retrieval v1 Pipeline]]
- [[../09_Module-System/Source Trust and Certainty Standard|Source Trust and Certainty Standard]]
- [[../02_Domain-Knowledge/Packs/README|Knowledge Packs]]
