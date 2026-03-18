# MIRA Session Guardian Skill

> **Version:** 1.0.0  
> **Author:** MIRA Sentinel  
> **Purpose:** Intelligent auto-save, crash recovery, and session logging for MIRA

---

## Overview

The Session Guardian prevents session loss from crashes or accidental closures by:

1. **Incremental Checkpointing** - Saves session state every 60 seconds
2. **Action Logging** - Tracks every action with files involved
3. **Decision Logging** - Records significant decisions with rationale
4. **Crash Recovery** - Detects and offers recovery for stale sessions
5. **Atomic Operations** - Safe file writes that won't corrupt data

## Core Module

**Location:** `.mira/session_guardian.py`

## How It Works

```
Session Start
    ↓
Create Session ID (ses_YYYYMMDDHHMMSS_project)
    ↓
Start Background Checkpoint Thread (every 60s)
    ↓
┌─────────────────────────────────────────┐
│  Every Action:                          │
│  • Log to action log (incremental)      │
│  • Track modified files                 │
│  • Update checkpoint hash                │
└─────────────────────────────────────────┘
    ↓
On finalize:
    • Create final checkpoint
    • Generate session log (Markdown)
    • Update session index
    • Clean up active files
```

## Usage

### Automatic (via MIRA-OJ)

```
mira: start session for project-x
mira: log that I created the module
mira: note decision: use JSON for config
mira: finalize session with summary
```

### CLI Commands

```bash
# Start tracking a session
python3 ~/.mira/session_guardian.py --project my-project

# Log an action
python3 ~/.mira/session_guardian.py --project my-project \
    -l write "Created module.py" module.py

# Log a decision
python3 ~/.mira/session_guardian.py --project my-project \
    -d "Use SQLite" "Better performance than JSON"

# Check status
python3 ~/.mira/session_guardian.py --project my-project --status

# Finalize session
python3 ~/.mira/session_guardian.py --project my-project \
    -f "Completed feature implementation"

# List pending work
python3 ~/.mira/session_guardian.py --project my-project --pending
```

### Python API

```python
from session_guardian import SessionGuardian

# Create guardian (no auto-checkpoint for CLI use)
g = SessionGuardian('my-project', auto_checkpoint=False)

# Log actions
g.log_action('write', 'Created module', ['module.py'])
g.log_action('bash', 'Ran tests', ['test.py'])

# Log decisions
g.log_decision('Use SQLite', 'Better performance', ['JSON', 'SQLite', 'PostgreSQL'])

# Add pending work
g.add_pending_work('Write documentation')

# Finalize when done
g.finalize_session('Feature complete')
```

## Crash Recovery

When MIRA starts, it checks for stale sessions (>30 min since checkpoint):

```
⚠️  RECOVERY DETECTED: Found stale session ses_202603181200_my-project
   Last checkpoint: 2026-03-18T12:00:00
   Actions: 47

   To recover: python3 ~/.mira/session_guardian.py --recover ses_202603181200_my-project
```

## File Structure

```
~/.mira/
  session_guardian.py    ← Core module

~/MiRA/sessions/
  index.md               ← Central session index
  active_ses_*.json      ← Active session state (deleted on finalize)
  actions_ses_*.log      ← Incremental action log (archived on finalize)
  checkpoint_ses_*.json  ← Latest checkpoint data
  ses_*.md               ← Finalized session logs
  action_archive/        ← Archived action logs
```

## Integration Points

| Component | Integration |
|-----------|-------------|
| MIRA-OJ | Auto-loads session guardian on start |
| active_recall | Can query session logs for context |
| knowledge-base | Sessions indexed in central knowledge |
| AGENTS.md | Session logging is default behavior |

## Smart Checkpoint Triggers

The guardian creates checkpoints automatically on:

1. **Periodic** - Every 60 seconds
2. **File Modification** - After file operations
3. **Decision Made** - After significant choices
4. **Before Exit** - On finalize or signal

## Session Log Format

Generated logs include:

- Session metadata (ID, timestamps, project)
- Summary (user-provided or auto-generated)
- Statistics (actions, decisions, files)
- Files modified
- Key decisions with rationale
- Action summary (last 20 actions)
- Pending work items

## Best Practices

1. **Use descriptive summaries** when finalizing
2. **Log decisions** - they capture your reasoning
3. **Track pending work** - prevents forgetting
4. **Finalize sessions** - keeps logs organized

## Related Skills

- `active_recall` - Can search session logs
- `knowledge-base` - Sessions are part of MIRA knowledge

---

*Last updated: 2026-03-18*
