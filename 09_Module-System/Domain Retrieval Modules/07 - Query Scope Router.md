---
type: internal-module
status: active
tags: [module-system, domain-retrieval, query-routing]
reliability: high
updated: 2026-09-07
---

# 07 - Query Scope Router

## One-line Summary

Translate a user question or expert task into a scoped retrieval query and filters.

## Purpose

Avoid whole-vault retrieval when a domain, knowledge pack, note type, tag, or reliability floor is known.

## Trigger

Use before retrieval whenever an expert receives a question or the builder tests a knowledge pack.

## Inputs

- User question or expert task.
- Agent blueprint.
- Known domain or knowledge pack.
- Tool policy.
- Required freshness or reliability.

## Outputs

- Retrieval query.
- Selected knowledge pack when available.
- Filters: domain, type, tag, status, reliability floor.
- Search intent: find source, concept, case, checklist, tool, eval, or gap.

## Dependencies

- [[05 - Knowledge Pack Builder]]
- [[../../01_Agent-Blueprints/Example - Domain Expert Advisor|Example - Domain Expert Advisor]]
- [[../../04_Tool-Specs/Tool Spec - Expert Vault Interface|Expert Vault Interface]]

## Runtime Instructions

- Use the expert's knowledge pack first when available.
- Use `--domain` when the domain is known.
- Use `--type` when looking for sources, concepts, cases, tools, or evals.
- Use `--reliability-floor medium` for claims that affect decisions.
- Broaden only after scoped retrieval fails.
- Preserve the user's wording but add domain terms when they are explicit in the blueprint or pack.

## Failure Modes

- Query is too broad and returns module-system notes instead of domain evidence.
- Query is too narrow and misses relevant notes.
- Reliability floor is omitted for high-stakes claims.
- The expert retrieves from the wrong domain.

## Eval Coverage

- Golden questions in each knowledge pack.
- [[../../06_Evals/Eval - Domain Retrieval Relevance|Domain Retrieval Relevance]]
