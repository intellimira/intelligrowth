# CLI Commands Reference

## Core Script: `core.py`

Location: `/home/sir-v/MiRA/skills/awesome-opencode-curator/scripts/core.py`

### Usage

```bash
python3 scripts/core.py <command> [arguments]
```

## Commands

### 1. `list` - List Categories or Items

List all available categories:
```bash
python3 scripts/core.py list
```

List items in a specific category:
```bash
python3 scripts/core.py list plugins
python3 scripts/core.py list themes
python3 scripts/core.py list agents
python3 scripts/core.py list projects
python3 scripts/core.py list resources
python3 scripts/core.py list official
```

**Output format:**
```json
{
  "categories": ["official", "plugins", "themes", "agents", "projects", "resources"]
}
```
or
```json
{
  "category": "plugins",
  "items": ["openai-codex-auth", "openskills", "agent-memory", ...]
}
```

---

### 2. Search - Find Plugins by Keyword

Search across all categories:
```bash
python3 scripts/core.py memory
python3 scripts/core.py auth
python3 scripts/core.py background
```

Search in specific category:
```bash
python3 scripts/core.py memory plugins
python3 scripts/core.py auth plugins
```

**Output format:**
```json
[
  {
    "file": "data/plugins/opencode-mem.yaml",
    "id": "opencode-mem",
    "data": {
      "name": "Opencode Mem",
      "repo": "https://github.com/tickernelz/opencode-mem",
      "tagline": "Persistent memory with vector database",
      "description": "A persistent memory system..."
    }
  }
]
```

---

### 3. `update` - Pull Latest Data

Update from GitHub:
```bash
python3 scripts/core.py update
```

**Output format:**
```json
{
  "success": true,
  "output": "Already up to date."
}
```
or
```json
{
  "success": true,
  "output": "Updating...\n..."
}
```

---

## Index Builder: `build_index.py`

Location: `/home/sir-v/MiRA/skills/awesome-opencode-curator/scripts/build_index.py`

### Rebuild Vector Index

```bash
python3 scripts/build_index.py
```

**Output:**
```
Index built: 67 plugins indexed across 6 categories
```

This rebuilds the `vectordb/index.json` file from the YAML data.

---

## Direct File Access

### Read Plugin YAML Directly

```bash
# List all plugins
ls /home/sir-v/MiRA/projects/awesome-opencode/data/plugins/

# Read specific plugin
cat /home/sir-v/MiRA/projects/awesome-opencode/data/plugins/agent-memory.yaml
```

### Read Category

```bash
# Count plugins in category
ls /home/sir-v/MiRA/projects/awesome-opencode/data/plugins/ | wc -l
```

### Search README

```bash
# Search in README
grep -i "memory" /home/sir-v/MiRA/projects/awesome-opencode/README.md
```

---

## Script Arguments Summary

| Command | Args | Description |
|---------|------|-------------|
| `list` | `[category]` | List categories or items |
| `update` | - | Pull latest from git |
| `<keyword>` | `[category]` | Search by keyword |

---

## Troubleshooting

### No results found
- Try a broader keyword
- Check spelling
- Use `list plugins` to see all available

### Import errors
```bash
pip install pyyaml
```

### Permission errors
```bash
chmod +x scripts/core.py
```
