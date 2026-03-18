---
name: cabal_spawner
description: Spawns autonomous ACCT sub-nodes for parallel task execution. Use when a complex task can be decomposed into independent sub-goals (e.g., analyzing two different repos simultaneously).
---

# Cabal Spawner

The engine for ACCT's distributed reasoning. It creates dedicated environments for "Sub-Nodes" to operate without cluttering the main context.

## Trigger Phrases
- "Spawn a node for..."
- "Parallelize this task..."
- "Create a sub-instance to analyze..."

## Usage
```python
python3 scripts/core.py [label] [node_type] [objective]
```
