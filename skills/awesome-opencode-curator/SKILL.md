---
name: awesome-opencode-curator
description: Curated access to awesome-opencode plugins, themes, agents, and resources for OpenCode. Use when building MVPs, finding plugins, or researching OpenCode capabilities.
---

# Awesome Opencode Curator

Autonomous access to the curated collection of OpenCode plugins, themes, agents, and resources.

## Trigger Phrases
- "Find OpenCode plugins for..."
- "What OpenCode resources exist for..."
- "Search awesome-opencode for..."
- "OpenCode capabilities for..."
- "Get OpenCode theme recommendations"

## Data Source
- **Location:** `/home/sir-v/MiRA/projects/awesome-opencode/`
- **Categories:** Official, Plugins, Themes, Agents, Projects, Resources

## Core Workflow

### 1. Category Lookup
```bash
# List available categories
ls /home/sir-v/MiRA/projects/awesome-opencode/data/
```

### 2. Plugin Search
```bash
# Search plugins by keyword
grep -ri "keyword" /home/sir-v/MiRA/projects/awesome-opencode/data/plugins/

# Find by category (auth, memory, background, etc.)
ls /home/sir-v/MiRA/projects/awesome-opencode/data/plugins/
```

### 3. Get Plugin Details
- Read from `data/plugins/` for plugin descriptions
- Extract GitHub URLs from README.md
- Check `data/schema.json` for structured data

### 4. Integration with MIRA Skills
- **skills_md_maker**: Reference for skill structure patterns
- **shadow-ops**: Pain mining for tool frustrations
- **opencode-builder**: Query available plugins for builds

## Usage

### Find Specific Plugin Type
```bash
# Find memory-related plugins
grep -l "memory" /home/sir-v/MiRA/projects/awesome-opencode/data/plugins/*.md

# Find auth plugins
grep -l "auth" /home/sir-v/MiRA/projects/awesome-opencode/data/plugins/*.md
```

### Update Sync
```bash
cd /home/sir-v/MiRA/projects/awesome-opencode && git pull origin main
```

## Available Categories

| Category | Description |
|----------|-------------|
| Official | Core OpenCode repositories (SDKs, CLI) |
| Plugins | 50+ community plugins |
| Themes | UI themes |
| Agents | Autonomous agents |
| Projects | Example projects |
| Resources | Learning resources |

## Integration Points

### For skills_md_maker
- Training data: "what makes a good skill"
- Pattern reference for SKILL.md structure

### For shadow-ops
- Pain mining source for tool frustrations
- Solution building: available plugins reference

### For opencode-builder
- Query available plugins during MVP build

---
**Status:** ACTIVE (v1.0)
**Tier:** 2-Tier Progressive Disclosure
**Related:** [[skills_md_maker]], [[sovereign_shadow_operator]], [[opencode-builder]]
