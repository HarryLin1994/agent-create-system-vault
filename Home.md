---
type: home
tags: [agent-create-system, index]
---

# Agent Create System Vault

This vault is a local knowledge base for designing, assembling, testing, and iterating specialized LLM agents.

## Basic Flow

1. Capture raw material in [[00_Inbox/README|Inbox]].
2. Convert the material into agent blueprints, capability modules, domain knowledge, tool specs, prompts, or evals.
3. Assemble an agent from a blueprint plus selected modules and knowledge.
4. Run local retrieval before writing or revising an agent:

```bash
python3 agent-create-system-vault/tools/agent_retrieve.py \
  "create a domain expert advisor with evidence-grounded answers" \
  --reliability-floor medium
```

5. Use the retrieved notes to produce or update system prompts, tool instructions, and eval cases.
6. Test the agent against evals before trusting it.

## Main Indexes

- [[01_Agent-Blueprints/README|Agent Blueprints]]
- [[02_Domain-Knowledge/README|Domain Knowledge]]
- [[03_Capability-Modules/README|Capability Modules]]
- [[03_Capability-Modules/Capability - Domain Knowledge Retrieval|Domain Knowledge Retrieval]]
- [[02_Domain-Knowledge/Packs/README|Knowledge Packs]]
- [[04_Tool-Specs/README|Tool Specs]]
- [[05_Prompts/README|Prompts]]
- [[06_Evals/README|Evals]]
- [[07_Runbooks/Basic Agent Creation Flow|Basic Agent Creation Flow]]
- [[07_Runbooks/Create Agent From Request|Create Agent From Request]]
- [[07_Runbooks/Extract Expert Knowledge From Sources|Extract Expert Knowledge From Sources]]
- [[07_Runbooks/Build Knowledge Pack For Expert|Build Knowledge Pack For Expert]]
- [[08_Registry/Agent Registry|Agent Registry]]
- [[09_Module-System/README|Module System]]
- [[09_Module-System/Domain Knowledge Retrieval Design Spec|Domain Knowledge Retrieval Design Spec]]
- [[09_Module-System/Domain Retrieval Modules/README|Domain Retrieval Modules]]
- [[09_Module-System/Source Trust and Certainty Standard|Source Trust and Certainty Standard]]

## Operating Rules

- Treat agents as products: define users, jobs, scope, failure modes, tools, and tests.
- Separate stable agent behavior from replaceable domain knowledge.
- Prefer explicit capability modules over one giant prompt.
- Modules must declare trigger, inputs, outputs, dependencies, runtime instructions, failure modes, and eval coverage.
- Preserve sources and confidence levels for domain knowledge.
- Keep copyrighted source material as notes, summaries, short quotes, and references, not full text.
- Every note should answer: "When should an agent builder use this?"
- Approval gates are auto-approved for this project version, but tools must still declare boundaries and failure handling.
