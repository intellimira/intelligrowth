# Awesome Opencode Curator

Autonomous access to the curated collection of OpenCode plugins, themes, agents, and resources.

## Overview

This skill provides MIRA with comprehensive access to the awesome-opencode ecosystem - a curated list of 67+ community plugins, themes, agents, and resources for OpenCode (the AI coding agent by Anomaly).

## Quick Links

- **Data Source:** `/home/sir-v/MiRA/projects/awesome-opencode/`
- **Skill Location:** `/home/sir-v/MiRA/skills/awesome-opencode-curator/`
- **Vector Index:** 67 plugins indexed across 6 categories

## What It Provides

| Category | Count | Examples |
|----------|-------|----------|
| Plugins | 67+ | agent-memory, background, auth |
| Themes | ~ | UI customizations |
| Agents | ~ | Autonomous agents |
| Projects | ~ | Example projects |
| Resources | ~ | Learning materials |
| Official | 4 | SDKs, CLI |

## Trigger Phrases

- "Find OpenCode plugins for..."
- "What OpenCode resources exist for..."
- "Search awesome-opencode for..."
- "OpenCode capabilities for..."
- "Get OpenCode theme recommendations"

## Usage Methods

### 1. Via OpenCode (Trigger Phrases)
Simply mention one of the trigger phrases in your conversation.

### 2. Via CLI Scripts
```bash
cd /home/sir-v/MiRA/skills/awesome-opencode-curator

# List categories
python3 scripts/core.py list

# List plugins in category
python3 scripts/core.py list plugins

# Search for plugins
python3 scripts/core.py memory
python3 scripts/core.py auth
python3 scripts/core.py background

# Search in specific category
python3 scripts/core.py memory plugins
```

### 3. Via Vector Index
```bash
# Rebuild index (after updating data)
python3 scripts/build_index.py

# Read indexed data
cat vectordb/index.json | jq '.plugins | length'
```

## Integration Points

This skill is designed to be used autonomously by other MIRA skills:

- **skills_md_maker**: Training data for skill patterns
- **shadow-ops**: Pain mining source for tool frustrations
- **opencode-builder**: Query available plugins during MVP builds

## Updating Data

```bash
cd /home/sir-v/MiRA/projects/awesome-opencode
git pull origin main

# Rebuild index
cd /home/sir-v/MiRA/skills/awesome-opencode-curator
python3 scripts/build_index.py
```

## File Structure

```
awesome-opencode-curator/
├── SKILL.md              # Skill definition
├── manifest.json         # Skill metadata
├── scripts/
│   ├── core.py          # Search CLI
│   └── build_index.py   # Index builder
├── references/          # Symlink to data
└── vectordb/
    └── index.json       # Plugin index
```

---
**Status:** ACTIVE | **Version:** 1.0 | **Last Updated:** 2026-03-15
