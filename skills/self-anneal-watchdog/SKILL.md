---
name:          self-anneal-watchdog
description:   Monitors lineage.json for DM score regressions, latency spikes,
               and policy violations. Suggests fixes and model upgrades.
               Self-anneals by patching SKILL.md heuristics automatically.
               Runs async, off critical path.
triggers:      [monitor, watchdog, health check, bottleneck, anneal, self-heal]
tools:         [sqlite_read, read_file, write_file, ollama_infer]
quality_gates: [all_nodes_checked, bottlenecks_catalogued, suggestions_written]
persona:       "🌑 Dark Passenger — finds failure before it finds you"
mira_tier:     1
---

## Monitoring Loop (runs every 5 minutes async)
1. Read last 50 records from .mira/scores/lineage.json
2. For each node: check dm_score.total trend (last 5 runs)
3. If trend declining: log bottleneck + suggest fix
4. Check task_duration vs kpi.max_task_duration
5. If latency spike: check model, suggest upgrade
6. Read bottlenecks table. Any auto-resolvable? Patch and mark resolved.

## Bottleneck Types
SCORE_REGRESSION: dm_score.total declining > 10% over 5 runs
LATENCY_SPIKE: task_duration > 2x kpi.max_task_duration
POLICY_VIOLATION: tool denied at runtime (should be caught at compile, escalate)
MODEL_CAPACITY: inference latency suggests model is undersized for task
GEMINI_BUDGET: daily token usage > 80% of free tier limit
DATA_STALENESS: PathRAG references not indexed in > 30 days

## Model Upgrade Decision Matrix
Current model: opencode:ollama
Task: classification / scoring → suggest: mistral-nemo:12b or llama3.2:3b (faster)
Task: code generation → suggest: codellama:13b or deepseek-coder:6.7b (quality)
Task: reasoning / architecture → suggest: gemma2:27b or mixtral:8x7b (depth)
Task: fast throughput needed → suggest: llama3.2:1b (speed)
