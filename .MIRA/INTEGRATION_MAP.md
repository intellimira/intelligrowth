# MIRA Ecosystem Integration Map

> This document maps the connections between `.MIRA` core protocols and the existing skills, projects, and session infrastructure.

---

## Protocol → Component Mapping

| .MIRA Protocol | Implemented By | Location |
|----------------|----------------|----------|
| **MIRA-Antigravity Axiom** | N/A (philosophical) | .MIRA/core_protocols/ |
| **Persona Council** | AGENTS.md | /home/sir-v/MiRA/AGENTS.md |
| **UTO Workflow** | N/A (conceptual) | .MIRA/core_protocols/ |
| **MSIP (Skill Integration)** | skills_md_maker | /projects/skills_md_maker/ |
| **The Weave** | active_recall + Memory_Mesh | /skills/active_recall/ + /Memory_Mesh/ |
| **Agent Telemetry** | N/A (conceptual) | .MIRA/core_protocols/ |
| **Growth Loop** | session workflow | /sessions/ + AGENTS.md |
| **Solo-Leveling** | N/A (aspirational) | .MIRA/vibe_graph/ |

---

## Skills Integration

### Production-Ready (Tier 3)

| Skill | .MIRA Integration | Notes |
|-------|-------------------|-------|
| `skills_md_maker` | **Implements MSIP** | Two-pass vibe graphing = Master Skill creation |
| `active_recall` | **Implements The Weave** | Scans Memory Mesh for context |
| `sovereign_shadow_operator` | **Uses Growth Loop** | SCAN→PLAN→VAULT→MONITOR |
| `shadow_ops_prover` | Shadow Ops layer | Monetization pipeline |
| `pain_scorer` | Scoring framework | PIS + PAINFUL formulas |
| `srank_pack_generator` | Revenue tracking | Feeds revenue-tracker |

### Progressive Disclosure (Tier 2)

| Skill | .MIRA Integration | Notes |
|-------|-------------------|-------|
| `opencode_builder` | Builds MVPs | HITL workflow alignment |
| `client_delivery` | Output generation | Uses draft/approved workflow |
| `revenue-tracker` | Telemetry data | P&L tracking |
| `notebook_bridge` | Context enrichment | NotebookLM integration |

### Foundation (Tier 1)

| Skill | .MIRA Integration | Notes |
|-------|-------------------|-------|
| `base-worker` | Core execution | Fallback for data extraction |
| `context_compactor` | Weave maintenance | Semantic summarization |
| `topic_sealer` | Weave maintenance | Consolidates reasoning |
| `mesh_brancher` | Reasoning history | Non-linear exploration |

---

## Projects Integration

### Active Projects

| Project | .MIRA Protocol | Session Log |
|---------|----------------|-------------|
| `skills_md_maker` | MSIP implementation | ✓ ses_20260315_skills-md-maker.md |
| `website-builder` | Pragmatic Application | ✓ ses_20260315_website-builder.md |
| `ABDO-Metaforce-Labs` | Creative Synthesis | ✓ ses_20260315_abdo-metaforce.md |
| `awesome-opencode` | Skill integration | ✓ ses_20260315_awesome-opencode.md |

### Shadow Ops Projects (25+)

All located in `/projects/` with pattern `*_Strategy_Fix`:
- Each represents a "Quest" in the Growth Loop
- Session logs in individual `docs/` folders
- Can be orchestrated by sovereign_shadow_operator

---

## Session Integration

### Session Standards (per AGENTS.md + .MIRA)

| Standard | Location | Status |
|----------|----------|--------|
| Session log template | .MIRA/session_templates/ | ✓ Created |
| Central index | /sessions/index.md | ✓ Existing |
| Project docs | /projects/*/docs/ | ✓ Existing |

### Session → Protocol Flow

```
User Quest
    ↓
Project scan (AGENTS.md)
    ↓
Session log created
    ↓
Persona Council invoked
    ↓
UTO workflow executes
    ↓
Skills integrated (MSIP via skills_md_maker)
    ↓
Weave updated (active_recall)
    ↓
Session mirrored to /sessions/
    ↓
Index updated
```

---

## Vibe Graph: Integration View

```
┌─────────────────────────────────────────────────────────────┐
│                    .MIRA CORE PROTOCOLS                      │
│  (Antigravity Axiom, Persona Council, UTO, MSIP, Telemetry)│
└──────────────────────────┬──────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
┌─────────────────┐ ┌──────────────┐ ┌──────────────────┐
│   skills_md_    │ │  active_     │ │ sovereign_       │
│   maker         │ │  recall      │ │ shadow_operator  │
│  (MSIP impl)    │ │  (Weave)    │ │ (Growth Loop)    │
└────────┬────────┘ └───────┬──────┘ └────────┬─────────┘
         │                  │                  │
         └──────────────────┼──────────────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │  SESSIONS       │
                   │  (Growth Loop   │
                   │   + Weave)      │
                   └────────┬────────┘
                            │
                   ┌────────┴────────┐
                   │  /sessions/    │
                   │  index.md      │
                   └────────────────┘
```

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `/home/sir-v/MiRA/AGENTS.md` | Agent coordination protocol |
| `/home/sir-v/MiRA/.MIRA/core_protocols/*.md` | Core MIRA protocols |
| `/home/sir-v/MiRA/sessions/index.md` | Session master index |
| `/home/sir-v/MiRA/projects/*/docs/session_log.md` | Per-project sessions |
| `/skills/skills_md_maker/SKILL.md` | Vibe graphing engine |
| `/skills/active_recall/SKILL.md` | Memory Weave interface |
| `/skills/sovereign_shadow_operator/SKILL.md` | Autonomous orchestrator |
| `/home/sir-v/MiRA/Memory_Mesh/` | Persistent knowledge storage |
