---
name: mira-oj
description: MIRA-oj (MIRA OpenJarvis) - Sovereign AI Agent with local-first inference, Weave learning system, Library Orchestrator, and Open Notebook integration. Powered by Stanford's OpenJarvis framework with Ollama backend.
agent: true
triggers: [mira, "mira:", "@mira", "ask mira", "mira-oj", "local AI", "sovereign AI", "privacy AI", "mira: library", "manage library", "sync skills", "library report", "self-anneal", "open notebook", "notebook search", "search knowledge", "create notebook"]
tools: [mira_think, mira_ask, weave_stats, weave_rules, weave_learn, mira_health, persona_bind, library_manage, library_sync, library_report, library_notify, library_search, library_add, notebook_search, notebook_create, notebook_list, notebook_delete, source_add, source_list, source_chat, generate_podcast]
persona: "🔬 Scientific Method — sovereign AI orchestration"
mira_tier: 1
---

## Overview

**MIRA-oj** is MIRA's sovereign AI agent - a local-first, privacy-preserving inference engine that learns from your interaction patterns through The Weave.

### Core Capabilities

| Capability | Description |
|------------|-------------|
| Local Inference | All reasoning happens locally via Ollama |
| Privacy First | No data leaves your machine |
| Weave Learning | Learns from session interactions |
| Offline Mode | Works without internet |
| Cost Free | No API costs after hardware |

### Architecture

```
User Query (via mira:)
    ↓
MIRA-oj Agent (this skill)
    ↓
Weave Router (learns patterns)
    ↓
┌─────────────┬─────────────┐
│   Local     │    Cloud    │
│ OpenJarvis  │   Fallback  │
│  (qwen3)    │   (API)     │
└─────────────┴─────────────┘
    ↓
Response + Learning
```

---

## Usage

### Trigger Phrases

```plaintext
mira: What is quantum computing?
ask mira explain Python
@mira write me a function
mira-oj analyze this code
```

### Commands

| Command | Description |
|---------|-------------|
| `mira: <query>` | Ask MIRA-oj (learns from use) |
| `weave stats` | Show learning statistics |
| `weave rules` | Show learned routing rules |
| `weave ingest` | Re-ingest session logs |
| `mira health` | Check system health |

---

## Weave Learning System

The Weave is MIRA-oj's learning system - it learns from every interaction to improve routing decisions.

### How It Works

1. **Query Analysis** - Extracts patterns from your queries
2. **Route Decision** - Chooses local vs cloud based on learned rules
3. **Outcome Recording** - Tracks success/failure
4. **Rule Refinement** - Improves confidence based on outcomes

### Learning Metrics

| Metric | Description |
|--------|-------------|
| Total Interactions | Queries processed |
| mj-simulated | Historical data from sessions |
| success | Real successful interactions |
| timeout | Queries that timed out |
| Rules Learned | Patterns identified |

### View Statistics

```bash
# View Weave stats
python3 .mira/openjarvis_bridge.py weave stats

# View learned rules
python3 .mira/openjarvis_bridge.py weave rules

# Re-ingest sessions
python3 .mira/openjarvis_bridge.py weave ingest
```

---

## Persona Integration

MIRA-oj binds to MIRA's Persona Council:

| Persona | Model | Best For |
|---------|-------|----------|
| ⚛️ First Principles | qwen3:8b | Foundational reasoning |
| 🔬 Scientific Method | qwen3:8b | Analysis, testing |
| 🤔 Philosophical | qwen3:8b | Ethics, meaning |
| ✨ Creative | qwen3:8b | Ideas, synthesis |
| ⚙️ Pragmatic | qwen2.5-coder:7b | Code, implementation |
| 🌑 Dark Passenger | qwen3:8b | Risk, failure modes |

---

## Privacy Features

### Data Sovereignty

- ✅ All inference runs locally
- ✅ No cloud API calls (unless forced)
- ✅ Query history stays on your machine
- ✅ Learnable patterns stored in SQLite

### Privacy Modes

| Mode | Behavior |
|------|----------|
| `offline=True` | Always local |
| `privacy_critical=True` | Always local |
| `force_route='cloud'` | Use cloud API |

---

## Session Log Training

MIRA-oj trains on ALL your session logs:

