# Session Log Template

## Session Header

| Field | Value |
|-------|-------|
| **Session ID** | `ses_YYYYMMDDHHMM_project-name` |
| **Date** | YYYY-MM-DD |
| **User** | [User Name] |
| **Status** | in_progress / pending_approval / complete |

---

## Quest Objective

[One sentence describing what this session aims to accomplish]

---

## Context

### Related Projects
- `/home/sir-v/MiRA/projects/` - Checked: [Yes/No]
- Related project found: [None / Project Name]

### Background
[Brief context from previous sessions or project history]

---

## Decisions & Rationale

| Decision | Rationale |
|----------|-----------|
| [Decision 1] | [Why this approach was chosen] |
| [Decision 2] | [Why this approach was chosen] |

---

## Actions Taken

1. [Action 1]
2. [Action 2]
3. [Action 3]

---

## Files Created/Modified

| File | Action | Description |
|------|--------|-------------|
| `path/to/file.md` | Created | [Description] |
| `path/to/file.py` | Modified | [Description of changes] |

---

## Output Summary

### Draft Outputs
- `outputs/draft/` - [List of draft outputs]

### Pending Decisions
- [ ] [Decision needed from user]

---

## Notes & Learnings

[Any insights, patterns discovered, or areas for improvement]

---

## Next Steps

- [ ] [Next action item]
- [ ] [Follow-up task]

---

## Session Status

- [ ] in_progress
- [ ] pending_approval (awaiting user confirmation)
- [ ] complete

---

## ⚠️ IMPORTANT: Memory Mesh Integration

After session is complete, ALWAYS:

1. **Create zettel** in `/home/sir-v/MiRA/Memory_Mesh/zettels/`:
```markdown
---
title: [Session Title]
date: YYYY-MM-DD
session_id: [Session ID]
project: [Project Name]
type: session
tags: [tag1, tag2]
protocols: [protocol1, protocol2]
---

# [Session Title]

**Session ID:** [Session ID]
**Date:** YYYY-MM-DD

## Summary

[Brief 2-3 sentence summary]

## Key Decisions

- [Decision 1]
- [Decision 2]

## Status

[Complete/Pending]

## Connections

- Related: [Related skill/protocol]
```

2. **Mirror session** to `/home/sir-v/MiRA/sessions/`

3. **Update index** at `/home/sir-v/MiRA/sessions/index.md`
