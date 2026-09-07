---
type: module-contract
status: active
tags: [module-system, contract, interface]
reliability: medium
---

# Module Contract

## One-line Summary

Every module must expose the same contract so agents can be assembled from reusable parts instead of custom one-off prompts.

## Required Fields

### Purpose

What this module is responsible for.

### Trigger

When the runtime agent or builder should activate this module.

### Inputs

The information this module needs from the user, retrieved knowledge, tools, or other modules.

### Outputs

The structured result this module produces for the agent.

### Dependencies

Other modules, tools, prompts, knowledge packs, or evals required for this module to work.

### Runtime Instructions

The exact behavior the agent should follow when this module is active.

### Failure Modes

Ways this module can produce bad behavior.

### Eval Coverage

Eval cases that verify the module works and prevent regressions.

## Optional Fields

- Confidence rules
- Refusal rules
- Escalation rules
- Output examples
- Version notes

## Builder Rule

Do not add a module to an agent blueprint unless its trigger, inputs, outputs, and failure modes are clear.

