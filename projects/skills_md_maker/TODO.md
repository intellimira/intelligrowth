# skills_md_maker - Build TODO

## Project Overview
Vibe Graphing skill that ingests URLs or folders, analyzes content via two-pass system (Persona Council + Specialization Layer), generates curated SKILL.md files, and provides vector-based skill inference/recommendations.

## Trigger: `/skillm <URL or folder path>`

---

## ✅ Phase 1: Core Infrastructure

- [x] **1.1** Create `projects/skills_md_maker/SKILL.md` - Main skill definition with `/skillm` trigger
- [x] **1.2** Create `src/ingest_url.py` - URL classifier (YouTube/GitHub/Reddit/Web) + local paths
- [x] **1.3** Create `src/fetch_content.py` - Content fetcher using webfetch/codesearch
- [x] **1.4** Create `src/analyze_content.py` - LLM analyzer to extract triggers, tools, patterns
- [x] **1.5** Create `src/generate_skill.py` - SKILL.md template generator
- [x] **1.6** Create `src/hitl_review.py` - Draft to approved workflow

---

## ✅ Phase 2: Vector Inference System

- [x] **2.1** Create `src/index_skills.py` - Index all skills/ into vectordb/
- [x] **2.2** Create `src/search_skills.py` - Vector similarity search
- [x] **2.3** Create `src/recommend.py` - CLI tool: `/skillm recommend <task>`
- [x] **2.4** Create `src/indexer.py` - Auto-index new approved skills

---

## ✅ Phase 3: Vibe Graphing Two-Pass System

- [x] **3.1** Create `src/ingest_folder.py` - Folder/file scanner
- [x] **3.2** Create `src/aggregate_content.py` - Combine multiple files
- [x] **3.3** Create `src/persona_council.py` - Pass 1: Persona Council (⚛️🔬🤔✨⚙️🌑)
- [x] **3.4** Create `src/specialization_layer.py` - Pass 2: Specialist agents
- [x] **3.5** Create `src/vibegraph_runner.py` - Main orchestrator

---

## ✅ Phase 4: Integration & Testing

- [x] **4.1** Test `/skillm` with sample folder ✅
- [x] **4.2** Test vector search with existing skills ✅
- [x] **4.3** Index existing ~30 skills in skills/ ✅ (32 indexed)
- [x] **4.4** End-to-end test: folder → draft → approved → indexed

---

## 📁 Final Folder Structure
```
projects/skills_md_maker/
├── SKILL.md                    # Main skill definition
├── TODO.md                     # This file
├── src/
│   ├── vibegraph_runner.py      # Main orchestrator (Two-Pass)
│   ├── ingest_url.py           # URL/folder/file classifier
│   ├── ingest_folder.py        # Folder scanner
│   ├── aggregate_content.py    # Content combiner
│   ├── persona_council.py      # Pass 1: Multi-perspective analysis
│   ├── specialization_layer.py # Pass 2: Specialist agents
│   ├── analyze_content.py      # Original LLM analyzer
│   ├── generate_skill.py       # SKILL.md generator
│   ├── hitl_review.py         # HITL workflow
│   ├── index_skills.py         # Vector indexer
│   ├── search_skills.py        # Similarity search
│   ├── recommend.py            # CLI recommendation
│   └── indexer.py             # Auto-index
├── outputs/
│   ├── draft/                 # Pending human review
│   │   └── opencode-builder.md
│   └── approved/              # Final skills (ready to index)
├── references/                # Cached source content
├── vectordb/                  # 32 skills indexed ✅
└── logs/                      # Execution logs
```

---

## 🚀 Usage

### Create skill from folder
```
/skillm /home/sir-v/MiRA/projects/my-project
```

### Create skill from URL
```
/skillm https://github.com/owner/repo
```

### Recommend skills for task
```
/skillm recommend "validate SaaS idea"
```

### Run vibegraph manually
```bash
python src/vibegraph_runner.py /path/to/folder
```

### Index all skills
```bash
python src/indexer.py --reindex
```

---

## Two-Pass Vibe Graphing

### Pass 1: Persona Council
| Persona | Perspective |
|---------|-------------|
| ⚛️ First Principles | Ground truth - What exists? |
| 🔬 Scientific Method | Patterns - What recurs? |
| 🤔 Philosophical Inquiry | Purpose - What should it do? |
| ✨ Creative Synthesis | Integration - How to combine? |
| ⚙️ Pragmatic Application | Validation - Will it work? |
| 🌑 The Dark Passenger | Edge cases - What could fail? |

### Pass 2: Specialists
| Content Type | Specialist | Persona |
|--------------|------------|---------|
| code | code_analyzer | ⚙️ Pragmatic |
| document | doc_analyzer | ✨ Creative |
| data | data_analyzer | 🔬 Scientific |
| config | config_analyzer | 🌑 Dark Passenger |
| script | script_analyzer | ⚙️ Pragmatic |
| web | web_analyzer | ✨ Creative |

---

## Dependencies
- webfetch (built-in)
- codesearch (built-in)
- masfactory.utils.embedding (for vector search)
- masfactory.utils.llm (for LLM analysis)
- TF-IDF fallback available
