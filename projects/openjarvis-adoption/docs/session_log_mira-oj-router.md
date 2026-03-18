# Session Log: MIRA-oj Router (The Weave)

> **Date**: 2026-03-17
> **Project**: MIRA-oj Router / The Weave
> **Mode**: Build
> **Status**: In Progress

---

## Session Overview

**Objective**: Implement intelligent routing layer that learns from interaction data to choose between local (OpenJarvis) and cloud inference.

**User's Vision**: Modify the invoke "/mira:" or "mira:" to default to MIRA-oj, letting OpenJarvis choose what to use - local or online - depending on what MIRA-oj learns through use (The Weave).

---

## C&C Analysis Applied

| Persona | Contribution |
|---------|--------------|
| ⚛️ First Principles | Core purpose: intelligent, learning-based routing |
| 🔬 Scientific Method | Reliable fallback, measurable outcomes |
| 🤔 Philosophical | Privacy-first, human-in-loop preserved |
| ✨ Creative | Meta-learning from interaction data |
| ⚙️ Pragmatic | Simple SQLite-based learning |
| 🌑 Dark Passenger | Error handling, graceful degradation |

---

## Todo List

- [ ] Phase 1: Enable 'mira:' trigger in OpenJarvis SKILL.md
- [ ] Phase 2: Build MIRARouter class with intelligent routing
- [ ] Phase 3: Create Weave SQLite database for interaction tracking
- [ ] Phase 4: Implement learning algorithm (rule refinement)
- [ ] Phase 5: CLI dashboard for routing stats

---

## Files Modified/Created

| File | Change | Description |
|------|--------|-------------|
| `skills/openjarvis/SKILL.md` | MODIFIED | Added 'mira:' trigger |
| `.mira/openjarvis_bridge.py` | MODIFIED | Added MIRARouter class |
| `.mira/weave.db` | CREATED | SQLite interaction tracking |
| `.mira/weave_router.py` | CREATED | New intelligent router module |

---

## Key Decisions

1. **Trigger**: Use keyword trigger "mira:" (not slash command) for natural conversation
2. **Learning**: Simple rule refinement based on success/failure outcomes
3. **Storage**: SQLite for local-first, privacy-preserving interaction history
4. **Override**: Users can force local/cloud with flags

---

## Session Log

### 2026-03-17 00:XX - Implementation Started

**Phase 1**: Adding 'mira:' to skill triggers
**Phase 2**: Building MIRARouter class

---

*Session started: 2026-03-17*
*Document status: IN_PROGRESS*
