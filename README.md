# agent-create-system-vault

Local Obsidian vault for designing, assembling, testing, and iterating specialized LLM agents.

The system keeps stable agent behavior separate from replaceable domain knowledge. A serious expert agent is assembled from:

- Agent blueprint
- Capability modules
- Knowledge pack
- Tool specs
- System prompt
- Eval set
- Registry entry

Start in [[Home.md]] when using this as an Obsidian vault.

## Current Focus

The current development focus is the module system and domain knowledge retrieval:

- `09_Module-System` defines module contracts, assembly rules, source trust standards, and retrieval pipelines.
- `09_Module-System/Domain Knowledge Retrieval Design Spec.md` is the main architecture spec for domain knowledge retrieval.
- `09_Module-System/Domain Retrieval Modules/` breaks retrieval into source intake, extraction, knowledge packs, indexing, ranking, evidence packs, Obsidian review, and eval feedback.
- `09_Module-System/Domain Retrieval Modules/System Architecture - 12 Module Pipeline.md` maps the 12 modules into one pipeline with module inputs and outputs.
- `02_Domain-Knowledge` stores sources, concepts, cases, and scoped knowledge packs.
- `04_Tool-Specs/Tool Spec - Vault Retrieval.md` defines the local retrieval tool.
- `tools/agent_retrieve.py` returns evidence packs with Obsidian links for AI review traceability and human checkpoints.
- `tools/ingest_sources.py` scans raw source files and creates source manifests with stable IDs and hashes.
- `tools/source_search.py` finds public source candidates, scores them for trust/public accessibility, and can queue them for review.
- `tools/source_download.py` downloads explicit web URLs or small same-host crawls into raw source intake with robots checks.
- `tools/validate_vault.py` checks module contracts, retrieval metadata, and Obsidian links.
- `tools/eval_retrieval.py` runs knowledge-pack golden retrieval questions.

## Dependencies

Core CLI dependencies:

- Python 3.10 or newer.
- Python standard library only for `agent_retrieve.py`, `ingest_sources.py`, `source_search.py`, `source_download.py`, `validate_vault.py`, and `eval_retrieval.py`.
- Optional `BRAVE_SEARCH_API_KEY` for live public-source search through Brave Search API. Without it, `source_search.py` generates manual search queries and still scores URLs already listed in a knowledge pack.
- Optional book-source connector environment variables: `GOOGLE_BOOKS_API_KEY`, `OREILLY_API_TOKEN`, `OREILLY_AUTH_SCHEME`, and `AMAZON_PARTNER_TAG`.
- Source search/download tools are designed for legal public sources, official metadata, licensed access, and user-provided files with processing permission. They do not support pirated PDFs or unauthorized full-book downloads.

Optional human/review dependencies:

- Obsidian for reading the vault as linked Markdown.
- Node.js plus the local `archify` skill only if architecture HTML needs to be regenerated.

Not V1 dependencies yet:

- OCR services such as Google Document AI, Azure Document Intelligence, or AWS Textract.
- Vector databases or embedding stores such as OpenAI Vector Stores, Azure AI Search, Qdrant, Weaviate, Pinecone, pgvector, or FAISS.
- Agent orchestration frameworks such as LangChain, LlamaIndex, or Semantic Kernel.

## Retrieval

```bash
python3 tools/agent_retrieve.py \
  "domain knowledge retrieval evidence pack obsidian" \
  --reliability-floor medium
```

Filtered JSON:

```bash
python3 tools/agent_retrieve.py \
  "evidence grounding unsupported certainty" \
  --type capability-module \
  --reliability-floor medium \
  --json
```

Validate the vault and run retrieval evals:

```bash
python3 tools/ingest_sources.py scan
python3 tools/validate_vault.py
python3 tools/eval_retrieval.py --all
```

Download explicit web sources:

```bash
python3 tools/source_download.py download "https://example.com/page" --domain your-domain
```

Find public source candidates:

```bash
python3 tools/source_search.py from-pack "Evidence-Based Startup Methodology" --report
```

Find book metadata/access candidates:

```bash
python3 tools/source_search.py books \
  --book "The Lean Startup | Eric Ries" \
  --book "Company of One: Why Staying Small Is the Next Big Thing for Business | Paul Jarvis" \
  --book "The 4-Hour Workweek | Tim Ferriss" \
  --domain evidence-based-startup-methodology \
  --report
```

For local Python certificate issues only, add `--insecure-skip-tls-verify` to
provider smoke tests. Keep TLS verification enabled for normal use.

## Tool Policy

For this project version, product workflow approvals are auto-approved. Tools still need explicit specs, boundaries, failure handling, and eval coverage.
