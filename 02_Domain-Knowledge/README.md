---
type: index
tags: [domain-knowledge, index]
---

# Domain Knowledge

Domain knowledge is replaceable content that agents retrieve while answering. Keep it separate from reusable agent capabilities.

## Subfolders

- `Sources`: books, articles, reports, interviews, transcripts, or internal documents.
- `Concepts`: reusable principles, frameworks, definitions, and heuristics.
- `Cases`: concrete successes, failures, incidents, examples, and counterexamples.
- `Packs`: scoped knowledge bundles that an expert agent can retrieve from.

## Rules

- Preserve provenance.
- Include confidence and limitations.
- Extract reusable lessons instead of dumping raw text.
- Use short quotes only when needed.
- Link each knowledge note to the agent capability or blueprint that uses it.
- Add enough metadata for both Obsidian and retrieval: `type`, `status`, `domain`, `tags`, and `reliability`.
- Prefer knowledge packs when attaching domain knowledge to an expert.

## Related

- [[Packs/README|Knowledge Packs]]
- [[../09_Module-System/Source Trust and Certainty Standard|Source Trust and Certainty Standard]]
