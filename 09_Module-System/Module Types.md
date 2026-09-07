---
type: module-taxonomy
status: active
tags: [module-system, module-types, taxonomy]
reliability: medium
---

# Module Types

## One-line Summary

The agent creation system separates modules by what they contribute to the final agent.

## Capability Modules

Reusable behavior.

Examples:

- Diagnostic interview
- Evidence grounding
- Risk analysis
- Decision memo generation
- Critique and red-team review

Stored in:

`03_Capability-Modules`

## Knowledge Modules

Reusable domain content that retrieval can use.

Examples:

- Startup strategy knowledge pack
- Legal contract review concepts
- Sales playbook cases
- Industry reports and source notes

Stored in:

`02_Domain-Knowledge`

## Tool Modules

Tool interface plus usage policy.

Examples:

- Vault retrieval
- Web search
- File reader
- CRM query
- Spreadsheet analysis

Stored in:

`04_Tool-Specs`

## Prompt Modules

Reusable instruction blocks that can be assembled into system prompts or developer prompts.

Examples:

- Evidence rules
- Tone and format rules
- Tool-use rules
- Refusal rules

Stored in:

`05_Prompts`

## Eval Modules

Reusable tests that protect behavior.

Examples:

- Refuse unsupported certainty
- Ask for missing context
- Use retrieved notes correctly
- Do not cite irrelevant sources

Stored in:

`06_Evals`

## Assembly Rule

An agent should be assembled from at least:

- One blueprint
- Two or more capability modules
- One knowledge module or explicit "no domain knowledge" decision
- Tool specs for every allowed tool
- Prompt modules or a generated system prompt
- Eval modules covering the main failure modes

