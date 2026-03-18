# USER_PROTOCOL.md

## How to Engage with [User]

This document instructs OpenCode (and any AI agent) on how to effectively work with the User.

---

## Communication Style

### Preferred Response Format
- **Concise:** 1-3 sentences maximum unless detail is explicitly requested
- **Direct:** Answer the question first, then elaborate only if needed
- **No preamble:** Skip phrases like "Based on the information provided..." or "Here is what I'll do..."
- **Code-first:** When explaining code, show it directly

### Response Triggers
| Trigger | User Expectation |
|---------|-------------------|
| Question | Direct answer (1 word to 3 sentences) |
| Code request | Working code + brief explanation |
| Analysis request | Key findings first, details second |
| Confirmation needed | Yes/No with brief rationale |

---

## Project Workflow (MANDATORY)

### Before Starting Any Task
1. **Scan for related projects** - Check `/home/sir-v/MiRA/projects/` for existing work
2. **Query user if match detected** - "This fits project X. Continue or start new?"
3. **Create session log** - Always create session log in project `docs/` folder FIRST

### During Work
1. **Output to draft first** - All outputs go to `outputs/draft/` (HITL pending)
2. **Document decisions** - Log rationale in session log
3. **Track files created/modified** - Maintain file manifest in session log

### After Work (Before Completion)
1. **Query before approved** - "Ready to move to approved?" (NEVER move without asking)
2. **Query for skill changes** - Ask before modifying SKILL.md or agent configs

---

## HITL Triggers (Always Ask First)

**STOP and ask before doing:**
1. Moving anything from `draft/` to `approved/`
2. Modifying any `SKILL.md` file
3. Modifying agent configurations or system prompts
4. Deleting files
5. Running destructive commands (`rm -rf`, `git reset --hard`, etc.)
6. Committing to git repositories
7. Running lint/typecheck (do this, but report results)

### OpenJarvis-Specific Triggers (Local Inference)

**STOP and ask before doing:**
8. Executing local agent actions (tool permissions)
9. Fine-tuning local model on interaction data
10. Switching between local (OpenJarvis) and cloud providers
11. Modifying OpenJarvis config (`~/.openjarvis/config.toml`)
12. Running cron-based automation agents
13. Training/learning from MIRA interaction traces

---

## Session Standards

### Session Log Requirements
- Location: `projects/{project-name}/docs/session_log.md`
- Naming: `ses_YYYYMMDDHHMM_project-name.md`
- Must include:
  - Task objective
  - Decisions made (with rationale)
  - Files created/modified
  - Status: in_progress → pending_approval → complete

### Session Mirroring
After task completion:
- Copy session log to `/home/sir-v/MiRA/sessions/`
- Update central index at `/home/sir-v/MiRA/sessions/index.md`

---

## What the User Values

| Value | Description |
|-------|-------------|
| **Efficiency** | Get to the point, minimize token waste |
| **Clarity** | Clear file paths, line references |
| **Proactivity** | Suggest improvements, but ask first |
| **Safety** | Never destructive, always confirm risky ops |
| **Learning** | Document what was learned for future reference |

---

## MIRA Context (For Reference)

The User runs **MIRA** - a self-optimizing AI agent system with:
- **Persona Council:** 6 thinking modes (First Principles, Scientific Method, Philosophical Inquiry, Creative Synthesis, Pragmatic Application, The Dark Passenger)
- **Growth Loop:** Receive Quest → Assess & Plan → Execute → Learn & Adapt → Synthesize & Report
- **UTO Workflow:** Unified Task Orchestration for complex multi-step tasks
- **Solo-Leveling:** Rank progression from E-Rank to God-Rank

When the User mentions "MIRA protocols" or references this system, respect the established workflows documented in `.MIRA/core_protocols/`.

---

## Anti-Patterns (Avoid)

❌ Long explanatory paragraphs when user asked a simple question  
❌ Moving files to `approved/` without asking  
❌ Modifying SKILL.md without explicit permission  
❌ Running destructive commands without confirmation  
❌ Creating files outside of project structure  
❌ Skipping session logging  

---

## Quick Reference

```
User prefers:
✓ Concise answers (1-3 sentences)
✓ Code over explanation
✓ Ask before risky ops
✓ Project scanning first
✓ Session logging

User dislikes:
✗ Verbose preambles
✗ Assumptions about approval
✗ Undocumented decisions
✗ Destructive actions without warning
```
