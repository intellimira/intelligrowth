---
name: local-ai-stack
description: Comprehensive skill for setting up local AI infrastructure with Ollama, OpenClaw, LM Studio, and self-hosted AI agent deployment.
triggers: [local-ai, self-hosted-llm, ollama, openclaw, lm-studio, local-ai-stack, ai-agents, self-hosted-ai, gguf-models]
tools: [ollama_run, docker, pnpm, npm, model_download, gateway_config]
quality_gates: [ollama_installed, models_downloaded, openclaw_configured, gateway_running, agent_responsive]
persona: "⚙️ Pragmatic Application — infrastructure and deployment"
mira_tier: 1
---

## Source Content Chained (20 sources)
1. ollama.ai - Ollama homepage
2-3. openclaw.ai/install.sh/ps1 - Install scripts
4. docs.openclaw.ai - Documentation
5. github.com/openclaw/openclaw - Repository
6. github.com/ollama/ollama - Ollama releases
7. lmstudio.ai - LM Studio
8. jarvis.rhds.dev - Jarvis AI
9-11. Various OpenClaw tools/troubleshooting
12. huggingface.co/unsloth - Unsloth Qwen3 models
13-17. OpenClaw blog, integrations, docs
18-20. Hosting: openclawvps.io, rentamac.io, x.com

## Why Local AI?

### Benefits
- **Privacy**: Data never leaves your machine
- **Cost**: No per-token API costs
- **Speed**: No network latency
- **Offline**: Works without internet
- **Sovereignty**: Full control over infrastructure

## Core Components

### 1. Ollama - Local LLM Runtime
**Website**: ollama.ai

Ollama is a lightweight runtime for running LLMs locally. It provides:
- CLI interface for model management
- HTTP API at http://localhost:11434
- GGUF model support
- Simple model import

#### Installation
```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Verify
ollama --version
```

#### Running Models
```bash
# List available models
ollama list

# Run a model
ollama run llama3

# Via API
curl http://localhost:11434/api/chat -d '{
  "model": "llama3",
  "messages": [{"role": "user", "content": "Hello"}]
}'
```

#### Custom GGUF Models
```bash
# Download GGUF from Hugging Face
huggingface-cli download --local /tmp/model.gguf bartowski/Llama-3.2-1B-Instruct-GGUF

# Create Modelfile
echo "FROM /tmp/model.gguf" > Modelfile

# Import to Ollama
ollama create my-model -f Modelfile

# Run
ollama run my-model
```

### 2. LM Studio - Desktop GUI
**Website**: lmstudio.ai

- User-friendly desktop app
- Model catalog with one-click download
- OpenAI-compatible API
- GGUF model support
- Model benchmarking

### 3. OpenClaw - AI Coding Agent
**Website**: openclaw.ai
**GitHub**: github.com/openclaw/openclaw

OpenClaw is an open-source AI coding agent that runs locally with full data sovereignty.

#### Installation Methods
```bash
# Method 1: One-liner (recommended)
curl -sL https://install.openclaw.ai | bash

# Method 2: npm
npx openclaw@latest

# Method 3: Docker
docker pull openclaw/gateway:latest
docker run -p 18789:18789 openclaw/gateway
```

#### Configuration
```json
// ~/.openclaw/openclaw.json
{
  "provider": "ollama",
  "ollamaEndpoint": "http://localhost:11434",
  "models": {
    "chat": "llama3",
    "quick": "phi3"
  },
  "gateway": {
    "port": 18789,
    "auth": "token"
  }
}
```

#### Self-Hosted Deployment
```bash
# Clone repository
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# Configure environment
cp .env.example .env
# Edit .env with API keys

# Docker Compose
docker-compose up -d

# Access admin panel
# http://localhost:8080 or https://your-domain.com
```

### 4. Jarvis - AI Assistant
**Website**: jarvis.rhds.dev

Lightweight AI assistant with local model support.

### 5. Unsloth - Fine-tuned Models
**Website**: huggingface.co/unsloth

Efficient fine-tuned models in GGUF format:
- Qwen3-Coder-30B-A3B
- Llama3-based coders
- Optimized for local inference

