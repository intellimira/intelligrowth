# MIRA-oj: Version Upgrade Notes

> **MIRA → MIRA-oj (OpenJarvis Edition)**
> **Version**: 1.0
> **Date**: 2026-03-17

---

## Version Overview

**MIRA-oj** (MIRA OpenJarvis) is the upgraded version of MIRA, now powered by Stanford's OpenJarvis framework for local-first AI operation.

---

## What's New in MIRA-oj

### Core Capabilities

| Capability | MIRA | MIRA-oj |
|------------|------|----------|
| **Inference** | Cloud API | Local (OpenJarvis + Ollama) |
| **Privacy** | ⚠️ Partial | ✅ Full |
| **Offline** | ❌ No | ✅ Yes |
| **Automation** | ❌ No | ✅ Cron |
| **Self-Improvement** | ❌ No | ✅ Traces |

### Technical Stack

| Component | Implementation |
|----------|---------------|
| Framework | OpenJarvis (Stanford) |
| Engine | Ollama v0.17.7 |
| Models | qwen3:8b, qwen2.5-coder:7b |
| Bridge | `.mira/openjarvis_bridge.py` |

---

## Enhancements Implemented

### HIGH Priority ✅

1. **Local Inference Engine**
   - All reasoning happens locally
   - No data leaves your machine
   - ~30s latency, ~430ms first token

2. **MIRA Bridge**
   - Core integration: `.mira/openjarvis_bridge.py`
   - Persona → Model mapping
   - Privacy-first routing

3. **Protocol Integration**
   - UTO: Updated with OpenJarvis
   - Growth Loop: Trace-driven learning

### MEDIUM Priority ✅

4. **Background Agents**
   - Automation: `.mira/mira_background_agents.py`
   - Cron scheduling ready

5. **HITL Updates**
   - 6 new OpenJarvis-specific triggers
   - Privacy preserved

### LOW Priority 🔶

6. **Telemetry Dashboard**
   - Script created: `skills/openjarvis/telemetry_dashboard.py`
   - UI pending

7. **Self-Improvement**
   - Trace collection enabled
   - Learning policies: sft, icl_updater

---

## Architecture

```
User Query
    ↓
MIRA Protocols (UTO, Growth Loop, Persona Council)
    ↓
MIRA → OpenJarvis Bridge (.mira/openjarvis_bridge.py)
    ↓
Ollama Engine (qwen3:8b, qwen2.5-coder:7b)
    ↓
Local Hardware (No cloud)
```

---

## How to Use

```bash
# Check health
python3 ~/.mira/openjarvis_bridge.py health

# Ask locally
python3 ~/.mira/openjarvis_bridge.py think "Your question"

# Or direct
cd /home/sir-v/OpenJarvis
uv run jarvis ask "Your question"
```

---

## Files Modified

| File | Change |
|------|--------|
| `.MIRA/core_protocols/unified_task_orchestration.md` | Added OpenJarvis |
| `.MIRA/vibe_graph/growth_loop.md` | Added learning |
| `.MIRA/opencode_engagement/USER_PROTOCOL.md` | HITL updates |

---

## Files Created

| File | Purpose |
|------|---------|
| `/home/sir-v/OpenJarvis/` | Stanford framework |
| `/home/sir-v/.openjarvis/config.toml` | Configuration |
| `/home/sir-v/.mira/openjarvis_bridge.py` | Core bridge |
| `/home/sir-v/.mira/mira_background_agents.py` | Automation |
| `/home/sir-v/skills/openjarvis/SKILL.md` | MIRA skill |
| `/home/sir-v/Memory_Mesh/zettels/ses_20260317_mira-openjarvis-adoption.md` | Zettel |

---

## Future Enhancements

| Enhancement | Priority | Notes |
|-------------|----------|-------|
| Fine-tuning training | LOW | Needs more data |
| Telemetry UI | LOW | Web dashboard |
| Full offline test | LOW | Network disconnect |

---

## Version History

| Version | Date | Notes |
|---------|------|-------|
| MIRA | 2026-03-15 | Original (cloud API) |
| **MIRA-oj** | 2026-03-17 | OpenJarvis integration |

---

*Document created: 2026-03-17*
*Upgrade: MIRA → MIRA-oj*
