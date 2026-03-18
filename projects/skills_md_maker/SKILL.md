---
name: skills_md_maker
description: Vibe Graphing skill that ingests URLs or folders, analyzes content via two-pass system (Persona Council + Specialization Layer), generates curated SKILL.md files, and provides vector-based skill inference/recommendations.
triggers: ["/skillm", "skillm", "create skill from", "extract skill", "generate skill md", "vibegraph", "/ar:optimize", "/ar:benchmark", "/ar:score", "autoresearch", "optimize skill"]
tools: [webfetch, codesearch, websearch, grep, read, glob, write, edit]
quality_gates: [draft_created, human_approved, skill_indexed, quality_score_85_plus]
persona: "✨ Creative Synthesis — pattern extraction and skill synthesis"
mira_tier: 1
---

## Hard Rules
1. Always store raw fetched content in `references/<timestamp>/` before analysis
2. Generate draft in `outputs/draft/<skill-name>.md` for HITL review
3. Only move to approved after human explicitly approves
4. Auto-index approved skills to vectordb/
5. Never overwrite existing skills without human confirmation

## Output Contract
- Draft: `projects/skills_md_maker/outputs/draft/<skill-name>.md`
- Approved: `skills/<skill-name>/SKILL.md`
- Indexed: `projects/skills_md_maker/vectordb/`

## Workflow (Two-Pass Vibe Graphing)

### Pass 1: Persona Council (Broad Analysis)
```
Input: URL or Folder
   ↓
[Input Classifier] → detect URL/folder/file
   ↓
[Content Fetcher] → fetch URL or scan folder
   ↓
[⚛️ First Principles]   → What's in here? (inventory)
[🔬 Scientific Method]   → What patterns exist?
[🤔 Philosophical]      → What's the purpose?
   ↓
Output: Consolidated findings → triggers, tools, patterns, purpose
```

### Pass 2: Specialization Layer (Targeted Expertise)
```
Persona Council Output
   ↓
[Specialist Selection] → code_analyzer | doc_analyzer | data_analyzer | config_analyzer
   ↓
[Specialized Extraction] → Deep-dive on specific type
   ↓
[Skill Synthesis] → Generate SKILL.md
   ↓
[Draft] → outputs/draft/<skill-name>.md
```

### HITL Approval
```
Human reviews draft
Human edits if needed
Human approves → moves to skills/<name>/SKILL.md
Auto-index → vectordb/
```

## Supported Input Types

| Type | Detection | Handler |
|------|-----------|---------|
| URL (web) | `https://*` | webfetch |
| URL (github) | `github.com/*` | codesearch |
| URL (youtube) | `youtube.com/*` | webfetch |
| URL (reddit) | `reddit.com/*` | webfetch |
| Folder | `/path/to/folder` | folder scanner |
| File | `/path/to/file.py` | single file scanner |

## Specialists (Pass 2)

| Content Type | Specialist | Persona |
|--------------|------------|---------|
| code | code_analyzer | ⚙️ Pragmatic Application |
| document | doc_analyzer | ✨ Creative Synthesis |
| data | data_analyzer | 🔬 Scientific Method |
| config | config_analyzer | 🌑 The Dark Passenger |
| script | script_analyzer | ⚙️ Pragmatic Application |
| web | web_analyzer | ✨ Creative Synthesis |

## Inference System

### Indexing
```
/skillm index
```
- Scans skills/ for all SKILL.md files
- Embeds name, description, triggers, tools
- Stores in vectordb/

### Recommendation
```
/skillm recommend "task description"
```
- Embeds task description
- Searches vectordb for top-k similar skills
- Returns ranked list with confidence scores

## Usage Examples

### Create skill from folder
```
/skillm /home/sir-v/MiRA/projects/my-project
```

### Create skill from URL
```
/skillm https://github.com/owner/repo
```

### Recommend skills
```
/skillm recommend "validate SaaS idea"
```

### Index all skills
```
python src/indexer.py --reindex
```

## Auto Research Integration

### Quality Scoring
```
python src/validate_skill.py outputs/draft/
```
- Calculates quality_score (0-100) for SKILL.md files
- Target: 85+ for "production ready"
- Scoring: YAML validity, trigger recall, tool coverage, persona fit, workflow clarity

### Benchmark (10-Run Evaluation)
```
python src/run_benchmark.py outputs/draft/DRAFT_my-skill.md
```
- Per instruct_opencode.md methodology
- Binary (Yes/No) evaluation across 4 criteria
- 10 runs to account for AI "noise"
- Output: 10x4 results matrix in TSV

### Optimization Loop
```
python src/autoresearch_loop.py outputs/draft/DRAFT_my-skill.md --target 85
```
- Autonomous iteration to improve quality_score
- Mutation strategies: trigger_tune, tool_expand, persona_align, hard_rules_add, workflow_refine
- Keeps improvements, discards regressions
- Logs all iterations to research history

### Research History
```
ls outputs/research/
cat outputs/research/my-skill_research.tsv
```
- Location: `outputs/research/`
- Schema: iteration, commit, score, delta, status, description

### OpenCode Commands

| Command | Description |
|---------|-------------|
| `/ar:optimize` | Run Auto Research on target SKILL.md |
| `/ar:benchmark` | Run 10-run benchmark |
| `/ar:score` | Calculate quality score |
| `/ar:status` | Show research history |

## File Structure
```
projects/skills_md_maker/
├── SKILL.md              # This skill
├── src/
│   ├── vibegraph_runner.py    # Main orchestrator
│   ├── ingest_url.py          # URL/file/folder classifier
│   ├── ingest_folder.py       # Folder scanner
│   ├── aggregate_content.py   # Content combiner
│   ├── persona_council.py     # Pass 1: Multi-perspective
│   ├── specialization_layer.py # Pass 2: Specialists
│   ├── generate_skill.py      # SKILL.md generator
│   ├── hitl_review.py         # HITL workflow
│   ├── validate_skill.py      # Quality scoring (Auto Research)
│   ├── run_benchmark.py       # 10-run evaluation (Auto Research)
│   ├── autoresearch_loop.py   # Optimization loop (Auto Research)
│   ├── index_skills.py        # Vector indexer
│   ├── search_skills.py       # Similarity search
│   ├── recommend.py           # CLI recommendation
│   └── indexer.py            # Auto-index
├── outputs/
│   ├── draft/                 # Pending review
│   ├── approved/              # Final skills
│   └── research/              # Research history logs
├── references/                # Cached content
└── vectordb/                 # Skill embeddings
```
