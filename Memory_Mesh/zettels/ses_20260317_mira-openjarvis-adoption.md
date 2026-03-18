---
title: "MIRA OpenJarvis Adoption"
type: zettel
tags: [openjarvis, local-ai, inference, privacy, sovereignty]
date: 2026-03-17
---

# MIRA OpenJarvis Adoption

**Date**: 2026-03-17
**Status**: COMPLETED
**Session**: ses_20260317_openjarvis-adoption

## Summary

Adopted Stanford's OpenJarvis framework into MIRA ecosystem, enabling local-first AI inference.

## Key Achievements

| Task | Status |
|------|--------|
| Install OpenJarvis | ✅ |
| Configure provider | ✅ |
| Test local inference | ✅ |
| Cron automation | ✅ |
| Fine-tuning config | ✅ |
| MIRA protocols integration | ✅ |
| Offline mode verified | ✅ |

## Technical Details

### Infrastructure
- **Ollama**: v0.17.7 (installed)
- **Models**: 6 available (qwen3:8b, qwen2.5-coder, etc.)
- **OpenJarvis**: `/home/sir-v/OpenJarvis/`

### Performance
- **Wall time**: ~20-90s (query dependent)
- **TTFT**: ~430ms
- **Throughput**: 6.7-17 tok/s
- **Model**: qwen3:8b (Q4_K_M)

## Files Created

- `/home/sir-v/OpenJarvis/` - Framework
- `/home/sir-v/.openjarvis/config.toml` - Config
- `/home/sir-v/skills/openjarvis/SKILL.md` - Skill
- `/home/sir-v/.mira/openjarvis_integration.md` - Integration

## Protocol Mapping

| MIRA Protocol | OpenJarvis |
|--------------|------------|
| UTO | orchestrator agent |
| Growth Loop | scheduler + traces |
| Persona Council | model selection |
| HITL | Preserved + extended |

## Next Steps

1. Full MIRA protocol integration
2. Telemetry dashboard refinement
3. Offline automation testing

---
*Zettel: MIRA-OpenJarvis-Adoption-001*
