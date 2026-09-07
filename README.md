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
- `09_Module-System/Domain Retrieval Modules/System Architecture - 12 Module Pipeline.md` maps the 12 modules into one pipeline with module inputs and outputs.
- `02_Domain-Knowledge` stores sources, concepts, cases, and scoped knowledge packs.
- `04_Tool-Specs/Tool Spec - Vault Retrieval.md` defines the local retrieval tool.
- `tools/agent_retrieve.py` returns evidence packs with Obsidian links for human review.
- `tools/validate_vault.py` checks module contracts, retrieval metadata, and Obsidian links.
- `tools/eval_retrieval.py` runs knowledge-pack golden retrieval questions.

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

Validate the vault and run retrieval evals:

```bash
python3 tools/validate_vault.py
python3 tools/eval_retrieval.py --all
```

## Tool Policy

For this project version, product workflow approvals are auto-approved. Tools still need explicit specs, boundaries, failure handling, and eval coverage.
