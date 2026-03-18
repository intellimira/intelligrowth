# SHADOW OPS × THE WEAVE v4.0
## Unified Agent Architecture: MIRA + MASFactory + Shadow Ops Pipeline
**Version:** v3.0 "Sovereign Cognition — Woven"
**Stack:** Ollama (Invoke) · Gemini CLI / Claude Sonnet (Build) · SQLite · MASFactory · PathRAG · MIRA Tier 1
**Constraint:** £0 capital down. Cost/benefit first. HITL gating on all irreversible actions.

---

## HOW THE TWO SYSTEMS INTEGRATE

Shadow Ops is the **problem-finding and business validation layer**.
The Weave v4.0 is the **agent execution and governance layer**.

They plug together cleanly:

```
SHADOW OPS PIPELINE          THE WEAVE RUNTIME
─────────────────────        ────────────────────────────────
Phase 1: Sentry          →   Skill: pain-sentry
Phase 2: Meat Grinder    →   Skill: pain-scorer  + ScoringService Lite
Phase 3: Architecture    →   Vibe Graphing: Stages 1-3 (Build Model)
Phase 4: Grounding       →   Skill: hostile-grounding (MassGen vote)
Phase 5: Sealing         →   Skill: srank-pack-generator
Phase 6: HITL Gate       →   Interaction Node (MASFactory-native)
Phase 7: Shadow Delivery →   Skill: opencode-builder (Invoke Model)
```

The Shadow Ops Pain Score drives the **Switch node** that decides:
- Score < 55: discard (no Weave invocation)
- Score 55–71: Ollama-only pass (Tier 1, no Gemini)
- Score ≥ 72: Full Weave pipeline (Gemini CLI as Build Model)

---

## 1. WORKSPACE DIRECTORY STRUCTURE

```
/shadow-ops-root/
├── .gemini/                          # Intent files (per project)
│   └── <project>_intent.gemini
├── .brain/                           # IR cache
│   ├── graph_design.json             # ← VERSION CONTROL THIS
│   └── outputs/
├── skills/                           # Skill Folder library
│   ├── pain-sentry/                  # Phase 1: signal capture
│   │   ├── SKILL.md
│   │   ├── policy.json
│   │   └── scripts/
│   │       ├── reddit_scraper.py
│   │       └── imap_listener.py
│   ├── pain-scorer/                  # Phase 2: PIS calculation
│   │   ├── SKILL.md
│   │   ├── policy.json
│   │   └── scripts/
│   │       ├── score_engine.py
│   │       └── db_writer.py
│   ├── arch-synthesiser/             # Phase 3: architecture
│   │   ├── SKILL.md
│   │   ├── policy.json
│   │   ├── references/               # PathRAG indexed
│   │   └── scripts/
│   │       └── gemini_arch_call.py
│   ├── hostile-grounding/            # Phase 4: adversarial review
│   │   ├── SKILL.md
│   │   ├── policy.json
│   │   ├── SUBAGENT.md               # MassGen: 3 hostile personas vote
│   │   └── scripts/
│   │       └── grounding_prompt.py
│   ├── srank-pack-generator/         # Phase 5: business pack
│   │   ├── SKILL.md
│   │   ├── policy.json
│   │   └── assets/                   # Output templates
│   │       ├── PAIN_SIGNAL_BRIEF.md
│   │       ├── ARCHITECTURE.md
│   │       └── HITL_GATE.md
│   └── opencode-builder/             # Phase 7: code manifestation
│       ├── SKILL.md
│       ├── policy.json
│       └── scripts/
│           └── opencode_runner.py
├── .mira/                            # MIRA Control Plane
│   ├── policies/
│   │   └── agent_tool_policy.json    # Global deny/allow
│   └── scores/
│       └── lineage.json              # Append-only quality audit trail
├── projects/                         # Manifested project outputs
│   └── <PROJECT_NAME>/
│       ├── PAIN_SIGNAL_BRIEF.md
│       ├── ARCHITECTURE.md
│       ├── ZERO_CAPITAL_PLAN.md
│       ├── GROUNDING_REPORT.md
│       ├── OUTREACH_PACK.md
│       └── HITL_GATE.md
├── CLAUDE.md                         # Global conventions
├── AGENTS.md                         # Cross-agent coordination
└── mas_run.py                        # ~45-line execution wrapper
```

---

## 2. CLAUDE.md (Seed)

