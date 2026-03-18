# MIRA Integration Guide

## Overview

The awesome-opencode-curator skill is designed to be used by other MIRA skills autonomously. This guide explains how other skills can leverage it.

## Architecture

```
┌─────────────────────────────────────────┐
│           MIRA Core                      │
├─────────────────────────────────────────┤
│  skills_md_maker                         │
│  sovereign_shadow_operator               │
│  opencode-builder                        │
│         ↓                                │
│  awesome-opencode-curator               │
│         ↓                                │
│  /projects/awesome-opencode/             │
│  (67+ indexed plugins)                  │
└─────────────────────────────────────────┘
```

## Integration Points

### 1. skills_md_maker

**Use Case:** Training data for skill patterns

When creating new skills, MIRA can reference awesome-opencode-curator to:
- Understand common skill patterns
- Find examples of similar skills
- Identify available tools for skill functionality

**How it works:**
```bash
# In skills_md_maker workflow
python3 /home/sir-v/MiRA/skills/awesome-opencode-curator/scripts/core.py memory
```

---

### 2. sovereign_shadow_operator (Shadow Ops)

**Use Case:** Pain mining & solution building

Shadow Ops can use this to:
- Find tool/plugin pain points (what frustrates users)
- Discover available solutions (existing plugins)
- Build solution packages for clients

**Workflow:**
```
User Pain: "I lose context when sessions end"
    ↓
Search awesome-opencode: "memory persistence"
    ↓
Find: opencode-mem, agent-memory, simple-memory
    ↓
Recommend: Solution package with memory plugin
```

---

### 3. opencode-builder

**Use Case:** MVP plugin selection

When building MVPs, query available plugins:
```bash
# Find relevant plugins for MVP
python3 scripts/core.py database
python3 scripts/core.py auth
python3 scripts/core.py api
```

---

## Using from Another Skill

### Method 1: Subprocess (Recommended)

```python
import subprocess
import json

def search_awesome_opencode(keyword: str, category: str = None):
    """Search awesome-opencode from another skill."""
    cmd = ["python3", "scripts/core.py", keyword]
    if category:
        cmd.append(category)
    
    result = subprocess.run(
        cmd,
        cwd="/home/sir-v/MiRA/skills/awesome-opencode-curator",
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        return json.loads(result.stdout)
    return []
```

### Method 2: Direct File Access

```python
import yaml
from pathlib import Path

def get_plugin(plugin_name: str):
    """Read plugin directly from YAML."""
    path = Path("/home/sir-v/MiRA/projects/awesome-opencode/data/plugins")
    
    for yaml_file in (path).glob("*.yaml"):
        if yaml_file.stem == plugin_name:
            with open(yaml_file) as f:
                return yaml.safe_load(f)
    return None
```

### Method 3: Vector Index

```python
import json

def search_index(keyword: str):
    """Search using pre-built index."""
    with open("/home/sir-v/MiRA/skills/awesome-opencode-curator/vectordb/index.json") as f:
        index = json.load(f)
    
    results = []
    for plugin in index.get("plugins", []):
        if keyword.lower() in json.dumps(plugin).lower():
            results.append(plugin)
    return results
```

---

## Adding as a Skill Dependency

### In Your Skill's SKILL.md

```yaml
---
name: my-awesome-skill
description: A skill that uses awesome-opencode
dependencies:
  - awesome-opencode-curator
---
```

### In References

```yaml
references:
  - type: skill
    name: awesome-opencode-curator
    purpose: Plugin discovery
```

---

## Auto-Discovery Pattern

Other skills can implement auto-discovery:

```python
def discover_relevant_plugins(need: str):
    """Auto-discover plugins matching a need."""
    keywords = {
        "memory": ["memory", "context", "persist"],
        "auth": ["auth", "oauth", "login"],
        "background": ["background", "async", "worker"],
    }
    
    for key, terms in keywords.items():
        for term in terms:
            if term in need.lower():
                return search_awesome_opencode(term)
    
    return []
```

---

## Updating the Index

When awesome-opencode data changes, rebuild the index:

```bash
# Pull latest
cd /home/sir-v/MiRA/projects/awesome-opencode
git pull origin main

# Rebuild index
cd /home/sir-v/MiRA/skills/awesome-opencode-curator
python3 scripts/build_index.py
```

---

## File Paths Reference

| Purpose | Path |
|---------|------|
| Raw Data | `/home/sir-v/MiRA/projects/awesome-opencode/` |
| Plugins | `/home/sir-v/MiRA/projects/awesome-opencode/data/plugins/` |
| Skill Script | `/home/sir-v/MiRA/skills/awesome-opencode-curator/scripts/core.py` |
| Vector Index | `/home/sir-v/MiRA/skills/awesome-opencode-curator/vectordb/index.json` |

---

## Troubleshooting

### Plugin not found
- Check plugin name: `python3 scripts/core.py list plugins`
- Rebuild index: `python3 scripts/build_index.py`

### Outdated data
- Update: `python3 scripts/core.py update`
- Rebuild index: `python3 scripts/build_index.py`

### Integration not working
- Verify paths are correct
- Check Python dependencies (pyyaml)
- Test CLI directly first