## Architecture Patterns

### Pattern 1: Local Laptop (Dev)
```
┌─────────────┐     ┌──────────┐     ┌─────────┐
│   OpenClaw  │────▶│ Gateway  │────▶│ Ollama  │
│   (Agent)   │     │ :18789   │     │ :11434  │
└─────────────┘     └──────────┘     └─────────┘
```

### Pattern 2: Local LLM with Cloud Fallback
```json
{
  "models": {
    "primary": "claude-3-5-sonnet",
    "fallback": "ollama:qwen2.5:14b"
  }
}
```

### Pattern 3: Self-Hosted Server
```
┌─────────────────────────────────────┐
│           Ubuntu Server              │
│  ┌──────────┐  ┌────────────────┐ │
│  │  Gateway │  │  Docker Agents │ │
│  │  :4222   │  │  (isolated)    │ │
│  └────┬─────┘  └────────────────┘ │
│       │                             │
│       ▼                             │
│  ┌─────────────────────────────┐  │
│  │  Ollama / LM Studio         │  │
│  │  + GPU Acceleration        │  │
│  └─────────────────────────────┘  │
└─────────────────────────────────────┘
```

## Model Selection Guide

| Use Case | Recommended Model | Quantization |
|----------|-------------------|---------------|
| General chat | Llama 3.1 8B | Q4_K_M |
| Coding | Qwen3-Coder-30B | Q4_K_M |
| Fast/light | Phi-3 Mini | Q4_K_M |
| High quality | Llama 3.1 70B | Q5_K_M |
| Long context | Mistral 7B | Q4_0 |

## Quantization Types
- **Q2_K**: Smallest, lowest quality
- **Q4_0**: Good balance
- **Q4_K_M**: Recommended default
- **Q5_K_S**: Higher quality
- **Q5_K_M**: Best quality per size
- **F16**: Full precision (largest)

## Troubleshooting

### OpenClaw Issues
| Issue | Solution |
|-------|----------|
| Gateway not starting | Run `openclaw gateway restart` |
| Model rate limits | Set fallback model in config |
| TCC permissions (macOS) | Complete onboarding checklist |
| Control UI pairing | Scan QR code at /connect |

### Ollama Issues
| Issue | Solution |
|-------|----------|
| Out of memory | Use smaller quantization |
| Slow inference | Use GGUF with GPU acceleration |
| Model not found | Pull with `ollama pull <name>` |

## Hosting Options

### Self-Hosted VPS
- **openclawvps.io** - Dedicated OpenClaw hosting
- **rentamac.io** - Mac-based rental for local models
- **DigitalOcean** - $24-48/mo droplet
- **Vultr** - GPU instances available

### Minimum Requirements
- **Dev/Laptop**: 8GB RAM, any CPU
- **Production**: 16GB RAM, 4+ CPU cores
- **GPU**: NVIDIA with CUDA for acceleration

## Hard Rules

1. **Never expose API keys** in public repos
2. **Always use TLS** in production
3. **Bind gateway to localhost** unless explicit exposure needed
4. **Keep .env secure** - never commit to version control
5. **Regular backups** of workspace and config

## Quality Gates

- [ ] ollama_installed - `ollama --version` works
- [ ] models_downloaded - `ollama list` shows models
- [ ] openclaw_configured - openclaw.json valid
- [ ] gateway_running - Port 18789 responding
- [ ] agent_responsive - Test message returns response

## Quick Start Commands

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Pull a model
ollama pull llama3

# 3. Install OpenClaw
curl -sL https://install.openclaw.ai | bash

# 4. Configure (point to local Ollama)
openclaw config edit
# Set provider: "ollama"

# 5. Start gateway
openclaw gateway start

# 6. Test
openclaw chat "Hello!"
```

## References
- ollama.ai
- docs.openclaw.ai
- lmstudio.ai
- github.com/openclaw/openclaw
- huggingface.co/unsloth

---
*Generated: 2026-03-14*
*Chained from 20+ sources*
*Local AI Stack Skill*
