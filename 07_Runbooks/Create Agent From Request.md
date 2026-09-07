---
type: runbook
status: active
tags: [runbook, agent-create-system, modularization]
reliability: medium
---

# Create Agent From Request

## One-line Summary

This is the minimum repeatable process for creating a modular agent from a plain-language request.

## Input

A request like:

```text
Create an agent that can become a professional startup advisor.
```

## Output

- Agent blueprint
- Selected modules
- Knowledge requirements
- Tool requirements
- System prompt draft
- Eval draft
- Registry entry

## Process

1. Capture the raw request.
2. Retrieve module-system notes:

```bash
python3 /Users/harrylin/agent-create-system-vault/tools/agent_retrieve.py "modularize agent blueprint capability knowledge tool eval"
```

3. Create the blueprint.
4. Select existing modules before creating new ones.
5. Create missing modules only when the behavior is reusable.
6. Draft prompt from blueprint plus modules.
7. Draft evals for the biggest failure modes.
8. Register the agent as `v0`.

## Version 0 Rule

For version 0, keep the agent small:

- One blueprint
- Two capability modules
- One knowledge pack or explicit knowledge gap
- One retrieval tool spec
- Three to five eval cases
- One system prompt

## Related

- [[../09_Module-System/Start Here - Modularize an Agent|Start Here - Modularize an Agent]]
- [[../09_Module-System/Module Assembly Pipeline|Module Assembly Pipeline]]
- [[Basic Agent Creation Flow]]

