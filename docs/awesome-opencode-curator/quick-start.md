# Quick Start Guide

## Setup (Already Complete)

The skill is already installed. Just start using it!

## Your First Search

### Option 1: Natural Language (in OpenCode)

Just say what you need:

```
Find OpenCode plugins for memory management
```

```
What auth plugins exist for OpenCode?
```

```
Search awesome-opencode for background task handling
```

### Option 2: CLI (Terminal)

```bash
cd /home/sir-v/MiRA/skills/awesome-opencode-curator
python3 scripts/core.py memory
```

**Expected output:**
```json
[
  {
    "file": "data/plugins/opencode-mem.yaml",
    "id": "opencode-mem",
    "data": {
      "name": "Opencode Mem",
      "repo": "https://github.com/tickernelz/opencode-mem",
      "tagline": "Persistent memory with vector database",
      "description": "A persistent memory system for AI coding agents..."
    }
  },
  {
    "file": "data/plugins/agent-memory.yaml",
    "id": "agent-memory",
    "data": {...}
  }
]
```

## Common Searches

| Need | Command |
|------|---------|
| Memory plugins | `python3 scripts/core.py memory` |
| Authentication | `python3 scripts/core.py auth` |
| Background tasks | `python3 scripts/core.py background` |
| Notifications | `python3 scripts/core.py notify` |
| Productivity | `python3 scripts/core.py productivity` |

## List Available Categories

```bash
python3 scripts/core.py list
```

**Output:**
```json
{
  "categories": ["official", "plugins", "themes", "agents", "projects", "resources"]
}
```

## List Items in Category

```bash
python3 scripts/core.py list plugins
```

## Get Plugin Details

Each plugin is stored as YAML in:
```
/home/sir-v/MiRA/projects/awesome-opencode/data/plugins/<plugin-name>.yaml
```

Example:
```bash
cat /home/sir-v/MiRA/projects/awesome-opencode/data/plugins/agent-memory.yaml
```

**Output:**
```yaml
name: Agent Memory
repo: https://github.com/joshuadavidthomas/opencode-agent-memory
tagline: Letta-inspired memory
description: Gives the agent persistent, self-editable memory blocks inspired by Letta agents.
```

## Next Steps

- See [commands.md](commands.md) for full CLI reference
- See [examples.md](examples.md) for more use cases
- See [integration.md](integration.md) for MIRA integration details