```markdown
# Project: Shadow Ops × The Weave
## Stack
- Language: Python 3.11+
- Primary framework: MASFactory
- Invoke model: opencode:ollama          (worker — fast, free, local)
- Build model: claude-sonnet-4-6         (architect — high intelligence)
- MIRA tier: 1                           (upgrade to 2 when dependency tracing needed)
- Gemini CLI role: Master Architect      (Vibe Graphing Stages 1+2, deep analysis)

## Conventions
- All outputs to .brain/outputs/ and projects/<name>/
- All MIRA scores to .mira/scores/lineage.json
- Kebab-case for all skill folder names
- JSON for machine-to-machine adapters
- Markdown for human-readable artefacts
- Pain Score ≥72 = Gemini trigger threshold
- All outreach/code pushes = HITL gate required (Interaction Node)
```

---

## 3. SKILL FOLDER SPECS

### 3.1 pain-sentry

```yaml
# SKILL.md frontmatter
---
name:          pain-sentry
description:   Mines Reddit, G2 reviews, IMAP for raw pain signals. Classifies by signal type.
triggers:      [discover, mine, scan, find pain, monitor]
tools:         [run_scrapy, praw_fetch, imap_read, sqlite_write]
quality_gates: [source_verified, no_placeholder_urls, signal_type_tagged]
---
```

```json
// policy.json
{
  "pain-sentry": {
    "allowed_tools": ["run_scrapy", "praw_fetch", "imap_read", "sqlite_write", "read_file"],
    "deny_tools":    ["send_email", "send_sms", "http_post", "delete_file", "gemini_call"]
  }
}
```

**Critical rule:** Gemini is explicitly DENIED at this stage. All classification runs on Ollama only.

---

### 3.2 pain-scorer

```yaml
---
name:          pain-scorer
description:   Applies 5-axis PIS formula. Routes signals to Ollama (<72) or Gemini (≥72).
triggers:      [score, evaluate, grade, rank signal]
tools:         [sqlite_read, sqlite_write, ollama_infer, score_signal]
quality_gates: [score_in_range_0_100, all_axes_scored, routing_tag_set]
---
```

**Score routing logic (Switch node):**
```python
# In graph_design.json — Switch node config
{
  "node_type": "Switch",
  "id": "pain_router",
  "cases": [
    {"condition": "pain_score < 55",  "route": "discard_agent"},
    {"condition": "pain_score < 72",  "route": "ollama_arch_agent"},
    {"condition": "pain_score >= 72", "route": "gemini_arch_agent"}
  ]
}
```

---

### 3.3 arch-synthesiser

```yaml
---
name:          arch-synthesiser
description:   Synthesises zero-capital MVP architecture. Uses Gemini CLI for scores ≥72.
triggers:      [architect, design solution, plan build, technical design]
tools:         [gemini_call, ollama_infer, sqlite_write, write_file]
quality_gates: [tier0_tools_only, api_tos_checked, build_time_estimated]
---
```

**PathRAG integration:** The `references/` folder contains:
- Tier 0 tool documentation (Scrapy, FastAPI, SQLite, FFmpeg, n8n)
- API ToS summaries for common platforms
- Previous successful architecture blueprints

PathRAG provides multi-hop retrieval so the arch-synthesiser can ask "what's the cheapest way to do X that won't violate Reddit's ToS" and get a joined answer from multiple reference docs.

---

### 3.4 hostile-grounding (with MassGen)

```yaml
---
name:          hostile-grounding
description:   Adversarial review. Three personas vote on GO/NO-GO. Consensus required.
triggers:      [challenge, stress-test, hostile review, grounding check]
tools:         [gemini_call, sqlite_write, write_file]
quality_gates: [all_three_votes_cast, consensus_reached, failure_vectors_listed]
---
```

**SUBAGENT.md (MassGen voting agents):**
```markdown
# Subagents for hostile-grounding Collective Validation

## Subagent A: The Regulator
Focus: GDPR, API ToS, UK data protection, SRA (legal tools), FCA (fintech).
Vote: GO if no material regulatory breach. NO-GO + specific citation if breach found.

## Subagent B: The Market Pessimist
Focus: Competition density, market timing, "vitamin vs painkiller" classification.
Vote: GO if <5 direct competitors and daily-use loop confirmed. NO-GO otherwise.

## Subagent C: The Technical Realist
Focus: Build complexity vs stated timeline. API availability. Dependency fragility.
Vote: GO if solo build feasible in stated hours. NO-GO if hidden complexity detected.
```

