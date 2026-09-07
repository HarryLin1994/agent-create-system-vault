# agent-create-system-vault

Local Obsidian vault for designing, assembling, testing, and iterating specialized LLM agents.

The system keeps stable agent behavior separate from replaceable domain knowledge. A serious expert agent is assembled from:

- Agent blueprint
- Capability modules
- Knowledge pack
- Tool specs
- System prompt
- Eval set
- Registry entry

Start in [[Home.md]] when using this as an Obsidian vault.

## Current Focus

The current development focus is the module system and domain knowledge retrieval:

- `09_Module-System` defines module contracts, assembly rules, source trust standards, and retrieval pipelines.
- `09_Module-System/Domain Knowledge Retrieval Design Spec.md` is the main architecture spec for domain knowledge retrieval.
- `09_Module-System/Domain Retrieval Modules/` breaks retrieval into source intake, extraction, knowledge packs, indexing, ranking, evidence packs, Obsidian review, and eval feedback.
- `02_Domain-Knowledge` stores sources, concepts, cases, and scoped knowledge packs.
- `04_Tool-Specs/Tool Spec - Vault Retrieval.md` defines the local retrieval tool.
- `tools/agent_retrieve.py` returns evidence packs with Obsidian links for human review.

## Retrieval

```bash
python3 tools/agent_retrieve.py \
  "domain knowledge retrieval evidence pack obsidian" \
  --reliability-floor medium
```

Filtered JSON:

```bash
python3 tools/agent_retrieve.py \
  "evidence grounding unsupported certainty" \
  --type capability-module \
  --reliability-floor medium \
  --json
```

## Tool Policy

For this project version, product workflow approvals are auto-approved. Tools still need explicit specs, boundaries, failure handling, and eval coverage.
