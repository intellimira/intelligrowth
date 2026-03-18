# MiRA Skill Maker Reference

> **Quick Start**: Open Notebook running at http://localhost:8502 (API: http://localhost:5055)
> **Created**: 2026-03-14 | **Last Updated**: 2026-03-14

---

## Table of Contents

1. [Command Reference](#1-skillm-command-reference)
2. [Input Sources](#2-input-sources)
3. [Architecture](#3-architecture-diagrams)
4. [Skill Locations](#4-skill-locations)
5. [Council & Cabal Integration](#5-council--cabal-integration)
6. [Open Notebook Tracking](#6-open-notebook-tracking)
7. [CLI Tools](#7-cli-tools)
8. [How To Guide](#8-how-to-guide)
9. [Storage Locations](#9-storage-locations)
10. [Current Status](#10-current-status)
11. [Session Log](#11-session-log)
12. [Quick Reference Card](#12-quick-reference-card)

---

## 1. `/skillm:` Command Reference

### Syntax

```
/skillm <input>              # Main trigger
skillm <input>               # Without slash (also works)
```

### Supported Actions

| Action | Syntax | Example |
|--------|--------|---------|
| **ingest** | `/skillm <path or URL>` | `/skillm /home/sir-v/MiRA/projects/my-project` |
| **recommend** | `/skillm recommend "task"` | `/skillm recommend "validate SaaS idea"` |
| **index** | `/skillm index` | Re-index all skills |

### Full Examples

```bash
# Local folder → skill
/skillm /home/sir-v/MiRA/projects/my-project

# GitHub → skill
/skillm https://github.com/BUPT-GAMMA/MASFactory

# Vector recommend
/skillm recommend "validate SaaS idea"

# Re-index skills
/skillm index
```

---

## 2. `/skillon:` and `/skillop:` Commands

### Syntax

```
/skillon:notebook-name       # CamelCase variant
/skillon:nb1 + nb2 + nb3    # Multiple notebooks
/skillon:name --force        # Force refresh cache

/skillop:notebook-name       # Lowercase variant (alias)
```

### Examples

```bash
# Single notebook
/skillon:micro-saas

# Multiple notebooks
/skillon:research + competitor-analysis

# Force refresh (bypass cache)
/skillon:my-notebook --force
```

---

## 3. Architecture Diagrams

### End-to-End Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MIRA SKILL MAKER PIPELINE                          │
└─────────────────────────────────────────────────────────────────────────────┘

   ┌─────────┐     ┌─────────────┐     ┌──────────────────────────────────┐
   │  USER   │────▶│ /skillm:   │────▶│    INPUT CLASSIFIER             │
   │ INPUT   │     │ /skillon:  │     │  (URL/Folder/OpenNotebook)      │
   └─────────┘     └─────────────┘     └────────────────┬─────────────────┘
                                                       │
                                                       ▼
   ┌──────────────────────────────────────────────────────────────────────┐
   │                    VIBEGRAPH TWO-PASS SYSTEM                         │
   ├──────────────────────────────────────────────────────────────────────┤
   │                                                                       │
   │   ┌─────────────────────────────────────────────────────────────┐    │
   │   │  PASS 1: PERSONA COUNCIL (6 Perspectives)                    │    │
   │   │                                                             │    │
   │   │  ⚛️ First Principles      ──► What's in here?              │    │
   │   │  🔬 Scientific Method    ──► What patterns exist?          │    │
   │   │  🤔 Philosophical Inquiry ──► What's the purpose?           │    │
   │   │  ✨ Creative Synthesis   ──► How to combine?                │    │
   │   │  ⚙️ Pragmatic Application ──► Will it work?               │    │
   │   │  🌑 Dark Passenger       ──► What could fail?              │    │
   │   └─────────────────────────────────────────────────────────────┘    │
   │                               │                                        │
   │                               ▼                                        │
   │   ┌─────────────────────────────────────────────────────────────┐    │
   │   │  PASS 2: SPECIALIZATION LAYER                              │    │
   │   │                                                             │    │
   │   │  Selected specialist does deep analysis:                  │    │
   │   │  • code_analyzer     • doc_analyzer     • data_analyzer   │    │
   │   │  • config_analyzer   • script_analyzer   • web_analyzer   │    │
   │   └─────────────────────────────────────────────────────────────┘    │
   │                                                                       │
   └──────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    DRAFT OUTPUT     │
                    │ outputs/draft/      │
                    └──────────┬──────────┘
                               │
                               ▼
   ┌──────────────────────────────────────────────────────────────────────┐
   │                    HITL WORKFLOW (Human-In-The-Loop)                │
   │                                                                       │
   │    ┌─────────┐     ┌─────────┐     ┌─────────────┐                   │
   │    │ Approve │────▶│  Move   │────▶│  APPROVED   │                   │
   │    └─────────┘     │ to      │     │  skills/    │                   │
   │                    │ skills/ │     │  <name>/    │                   │
   │    ┌─────────┐     └─────────┘     └─────────────┘                   │
   │    │ Reject  │                                                   │
   │    │ (delete)│                                                   │
   │    └─────────┘                                                   │
   │                                                                       │
   │    ┌─────────┐                                                    │
   │    │  Edit   │────▶ Manual edit then re-approve                   │
   │    └─────────┘                                                    │
   └──────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   AUTO-INDEXED      │
                    │   vectordb/         │
                    └─────────────────────┘
```

### Skill → MIRA Core Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SKILL → MIRA COUNCIL & CABAL FLOW                      │
└─────────────────────────────────────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────────────────────────────────┐
   │                      APPROVED SKILL STRUCTURE                          │
   │  ─────────────────────────────────────────────────────────────────────  │
   │  ---                                                                   │
   │  name:          <skill-name>                                           │
   │  description:   <what it does>                                          │
   │  triggers:      [word1, word2, word3]  ← How agent gets invoked        │
   │  tools:         [tool1, tool2, tool3]  ← What agent can use            │
   │  quality_gates: [gate1, gate2]        ← Acceptance criteria            │
   │  persona:       "<Persona> — <description>"  ← Council mapping        │
   │  mira_tier:     1                                                        │
   │  ---                                                                   │
   │                                                                         │
   │  ## Role                                                               │
   │  ## Hard Rules                                                         │
   │  ## Output Contract                                                    │
   └─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
   ┌─────────────────────────────────────────────────────────────────────────┐
   │                    COUNCIL & CABAL GROUNDING                          │
   │                                                                         │
   │   ┌────────────────────────────────────────────────────────────────┐   │
   │   │  COUNCIL (Strategic Governance)                               │   │
   │   │  • Reviews skill for alignment with MIRA's purpose           │   │
   │   │  • Assigns primary persona                                    │   │
   │   │  • Validates triggers and quality gates                       │   │
   │   │  • council_verdict: "GROUNDED"                               │   │
   │   └────────────────────────────────────────────────────────────────┘   │
   │                                    │                                    │
   │                                    ▼                                    │
   │   ┌────────────────────────────────────────────────────────────────┐   │
   │   │  CABAL (Tactical Execution)                                  │   │
   │   │  • Creates NodeTemplate JSON                                  │   │
   │   │  • Defines invoke_model                                        │   │
   │   │  • Sets quality_gates (runtime validation)                     │   │
   │   │  • Establishes self_anneal_triggers                          │   │
   │   │  • cabal_verdict: "GROUNDED"                                 │   │
   │   └────────────────────────────────────────────────────────────────┘   │
   │                                                                         │
   │   C&C Sign-off (appended to lineage):                                 │
   │   {                                                                   │
   │     "council_verdict": "GROUNDED",                                   │
   │     "cabal_verdict": "GROUNDED",                                     │
   │     "persona_assigned": "First Principles",                          │
   │     "grounding_hash": "<sha256>",                                     │
   │     "signed_at": "<ISO8601>"                                         │
   │   }                                                                   │
   └─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
   ┌─────────────────────────────────────────────────────────────────────────┐
   │                    MIRA CORE 6 PERSONAS                                │
   │                                                                         │
   │   ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │
   │   │ ⚛️ FIRST         │  │ 🔬 SCIENTIFIC     │  │ 🤔 PHILOSOPHICAL │   │
   │   │ PRINCIPLES       │  │ METHOD            │  │ INQUIRY          │   │
   │   ├──────────────────┤  ├──────────────────┤  ├──────────────────┤   │
   │   │ pain-sentry     │  │ pain-scorer      │  │ (reserved)      │   │
   │   │                 │  │ ai-agent-found.  │  │                  │   │
   │   └──────────────────┘  └──────────────────┘  └──────────────────┘   │
   │                                                                         │
   │   ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │
   │   │ ✨ CREATIVE      │  │ ⚙️ PRAGMATIC     │  │ 🌑 DARK PASSENGER│   │
   │   │ SYNTHESIS       │  │ APPLICATION      │  │                  │   │
   │   ├──────────────────┤  ├──────────────────┤  ├──────────────────┤   │
   │   │ arch-synthesiser│  │ opencode-builder │  │ hostile-grounding│  │
   │   │                 │  │ revenue-tracker  │  │ self-anneal-w..  │  │
   │   └──────────────────┘  └──────────────────┘  └──────────────────┘   │
   │                                                                         │
   │   Skills indexed to vectordb/ → Semantic search available            │
   │   /skillm recommend "task" → Matches task to persona-aligned skills  │
   └─────────────────────────────────────────────────────────────────────────┘
```

### Workflow A: Open Notebook → Skill

```
┌────────────────────────────────────────────────────────────────────────────┐
│  WORKFLOW A: Open Notebook → Skill → MIRA Core                          │
└────────────────────────────────────────────────────────────────────────────┘

  1. OPEN NOTEBOOK (http://localhost:8502)
     ┌──────────────────────────────────────────┐
     │  • Add sources (PDF, URL, video)        │
     │  • Chat with AI to extract insights      │
     │  • Sources + Chat → Notebook content     │
     └────────────────────┬─────────────────────┘
                          │
  2. /skillon: <notebook-name>
                          │
                          ▼
  3. VIBEGRAPH PIPELINE
     ┌─────────────────────────────────────────────────────────────┐
     │  • Input: /skillon:my-research                              │
     │  • Classifier: detects open_notebook type                    │
     │  • Fetch: calls Open Notebook API (http://localhost:5055)    │
     │  • Pass 1: Persona Council (⚛️🔬🤔✨⚙️🌑)                   │
     │  • Pass 2: Specialist (doc_analyzer)                        │
     │  • Output: Draft SKILL.md                                   │
     └────────────────────┬────────────────────────────────────────┘
                          │
  4. HITL REVIEW → Approve/Reject/Edit
  5. APPROVED → Indexed to vectordb/
  6. COUNCIL & CABAL GROUNDING → Ready for invocation
```

### Workflow B: Folder → Skill

```
┌────────────────────────────────────────────────────────────────────────────┐
│  WORKFLOW B: Local Folder → Skill → MIRA Core                            │
└────────────────────────────────────────────────────────────────────────────┘

  1. LOCAL FOLDER
     /home/sir-v/MiRA/projects/my-project
     (contains: code, docs, configs)
                          │
  2. /skillm /path/to/folder
                          │
                          ▼
  3. VIBEGRAPH PIPELINE
     ┌─────────────────────────────────────────────────────────────┐
     │  • Classifier: detects folder type                          │
     │  • Scanner: walks directory, aggregates files                │
     │  • Pass 1: Persona Council                                  │
     │  • Pass 2: Specialist (code/doc/data/config_analyzer)      │
     │  • Output: Draft SKILL.md                                   │
     └────────────────────┬────────────────────────────────────────┘
                          │
  [Continue: HITL → Approved → Indexed → Grounded]
```

---

## 4. Skill Locations

### All Skills in `/home/sir-v/MiRA/skills/`

```
/home/sir-v/MiRA/skills/
├── ACCT_Dashboard/
├── active_recall/
├── ai-agent-foundations/           # Persona: 🔬 Scientific Method
├── arch-synthesiser/              # Persona: ✨ Creative Synthesis
├── base-worker/
├── b_line_arsenal/
├── cabal_commander/
├── cabal_spawner/
├── client-delivery/
├── Consensus_Engine/
├── context_compactor/
├── dashboard/
├── email_manager/
├── hostile-grounding/             # Persona: 🌑 Dark Passenger
├── knowledge-base/
├── lab-utility/
├── local-ai-stack/                # Persona: ⚙️ Pragmatic Application
├── mesh_brancher/
├── notebook_bridge/
├── opencode-builder/              # Persona: ⚙️ Pragmatic Application
├── pain-scorer/                   # Persona: 🔬 Scientific Method
├── pain-sentry/                   # Persona: ⚛️ First Principles
├── Project_Affiliate_Synapse/
├── Quest_OpenClaw/
├── revenue-tracker/               # Persona: ⚙️ Pragmatic Application
├── saas-shadow-pro/
├── self-anneal-watchdog/          # Persona: 🌑 Dark Passenger
├── shadow_monetizer/
├── shadow-ops-prover/
├── sovereign_cockpit/
├── sovereign_shadow_operator/
├── srank-pack-generator/          # Persona: ⚙️ Pragmatic Application
├── stream_monitor/
├── topic_sealer/
└── Vector_Mesh/

Total: 35 skills
```

### Persona Mapping

| Persona | Skills |
|---------|--------|
| ⚛️ First Principles | pain-sentry |
| 🔬 Scientific Method | pain-scorer, ai-agent-foundations |
| 🤔 Philosophical Inquiry | (reserved) |
| ✨ Creative Synthesis | arch-synthesiser |
| ⚙️ Pragmatic Application | opencode-builder, revenue-tracker, local-ai-stack, srank-pack-generator |
| 🌑 Dark Passenger | hostile-grounding, self-anneal-watchdog |

---

## 5. Council & Cabal Integration

### Grounding Process

When a skill moves from draft → approved, the Council & Cabal perform grounding:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    COUNCIL & CABAL GROUNDING STEPS                        │
└─────────────────────────────────────────────────────────────────────────────┘

  Step 1: COUNCIL (Strategic Governance)
  ┌───────────────────────────────────────────────────────────────┐
  │ • Review skill alignment with MIRA's purpose                 │
  │ • Assign primary persona (⚛️🔬🤔✨⚙️🌑)                    │
  │ • Validate triggers and quality gates                         │
  │ • Output: council_verdict: "GROUNDED" | "REJECTED"          │
  └───────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  Step 2: CABAL (Tactical Execution)
  ┌───────────────────────────────────────────────────────────────┐
  │ • Create NodeTemplate JSON                                   │
  │ • Define invoke_model (opencode:ollama, gemini-2.5-pro)     │
  │ • Set quality_gates for runtime validation                   │
  │ • Establish self_anneal_triggers                             │
  │ • Output: cabal_verdict: "GROUNDED" | "REJECTED"            │
  └───────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  Step 3: SIGN-OFF (appended to lineage record)
  ┌───────────────────────────────────────────────────────────────┐
  │ {                                                               │
  │   "council_verdict": "GROUNDED",                              │
  │   "cabal_verdict": "GROUNDED",                               │
  │   "grounding_hash": "<sha256 of SKILL.md + policy.json>",    │
  │   "signed_at": "<ISO8601>",                                   │
  │   "persona_assigned": "<First Principles | Scientific ...>", │
  │   "self_anneal_triggers": ["condition1", "condition2"],      │
  │   "upgrade_suggestions": []                                   │
  │ }                                                               │
  └───────────────────────────────────────────────────────────────┘
```

### Skill SKILL.md Structure

```yaml
---
name:          <skill-name>
description:   <what it does>
triggers:      [word1, word2, word3]    # How agent gets invoked
tools:         [tool1, tool2, tool3]    # What agent can use
quality_gates: [gate1, gate2]           # Acceptance criteria
persona:       "<Persona> — <description>"
mira_tier:     1
---

## Role
You are the <role description>.

## Hard Rules
1. Rule 1
2. Rule 2

## Output Contract
<JSON schema or file output format>
```

---

## 6. Open Notebook Tracking

### Current Status

- **Open Notebook**: Running at http://localhost:8502
- **API**: http://localhost:5055
- **Notebooks**: 1 (Test_skill_md_maker)

### Creating Skills Tracker Notebook

To track all skills in Open Notebook for interrogation:

```
1. Create new notebook: "MIRA Skills"
2. Add sources:
   - skills_registry.md (all skills with status)
   - persona_map.md (persona → skills mapping)
3. Chat with AI to query skills
```

### Using Open Notebook to Review Drafts

The recommended workflow for reviewing drafts:

```
1. GENERATE: Run /skillm or /skillon: to create draft
2. ADD TO NOTEBOOK: Open Notebook → Add skills_registry.md as source
3. REVIEW: Chat with notebook:
   - "Summarize the DRAFT_ai-agent-foundations skill"
   - "What triggers does this skill have?"
   - "Is this skill ready for approval?"
4. APPROVE/REJECT:
   python src/draft_workflow.py approve <name> --move-to-skills
   python src/draft_workflow.py reject <name>
5. REGENERATE: Update registry
   python src/draft_workflow.py regenerate
6. UPDATE NOTEBOOK: Refresh sources with new registry
```

### Export Skills to Markdown

```bash
cd /home/sir-v/MiRA/projects/skills_md_maker

# Regenerate skills registry with latest status
python src/draft_workflow.py regenerate

# Export all skills to markdown for adding to Open Notebook
python src/index_skills.py --export ~/docs/skills_index.md

# Or view indexed skills
python src/index_skills.py
```

### Chat Queries for Skills Tracker

Once notebook is set up, ask AI:

```
• "Which skills have First Principles persona?"
• "Show me all skills with tool: sqlite_write"
• "What skills are NOT yet grounded?"
• "Find skills related to revenue tracking"
• "List all skills with trigger: architect"
• "Summarize the draft: local-ai-stack"
```

---

## 7. CLI Tools

### Open Notebook Management

```bash
cd /home/sir-v/MiRA/projects/skills_md_maker

# List all notebooks
python src/ingest_open_notebook.py list

# Find notebook by name
python src/ingest_open_notebook.py find "research"

# Fetch single notebook
python src/ingest_open_notebook.py fetch "my-notebook"

# Fetch multiple notebooks
python src/ingest_open_notebook.py fetch "nb1 + nb2"

# Force refresh cache
python src/ingest_open_notebook.py fetch "nb" --force

# List cached notebooks
python src/ingest_open_notebook.py cached
```

### VibeGraph Runner

```bash
# Run vibegraph directly
python src/vibegraph_runner.py /path/to/folder
python src/vibegraph_runner.py /skillOn:my-notebook
python src/vibegraph_runner.py https://github.com/owner/repo

# With custom skill name
python src/vibegraph_runner.py /skillOn:research --force my-custom-skill
```

### Draft Workflow (NEW)

```bash
cd /home/sir-v/MiRA/projects/skills_md_maker

# Show status of all drafts
python src/draft_workflow.py status

# List all drafts with details
python src/draft_workflow.py list

# Approve draft (moves to outputs/approved/)
python src/draft_workflow.py approve <skill-name>

# Approve AND move to /skills/
python src/draft_workflow.py approve <skill-name> --move-to-skills

# Reject draft (moves to outputs/rejected/)
python src/draft_workflow.py reject <skill-name>

# Edit draft manually
python src/draft_workflow.py edit <skill-name>

# Regenerate skills registry
python src/draft_workflow.py regenerate
```

### Indexing & Search

```bash
# Re-index all skills
python src/indexer.py --reindex

# Manual search
python src/search_skills.py "query text"

# Recommend skills
python src/recommend.py "validate SaaS idea"

# Export skills
python src/index_skills.py --export ~/docs/output.md
---

## 8. How To Guide

### 8.1 Add Skills Registry to Open Notebook

1. Open **http://localhost:8502**
2. Create new notebook or use existing
3. Click **"Add Source"**
4. Select `/home/sir-v/MiRA/docs/skills_registry.md`
5. Click **Save**

### 8.2 Review Drafts via Open Notebook

1. Open notebook with `skills_registry.md` as source
2. Chat with the AI to review drafts:

```
• "Summarize the draft: ai-agent-foundations"
• "What triggers does this skill have?"
• "Is this skill ready for approval?"
• "What persona is assigned to local-ai-stack?"
```

3. Decide: **Approve** or **Reject**

### 8.3 Approve a Draft

```bash
cd /home/sir-v/MiRA/projects/skills_md_maker

# View all drafts
python3 src/draft_workflow.py list

# Approve and move to /skills/
python3 src/draft_workflow.py approve <name> --move-to-skills

# Regenerate registry to reflect changes
python3 src/draft_workflow.py regenerate
```

### 8.4 Reject a Draft

```bash
cd /home/sir-v/MiRA/projects/skills_md_maker

# Reject a draft (moves to outputs/rejected/)
python3 src/draft_workflow.py reject <name>

# Regenerate registry
python3 src/draft_workflow.py regenerate
```

### 8.5 Create a Skill from Open Notebook

```bash
cd /home/sir-v/MiRA/projects/skills_md_maker

# Using /skillon: command (single notebook)
python3 src/vibegraph_runner.py /skillon:my-notebook

# Using /skillon: with multiple notebooks
python3 src/vibegraph_runner.py "/skillon:notebook1 + notebook2"

# Using /skillm: with local folder
python3 src/vibegraph_runner.py /skillm /path/to/folder

# Using /skillm: with GitHub URL
python3 src/vibegraph_runner.py /skillm https://github.com/owner/repo

# Force refresh cache (bypass delta detection)
python3 src/vibegraph_runner.py /skillon:my-notebook --force
```

### 8.6 Query Skills in Open Notebook

Once the registry is added as a source, chat with the AI:

```
• "Which skills have First Principles persona?"
• "Show me all skills with trigger: architect"
• "What tools does pain-sentry have?"
• "Find skills related to revenue tracking"
• "List all skills with tool: sqlite_write"
• "What skills are NOT yet grounded?"
• "Show me the draft: masfactory-vibegraph"
```

### 8.7 Manage Open Notebook

```bash
# List all notebooks
python3 src/ingest_open_notebook.py list

# Find notebook by name
python3 src/ingest_open_notebook.py find "research"

# Fetch single notebook
python3 src/ingest_open_notebook.py fetch "my-notebook"

# Fetch multiple notebooks
python3 src/ingest_open_notebook.py fetch "nb1 + nb2"

# Force refresh cache
python3 src/ingest_open_notebook.py fetch "nb" --force

# List cached notebooks
python3 src/ingest_open_notebook.py cached
```

### 8.8 Indexing & Search

```bash
cd /home/sir-v/MiRA/projects/skills_md_maker

# Re-index all skills to vectordb
python3 src/indexer.py --reindex

# Manual search
python3 src/search_skills.py "query text"

# Recommend skills for a task
python3 src/recommend.py "validate SaaS idea"

# Export skills to markdown
python3 src/index_skills.py --export ~/docs/skills_index.md
```

---

## 9. Storage Locations

```
/home/sir-v/MiRA/
├── skills/                                 # Approved skills (35)
│   ├── pain-sentry/SKILL.md               # ⚛️ First Principles
│   ├── pain-scorer/SKILL.md               # 🔬 Scientific Method
│   ├── arch-synthesiser/SKILL.md          # ✨ Creative Synthesis
│   ├── opencode-builder/SKILL.md          # ⚙️ Pragmatic Application
│   ├── hostile-grounding/SKILL.md         # 🌑 Dark Passenger
│   └── ... (30 more)
│
├── projects/skills_md_maker/
│   ├── outputs/
│   │   ├── draft/                         # DRAFT_* - Pending review
│   │   │   └── DRAFT_*.md                 # (prefixed with DRAFT_)
│   │   ├── pending/                       # In review
│   │   ├── approved/                      # Approved, awaiting move to /skills/
│   │   └── rejected/                      # Rejected drafts
│   ├── references/
│   │   └── open_notebook/                 # Cached notebooks
│   └── vectordb/
│       ├── skills_index.pkl                # Vector embeddings
│       └── skills_meta.json               # Skill metadata (38 indexed)
│
├── docs/
│   ├── skill_maker_reference.md           # This document
│   └── skills_registry.md                # Skills registry with status
```

### Draft Naming Convention

- **Prefix**: `DRAFT_` (e.g., `DRAFT_ai-agent-foundations.md`)
- **Location**: `outputs/draft/`
- **Status**: Marked in registry as "DRAFT - PENDING REVIEW"

---

## 10. Current Status

| Item | Value |
|------|-------|
| Open Notebook | Running at http://localhost:8502 |
| API Endpoint | http://localhost:5055 |
| Approved Skills | 35 |
| Indexed in vectordb | 38 |
| Persona Coverage | All 6 represented |

---

## 11. Session Log

### 2026-03-14: Session 2 - Draft Workflow Automation

**Goal**: Implement programmatic differentiation between drafts and approved skills, and create workflow automation.

**Actions Taken**:

1. **Prefixed drafts with DRAFT_**
   - All drafts now named `DRAFT_*.md` in `outputs/draft/`
   - 6 drafts: ai-agent-foundations, github:bupt-gamma, local-ai-stack, masfactory-vibegraph, notebooklm.google.com, opencode-builder

2. **Created folder structure**
   - `outputs/draft/` - Pending review (DRAFT_*.md)
   - `outputs/pending/` - In review
   - `outputs/approved/` - Approved, awaiting move to /skills/
   - `outputs/rejected/` - Rejected

3. **Created draft_workflow.py** (`src/draft_workflow.py`)
   - Commands: `status`, `list`, `approve`, `reject`, `edit`, `regenerate`
   - Auto-updates registry on approve/reject
   - Optional `--move-to-skills` flag to move directly to /skills/

4. **Created skills_registry.md**
   - Located at `/home/sir-v/MiRA/docs/skills_registry.md`
   - Shows status: APPROVED, DRAFT - PENDING REVIEW
   - Includes 38 approved + 6 drafts

5. **Updated reference document**
   - Added draft workflow section
   - Updated storage locations
   - Added Open Notebook review workflow

---

### 2026-03-14: Session 3 - Bug Fixes & Testing

**Goal**: Fix LSP errors, debug Open Notebook integration, and test end-to-end workflow.

**Actions Taken**:

1. **Fixed LSP type errors**
   - `vibegraph_runner.py`: Fixed `url_type` and `file_index` type hints
   - `ingest_open_notebook.py`: Fixed API return type handling
   - `aggregate_content.py`: Updated `file_index` to allow lists

2. **Fixed notebook classifier**
   - Added `/skillon:` support (lowercase variant) to `src/ingest_url.py`
   - Fixed classifier not recognizing `/skillon:` prefix

3. **Fixed notebook finder**
   - Improved `find_notebook_by_name()` to prefer exact matches over partial matches
   - Fixed issue where "test" notebook was matched before "Test_skill_md_maker"

4. **Fixed empty sources handling**
   - Added graceful handling when notebook has no sources (returns empty list)

5. **Tested end-to-end workflow**
   - Verified `/skillon:` command works: `/skillon:Test_skill_md_maker`
   - Created new draft: `DRAFT_test_skill_md_maker.md`
   - Approved `local-ai-stack` and moved to `/skills/`
   - Regenerated registry

6. **Created draft_workflow.py regeneration command**
   - Auto-updates skills_registry.md with current status
   - Tracks approved vs draft vs rejected

---

### 2026-03-14: Session 1 - Initial Setup

**Goal**: Create comprehensive reference documentation for skill_md_maker and Open Notebook integration.

**Actions Taken**:

1. **Explored codebase** to understand:
   - `/skillm` command parsing in `src/ingest_url.py`
   - `/skillon:` and `/skillop:` support in `src/ingest_open_notebook.py`
   - VibeGraph two-pass system in `src/vibegraph_runner.py`
   - Existing skills in `/home/sir-v/MiRA/skills/`

2. **Identified skill locations**: 35 skills in `/home/sir-v/MiRA/skills/`

3. **Documented persona mapping**:
   - ⚛️ First Principles: pain-sentry
   - 🔬 Scientific Method: pain-scorer, ai-agent-foundations
   - ✨ Creative Synthesis: arch-synthesiser
   - ⚙️ Pragmatic Application: opencode-builder, revenue-tracker, local-ai-stack, srank-pack-generator
   - 🌑 Dark Passenger: hostile-grounding, self-anneal-watchdog

4. **Created this reference document** at `/home/sir-v/MiRA/docs/skill_maker_reference.md`

5. **Open Notebook status**:
   - Running at http://localhost:8502
   - API at http://localhost:5055
   - 1 test notebook: "Test_skill_md_maker"

---

## 12. Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         QUICK REFERENCE                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  WORKFLOW COMMANDS                                                         │
│  ─────────────────                                                         │
│  cd /home/sir-v/MiRA/projects/skills_md_maker                             │
│                                                                             │
│  python3 src/draft_workflow.py status           # Show all drafts          │
│  python3 src/draft_workflow.py list             # List with details       │
│  python3 src/draft_workflow.py approve <name> --move-to-skills            │
│  python3 src/draft_workflow.py reject <name>                             │
│  python3 src/draft_workflow.py regenerate       # Update registry       │
│                                                                             │
│  VIBEGRAPH COMMANDS                                                        │
│  ────────────────                                                          │
│  python3 src/vibegraph_runner.py /skillon:<notebook>                      │
│  python3 src/vibegraph_runner.py /skillm /path/to/folder                  │
│  python3 src/vibegraph_runner.py /skillm https://github.com/owner/repo    │
│                                                                             │
│  OPEN NOTEBOOK                                                             │
│  ────────────                                                              │
│  Web UI:    http://localhost:8502                                         │
│  API:       http://localhost:5055                                         │
│                                                                             │
│  KEY FILES                                                                 │
│  ────────                                                                 │
│  /home/sir-v/MiRA/docs/skill_maker_reference.md   # This document        │
│  /home/sir-v/MiRA/docs/skills_registry.md          # Skills with status   │
│  /home/sir-v/MiRA/skills/                         # Approved skills       │
│  /home/sir-v/MiRA/projects/skills_md_maker/outputs/draft/  # Pending      │
│                                                                             │
│  COMMON QUERIES (Open Notebook Chat)                                       │
│  ────────────────────────────────                                          │
│  • "Which skills have First Principles persona?"                          │
│  • "Show me all skills with trigger: architect"                          │
│  • "Summarize the draft: ai-agent-foundations"                           │
│  • "What tools does pain-sentry have?"                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### To Resume If Session Closes

If this session closes unexpectedly, to resume:

```bash
# 1. Check Open Notebook is running
curl -s http://localhost:5055/api/notebooks

# 2. List drafts
python3 /home/sir-v/MiRA/projects/skills_md_maker/src/draft_workflow.py status

# 3. Regenerate registry
python3 /home/sir-v/MiRA/projects/skills_md_maker/src/draft_workflow.py regenerate

# 4. View reference
cat /home/sir-v/MiRA/docs/skill_maker_reference.md

# 5. View registry
cat /home/sir-v/MiRA/docs/skills_registry.md
```

### Next Steps (If Session Resumes)

1. Add skills_registry.md to Open Notebook as source
2. Test reviewing drafts via notebook chat
3. Approve/reject drafts using workflow script
4. Begin Council & Cabal grounding process
5. Test full flow: notebook → draft → approved → grounded

---

*Document created for MIRA Skill Maker Reference*
*Last updated: 2026-03-14*
