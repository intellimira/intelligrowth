---
name: notebook_bridge
description: Programmatically interacts with Google NotebookLM for ingestion, authoring, and presentation (audio/slides). Use to bridge local ACCT context with Google's high-fidelity cognitive tools.
---

# NotebookLM Bridge

Enables ACCT to utilize external NotebookLM workbooks as "Cognitive Accelerators."

## Trigger Phrases
- "Sync with NotebookLM..."
- "Create a notebook for this project..."
- "Extract data from notebook ID..."
- "Generate an audio overview for..."

## Core Workflow
1.  **Auth Sync:** Uses established session tokens in ~/.notebooklm/.
2.  **Context Mapping:** Map local Zettels to external sources.
3.  **RPC Execution:** Direct backend communication for fast ingestion/authoring.

## Usage
- List notebooks: `notebooklm list`
- Use notebook: `notebooklm use [ID]`
- Add source: `notebooklm source add [PATH]`
- Summary: `notebooklm summary`

---
**Status:** VAULTED (v1.0)
**Tier:** 3-Tier Production