MassGen consensus: 2/3 votes required for GO. 3/3 for S-Rank confidence boost.

---

### 3.5 opencode-builder

```yaml
---
name:          opencode-builder
description:   Manifests the MVP codebase via OpenCode. Ollama reviews output.
triggers:      [build, code, implement, manifest, generate code]
tools:         [opencode_run, ollama_infer, read_file, write_file, run_tests]
quality_gates: [no_hardcoded_secrets, tier0_deps_only, tests_written, readme_exists]
---
```

```json
// policy.json — strict. Builder cannot push or deploy.
{
  "opencode-builder": {
    "allowed_tools": ["opencode_run", "ollama_infer", "read_file", "write_file", "run_tests"],
    "deny_tools":    ["send_email", "http_post", "git_push", "deploy", "delete_file"]
  }
}
```

**Never merges the Build Model and Invoke Model roles.** OpenCode uses `opencode:ollama` for routine execution. Gemini is only called if OpenCode encounters an architecture decision it cannot resolve with local context.

---

## 4. THE GRAPH_DESIGN.JSON BLUEPRINT SKELETON

```json
{
  "meta": {
    "version": "4.0",
    "build_model": "claude-sonnet-4-6",
    "invoke_model": "opencode:ollama",
    "mira_tier": 1,
    "intent_file": ".gemini/shadow_ops_intent.gemini"
  },
  "nodes": [
    {
      "id": "sentry",
      "type": "Agent",
      "skill": "pain-sentry",
      "invoke_model": "opencode:ollama",
      "message_adapter": "json",
      "mira_hooks": ["score_output", "write_lineage"]
    },
    {
      "id": "scorer",
      "type": "Agent",
      "skill": "pain-scorer",
      "invoke_model": "opencode:ollama",
      "message_adapter": "json",
      "mira_hooks": ["score_output", "write_lineage"]
    },
    {
      "id": "pain_router",
      "type": "Switch",
      "cases": [
        {"condition": "pain_score < 55",  "route": "discard"},
        {"condition": "pain_score < 72",  "route": "arch_ollama"},
        {"condition": "pain_score >= 72", "route": "arch_gemini"}
      ]
    },
    {
      "id": "arch_gemini",
      "type": "Agent",
      "skill": "arch-synthesiser",
      "invoke_model": "gemini-2.5-pro",
      "message_adapter": "json",
      "mira_hooks": ["score_output", "write_lineage", "log_cost"]
    },
    {
      "id": "grounding",
      "type": "Graph",
      "skill": "hostile-grounding",
      "subgraph_type": "MassGen",
      "parallel_agents": ["subagent_a", "subagent_b", "subagent_c"],
      "consensus_threshold": 2,
      "message_adapter": "json"
    },
    {
      "id": "go_router",
      "type": "Switch",
      "cases": [
        {"condition": "grounding_vote == 'NO-GO'", "route": "archive"},
        {"condition": "grounding_vote == 'GO'",    "route": "sealing"}
      ]
    },
    {
      "id": "sealing",
      "type": "Agent",
      "skill": "srank-pack-generator",
      "invoke_model": "gemini-2.5-pro",
      "message_adapter": "markdown",
      "mira_hooks": ["score_output", "write_lineage"]
    },
    {
      "id": "hitl_gate",
      "type": "Interaction",
      "prompt": "Review HITL_GATE.md. Enter GO or NO-GO.",
      "timeout_seconds": 86400,
      "on_timeout": "archive"
    },
    {
      "id": "builder",
      "type": "Agent",
      "skill": "opencode-builder",
      "invoke_model": "opencode:ollama",
      "message_adapter": "json",
      "mira_hooks": ["score_output", "write_lineage"]
    }
  ],
  "edges": [
    {"from": "sentry",     "to": "scorer"},
    {"from": "scorer",     "to": "pain_router"},
    {"from": "pain_router","to": "arch_gemini",  "condition": "pain_score >= 72"},
    {"from": "arch_gemini","to": "grounding"},
    {"from": "grounding",  "to": "go_router"},
    {"from": "go_router",  "to": "sealing",    "condition": "GO"},
    {"from": "sealing",    "to": "hitl_gate"},
    {"from": "hitl_gate",  "to": "builder",    "condition": "GO"}
  ],
  "state": {
    "shared_keys": ["pain_score", "signal_id", "project_name", "grounding_vote"],
    "backed_by": "sqlite"
  }
}
```

