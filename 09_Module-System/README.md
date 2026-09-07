---
type: index
tags: [module-system, index]
---

# Module System

This folder defines how modules work in the agent creation system.

## Core Idea

A module is a reusable unit that can be attached to an agent blueprint. It must have a stable contract so prompts, tools, evals, and runtime behavior can be assembled consistently.

## Start Here

- [[Start Here - Modularize an Agent]]
- [[Module Contract]]
- [[Module Types]]
- [[Module Assembly Pipeline]]
- [[Module Registry]]
- [[Expert Skill Factory v1 Pipeline]]
- [[Domain Knowledge Retrieval v1 Pipeline]]
- [[Source Trust and Certainty Standard]]

## Module Types

- Capability module: reusable behavior, such as diagnostic interview or evidence grounding.
- Knowledge module: reusable domain knowledge pack, such as startup strategy or legal review.
- Tool module: a tool interface plus usage policy.
- Prompt module: reusable instruction block.
- Eval module: reusable quality test.
- Standard module: cross-cutting rules such as source trust, certainty, or approval policy.

## Required Contract

Every module should define:

- Purpose
- Trigger
- Inputs
- Outputs
- Dependencies
- Runtime instructions
- Failure modes
- Eval coverage

## First Goal

Before creating more agents, make the existing capability modules conform to this contract.

## Current Policy

For this project version, workflow approval gates are auto-approved. Module and tool specs must still document tool boundaries, failure handling, and eval coverage.
