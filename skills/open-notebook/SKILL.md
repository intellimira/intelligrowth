---
name: open-notebook
description: Open Notebook LM integration for MIRA-OJ. Privacy-first AI research assistant for semantic search, notebook management, source ingestion, AI chat with documents, and podcast generation. Use when user wants to search knowledge, create notebooks, chat with sources, or generate summaries.
agent: true
triggers: [open-notebook, "open notebook", notebook search, semantic search, chat with documents, create notebook, search knowledge]
tools: [notebook_search, notebook_create, notebook_list, notebook_delete, source_add, source_list, source_chat, search_knowledge, generate_insights, generate_podcast]
persona: "📚 Librarian — knowledge synthesis and semantic discovery"
mira_tier: 1
protocol: The Weave
---

# Open Notebook Skill

> Privacy-first AI research assistant powered by local models and Open Notebook LM

## Overview

**Open Notebook** is an open-source, self-hosted alternative to Google NotebookLM. MIRA-OJ integrates with it to provide:

- **Semantic Search** — Search across all ingested sources
- **Notebook Management** — Create, organize, and manage research notebooks
- **Source Ingestion** — Add PDFs, URLs, audio, video, and documents
- **AI Chat** — Ask questions about your sources
- **Podcast Generation** — Create AI-powered audio summaries

## Architecture

```
MIRA-OJ
  │
  └── open-notebook Skill
        │
        ├── API: http://localhost:5055
        │     ├── /api/notebooks/      → Notebook CRUD
        │     ├── /api/sources/       → Source management
        │     ├── /api/search/        → Semantic search
        │     ├── /api/chat/          → Chat with sources
        │     └── /api/podcasts/      → Podcast generation
        │
        ├── Database: SurrealDB @ localhost:8000
        │
        └── Models: Ollama (qwen3:8b, nomic-embed-text)
```

## Prerequisites

### Running Open Notebook

```bash
# Check if running
curl -s http://localhost:5055/health 2>/dev/null && echo "Running" || echo "Not running"

# Start Open Notebook (if installed locally)
# Note: Archived to /media/sir-v/Axion-Ext/MiRA/open_notebook_local/
```

### API Configuration

```bash
OPEN_NOTEBOOK_API_URL=http://localhost:5055
OPEN_NOTEBOOK_API_KEY=your-api-key
```

## Core Capabilities

### 1. Semantic Search

Search across all notebooks and sources using natural language.

```bash
# Search for "revenue growth strategies"
curl -X POST http://localhost:5055/api/search \
  -H "Authorization: Bearer $OPEN_NOTEBOOK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "revenue growth strategies", "limit": 10}'
```

**MIRA-OJ Command:**
```
mira: search open notebook for revenue optimization
mira: find notes about machine learning
```

### 2. Notebook Management

Create and manage research notebooks.

```bash
# List all notebooks
curl http://localhost:5055/api/notebooks \
  -H "Authorization: Bearer $OPEN_NOTEBOOK_API_KEY"

# Create notebook
curl -X POST http://localhost:5055/api/notebooks \
  -H "Authorization: Bearer $OPEN_NOTEBOOK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "MIRA Research", "description": "MIRA ecosystem research"}'

# Delete notebook
curl -X DELETE http://localhost:5055/api/notebooks/{notebook_id} \
  -H "Authorization: Bearer $OPEN_NOTEBOOK_API_KEY"
```

**MIRA-OJ Command:**
```
mira: create a new notebook called "Shadow Ops Research"
mira: list all my notebooks
mira: delete the old notebook
```

### 3. Source Ingestion

Add documents, URLs, audio, and video to notebooks.