### Sources

- `sessions/` - Primary session files
- `Memory_Mesh/zettels/` - Zettelkasten
- `projects/*/docs/session*.md` - Project logs

### Outcome Types

| Outcome | Meaning |
|---------|---------|
| `mj-simulated` | Historical data (from session logs) |
| `success` | Real successful query |
| `timeout` | Query timed out |
| `failure` | Query failed |

---

## Quality Gates

| Gate | Check | Command |
|------|-------|---------|
| ollama_running | Ollama API responding | `curl localhost:11434/api/tags` |
| models_installed | At least one model | `ollama list` |
| config_valid | Config parses | Check `~/.openjarvis/config.toml` |
| weave_working | Weave DB accessible | Query `.mira/weave.db` |

---

## Configuration

### OpenJarvis Config

Location: `~/.openjarvis/config.toml`

```toml
[intelligence]
default_model = "qwen3:8b"
preferred_engine = "ollama"
provider = "local"

[engine.ollama]
host = "http://localhost:11434"

[telemetry]
enabled = true
db_path = "~/.mira/telemetry/openjarvis.db"
```

### Weave Config

Location: `~/.mira/weave.db` (auto-created)

---

## Files & Locations

| File | Purpose |
|------|---------|
| `.mira/weave_router.py` | Weave Router module |
| `.mira/openjarvis_bridge.py` | MIRA-oj Bridge |
| `.mira/weave.db` | Learning database |
| `skills/mira-oj/SKILL.md` | This file |
| `/home/sir-v/OpenJarvis/` | OpenJarvis installation |

---

## Related Skills

- `openjarvis` - Base OpenJarvis framework
- `local-ai-stack` - Ollama setup
- `active_recall` - Memory context
- `sovereign_shadow_operator` - Privacy automation

---

## Library Orchestrator

MIRA-OJ manages The Library for skill distribution, self-annealing, and notifications.

### What The Library Does

- **Catalogs** all MIRA skills with source references
- **Syncs** skills from source repos on demand
- **Self-Anneals** by detecting broken references and missing dependencies
- **Notifies** via email (Thunderbird `intellimira@gmail.com`) on events

### Library Manager Module

Location: `.mira/library_manager.py`

### Usage Commands

| Command | Description |
|---------|-------------|
| `mira: library list` | List all cataloged skills with status |
| `mira: library sync` | Sync all installed skills from sources |
| `mira: library search "keyword"` | Find skills by name/description |
| `mira: library add <name> <source>` | Add skill to catalog |
| `mira: library anneal` | Run self-anneal health check |
| `mira: library report` | Generate status report |

### Email Notifications

Reports are sent to Thunderbird folder: `MIRA-OJ Orchestrator/Library Reports`

| Event | Notification |
|-------|-------------|
| Sync complete | Summary of synced skills |
| Broken reference | Alert with fix recommendation |
| Self-anneal complete | Issues found + actions taken |
| Dependency conflict | Query for your decision |

### Configuration

The Library catalog: `~/.claude/skills/library/library.yaml`

MIRA skills directory: `/home/sir-v/MiRA/skills/`

### Example Queries

```
mira: library list
mira: library search "revenue"
mira: library anneal and send me the report
mira: add a new skill called test-skill from /path/to/SKILL.md
```

### Self-Anneal Checks

1. **Broken References** - Source paths that no longer exist
2. **Missing Dependencies** - Skills that require unavailable dependencies
3. **Stale Entries** - Skills not synced in 30+ days
4. **Duplicates** - Skills registered multiple times

---

## Open Notebook Integration

MIRA-OJ integrates with Open Notebook LM for semantic search, notebook management, and knowledge synthesis.

### What Open Notebook Does

- **Semantic Search** — Search across all ingested sources
- **Notebook Management** — Create and organize research notebooks
- **Source Ingestion** — Add PDFs, URLs, audio, video
- **AI Chat** — Ask questions about your sources
- **Podcast Generation** — Create audio summaries

### Open Notebook Commands

| Command | Description |
|---------|-------------|
| `mira: search open notebook for X` | Semantic search |
| `mira: create notebook "name"` | Create new notebook |
| `mira: list notebooks` | Show all notebooks |
| `mira: add source to notebook` | Ingest document |
| `mira: ask my notebook about X` | Chat with sources |
| `mira: generate podcast` | Create audio summary |

