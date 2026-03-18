# Workflows: Idea → Skill.md

## Quick Validation Workflows

### 1. Rapid Skill Generation (5 min)

```
┌─────────────────────────────────────────────────────────────┐
│  INPUT: Quick idea/notes                                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Open Notebook: Quick Chat Validation                       │
│  - Paste idea                                               │
│  - Ask: "Is this viable? What's missing?"                   │
│  - Ask: "What would make this a skill?"                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  /skillOn:validation-notebook                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  VibeGraph Pipeline                                         │
│  - Pass 1: Persona Council (quick)                          │
│  - Pass 2: Specialist (auto)                                │
│  - Draft: SKILL.md                                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Output: Draft SKILL.md → Review → Approve                  │
└─────────────────────────────────────────────────────────────┘
```

**Use case**: When you have a rough idea and want to quickly see if it's "skill-worthy"

---

### 2. Deep Research Workflow (30 min)

```
┌─────────────────────────────────────────────────────────────┐
│  Open Notebook: Research Phase                              │
│                                                             │
│  1. Add sources:                                           │
│     - Reddit threads (r/microsaas, r/SaaS)                │
│     - YouTube videos                                        │
│     - Articles/blogs                                        │
│     - GitHub repos                                          │
│                                                             │
│  2. Chat exploration:                                       │
│     - "What patterns do I see?"                             │
│     - "What problems are people solving?"                   │
│     - "What tools/approaches work?"                        │
│                                                             │
│  3. Generate insights:                                       │
│     - AI summarization                                      │
│     - Key takeaways                                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  /skillOn:research-notebook                                │
│  /skillOp:source1 + source2 + source3                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  VibeGraph Pipeline (Full)                                 │
│                                                             │
│  - Pass 1: Full Persona Council                            │
│    ⚛️ What exists? (First Principles)                      │
│    🔬 What recurs? (Scientific)                            │
│    🤔 What should it do? (Philosophical)                    │
│    ✨ How combine? (Creative)                               │
│    ⚙️ Will it work? (Pragmatic)                            │
│    🌑 What could fail? (Dark Passenger)                    │
│                                                             │
│  - Pass 2: Specialist Analysis                             │
│    - code_analyzer                                         │
│    - doc_analyzer                                          │
│    - data_analyzer                                         │
│    - config_analyzer                                        │
│                                                             │
│  - Generate: Full SKILL.md                                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Output: Full SKILL.md                                      │
│  - Triggers                                                │
│  - Tools                                                   │
│  - Hard Rules                                              │
│  - Quality Gates                                           │
│  - Workflow                                                │
└─────────────────────────────────────────────────────────────┘
```

**Use case**: Comprehensive skill from extensive research

---

### 3. Multi-Notebook Synthesis

```
┌─────────────────────────────────────────────────────────────┐
│  Notebook A: Problem Space                                  │
│  └─ r/microsaas, r/bootstrapped, pain points              │
│                                                             │
│  Notebook B: Solution Space                                │
│  └─ GitHub repos, tools, frameworks                        │
│                                                             │
│  Notebook C: Validation Space                               │
│  └─ Case studies, success/failure stories                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  /skillOp:problems + solutions + validation              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  VibeGraph: Cross-Notebook Analysis                        │
│  - Combines all sources                                     │
│  - Identifies patterns across domains                       │
│  - Generates integrated skill                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Output: Synthesized SKILL.md                              │
└─────────────────────────────────────────────────────────────┘
```

**Use case**: When you have different aspects in different notebooks

---

### 4. Persona-Aligned Skill Creation

```
┌─────────────────────────────────────────────────────────────┐
│  Target Persona: ⚛️ First Principles                       │
│  (Or any of: 🔬🤔✨⚙️🌑)                                   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Open Notebook: Persona-Focused Research                   │
│                                                             │
│  - Add sources relevant to that perspective                │
│  - Chat: "What are the fundamentals?"                     │
│  - Chat: "What's the underlying principle?"               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  /skillOn:[topic]-foundations                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  VibeGraph: Generate Skill                                 │
│  - Tags: Assign to target persona                           │
│  - Workflow: Persona-specific steps                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Output: Persona-Aligned SKILL.md                          │
│  → Auto-added to that persona's skill library              │
└─────────────────────────────────────────────────────────────┘
```

**Use case**: Building skills specifically for one of the 6 Core Personas

---

### 5. Iterative Refinement

```
┌─────────────────────────────────────────────────────────────┐
│  Round 1: /skillOn:seed-notebook                           │
│  → Draft SKILL.md v1                                       │
│                                                             │
│  Review v1:                                                │
│  - What's missing?                                          │
│  - What needs refinement?                                   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Open Notebook: Add to same notebook                        │
│  - New sources addressing gaps                             │
│  - Chat: "Refine this aspect..."                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Round 2: /skillOn:seed-notebook (cached)                 │
│  → Draft SKILL.md v2 (refined)                            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Repeat until satisfied                                     │
└─────────────────────────────────────────────────────────────┘
```

**Use case**: Building a skill incrementally over time

---

## Recommended First Workflows

### For Testing the Integration

1. **Hello World**: Create simple notebook → `/skillOn:test` → Verify pipeline works

2. **Single Source**: Add one URL/notes → Quick skill → Check output

### For Real Use

1. **Quick Validate**: 
   - Open Notebook: Chat validation
   - `/skillOn:quick-validate` 
   - 5 min → draft skill

2. **Deep Research**:
   - Open Notebook: 1-2 hours research
   - `/skillOp:nb1 + nb2`
   - 30 min → full skill

3. **Multi-Notebook**:
   - Organize by concern (problems, solutions, validation)
   - Synthesize with `+`
   - Cross-pollinate insights

---

## Integration with MIRA Core 6 Personas

| Persona | Workflow Focus |
|---------|----------------|
| ⚛️ First Principles | Foundational knowledge, ground truths |
| 🔬 Scientific | Patterns, data, evidence-based |
| 🤔 Philosophical | Purpose, meaning, should/shouldn't |
| ✨ Creative | Integration, novel combinations |
| ⚙️ Pragmatic | Implementation, will it work |
| 🌑 Dark Passenger | Edge cases, failure modes |

**Idea**: Tag skills by target persona during/after generation for automatic routing to persona libraries.