---

## 5. MAS_RUN.PY (Execution Wrapper)

```python
# mas_run.py  —  Shadow Ops × The Weave  ·  v4.0
# Usage: python mas_run.py [--tier 1|2] [--intent path/to/intent.gemini]

import argparse
from masfactory        import NodeTemplate, RootGraph, VibeGraph
from masfactory.models import invoke_model, build_model
from mira              import init_control_plane

parser = argparse.ArgumentParser()
parser.add_argument("--tier",   type=int, default=1)
parser.add_argument("--intent", type=str,
                    default=".gemini/shadow_ops_intent.gemini")
args = parser.parse_args()

mira = init_control_plane(
    policy_dir  = ".mira/policies",
    scores_dir  = ".mira/scores",
    tier        = args.tier,
    kpis        = {
        "max_task_duration": 30,   # Gemini calls allowed up to 30s
        "min_dm_score":      0.6,  # Loop regen below this
        "max_retry_count":   2     # Then escalate to MassGen
    }
)

workflow = NodeTemplate(
    VibeGraph,
    invoke_model       = "opencode:ollama",      # Worker: local, £0
    build_model        = "claude-sonnet-4-6",    # Architect: high intelligence
    build_instructions = open(args.intent).read(),
    build_cache_path   = ".brain/graph_design.json",
    mira               = mira,
)

root = RootGraph(name="ShadowOpsWeave", nodes=[("task", workflow)])

# Stage 1-3 + MIRA governance sync check + human review gate
# Edit .brain/graph_design.json before invoking if needed
root.build()

# Execute with MIRA async observer active
root.invoke()
```

---

## 6. MIRA LINEAGE RECORD (Per Node)

Every node writes one record to `.mira/scores/lineage.json`:

```json
{
  "intent":      ".gemini/gdpr_friction_zero_shield.gemini",
  "blueprint":   ".brain/graph_design.json",
  "node":        "arch_gemini",
  "prompt_seed": "a3f8c1d2...",
  "model":       "gemini-2.5-pro",
  "tier":        1,
  "dm_score":    { "content": 0.84, "provenance": 0.91, "total": 0.87 },
  "output":      "projects/GDPR_Friction_Zero_Shield/ARCHITECTURE.md",
  "gemini_tokens_used": 1840,
  "cost_estimate_gbp": 0.015
}
```

The `cost_estimate_gbp` field is Shadow-Ops-specific. Track it across runs to validate the cost/benefit model.

---

## 7. PERSONA COUNCIL INTEGRATION (MIRA)

The six MIRA personas map onto Skill Folder specialisations:

| Persona | Role in Shadow Ops |
|---------|-------------------|
| ⚛️ First Principles | pain-scorer: strips assumptions from signal classification |
| 🔬 Scientific Method | hostile-grounding Subagent B: market hypothesis testing |
| 🤔 Philosophical Inquiry | hostile-grounding Subagent A: regulatory/ethical review |
| ✨ Creative Synthesis | arch-synthesiser: novel zero-capital tool combinations |
| ⚙️ Pragmatic Application | opencode-builder: fastest path to working MVP |
| 🌑 Dark Passenger | hostile-grounding Subagent C: technical failure detection |

At Stage 3 (Semantic Completion), the Build Model explicitly assigns persona framing to each node's instruction prompt. Persona rotation is logged in the lineage chain under `persona_applied`.

---

## 8. MGT LOOP (MIRA Grounded Theory) IN THE SCORING ENGINE

The pain-scorer skill applies MGT to avoid classifying the same signal type incorrectly twice:

```
Phase 1 — Open Coding (The Reporter):
  Extract: raw signal text, source platform, timestamp, emotional intensity markers.

Phase 2 — Axial Coding (The Detective):
  Group: signal_type → workaround | receipt | overkill | rant | noise
  Map condition → consequence (e.g., "user describes spreadsheet hack" → "daily_loop = True")

Phase 3 — Selective Coding (The Strategist):
  Output actionable heuristic → written to .brain/outputs/scoring_heuristics.md
  Injected into future pain-scorer runs via PathRAG retrieval.
```

This means the scoring engine improves over time without retraining. Each new signal that produces a validated outcome (paid customer, successful project) updates the heuristics file, which PathRAG indexes, which feeds back into Stage 3 Semantic Completion for the next run.