```bash
# Add URL source
curl -X POST http://localhost:5055/api/sources \
  -H "Authorization: Bearer $OPEN_NOTEBOOK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "notebook_id": "uuid",
    "type": "url",
    "url": "https://example.com/article"
  }'

# Add PDF (multipart)
curl -X POST http://localhost:5055/api/sources/upload \
  -H "Authorization: Bearer $OPEN_NOTEBOOK_API_KEY" \
  -F "file=@/path/to/document.pdf" \
  -F "notebook_id=uuid"
```

**MIRA-OJ Command:**
```
mira: add this URL to my notebook
mira: ingest the PDF I just downloaded
mira: add this YouTube video as a source
```

### 4. Chat with Sources

Ask questions about your ingested documents.

```bash
# Chat with notebook
curl -X POST http://localhost:5055/api/chat \
  -H "Authorization: Bearer $OPEN_NOTEBOOK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "notebook_id": "uuid",
    "message": "What are the key findings?",
    "model": "qwen3:8b"
  }'
```

**MIRA-OJ Command:**
```
mira: ask my notebook about the main conclusions
mira: what does this source say about pricing?
```

### 5. Podcast Generation

Generate AI-powered audio summaries.

```bash
# Generate podcast
curl -X POST http://localhost:5055/api/podcasts \
  -H "Authorization: Bearer $OPEN_NOTEBOOK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "notebook_id": "uuid",
    "style": "educational",
    "language": "en"
  }'
```

**MIRA-OJ Command:**
```
mira: create a podcast summary of this notebook
mira: generate an audio digest of my research
```

## MIRA-OJ Integration

### Tool Mapping

| MIRA Tool | Open Notebook Endpoint | Purpose |
|-----------|----------------------|---------|
| `notebook_search` | `/api/search` | Semantic search |
| `notebook_create` | `/api/notebooks` (POST) | Create notebook |
| `notebook_list` | `/api/notebooks` (GET) | List notebooks |
| `notebook_delete` | `/api/notebooks/{id}` (DELETE) | Delete notebook |
| `source_add` | `/api/sources` (POST) | Add source |
| `source_list` | `/api/sources` (GET) | List sources |
| `source_chat` | `/api/chat` (POST) | Chat with sources |
| `search_knowledge` | `/api/search` | Knowledge search |
| `generate_insights` | `/api/insights` | Generate insights |
| `generate_podcast` | `/api/podcasts` (POST) | Create podcast |

### Example MIRA Commands

```markdown
# Create and populate a notebook
mira: create notebook "Shadow Ops Strategy" and add these sources:
  - https://example.com/strategy-guide
  - /path/to/analysis.pdf

# Search and summarize
mira: search open notebook for "monetization strategies" and summarize the top 3 results

# Chat with research
mira: ask my "MIRA Research" notebook what the key insights are about AI agents

# Generate podcast
mira: create a podcast summary of my "Shadow Ops" notebook
```

## Configuration

### Environment Variables

```bash
# Open Notebook API
OPEN_NOTEBOOK_API_URL=http://localhost:5055
OPEN_NOTEBOOK_API_KEY=your-secret-key

# Or use credential reference
OPEN_NOTEBOOK_CREDENTIAL=credential:open-notebook-api
```

### Default Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `default_model` | qwen3:8b | Chat model |
| `embedding_model` | nomic-embed-text | Embeddings |
| `max_results` | 10 | Search results |
| `podcast_style` | educational | Podcast style |

## Files & Locations

| File | Purpose |
|------|---------|
| `/media/sir-v/Axion-Ext/MiRA/open_notebook_local/` | Open Notebook source (archived) |
| `skills/open-notebook/SKILL.md` | This file |
| `skills/open-notebook/cookbook/` | Usage guides |
| `skills/open-notebook/references/` | API reference |

## Related Skills

- `active_recall` — Memory Mesh context retrieval
- `notebook_bridge` — Google NotebookLM integration
- `mira-oj` — Orchestrates all tools
- `session_guardian` — Logs usage for learning

---

*Skill: open-notebook v1.0*
*Protocol: The Weave*
*2026-03-18*
