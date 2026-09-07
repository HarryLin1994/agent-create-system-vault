---
type: knowledge-source
source_type: official-docs-and-research
title: Retrieval and Tooling Best Practices
author: OpenAI, Anthropic, Model Context Protocol, Obsidian
status: active
tags: [source, domain-knowledge, retrieval, tools, obsidian, mcp]
reliability: high
domain: agent-create-system
updated: 2026-09-07
---

# Source - Retrieval and Tooling Best Practices

## One-line Summary

Use official docs, protocol specs, and well-scoped engineering references to design retrieval as a structured evidence system, not as a generic search box.

## Sources Reviewed

| Source | Why It Is Trusted | Used For |
| --- | --- | --- |
| [OpenAI File Search docs](https://developers.openai.com/api/docs/guides/tools-file-search) | Official API documentation from the platform provider | File search, vector-store-backed retrieval, tool output expectations |
| [Anthropic Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) | Provider engineering/research writeup focused on retrieval quality | Context-aware chunks, hybrid lexical/semantic retrieval, reranking direction |
| [MCP Tools spec](https://modelcontextprotocol.io/specification/2025-06-18/server/tools) | Official protocol specification | Tool schema, structured output, tool safety expectations |
| [MCP Resources spec](https://modelcontextprotocol.io/specification/2025-06-18/server/resources) | Official protocol specification | Treating vault notes as model-readable resources |
| [MCP Prompts spec](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts) | Official protocol specification | Treating runbooks and templates as reusable prompts |
| [Obsidian Properties docs](https://help.obsidian.md/Properties) | Official Obsidian documentation | YAML/frontmatter properties for human and machine-readable metadata |
| [Obsidian Internal Links docs](https://help.obsidian.md/Linking+notes+and+files/Internal+links) | Official Obsidian documentation | Human navigation through wiki links and note references |

## Claims Worth Using

- Claim: Retrieval should return structured evidence, not just unranked snippets.
  Evidence: Tool and retrieval APIs increasingly support structured result data, metadata, and schemas.
  Caveat: V1 can use local JSON before adding a full MCP server or managed vector store.

- Claim: Metadata matters as much as embeddings for expert retrieval.
  Evidence: Domain, type, status, reliability, source, and freshness filters prevent unrelated notes from entering the answer.
  Caveat: Poor metadata will make both keyword and embedding search look worse than they are.

- Claim: Human review links should be first-class output.
  Evidence: This vault is maintained in Obsidian, so every agent-facing evidence item should resolve to an Obsidian note path or URI.
  Caveat: Obsidian links do not prove a claim; they only preserve traceability.

- Claim: Tools, resources, and prompts should remain separate.
  Evidence: MCP separates model-invoked tools, application-provided resources, and user-controlled prompts.
  Caveat: V1 can document this split before implementing a server.

## Concepts Extracted

- Evidence pack
- Knowledge pack
- Reliability floor
- Answerability label
- Source trust tier
- Obsidian review link
- Tool/resource/prompt split

## Cases Extracted

- Bad retrieval returns a popular note whose keywords match but whose evidence does not support the expert answer.
- Bad tool design gives the expert raw notes without schema, source reliability, or human-review links.
- Bad Obsidian integration creates machine-only JSON that humans cannot navigate or maintain.

## Agent Usage

Use this source when designing:

- Domain knowledge retrieval.
- Expert tool policy.
- Obsidian-facing note metadata.
- MCP-compatible future interfaces.
- Retrieval evals and evidence-pack schemas.

## Source References

- OpenAI: https://developers.openai.com/api/docs/guides/tools-file-search
- Anthropic: https://www.anthropic.com/engineering/contextual-retrieval
- MCP Tools: https://modelcontextprotocol.io/specification/2025-06-18/server/tools
- MCP Resources: https://modelcontextprotocol.io/specification/2025-06-18/server/resources
- MCP Prompts: https://modelcontextprotocol.io/specification/2025-06-18/server/prompts
- Obsidian Properties: https://help.obsidian.md/Properties
- Obsidian Internal Links: https://help.obsidian.md/Linking+notes+and+files/Internal+links
