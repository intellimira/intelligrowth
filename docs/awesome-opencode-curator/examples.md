# Usage Examples

## Finding Specific Plugins

### Memory & Context

```bash
python3 scripts/core.py memory
```

**Results:**
- `opencode-mem` - Persistent memory with vector database
- `agent-memory` - Letta-inspired memory
- `simple-memory` - Git-based memory

### Authentication

```bash
python3 scripts/core.py auth
```

**Results:**
- `antigravity-auth` - Google Antigravity models
- `antigravity-multi-auth` - Multiple Google accounts
- `gemini-auth` - Google account auth
- `openai-codex-auth` - ChatGPT Plus/Pro OAuth
- `kilo-auth` - Kilo Gateway provider
- `openhax-codex` - OAuth authentication
- `omnisync-auth` - Omniroute authentication

### Background Tasks

```bash
python3 scripts/core.py background
```

**Results:**
- `background` - Background process management
- `background-agents` - Async agent delegation
- `oh-my-opencode` - Background agents

### Notifications

```bash
python3 scripts/core.py notify
```

**Results:**
- `opencode-notify` - Native OS notifications
- `opencode-ntfy.sh` - Push notifications
- `smart-voice-notify` - Voice notifications

### Productivity

```bash
python3 scripts/core.py productivity
```

### Tool Enhancement

```bash
python3 scripts/core.py tool
```

---

## Use Cases

### 1. Building a New Skill

You want to add memory to your skill:
```
Find OpenCode plugins for memory management
```

Result: Use `agent-memory` or `opencode-mem`

### 2. Solving Pain Points

Users complain about losing context:
```
Search awesome-opencode for context persistence
```

### 3. Finding Integrations

You need GitHub integration:
```
python3 scripts/core.py github
```

### 4. Theme Customization

You want a dark theme:
```
python3 scripts/core.py list themes
```

---

## Real-World Scenarios

### Scenario A: MVP Development

**Context:** Building a SaaS MVP, need background processing

```bash
# Find relevant plugins
python3 scripts/core.py background
python3 scripts/core.py queue
python3 scripts/core.py worker
```

**Decision:** Use `background` or `background-agents` plugin

---

### Scenario B: Multi-Agent Setup

**Context:** Need multiple agents to collaborate

```bash
# Find agent-related plugins
python3 scripts/core.py agent
```

**Result:** Explore multi-agent orchestration plugins

---

### Scenario C: Development Environment

**Context:** Need devcontainers integration

```bash
python3 scripts/core.py devcontainer
```

**Result:** `devcontainers` - Multi-branch devcontainers

---

### Scenario D: Performance Optimization

**Context:** Need faster code editing

```bash
python3 scripts/core.py fast-apply
python3 scripts/core.py morph
```

**Result:** `morph-fast-apply` - 10,500+ tokens/sec code editing

---

## Advanced Queries

### Combining Searches

Search for plugins that match multiple criteria by running multiple queries:

```bash
# Find memory + notifications
python3 scripts/core.py memory
python3 scripts/core.py notify
```

### Category Filtering

Search within specific category:

```bash
python3 scripts/core.py memory plugins
python3 scripts/core.py auth themes
```

### Plugin Discovery Workflow

1. **List categories:** `python3 scripts/core.py list`
2. **Browse category:** `python3 scripts/core.py list plugins`
3. **Search keyword:** `python3 scripts/core.py <keyword>`
4. **Get details:** `cat data/plugins/<plugin-name>.yaml`
5. **Visit repo:** Extract URL from YAML, open in browser

---

## Integration with MIRA

### From OpenCode

Simply trigger the skill:

```
Find OpenCode plugins for memory management
```

MIRA will:
1. Load the awesome-opencode-curator skill
2. Search the indexed plugins
3. Return relevant results with descriptions and links

### From Another Skill

```python
# In another skill's code
import subprocess
result = subprocess.run(
    ["python3", "scripts/core.py", "memory"],
    cwd="/home/sir-v/MiRA/skills/awesome-opencode-curator",
    capture_output=True,
    text=True
)
plugins = json.loads(result.stdout)
```

---

## Extracting GitHub URLs

Each plugin YAML contains a `repo` field:

```yaml
name: Agent Memory
repo: https://github.com/joshuadavidthomas/opencode-agent-memory
tagline: Letta-inspired memory
description: Gives the agent persistent...
```

To clone a plugin:
```bash
git clone https://github.com/joshuadavidthomas/opencode-agent-memory
```