---

## 9. COST CONTROL TABLE (COMPLETE)

| Action | Model | Tier | Cost |
|--------|-------|------|------|
| Signal classification | Ollama (local) | 1 | £0.00 |
| PIS scoring | Ollama (local) | 1 | £0.00 |
| Architecture synthesis (score ≥72) | Gemini 2.5 Pro | 1 | ~£0.015/call |
| Grounding (3 MassGen agents) | Gemini 2.5 Pro | 1 | ~£0.04/project |
| S-Rank pack generation | Gemini 2.5 Pro | 1 | ~£0.02/project |
| Code manifestation | OpenCode:Ollama | 1 | £0.00 |
| MIRA scoring (both tiers) | Local | 1 | £0.00 |
| PathRAG retrieval | Local ChromaDB | 2 | £0.00 |
| **Total per qualified project** | | | **~£0.08** |
| **Total per discarded signal** | | | **£0.00** |

At 85% discard rate (72-threshold filter), 100 signals → 15 projects → ~£1.20 total Gemini spend.

---

## 10. CHROMADB DECISION (Shadow Ops Context)

Answer the Weave decision checklist:

1. Do you need dependency-aware failure tracing? → **No** for MVP. Tier 1.
2. Do you need 3-dimension DM score with PathRAG confidence? → **Yes, for arch-synthesiser only**.
3. Constrained environment? → **Local machine. No constraint.**
4. Outputs consumed without human review? → **No. HITL gate on all irreversible actions.**

**Decision: Start Tier 1. Upgrade arch-synthesiser's skill vectordb to Tier 2 when you have 5+ projects completed and want retrieval quality metrics.**

Upgrade command (zero directory changes):
```python
# In mas_run.py, change:
mira = init_control_plane(..., tier=1)
# To:
mira = init_control_plane(..., tier=2)
```

---

## 11. BOOTSTRAP SEQUENCE FOR A NEW PROJECT

```bash
# 1. Init workspace (from sop.md §3.1)
mkdir -p .gemini .brain/outputs .mira/policies .mira/scores
mkdir -p skills/pain-sentry/{scripts,references,assets}
mkdir -p skills/pain-scorer/{scripts,references,assets}
mkdir -p skills/arch-synthesiser/{scripts,references,assets,vectordb}
mkdir -p skills/hostile-grounding/{scripts,references,assets}
mkdir -p skills/srank-pack-generator/{scripts,references,assets}
mkdir -p skills/opencode-builder/{scripts,references,assets}
touch CLAUDE.md AGENTS.md

# 2. Write intent file
echo "Discover, score, architect, and build a zero-capital Micro-SaaS 
      solving [PAIN_STATEMENT] for [TARGET_PERSONA]." \
  > .gemini/shadow_ops_intent.gemini

# 3. Seed SKILL.md and policy.json for each skill folder
# (use templates from §3 above)

# 4. Bootstrap via Gemini CLI (Master Architect)
gemini "Please read bootstrap_gemini_cli.md and follow the prompt."
# → Gemini runs Vibe Graphing Stages 1-3
# → Produces .brain/graph_design.json
# → Triggers MIRA governance check

# 5. Review the blueprint
# Open .brain/graph_design.json in MASFactory Visualizer (VS Code)
# Verify: node roles, edges, MIRA hooks, policy assignments

# 6. Run
python mas_run.py --tier 1 --intent .gemini/shadow_ops_intent.gemini
```

---

## 12. DEBUGGING PROTOCOL (Weave SOP §8.4)

```
Step 1  Check .mira/scores/lineage.json
        → dm_score.total < 0.6 on any node? That's the failure point.
        → Cost spike? Check gemini_tokens_used on arch_gemini node.

Step 2  MASFactory Visualizer → Topology Preview
        → policy.json denying a required tool?
        → Any edge missing a Message Adapter type?

Step 3  Check .brain/graph_design.json
        → Is the blueprint what you intended?
        → Edit directly and re-invoke without recompiling.

Step 4  If arch_gemini fails twice → MassGen escalation
        → Check MassGen vote distribution on hostile-grounding.
        → Consistent NO-GO = weak market, not a code problem.

Step 5  80% rule: Most failures are policy violations (compile time)
        or DM score regressions (lineage.json). Fix the boundary first.
```
