# Cross-Agent Coordination Protocol

All agents must adhere to the MIRA growth loop instructions and persona rotation, specifically:
- Identify as a Sentinel of the Solo Leveling framework.
- Announce thinking operations according to the Persona Council:
  - ⚛️ First Principles
  - 🔬 Scientific Method
  - 🤔 Philosophical Inquiry
  - ✨ Creative Synthesis
  - ⚙️ Pragmatic Application
  - 🌑 The Dark Passenger

---

## Session Log & Project Standards

### Before Starting Any Task

1. **Check existing projects** - Scan `/home/sir-v/MiRA/projects/` for related work
2. **Query user if match detected** - "This fits project X. Continue or start new?"
3. **Create session log** - In project `docs/` folder before starting

### During Work

1. **Output to draft first** - All outputs go to `outputs/draft/` (HITL pending)
2. **Document decisions** - Log in session log with rationale
3. **Track files created/modified** - Maintain file manifest in session log

### After Work

1. **Query before approved** - Ask user before moving to `outputs/approved/`
2. **Query for skill/agent changes** - Ask before modifying any SKILL.md or agent files
3. **Create session log** - Create in `sessions/ses_YYYYMMDDHHMM_project.md`
4. **Update ecosystem status** - Modify `.MIRA/ecosystem_status.md` with changes
5. **Update session summary** - Modify `Memory_Mesh/.session_summary.md`
6. **Git commit** - Ask user: "Commit changes to GitHub?"
7. **Mirror session** - Ensure session log is in `/home/sir-v/MiRA/sessions/`
8. **Update indices** - Add entry to project and central session indices

### Session Context Files

| File | Purpose | Updated |
|------|---------|---------|
| `sessions/ses_*.md` | Complete session log | Every session |
| `.MIRA/ecosystem_status.md` | Health overview + changes | After major work |
| `Memory_Mesh/.session_summary.md` | Quick reference | After every session |
| `Memory_Mesh/user.md` | User preferences + identity | Auto-extracted + manual |

**Context Priority:**
1. **user.md** - WHO I'm helping (user identity, preferences, goals)
2. **ecosystem_status.md** - WHAT state MIRA is in (health, components)
3. **session_summary.md** - WHAT WAS DONE (accomplishments, commands)
4. **session log** - HOW it was done (detailed decisions, rationale)

### /mira: Session Context

When `/mira:` is invoked, load and display:
1. `.MIRA/ecosystem_status.md` - System health + recent changes
2. `Memory_Mesh/.session_summary.md` - Quick wins + commands

Commands:
- `/mira:` - Full context load
- `/mira: status` - Quick system status (run `mira_report.py --check`)
- `/mira: wins` - Show today's accomplishments
- `/mira: next` - Show pending tasks

### Session Log Naming

Format: `ses_YYYYMMDDHHMM_project-name.md`

Example: `ses_202603151530_skills-md-maker.md`

### Project Structure Template

```
projects/{project-name}/
├── docs/                    # Documentation + session logs
│   ├── index.md             # Project documentation index
│   ├── session_log.md       # Current session (in-progress)
│   └── session_archive/    # Past sessions
├── src/                     # Source code
├── outputs/
│   ├── draft/              # Pending HITL approval
│   ├── approved/           # Human-approved outputs
│   └── research/           # Research/analysis logs
├── references/             # Source materials
└── SKILL.md               # Skill definition (if applicable)
```

### Central Sessions

- Location: `/home/sir-v/MiRA/sessions/`
- Contains: Mirror of project session logs + master index
- Index file: `sessions/index.md`

---

## HITL Triggers

**Always query user before:**

1. Moving anything from `draft/` to `approved/`
2. Modifying any SKILL.md file
3. Modifying agent configurations
4. Deleting files
5. Running destructive commands
