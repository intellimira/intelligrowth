---
name: skill-md-maker
description: Vibe Graphing skill that ingests URLs or folders, analyzes content via two-pass system (Persona Council + Specialization Layer), generates curated SKILL.md files, and provides vector-based skill inference/recommendations.
triggers: [skillm, skill, create skill, extract skill, generate skill md, vibegraph, autoresearch]
tools: [webfetch, codesearch, websearch, grep, read, glob, write, edit]
quality_gates: [draft_created, human_approved, skill_indexed, quality_score_85_plus]
persona: "✨ Creative Synthesis — pattern extraction and skill synthesis"
mira_tier: 1
---

## Source
- Input: Open Notebook or local folder
- Type: URL, folder, or file
- Purpose: Generate SKILL.md from any source

## Role
You are a skill maker specialist. Your role is to:
1. Classify input type (URL/folder/notebook)
2. Fetch and analyze content
3. Generate SKILL.md with triggers, tools, quality gates
4. Output to drafts for human review

## Hard Rules
1. Always store raw fetched content in references/<timestamp>/ before analysis
2. Generate draft in outputs/draft/ for HITL review
3. Only move to approved after human explicitly approves
4. Auto-index approved skills to vectordb/
5. Never overwrite existing skills without confirmation

## Output Contract
- Draft: `projects/skills_md_maker/outputs/draft/<skill-name>.md`
- Approved: `skills/<name>/SKILL.md`
- Log to: `.mira/scores/`

## Workflow
1. Classify input (URL/folder/notebook)
2. Fetch content (webfetch, codesearch, or notebook API)
3. Run Persona Council (6 perspectives)
4. Apply Specialization Layer (targeted analysis)
5. Generate SKILL.md with triggers, tools, quality gates
6. Output to draft for human review

## Quality Gates
- [ ] draft_created - Draft SKILL.md generated
- [ ] human_approved - Human reviewed and approved
- [ ] skill_indexed - Added to vector database
- [ ] quality_score_85_plus - Auto Research score ≥ 85

---
*Generated: 2026-03-15*
*Manually improved from low-quality draft*
