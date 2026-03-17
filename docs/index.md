# MIRA Portfolio

> Multi-section portfolio showcasing Business, Agents, and emerging What-If projects

---

## Current Version: MIRA-oj (OpenJarvis Edition)

> **MIRA → MIRA-oj** - Upgraded on 2026-03-17

**What's New**:
- Local-first AI (no cloud dependencies)
- Privacy-preserving inference
- Cron-based automation
- Self-improving system

---

## Sections

| Section | Description | Status |
|---------|-------------|--------|
| **Business** | Shadow Ops, client projects, revenue-generating solutions | Building |
| **Agents** | Technical AI agent work, MIRA system, skills | Building |
| **What-If** | Emerging ideas from project gleans (draft portfolio pieces) | Planning |

---

## MIRA-oj (OpenJarvis) Project

| Attribute | Details |
|-----------|---------|
| **Name** | MIRA-oj: OpenJarvis Integration |
| **Description** | Stanford's OpenJarvis framework integrated with MIRA for local-first AI operation |
| **Status** | ✅ Complete |
| **Features** | Local inference, privacy-first, automation, self-improvement |

### Quick Commands

```bash
# Health check
python3 ~/.mira/openjarvis_bridge.py health

# Ask locally
python3 ~/.mira/openjarvis_bridge.py think "Your question"
```

---

## Workflow

1. Projects in `/home/sir-v/MiRA/projects/` are scanned
2. Each project has `publish: true/false` in `docs/index.md` (HITL-controlled)
3. GitHub Action auto-generates portfolio on push
4. Only `publish: true` projects appear on live site

---

## Live Site

**URL**: https://intellimira.github.io/mira-portfolio/

---

*Project started: 2026-03-16*
