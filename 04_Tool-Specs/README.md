---
type: index
tags: [tool-spec, index]
---

# Tool Specs

Tool specs define how agents interact with local scripts, APIs, files, databases, and external systems.

Use [[../_templates/Tool Spec Template|Tool Spec Template]].

## Rules

- Define when the tool should be used.
- Define inputs and outputs.
- Define safety limits.
- Define failure handling.
- Add at least one eval that checks tool behavior.

## Current Tools

- [[Tool Spec - Source Ingestion|Source Ingestion]]
- [[Tool Spec - Vault Retrieval|Vault Retrieval]]
- [[Tool Spec - Expert Vault Interface|Expert Vault Interface]]

## Current Policy

For this project version, approval gates are auto-approved. Keep tool specs strict anyway so future MCP/server integrations can expose clear schemas and boundaries.
