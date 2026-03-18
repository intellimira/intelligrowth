# Skill Registry

> Master index of all MIRA skills with protocol/Weave tags
> **Last Updated:** 2026-03-18

---

## Registry Format

Each skill is tagged with:
- **.MIRA Protocol:** Which core protocol it relates to
- **Tier:** 1 (Foundation), 2 (Progressive), 3 (Production)
- **Status:** VAULTED, ACTIVE, STUB

---

## NEW: Foundation Skills - Session & Recovery

| Skill | .MIRA Protocol | Status | Description |
|-------|----------------|--------|-------------|
| `mira-oj` | UTO | ACTIVE | Sovereign AI agent with Weave learning + Library Orchestrator |
| `openjarvis` | UTO | ACTIVE | Stanford OpenJarvis local-first inference |
| `session-guardian` | Telemetry | ACTIVE | Auto-save, crash recovery, decision logging |
| `open-notebook` | The Weave | ACTIVE | Open Notebook LM integration for semantic search |
| `mira-secure-vault` | Security | ACTIVE | Military-grade secrets management (GPG 4096-bit RSA) |

---

## Tier 3: Production Skills

| Skill | .MIRA Protocol | Status | Description |
|-------|----------------|--------|-------------|
| `skills_md_maker` | MSIP | ACTIVE | Vibe graphing - creates new skills |
| `active_recall` | The Weave | ACTIVE | Memory/Context surface |
| `sovereign_shadow_operator` | Growth Loop | VAULTED | Autonomous monetization |
| `shadow_ops_prover` | Growth Loop | ACTIVE | 7-stage monetization pipeline |
| `pain_scorer` | Telemetry | ACTIVE | Dual-layer scoring (PIS + PAINFUL) |
| `srank_pack_generator` | Telemetry | ACTIVE | Business pack + revenue model |
| `revenue-tracker` | Telemetry | ACTIVE | SQLite P&L tracking |
| `client-delivery` | UTO | ACTIVE | NotebookLM/Docs packages |

---

## Tier 2: Progressive Disclosure

| Skill | .MIRA Protocol | Status | Description |
|-------|----------------|--------|-------------|
| `opencode-builder` | MSIP | ACTIVE | MVP manifest via OpenCode |
| `notebook_bridge` | The Weave | ACTIVE | Google NotebookLM integration |
| `context_compactor` | The Weave | ACTIVE | Mass semantic summarization |
| `topic_sealer` | The Weave | ACTIVE | Consolidates reasoning |
| `base-worker` | UTO | ACTIVE | Data extraction fallback |
| `arch-synthesiser` | MSIP | ACTIVE | Zero-capital MVP architecture |
| `awesome-opencode-curator` | MSIP | ACTIVE | Plugin/theme curation |
| `ai-website-builder` | MSIP | ACTIVE | AI website from tutorials |
| `saas-shadow-pro` | Growth Loop | ACTIVE | SaaS pain point solver |

---

## Tier 1: Foundation Skills

| Skill | .MIRA Protocol | Status | Description |
|-------|----------------|--------|-------------|
| `mesh_brancher` | The Weave | ACTIVE | Non-linear reasoning history |
| `topic_sealer` | The Weave | ACTIVE | Zettel consolidation |
| `cabal_commander` | Growth Loop | ACTIVE | Multi-node orchestration |
| `cabal_spawner` | Growth Loop | ACTIVE | Parallel sub-node spawner |
| `stream_monitor` | Telemetry | ACTIVE | Reasoning stream validation |
| `self-anneal-watchdog` | Telemetry | ACTIVE | Lineage regression monitor |

---

## Updated: The Library System

| Skill | .MIRA Protocol | Status | Description |
|-------|----------------|--------|-------------|
| `library-orchestrator` | The Weave | ACTIVE | The Library skill distribution via MIRA-OJ |
| `library_manager` | Telemetry | ACTIVE | Python module for catalog operations |

---

## STUB Skills (Implemented as Needed)

| Skill | .MIRA Protocol | Status | Description |
|-------|----------------|--------|-------------|
| `knowledge-base` | The Weave | STUB | Knowledge base (see skill_registry.md) |
| `ACCT_Dashboard` | Telemetry | STUB | Dashboard (placeholder) |
| `shadow_monetizer` | Growth Loop | DEPRECATED | Use `shadow_ops_prover` |
| `Vector_Mesh` | The Weave | STUB | Vector storage (placeholder) |
| `Project_Affiliate_Synapse` | Growth Loop | STUB | Affiliate (placeholder) |
| `Consensus_Engine` | Persona Council | STUB | Consensus (placeholder) |
| `lab-utility` | UTO | STUB | Lab utility (placeholder) |

---

## Quest_OpenClaw Skills (External)

Located in `/skills/knowledge-base/references/acct_core/Laboratory/Quest_OpenClaw/`:

| Category | Skills |
|----------|--------|
| **Productivity** | apple-notes, apple-reminders, things-mac, bear-notes, obsidian |
| **Communication** | himalaya, slack, discord, imsg, bluebubbles, wacli |
| **Media** | spotify-player, songsee, openai-whisper, sherpa-onnx-tts, sag |
| **Data** | notion, gog, github, trello, blogwatcher |
| **Dev Tools** | coding-agent, gh-issues, mcporter, tmux, healthcheck |
| **Vision** | camsnap, video-frames, gifgrep, openai-image-gen, nano-banana-pro |
| **Home** | sonoscli, blucli, openhue, eightctl |
| **Location** | goplaces, weather |
| **Utility** | summarize, oracle, gemini, session-logs, xurl |

---

## Protocol → Skill Lookup

### UTO (Unified Task Orchestration)
- `mira-oj` (primary - sovereign AI)
- `openjarvis` (inference engine)
- `session-guardian` (recovery)
- `base-worker` (fallback)

### MSIP (Master Skill Integration)
- `skills_md_maker`
- `opencode-builder`
- `arch-synthesiser`
- `awesome-opencode-curator`
- `ai-website-builder`

### The Weave
- `open-notebook` (NEW - Open Notebook LM)
- `active_recall` (primary)
- `notebook_bridge`
- `context_compactor`
- `topic_sealer`
- `mesh_brancher`

### Growth Loop
- `sovereign_shadow_operator` (primary)
- `shadow_ops_prover`
- `saas-shadow-pro`
- `cabal_commander`
- `cabal_spawner`

### Telemetry
- `session-guardian` (NEW - auto-save/recovery)
- `pain_scorer` (primary)
- `srank-pack-generator`
- `revenue-tracker`
- `stream_monitor`
- `self-anneal-watchdog`

### Persona Council
- `skills_md_maker` (uses in workflow)
- `Consensus_Engine` (stub)

---

## The Library System

The Library provides skill distribution and catalog management:

| Component | Location | Description |
|-----------|----------|-------------|
| `library.yaml` | `~/.claude/skills/library/` | 44 skills cataloged |
| `library_manager.py` | `.mira/` | Python orchestration module |
| `session_guardian.py` | `.mira/` | Crash recovery + auto-save |

---

## External Skills (Quest_OpenClaw)

Located in `/skills/knowledge-base/references/acct_core/Laboratory/Quest_OpenClaw/`:

---

## Usage

### Find skills by protocol:
```bash
# Manual lookup via this registry
grep -i "The Weave" .MIRA/skill_registry.md
```

### Find active vs stub:
```bash
grep "ACTIVE" .MIRA/skill_registry.md
grep "STUB" .MIRA/skill_registry.md
```

---

*Last updated: 2026-03-15*
*Auto-generated from /skills/ directory scan*
