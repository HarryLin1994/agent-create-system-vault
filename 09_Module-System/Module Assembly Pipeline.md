---
type: module-pipeline
status: active
tags: [module-system, pipeline, assembly]
reliability: medium
---

# Module Assembly Pipeline

## One-line Summary

This pipeline turns an agent request into a composed agent using blueprints, modules, prompts, tools, and evals.

## Pipeline

1. Parse request.
2. Draft or select an agent blueprint.
3. Identify required capabilities.
4. Select capability modules by trigger and output.
5. Identify domain knowledge requirements.
6. Select knowledge modules or create missing source notes.
7. Identify required tools.
8. Attach tool specs and safety limits.
9. Assemble prompt modules into a system prompt.
10. Select eval modules for the highest-risk failure modes.
11. Register the agent version.
12. Run retrieval and eval smoke tests.

## Assembly Checks

- Every selected module has a clear trigger.
- Every selected module has explicit inputs and outputs.
- Prompt instructions do not conflict across modules.
- Tools have usage boundaries.
- Knowledge has provenance and reliability labels.
- Evals cover the agent's main failure modes.

## Output Bundle

The final agent bundle should contain:

- Blueprint
- Selected modules
- Knowledge dependencies
- Tool permissions
- System prompt
- Eval set
- Registry entry

## Related

- [[Module Contract]]
- [[Module Types]]
- [[../07_Runbooks/Basic Agent Creation Flow|Basic Agent Creation Flow]]

