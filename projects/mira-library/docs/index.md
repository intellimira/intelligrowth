# MIRA Library Orchestrator

**Project:** MIRA-OJ + The Library Integration  
**Status:** ✅ Active  
**Started:** 2026-03-18

---

## Overview

This project integrates `disler/the-library` meta-skill into MIRA-OJ as an Orchestrator for managing MIRA's skill ecosystem.

## Architecture

```
MIRA-OJ (Orchestrator)
    │
    ├── .mira/library_manager.py     ← Python module
    │
    └── ~/.claude/skills/library/    ← The Library
            ├── SKILL.md
            ├── library.yaml          ← 40 skills cataloged
            └── cookbook/mira-oj/     ← Documentation
```

## Key Features

1. **Catalog-Based Distribution** - Skills stored as references, pulled on demand
2. **Self-Annealing** - Automatic health checks for broken references
3. **Event Notifications** - Email via himalaya to Thunderbird
4. **Dependency Resolution** - Typed dependencies (skill:name, agent:name)

## Components

| Component | Location | Purpose |
|-----------|----------|---------|
| Library Manager | `.mira/library_manager.py` | Core orchestration module |
| Skill Catalog | `~/.claude/skills/library/library.yaml` | 40 skills with dependencies |
| MIRA-OJ Integration | `skills/mira-oj/SKILL.md` | Natural language commands |
| Cookbook | `~/.claude/skills/library/cookbook/mira-oj/orchestrator.md` | Full documentation |

## Commands

```bash
# List all skills
python3 ~/.mira/library_manager.py list

# Self-anneal (health check)
python3 ~/.mira/library_manager.py anneal

# Generate report
python3 ~/.mira/library_manager.py report

# Search skills
python3 ~/.mira/library_manager.py search "revenue"

# Sync all
python3 ~/.mira/library_manager.py sync
```

## Notification Destination

- **Email:** `intellimira@gmail.com`
- **Thunderbird Folder:** `MIRA-OJ Orchestrator/Library Reports`

## Current Status

- ✅ 40 skills cataloged
- ✅ 0 broken references
- ✅ 0 missing dependencies
- ⏳ Gmail/himalaya configuration pending
- ⏳ Private GitHub repo setup pending

## Related Documentation

- Session Log: `sessions/ses_202603181400_mira-library.md`
- Library Cookbook: `~/.claude/skills/library/cookbook/mira-oj/orchestrator.md`
