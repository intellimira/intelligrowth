# Open Notebook Integration

## Overview

This integration connects Open Notebook (local AI research cockpit) to the `/skillm` vibegraph pipeline for skill creation.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      OPEN NOTEBOOK (COCKPIT)                            │
│  Local AI-powered research tool with:                                  │
│  - Multi-source ingestion (PDF, video, audio, web)                    │
│  - AI chat with context                                                │
│  - Vector search                                                       │
│  - Podcast generation                                                  │
│                                                                         │
│  Running at: http://localhost:8502                                    │
│  API at: http://localhost:5055                                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │   Hybrid Pull System          │
                    │   - Full copy on first fetch │
                    │   - Delta detection          │
                    │   - Position tracking        │
                    │   - Cached in references/    │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     /skillm PIPELINE                                    │
│  1️⃣ Ingest: /skillOn:nb_name or /skillOp:nb1 + nb2                  │
│  2️⃣ Persona Council: ⚛️🔬🤔✨⚙️🌑 analysis                           │
│  3️⃣ Specialization Layer: Expert refinement                          │
│  4️⃣ Generate: SKILL.md draft                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      MIRA CORE 6 PERSONAS                               │
│   ⚛️ First Principles  🔬 Scientific  🤔 Philosophical  ✨ Creative    │
│   ⚙️ Pragmatic         🌑 Dark Passenger                                │
│                                                                         │
│   + New Skills Added to Persona Skill Libraries                        │
└─────────────────────────────────────────────────────────────────────────┘
```

## Commands

### Open Notebook Commands

```bash
# List available notebooks
python src/ingest_open_notebook.py list

# Find notebook by name
python src/ingest_open_notebook.py find "research"

# Fetch single notebook
python src/ingest_open_notebook.py fetch "my-notebook"

# Fetch multiple notebooks
python src/ingest_open_notebook.py fetch "nb1 + nb2 + nb3"

# Force refresh (skip cache)
python src/ingest_open_notebook.py fetch "nb1" --force

# List cached notebooks
python src/ingest_open_notebook.py cached
```

### VibeGraph Commands

```bash
# Single notebook to skill
python src/vibegraph_runner.py "/skillOn:my-research"

# Multiple notebooks to skill
python src/vibegraph_runner.py "/skillOp:nb1 + nb2"

# With force refresh
python src/vibegraph_runner.py "/skillOn:nb1 --force"
```

## Implementation Details

### Files Modified/Created

| File | Purpose |
|------|---------|
| `src/ingest_open_notebook.py` | Open Notebook API client + caching |
| `src/ingest_url.py` | Added `/skillOn:` and `/skillop:` URL types |
| `src/vibegraph_runner.py` | Added `_fetch_open_notebook()` method |
| `docker-compose.yml` | Open Notebook deployment config |

### Cache Structure

```
references/
└── open_notebook/
    └── <notebook_id>/
        ├── content.md          # Full content (sources + chat)
        ├── metadata.json        # Notebook metadata
        └── last_accessed.json   # Position tracking + hash for delta
```

### URL Types Supported

| Syntax | Type | Example |
|--------|------|---------|
| `/skillOn:name` | Single notebook | `/skillOn:micro-saas` |
| `/skillop:name` | Single notebook | `/skillop:research` |
| `skillOn:name` | Single notebook | `skillOn:test` |
| `nb1 + nb2 + nb3` | Multiple notebooks | `/skillOn:a + b + c` |

## Dependencies

- **Open Notebook**: Running in Docker (localhost:8502)
- **Ollama**: Local LLM (qwen3:8b, qwen2.5-coder available)
- **requests**: Python HTTP client

## Getting Started

1. **Access Open Notebook**: http://localhost:8502
2. **Configure AI Provider**: Settings → API Keys → Add Ollama
3. **Create Notebooks**: Add research sources, chat with AI
4. **Generate Skills**: Use `/skillOn:notebook-name`

## Notes

- First fetch = full copy to `references/open_notebook/`
- Subsequent fetches = delta detection (compare hash)
- Position tracking allows resume of interrupted sessions
- All data stays local (privacy-focused)
