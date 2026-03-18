---
name: active_recall
description: Proactively surfaces relevant historical context, Zettels, and logic-streams from the ACCT Memory Mesh and MIRA manifest. Use when starting a new Quest, exploring legacy documentation, or whenever "deep memory" is required.
---

# Active Recall

The primary "Optic Nerve" for the ACCT Second Brain. This skill enables the AI to "remember" by scanning hundreds of local files for semantic keywords and entities relevant to the current task.

## Trigger Phrases
- "Recall relevant context for..."
- "What do we know about..."
- "Scan the manifest for..."
- "Initialize Active Recall Pulse"

## Core Workflow
1.  **Semantic Keying:** Identify high-signal terms in the user prompt (e.g., project names, protocol IDs, specific personas).
2.  **Manifest Search:** Execute the `core.py` script to scan `/Knowledge_Base/` and `/Memory_Mesh/`.
3.  **Result Ranking:** Review the top 5 ranked "Memory Sparks."
4.  **Synthesis:** Integrate the discovered context directly into the reasoning stream.

## Usage
```python
# Internal invocation via UTO
python3 scripts/core.py [term1] [term2]
```

---
**Status:** VAULTED (v1.1)
**Tier:** 3-Tier Progressive Disclosure
**Related:** [[ACCT_PROTOCOL_HUB]], [[ACCT_Semantic_Weave]]