### Example Queries

```
mira: create a notebook called "Shadow Ops Research"
mira: add this URL to my research notebook
mira: search open notebook for revenue optimization strategies
mira: ask my notebook what the key insights are
mira: create a podcast summary of my research
```

### Configuration

Open Notebook runs at `http://localhost:5055`

For details, see: `skills/open-notebook/SKILL.md`

---

## VRAM Optimizer & Efficiency Mode

MIRA-OJ includes AutoResearch-powered optimization for local inference.

### Based On

Experiments on RTX 2060 (6GB VRAM) with 4 training runs:

| Finding | Result |
|---------|--------|
| Optimal depth | 4 layers |
| Optimal embedding | 384 dims |
| Optimal learning rate | 0.001 |
| VRAM efficiency | 0.25 GB baseline |

### Commands

```bash
# Check device profile
python3 .mira/vram_optimizer.py

# Get optimization params
python3 -c "from .mira.vram_optimizer import get_device_profile; print(get_device_profile())"
```

### Device Tiers

| Tier | VRAM | Profile |
|------|------|---------|
| High | 24+ GB | Full model capacity |
| Medium | 12-24 GB | Balanced |
| Low | 6-12 GB | Efficiency recommended |
| Minimal | 2-6 GB | Efficiency mode |
| CPU | <2 GB | Minimal inference |

### Efficiency Mode

For constrained devices, MIRA-OJ can use:

- **Reduced depth** (2-4 layers vs 12+)
- **Smaller embeddings** (256-384 vs 768+)
- **FP16 precision** when available
- **Standard attention** (no Flash Attention)

### Council Decision

Persona Council approved integration (85% consensus):
- Token bounds safety ✅
- VRAM-aware detection ✅
- Memory-efficient mode ✅

---

## Trained Models (MIRA_ARCH)

MIRA-OJ includes self-trained models learned from MIRA_ARCH data.

### Based On

- **MIRA_ARCH corpus**: 26,634 documents, 39.6M tokens
- **Training date**: 2026-03-22
- **Method**: AutoResearch baseline (depth=4, n_embd=384)

### Weave Models

Location: `~/.mira/weave_models/`

| Model | Size | Purpose |
|-------|------|---------|
| `link_predictor.pt` | 1.0 MB | Predicts zettel links |
| `summarizer.pt` | 772 KB | Generates zettel summaries |
| `quality_scorer.pt` | 228 KB | Scores content quality |

### MIRA-OJ Models

Location: `~/.mira/miraoj_models/`

| Model | Size | Purpose |
|-------|------|---------|
| `response_generator.pt` | 18 MB | Base response generation |
| `persona_first_principles.pt` | 772 KB | ⚛️ First Principles persona |
| `persona_scientific.pt` | 772 KB | 🔬 Scientific Method persona |
| `persona_philosophical.pt` | 772 KB | 🤔 Philosophical Inquiry persona |
| `persona_creative.pt` | 772 KB | ✨ Creative Synthesis persona |
| `persona_pragmatic.pt` | 772 KB | ⚙️ Pragmatic Application persona |
| `persona_dark_passenger.pt` | 772 KB | 🌑 Dark Passenger persona |

### Training Commands

```bash
# Retrain Weave models
cd /home/sir-v/MiRA && python3 Memory_Mesh/weave_trainer.py

# Retrain MIRA-OJ models
cd /home/sir-v/MiRA && python3 Memory_Mesh/miraoj_trainer.py

# View training data
ls -la ~/MIRA_ARCH_extracted/
```

### Data Sources

| Dataset | Documents | Tokens (est.) |
|---------|-----------|---------------|
| Session logs | 419 | 130K |
| Council decisions | 774 | 226K |
| Weave training | 7,035 | 2.2M |
| MIRA-OJ training | 2,572 | 783K |
| Full corpus | 26,634 | 39.6M |

---

*Agent: MIRA-oj v2.2*
*Weave Learning: Active*
*AutoResearch: Integrated*
*Open Notebook: Integrated*
*Trained Models: v2.2*
*2026-03-22*
