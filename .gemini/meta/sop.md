# MAS-Master: MIRA
### Unified Multi-Agent Orchestration SOP · v4.0
**Stack:** MASFactory · MassGen · PathRAG · MIRA (Tiered)  
**Projects:** antigravity · opencode · Gemini CLI  
**Source:** arXiv:2603.06007 · BUPT-GAMMA/MASFactory · BUPT-GAMMA/PathRAG

---

## Quick Reference

| Need | Go to |
|---|---|
| Start a new task | [§3 — Workspace Init](#3-workspace-initialisation) |
| Compile intent → graph | [§5 — Vibe Graphing Pipeline](#5-vibe-graphing-pipeline) |
| Run the graph | [§6 — Execution Wrapper](#6-standard-execution-wrapper) |
| Add an agent capability | [§4 — Skill Folder Anatomy](#4-skill-folder-anatomy) |
| Decide on ChromaDB | [§7 — MIRA Tiers](#7-mira-control-plane--tiered) |
| Debug a failure | [§8 — Observability](#8-observability--debugging) |
| Understand the full stack | [§1 — Architecture](#1-architecture-overview) |

---

## 1. Architecture Overview

The Weave separates into two planes that must never be conflated.

```
┌─────────────────────────────────────────────────────────────┐
│  DATA PLANE  ·  what agents DO                              │
│                                                             │
│  MASFactory ──► MassGen (scale-out) ──► PathRAG (retrieval) │
│  Compiles intent → IR → executable directed graph           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  MIRA CONTROL PLANE  ·  what agents are PERMITTED to do,    │
│  what they ARE doing, how GOOD their outputs are            │
│                                                             │
│  Tier 1 (always-on, no ChromaDB)                           │
│    GovernanceEngine · ScoringService Lite · Lineage Chain   │
│                                                             │
│  Tier 2 (full observability, requires ChromaDB)             │
│    WorkflowMonitoringAgent · ScoringService Full            │
└─────────────────────────────────────────────────────────────┘
```

**Critical path rule:** All MIRA interactions with the runtime are **async and off the critical path**. The only synchronous MIRA call is the GovernanceEngine policy check at the end of Stage 3 — it fires once at compile time, never at runtime.

### 1.1 Component Index

| Component | Repo / Source | Plane | ChromaDB? |
|---|---|---|---|
| MASFactory | [BUPT-GAMMA/MASFactory](https://github.com/BUPT-GAMMA/MASFactory) | Data | No |
| MassGen | [massgen/MassGen](https://github.com/massgen/MassGen) | Data | No |
| PathRAG | [BUPT-GAMMA/PathRAG](https://github.com/BUPT-GAMMA/PathRAG) | Data | No |
| AgentXRay | [arXiv:2602.05353](https://arxiv.org/abs/2602.05353) | Diagnostics | No |
| MIRA · GovernanceEngine | MIRA-TitanOS/governance | Control · T1 | **No** |
| MIRA · ScoringService Lite | MIRA-TitanOS/scoring | Control · T1 | **No** |
| MIRA · Lineage Chain | MIRA-TitanOS/scoring | Control · T1 | **No** |
| MIRA · WorkflowMonitoringAgent | MIRA-TitanOS/monitoring | Control · T2 | **Yes** |
| MIRA · ScoringService Full | MIRA-TitanOS/scoring | Control · T2 | **Yes** |

### 1.2 ChromaDB Decision

Answer these questions before initialising any new project:

1. **Do you need dependency-aware failure tracing?** (DEPENDS_ON / CALLS graph traversal) → Yes = Tier 2
2. **Do you need the full 3-dimension DM score** including retrieval confidence from PathRAG? → Yes = Tier 2
3. **Are you in a constrained environment** (edge, CI, serverless)? → Yes = Tier 1 only
4. **Will outputs be consumed without human review?** → Yes = strongly consider Tier 2

If none of questions 1–2 apply: **use Tier 1. No ChromaDB required.**  
Upgrade path: change `tier=1` to `tier=2` in `mas_run.py`. No directory or schema changes needed.

---

## 2. The Vibe Gap

**The problem:** The distance between a high-level project goal expressed in natural language and a correctly wired, executable multi-agent system.

**The solution:** Vibe Graphing — a 3-stage, human-in-the-loop compilation pipeline that converts a `.gemini` intent file into a version-controlled JSON blueprint (`graph_design.json`), which MASFactory then compiles into an executable directed computation graph.

**The efficiency gain:** Traditional manual orchestration (e.g. ChatDev) requires 1,500+ lines of code. The Weave reduces this to a ~45-line Python wrapper. The complexity moves into well-authored Skill Folders, not glue code.

---

## 3. Workspace Initialisation

Every project using The Weave must be initialised with this directory structure. **Automatic Context Discovery** depends on every path being present.

```
/project-root/
├── .gemini/                    # Intent files  ·  Data plane
│   └── <feature>_intent.gemini
├── .brain/                     # IR cache  ·  Data plane
│   ├── graph_design.json       # ← version-control this
│   └── outputs/
├── skills/                     # Skill Folder library  ·  Data + Control
│   └── <skill-name>/           # kebab-case
│       ├── SKILL.md            # required
│       ├── policy.json         # required  ·  MIRA governance
│       ├── scripts/            # required  ·  CodeAct tools
│       ├── references/         # recommended  ·  PathRAG index source
│       ├── assets/             # optional  ·  output templates
│       └── SUBAGENT.md         # optional  ·  MassGen voting agents
│           └── vectordb/       # optional  ·  local ChromaDB store
│               └── chroma.sqlite3
├── .mira/                      # MIRA control plane
│   ├── policies/
│   │   └── agent_tool_policy.json
│   └── scores/
│       └── lineage.json
├── CLAUDE.md                   # Global conventions  ·  injected into every agent
└── AGENTS.md                   # Cross-agent coordination protocols
```

> **Vector store placement:** If a Skill Folder requires a local ChromaDB (Tier 2 or PathRAG indexing of `/references/`), the store lives at `skills/<skill-name>/vectordb/`. This keeps the vector data co-located with the knowledge it indexes, avoids a shared singleton, and means the folder is self-contained — zip it up and it works anywhere.

### 3.1 Init Checklist (Agentic Instantiation)

When the Gemini CLI (The Architect) is deployed to a new environment lacking this scaffolding, it MUST proactively execute this checklist via terminal commands before proceeding with orchestration.

```bash
# 1. Create directory structure
mkdir -p .gemini .brain/outputs .mira/policies .mira/scores

# 2. Create at least one Skill Folder template
mkdir -p skills/base-worker/{scripts,references,assets,vectordb}

# 3. Seed global context files
touch CLAUDE.md AGENTS.md

# 4. Write your first intent file stub
echo "I want to..." > .gemini/first_intent.gemini

# 5. If Tier 2: verify ChromaDB is accessible
python3 -c "import chromadb; print('ChromaDB ready')"

# 6. If PathRAG: index references
# pathrag index --source skills/*/references/ --store skills/*/vectordb/
```

### 3.2 CLAUDE.md Seed Template

```markdown
# Project: <name>
## Stack
- Language: Python 3.11+
- Primary framework: MASFactory
- Invoke model: opencode:ollama  (worker - fast, free, local)
- Build model:  claude-sonnet-4-6 or gemini-2.5-pro (architect - high intelligence)
- MIRA tier: 1  (upgrade to 2 when dependency tracing needed)

## Conventions
- All outputs to .brain/outputs/
- All logs to .mira/scores/
- Kebab-case for all file and folder names
- JSON for machine-to-machine message adapters
- Markdown for human-readable intermediate artefacts
```

---

## 4. Skill Folder Anatomy

Every agent capability is a self-contained **Skill Folder** inside `/skills/`. The Build Model scans SKILL.md metadata during Stage 1 without loading full content — only Stage 3 hydrates the full instructions.

### 4.1 File Reference

| File / Dir | Status | MIRA | Purpose |
|---|---|---|---|
| `SKILL.md` | **Required** | Both tiers | Agent brain. YAML frontmatter scanned at Stage 1. Full instructions loaded at Stage 3 only. |
| `policy.json` | **Required** | Both tiers | MIRA governance declaration. Defines `allowed_tools` and `deny_tools`. Merged into `.mira/policies/agent_tool_policy.json` at workspace init. |
| `scripts/` | **Required** | — | Python / Bash tools. Directly invocable by the agent as function calls (CodeAct paradigm). |
| `references/` | Recommended | T2 | Documentation indexed by PathRAG. Source for `relevance_distance` dimension. |
| `assets/` | Optional | — | Static output templates. Standardises Answer Agent deliverable format. |
| `SUBAGENT.md` | Optional | — | Defines parallel sub-agents for MassGen Collective Validation voting. Same schema as SKILL.md. |
| `vectordb/` | Conditional | T2 | Local ChromaDB store for this skill's PathRAG index. Required only if Tier 2 and skill has `/references/`. |

### 4.2 Canonical SKILL.md

```yaml
---
name:           web-researcher
description:    Searches the web, retrieves pages, extracts structured facts.
triggers:       [research, search, find information, look up]
tools:          [web_search, web_fetch, extract_json]
quality_gates:  [completeness, source_count_min_3]
---

# Full agent instructions follow here.
# Stage 3 reads everything below the frontmatter.
# Keep the frontmatter tight — the Build Model scans thousands of these.
```

### 4.3 Canonical policy.json

```json
{
  "web-researcher": {
    "allowed_tools": ["web_search", "web_fetch", "extract_json"],
    "deny_tools":    ["delete_file", "send_email", "write_file"]
  },
  "default": {
    "allowed_tools": ["read_log_file"],
    "deny_tools":    ["delete_file", "send_email"]
  }
}
```

**Policy resolution order:**
1. Check agent-specific entry by agent ID
2. `deny_tools` match → **DENY** (overrides everything)
3. `allowed_tools` match → **ALLOW**
4. Fall back to `default` entry, repeat 2–3
5. Not specified anywhere → **DENY** (fail-closed)

> **Rule:** The `tools` list in `SKILL.md` and `allowed_tools` in `policy.json` must be identical. If an agent needs a new tool, update `policy.json` first. New tools are denied until explicitly permitted.

### 4.4 Single Responsibility Rule

Each Skill Folder does exactly one thing well. Composition of primitives is the Build Model's job — not the skill author's. A well-authored `SKILL.md` eliminates an entire class of prompt engineering at runtime. A well-authored `policy.json` eliminates a class of governance failures in production.

---

## 5. Vibe Graphing Pipeline

The Build Model (architect — high intelligence, e.g. claude-sonnet) executes this pipeline. The Invoke Model (worker — fast, cheap, e.g. claude-haiku) runs the resulting graph. **Never merge these roles.**

Paper-canonical terminology: arXiv:2603.06007, BUPT-GAMMA.

```
.gemini/intent.gemini
        │
        ▼
┌───────────────────────────────────────────────────────┐
│  Stage 1 · Role Assignment                            │
│  Scan /skills/ YAML frontmatter only.                 │
│  Map intent → required agent specialisations.         │
│  No full instruction load at this stage.              │
└───────────────┬───────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────────┐
│  Stage 2 · Structure Design  [paper-canonical term]   │
│  Generate DAG skeleton.                               │
│  Wire Control Flow (causality),                       │
│       Message Flow (data payloads),                   │
│       State Flow (shared memory).                     │
│  Insert MIRA async event hooks at node boundaries.    │
└───────────────┬───────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────────┐
│  Stage 3 · Semantic Completion + MIRA Validation      │
│  Hydrate nodes: full SKILL.md instructions            │
│               + toolsets + context adapters.          │
│  ── MIRA GovernanceEngine (sync, once) ──────────────│
│  Validate compiled toolsets against policy.json.      │
│  Reject any node violating its policy → revise.       │
└───────────────┬───────────────────────────────────────┘
                │
                ▼
        .brain/graph_design.json
        ── HUMAN REVIEW GATE ──
        Edit the JSON directly if needed.
        Policy violations already resolved.
        Your review: intent accuracy + topology.
                │
                ▼
        root.invoke()  →  Executable Graph
```

### 5.1 Flow Types

| Flow | Direction | Purpose |
|---|---|---|
| **Control Flow** | Along edges | Causality and sequencing — which nodes must complete before others begin |
| **Message Flow** | Horizontal along edges | Data payloads carried between nodes via Message Adapters |
| **State Flow** | Hierarchical (graph ↔ subgraph) | Shared memory regions — backed by Mem0 or equivalent |
| **MIRA Event Flow** | Async, node → observer | Structured monitoring events. Written to `.mira/scores/`. Off critical path. |

### 5.2 Node Types (MASFactory-native)

| Node Type | Use For |
|---|---|
| `Agent` | Perception–Reasoning–Action loop. Primary workhorse. |
| `Graph` | DAG sub-workflow. Groups a set of sequential/parallel agents. |
| `Loop` | Cyclic structures: reflection, revision, retry. Use for regen on low DM score. |
| `Switch` | Conditional routing. Selects downstream path based on runtime state. |
| `Interaction` | Human-in-the-loop entry point. Collects feedback, injects back into workflow. |
| `CustomNode` | Arbitrary computation unit. Extend for domain-specific logic. |

### 5.3 Message Adapters

Declare per edge in `graph_design.json`. WorkflowMonitor validates schemas at runtime (Tier 2).

| Adapter | Use When |
|---|---|
| `json` | Machine-to-machine edges. Schema-validated. Default choice. |
| `markdown` | Human-readable intermediate artefacts. |
| `plaintext` | Receiving agent performs its own parsing. Use sparingly. |

---

## 6. Standard Execution Wrapper

~45 lines. Architect/Worker separation enforced by construction.

```python
# mas_run.py  —  The Weave  ·  v4
# Usage: python mas_run.py [--tier 1|2] [--intent path/to/intent.gemini]

import argparse
from masfactory        import NodeTemplate, RootGraph, VibeGraph
from masfactory.models import invoke_model, build_model
from mira              import init_control_plane

parser = argparse.ArgumentParser()
parser.add_argument("--tier",   type=int, default=1,
                    help="MIRA tier: 1 (no ChromaDB) or 2 (full observability)")
parser.add_argument("--intent", type=str,
                    default=".gemini/current_intent.gemini")
args = parser.parse_args()

# ── MIRA Control Plane ─────────────────────────────────────────
# Tier 1: GovernanceEngine + ScoringService Lite + Lineage Chain
# Tier 2: adds WorkflowMonitoringAgent + ScoringService Full
#         requires ChromaDB running and accessible
mira = init_control_plane(
    policy_dir  = ".mira/policies",
    scores_dir  = ".mira/scores",
    tier        = args.tier,
    kpis        = {
        "max_task_duration": 10,   # seconds per node
        "min_dm_score":      0.6,  # triggers Loop regen below this
        "max_retry_count":   2     # Loop cap before MassGen escalation
    }
)

# ── Compile ─────────────────────────────────────────────────────
workflow = NodeTemplate(
    VibeGraph,
    invoke_model       = invoke_model,       # Worker: fast, cheap
    build_model        = build_model,        # Architect: high-intelligence
    build_instructions = open(args.intent).read(),
    build_cache_path   = ".brain/graph_design.json",
    mira               = mira,
)

root = RootGraph(name="TheWeave", nodes=[("task", workflow)])

# Stage 1–3 + MIRA policy check (sync, once) + human review gate
# Edit .brain/graph_design.json before invoking if needed
root.build()

# Execute with MIRA async observer active
root.invoke()
```

**Run commands:**
```bash
# Tier 1 — no ChromaDB
python mas_run.py --tier 1 --intent .gemini/my_feature.gemini

# Tier 2 — full observability (ChromaDB must be running)
python mas_run.py --tier 2 --intent .gemini/my_feature.gemini
```

---

## 7. MIRA Control Plane (Tiered)

### 7.1 Tier 1 — Always On · No ChromaDB

**GovernanceEngine**

Enforces `agent_tool_policy.json`. Called synchronously once at Stage 3. Not called at runtime — the validated blueprint is the authority.

**ScoringService Lite**

Scores each node output async on 2 dimensions after completion:

```
DM Score = f(document_content, metadata.source)
         = f(semantic quality, provenance trust)
```

| Score | Action |
|---|---|
| 0.8 – 1.0 | Proceed |
| 0.6 – 0.79 | Proceed with flag — lineage tagged, human review recommended |
| < 0.6 | Trigger `Loop` node regen → up to `max_retry_count` → escalate to MassGen |

**Lineage Chain**

Append-only, async. Every node writes one record:

```json
{
  "intent":      ".gemini/current_intent.gemini",
  "blueprint":   ".brain/graph_design.json",
  "node":        "synthesiser_agent",
  "prompt_seed": "a3f8c1d2...",
  "model":       "claude-haiku-4-5",
  "tier":        1,
  "dm_score":    { "content": 0.82, "provenance": 0.90, "total": 0.86 },
  "output":      ".brain/outputs/synthesiser_001.md"
}
```

---

### 7.2 Tier 2 — Full Observability · Requires ChromaDB

Activate by setting `tier=2` in `mas_run.py`. Tier 1 services remain active. Lineage records are automatically enriched with the third score dimension.

**WorkflowMonitoringAgent**

Consumes async event stream. Evaluates KPIs. Cross-references live ChromaDB-backed KnowledgeGraph to surface upstream dependency faults.

Event schema emitted by each node:
```json
{ "event": "task_started",   "task_name": "...", "timestamp": "..." }
{ "event": "task_completed", "task_name": "...", "duration": 4.2    }
{ "event": "task_failed",    "task_name": "...", "reason": "..."    }
```

Graph relationships populated from `graph_design.json` at invoke time:
- `DEPENDS_ON` — causality between nodes
- `CALLS` — external service dependencies

**ScoringService Full**

```
DM Score = f(document_content, metadata.source, relevance_distance)
         = f(semantic quality, provenance trust, PathRAG retrieval confidence)
```

`relevance_distance` sourced from ChromaDB vector query. Lower = more relevant.

**Enriched Lineage Record (Tier 2):**
```json
{
  "tier":     2,
  "dm_score": {
    "content":    0.82,
    "provenance": 0.90,
    "relevance":  0.88,
    "total":      0.87
  }
}
```

---

### 7.3 MIRA Analysis Patterns (Both Tiers)

**Consistency Enforcer**  
Insert before any parallel execution branch with 2+ nodes producing human-readable output. Generates a shared constraint document (`constraint.md` in `.brain/`) injected into all downstream node prompts at Stage 3. Prevents stylistic drift.

**Tool Agnosticism Protocol**  
Declare a `tools_selection` decision matrix in `SKILL.md`. Build Model evaluates it at Stage 3 — not hardcoded tool names. Example:
```python
if task.requires_photorealism and budget > threshold:
    tool = "flux-pro"
elif task.style == "artistic":
    tool = "midjourney"
else:
    tool = "rapid-iteration-model"
```

**Quality Gate**  
Insert a lightweight defect-detection node before any high-cost downstream node (external API, long generation, expensive compute). Gate runs ScoringService and checks `quality_gates` declared in `SKILL.md` before the expensive step executes.

**Metadata Lineage Chain**  
Enforced by default in both tiers. Full audit trail from intent → blueprint → node → prompt_seed → model → score → output. Enables exact reproduction of any output and regression detection across runs.

---

## 8. Observability & Debugging

### 8.1 Capability Matrix

| Capability | Tier 1 | Tier 2 |
|---|---|---|
| Policy violation caught at compile time | ✓ | ✓ |
| Per-node DM score (2-dimension) | ✓ | ✓ |
| Full lineage audit trail | ✓ | ✓ (enriched) |
| MASFactory Visualizer (topology + trace) | ✓ | ✓ |
| Score-based Loop regen | ✓ | ✓ (3-dim threshold) |
| KPI breach detection | — | ✓ |
| Dependency-aware fault tracing | — | ✓ (ChromaDB) |
| Per-node DM score (3-dimension) | — | ✓ (ChromaDB) |

### 8.2 MASFactory Visualizer (VS Code Extension)

Two mandatory usage modes:

1. **Topology Preview** — inspect `graph_design.json` before `root.invoke()`. Verify node roles, dependency edges, adapter assignments, MIRA event hook placements.
2. **Runtime Tracing** — monitor live message propagation. Surfaces latency hotspots and failed edges during execution.

### 8.3 AgentXRay (Diagnostics)

If integrating an opaque third-party system:
1. Feed execution traces and input/output pairs to AgentXRay
2. AgentXRay synthesises a white-box surrogate directed graph
3. Import surrogate into MASFactory, extend with Skill Folders

### 8.4 Debugging Protocol

```
Step 1  Check .mira/scores/lineage.json
        → Are DM scores declining across runs? Skill Folder needs work, not a prompt tweak.
        → Any node with dm_score.total < 0.6? That's your failure point.

Step 2  Open MASFactory Visualizer → Topology Preview
        → Are all policy.json declarations correct?
        → Any edge missing a Message Adapter type?

Step 3  (Tier 2 only) Check WorkflowMonitor KPI report
        → Any task_duration breach? Upstream dependency fault?
        → Traverse DEPENDS_ON edges backward from the failing node.

Step 4  Inspect .brain/graph_design.json
        → Is the blueprint what you intended?
        → If not: edit and re-invoke without recompiling.

Step 5  If failure persists after 2 Loop retries → MassGen escalation
        → Check MassGen vote distribution. Consistent minority = weak skill.
```

> **80% rule:** Most runtime failures originate in policy violations (caught at compile time) or DM score regressions visible in `lineage.json`. Fix the boundary first, not the prompt.

---

## 9. Integration Protocols

### 9.1 Context Adapters

Decouple agent logic from external data sources. Each adapter sets the `metadata.source` provenance tag used by ScoringService.

| Adapter | Provenance Tag | Score Weight | Notes |
|---|---|---|---|
| Mem0 | `internal_system` | High | Persistent cross-session memory |
| LlamaIndex / PathRAG | `knowledge_base` | High | Index `skills/*/references/` at init |
| MCP | `external` | Medium | Standardised tool protocol |
| Raw web / scraping | `external_unverified` | Low | Flag for human review |

### 9.2 MassGen Scaling

Insert a Collective Validation node for high-stakes outputs. Parallel subagents (defined via `SUBAGENT.md`) vote; MassGen selects consensus. ScoringService scores each candidate before the vote to weight by quality.

**When to use:**
- Task has no objectively verifiable ground truth
- A node has exhausted `max_retry_count` with score still < 0.6
- Output will be consumed by a human without further review

### 9.3 PathRAG Integration

PathRAG provides multi-hop retrieval over connected knowledge rather than isolated chunks.

```bash
# Index a skill's references (run at workspace init or when references change)
pathrag index \
  --source  skills/<skill-name>/references/ \
  --store   skills/<skill-name>/vectordb/ \
  --graph   skills/<skill-name>/vectordb/graph.json
```

`relevance_distance` from PathRAG queries feeds directly into Tier 2 ScoringService Full as the third DM score dimension.

---

## 10. Project-Specific Conventions

Applies to: **antigravity · opencode · Gemini CLI**

| Convention | Rule |
|---|---|
| Default MIRA tier | Tier 1 until Tier 2 decision criteria met (§1.2) |
| Intent file naming | `.gemini/<feature>_intent.gemini` |
| Blueprint versioning | Commit `.brain/graph_design.json`. Treat changes with code-review rigour. |
| Policy changes | `.mira/policies/agent_tool_policy.json` changes require explicit approval before merge. |
| New capability | New Skill Folder + `policy.json` first. Never expand existing skill beyond declared trigger set. |
| New external service | Declare provenance tag in Context Adapter before node is permitted to call it. |
| Gemini CLI role | Acts as the **Master Architect** — submits `.gemini` intent files, triggers `root.build()`, reviews the IR, approves `root.invoke()`. |
| Build model | `claude-sonnet-4-6` (architect / compiler) |
| Invoke model | `claude-haiku-4-5` (worker / executor) |
| Tier upgrade | Change `tier=1` → `tier=2` in `mas_run.py`. No directory changes. No schema changes. |

---

## 11. Alignment with arXiv:2603.06007

This SOP extends the MASFactory paper. Deviations and additions are explicitly labelled.

| Concept | Status | Notes |
|---|---|---|
| 3-Stage Vibe Graphing Pipeline | ✓ Paper-canonical | Stage 2 = "Structure Design" (not "Topology Design") |
| Control / Message / State Flow | ✓ Paper-canonical | MIRA Event Flow is an SOP extension |
| Context Adapter | ✓ Paper-canonical | Provenance tagging is an SOP extension |
| NodeTemplate / execution wrapper | ✓ Paper-canonical | |
| Human-in-the-loop gate | ✓ Paper-canonical | |
| Switch / Loop / Interaction nodes | ✓ Paper-canonical | Loop used for MIRA regen; Switch for routing |
| Declarative + Imperative interfaces | ✓ Paper-canonical | SOP focuses on Vibe Graphing but all three modes are valid |
| Skill Folder system | ➕ SOP extension | Not in paper. Our operational scaffolding. |
| Directory schema | ➕ SOP extension | Not in paper. Our operational convention. |
| MIRA Control Plane (all tiers) | ➕ SOP extension | Not in paper. Original contribution from MIRA-TitanOS. |
| `vectordb/` inside Skill Folder | ➕ SOP extension | Co-location pattern. Not in paper or MIRA-TitanOS. |
| PathRAG `relevance_distance` → DM score | ➕ SOP extension | Integration design. PathRAG paper is separate. |

---

## 12. Glossary

| Term | Definition |
|---|---|
| **The Weave** | The full integrated stack: MASFactory + MassGen + PathRAG + MIRA |
| **Vibe Graphing** | The 3-stage, human-in-the-loop compilation of natural-language intent into an executable directed computation graph |
| **Vibe Gap** | The distance between a high-level project goal and a correctly wired executable MAS |
| **IR / Blueprint** | `graph_design.json` — the structured intermediate representation produced by Stage 3 |
| **Skill Folder** | A self-contained agent primitive: `SKILL.md` + `policy.json` + `scripts/` + optional directories |
| **Build Model** | The architect LLM. High intelligence. Runs Vibe Graphing compilation. Not used at execution time. |
| **Invoke Model** | The worker LLM. Fast and cheap. Runs agent nodes at execution time. |
| **DM Score** | Decision-Making score. Continuous quality signal per node output. 2-dimension in Tier 1, 3-dimension in Tier 2. |
| **MIRA Tier 1** | GovernanceEngine + ScoringService Lite + Lineage Chain. No ChromaDB. Zero runtime overhead. |
| **MIRA Tier 2** | Tier 1 + WorkflowMonitoringAgent + ScoringService Full. Requires ChromaDB. Async, not on critical path. |
| **Collective Validation** | MassGen voting pattern. Multiple subagents produce candidates; consensus selects the result. |
| **White-boxing** | Making an opaque system interpretable via AgentXRay workflow reconstruction. |

---

*MAS-Master v4.0 · The Weave · CC BY-SA 4.0*  
*Sources: arXiv:2603.06007 (MASFactory) · arXiv:2502.14902 (PathRAG) · arXiv:2602.05353 (AgentXRay) · MIRA-TitanOS*
