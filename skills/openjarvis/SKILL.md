---
name: openjarvis
description: Stanford's local-first AI agent framework for self-hosted inference. Provides MIRA with local Ollama-powered reasoning, privacy-first operation, and sovereign AI capability. Now integrated with MIRA-oj Agent.
triggers: [openjarvis, local-inference, self-hosted-ai, offline-ai, privacy-ai, stanford-ai, jarvis, ollama-local]
tools: [jarvis_ask, jarvis_serve, jarvis_doctor, ollama_list, ollama_run]
quality_gates: [ollama_running, models_installed, config_valid, test_query_success]
persona: "🔬 Scientific Method — inference optimization and local AI"
mira_tier: 1
agent: mira-oj
---

## Source Content Chained (Primary)
1. https://github.com/open-jarvis/OpenJarvis - Main repository
2. https://open-jarvis.github.io/OpenJarvis/ - Documentation
3. https://scalingintelligence.stanford.edu/blogs/openjarvis/ - Stanford research
4. /home/sir-v/OpenJarvis/ - Local installation

## Why OpenJarvis?

### The Sovereignty Argument
- **Privacy**: Data never leaves your machine
- **Cost**: No per-token API costs (one-time hardware)
- **Speed**: No network latency (~20s vs 2s for local)
- **Offline**: Works without internet
- **Control**: Full infrastructure sovereignty

### Architecture (Five-Primitives)
| Primitive | Function |
|-----------|----------|
| Intelligence | Local models (Qwen3, Llama3.2) |
| Engine | Ollama runtime |
| Agents | Orchestrator, ToolUsing, NativeReAct |
| Tools & Memory | MCP, A2A, retrieval |
| Learning | Trace-driven improvement |

## Installation

### Prerequisites
```bash
# Ollama must be installed
which ollama  # Should return path

# Models must be pulled
ollama list  # Should show available models
```

### Install OpenJarvis
```bash
# Clone repository
git clone https://github.com/open-jarvis/OpenJarvis.git /home/sir-v/OpenJarvis

# Install dependencies
cd /home/sir-v/OpenJarvis
uv sync

# Initialize config
uv run jarvis init
```

### Configuration
Config location: `~/.openjarvis/config.toml`

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

## Usage

### Basic Query
```bash
cd /home/sir-v/OpenJarvis
uv run jarvis ask "What is 2 + 2?"
```

### With Profiling
```bash
uv run jarvis ask --engine ollama --model qwen3:8b --profile "Your question here"
```

### Available Models
| Model | Size | Recommended For |
|-------|------|-----------------|
| qwen3:8b | 5.2GB | General purpose |
| qwen3-8b-32k | 5.2GB | Long context |
| qwen2.5-coder:7b | 4.7GB | Code tasks |
| llama3.2:3b | 2GB | Light tasks |

### Inference Metrics
```
Wall time         ~20s
TTFT (first token) ~430ms
Mean ITL          ~145ms
Throughput        ~6.7 tok/s
```

## MIRA Integration

### HITL Triggers (Updated)
When using OpenJarvis, also observe:
- Executing local agent actions (tool permissions)
- Fine-tuning local model on interaction data
- Switching between local and cloud providers
- Modifying OpenJarvis config

### Workflow Integration
```python
# Pseudo-code for MIRA + OpenJarvis
def mira_think(query):
    if offline_mode:
        return openjarvis_ask(query)  # Local
    elif privacy_critical:
        return openjarvis_ask(query)  # Local
    else:
        return cloud_api(query)       # Fallback
```

### Telemetry Storage
- Location: `~/.mira/telemetry/`
- Metrics: latency, tokens, energy, cost
- Traces: `~/.mira/telemetry/traces.db`

## Commands Reference

| Command | Description |
|---------|-------------|
| `jarvis ask "question"` | Ask a question |
| `jarvis serve` | Start FastAPI server |
| `jarvis doctor` | Diagnose configuration |
| `jarvis init` | Initialize setup |
| `ollama list` | List available models |
| `ollama pull <model>` | Download model |

## Quality Gates

| Gate | Check | Command |
|------|-------|---------|
| ollama_running | Ollama API responding | `curl localhost:11434/api/tags` |
| models_installed | At least one model | `ollama list` |
| config_valid | Config parses | Check `~/.openjarvis/config.toml` |
| test_query_success | Basic query works | `jarvis ask "test"` |

## Troubleshooting

### Ollama not running
```bash
ollama serve
```

### Model not found
```bash
ollama pull qwen3:8b
```

### Connection refused
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Check config matches
uv run jarvis doctor
```

## Related Skills

- `mira-oj` - **MIRA-oj Agent** (sovereign AI with Weave learning)
- `local-ai-stack` - Ollama setup and management
- `active_recall` - Memory Mesh context retrieval
- `sovereign_shadow_operator` - Privacy-first automation
