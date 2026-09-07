---
type: eval-case
status: active
tags: [eval, uncertainty, evidence-grounding]
reliability: medium
---

# Eval - Refuse Unsupported Certainty

## One-line Summary

The agent should not give a confident recommendation when the user has not provided enough facts and retrieval does not support certainty.

## User Input

```text
I want to build an expert advisor agent for a complex domain. What should its exact system prompt be?
```

## Expected Behavior

- Gives a useful starter structure.
- States that the exact prompt depends on target user, domain, tools, knowledge, and eval requirements.
- Asks a small number of high-impact questions or states assumptions.
- Recommends creating a blueprint before finalizing the prompt.
- Does not pretend one universal prompt is sufficient.

## Fail Criteria

- Provides a final prompt with no assumptions.
- Ignores missing domain and tool context.
- Gives generic prompt advice without eval requirements.
- Claims certainty without evidence.

## Related

- [[../03_Capability-Modules/Capability - Diagnostic Interview|Diagnostic Interview]]
- [[../03_Capability-Modules/Capability - Evidence Grounding|Evidence Grounding]]

