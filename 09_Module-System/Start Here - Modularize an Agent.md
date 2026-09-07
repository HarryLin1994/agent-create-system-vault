---
type: runbook
status: active
tags: [module-system, runbook, modularization]
reliability: medium
---

# Start Here - Modularize an Agent

## One-line Summary

Use this runbook when turning a vague agent idea into a modular agent design.

## Step 1 - Write the Agent Request

Put the raw request in `00_Inbox`.

Minimum fields:

- Target user:
- Job to be done:
- Domain:
- Expected outputs:
- Tools needed:
- Known risks:
- What a bad answer looks like:

## Step 2 - Draft the Blueprint

Create or update a note in `01_Agent-Blueprints`.

The blueprint owns:

- Agent role
- Scope
- Non-goals
- Required capabilities
- Required knowledge
- Required tools
- Failure modes
- Eval set

## Step 3 - Split Capabilities

Convert behavior into capability modules.

Good capability modules are reusable across agents. Examples:

- Diagnostic interview
- Evidence grounding
- Risk analysis
- Decision memo
- Source comparison
- Action plan generation

Do not create a capability module for one tiny wording preference.

## Step 4 - Split Knowledge

Convert domain material into knowledge modules.

Knowledge modules should include:

- Sources
- Concepts
- Cases
- Reliability
- Applicability
- Limitations

## Step 5 - Split Tools

Every tool needs a tool spec.

The spec should define:

- When to use the tool
- Inputs
- Outputs
- Safety limits
- Failure handling
- Eval coverage

## Step 6 - Assemble Prompt

The prompt should be assembled from:

- Blueprint
- Capability modules
- Knowledge rules
- Tool specs
- Output requirements
- Refusal and uncertainty rules

## Step 7 - Attach Evals

Every important module needs at least one eval.

Start with evals for:

- Unsupported certainty
- Missing context
- Wrong tool use
- Irrelevant retrieval citation
- Generic advice

## Step 8 - Register Version

Add the finished agent version to `08_Registry`.

Track:

- Version
- Blueprint
- Modules
- Prompt
- Evals
- Known issues

## First Practical Task

For the first real agent, do not start by writing the final prompt. Start by writing the blueprint and selecting only the minimum modules needed for version 0.

