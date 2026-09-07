---
type: runbook
status: active
tags: [runbook, agent-create-system, workflow]
reliability: medium
---

# Basic Agent Creation Flow

## One-line Summary

Use this flow to turn an agent idea into a testable first version.

## Flow

1. Capture the request in `00_Inbox`.
2. Create an agent blueprint in `01_Agent-Blueprints`.
3. Check [[../09_Module-System/Module Contract|Module Contract]] before adding modules.
4. Select capability modules from `03_Capability-Modules`.
5. Add domain sources, concepts, and cases in `02_Domain-Knowledge`.
6. Define tool specs in `04_Tool-Specs`.
7. Assemble or revise prompts in `05_Prompts`.
8. Create evals in `06_Evals`.
9. Register the agent in `08_Registry`.
10. Run retrieval to inspect what context the builder or runtime agent will see.

## First Local Test

```bash
python3 agent-create-system-vault/tools/agent_retrieve.py "diagnostic interview evidence grounding domain expert"
```

## Definition of Done for Version 0

- Blueprint exists.
- At least two capability modules are linked.
- Selected modules conform to [[../09_Module-System/Module Contract|Module Contract]].
- At least three domain knowledge notes exist.
- At least one tool spec exists if the agent uses tools.
- At least five eval cases exist.
- A system prompt draft exists.
- Retrieval returns relevant notes for expected user questions.
