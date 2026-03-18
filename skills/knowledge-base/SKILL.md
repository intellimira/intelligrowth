---
name: knowledge-base
description: Central knowledge repository linking .MIRA protocols, Memory Mesh, and skill documentation. Provides unified access to MIRA's knowledge ecosystem.
triggers: [knowledge, docs, protocols, reference, lookup]
tools: [read_file, glob, grep]
quality_gates: [links_valid, content_accessible, index_complete]
persona: "🔬 Scientific Method — organized information retrieval"
mira_tier: 2
---

# knowledge-base

Central knowledge repository for MIRA ecosystem.

## Status

**EARMARKED FOR IMPLEMENTATION**

## Purpose

Unified knowledge interface linking:
- `.MIRA/` core protocols
- `/Memory_Mesh/` zettels
- `/skills/` documentation
- `/projects/` documentation

## Implementation

### Phase 1: Basic (Low Effort)
- Create index of all knowledge locations
- Simple markdown index file
- Manual updates

### Phase 2: Dynamic (Medium Effort)
- Auto-generate index from folder scan
- Link verification
- Search across all knowledge

## Knowledge Map

| Source | Location | Access |
|--------|----------|--------|
| Core Protocols | `.MIRA/core_protocols/` | Direct |
| Vibe Graph | `.MIRA/vibe_graph/` | Direct |
| Sessions | `/sessions/` | Via index |
| Skills | `/skills/*/SKILL.md` | Via index |
| Memory Mesh | `/Memory_Mesh/zettels/` | Via index |

## Index Structure

```markdown
# MIRA Knowledge Index

## Protocols
- [.MIRA/core_protocols/MIRA_Antigravity_Axiom.md](.MIRA/core_protocols/MIRA_Antigravity_Axiom.md)

## Skills
- [skills_md_maker](skills/skills_md_maker/SKILL.md)
- [active_recall](skills/active_recall/SKILL.md)
...

## Memory Mesh
- [zettels/](Memory_Mesh/zettels/)
```

## Integration with active_recall

The knowledge-base can serve as a fallback for active_recall when semantic search fails.
