# Lesson 13: Memory for AI Agents

## Introduction

Memory allows agents to retain and recall information, enabling them to be reflective, interactive, proactive, and autonomous.

## Types of Memory

### Working Memory
Scratch paper for immediate task - holds current requirements, decisions, actions.

### Short-Term Memory
Duration of single conversation - maintains context across dialogue turns.

### Long-Term Memory
Persists across sessions - user preferences, historical interactions.

### Specialized Memories
- **Persona Memory**: Consistent personality/role
- **Workflow/Episodic Memory**: Sequence of steps, successes/failures
- **Entity Memory**: Specific entities (people, places, things)

## Implementing Memory

### Specialized Tools

#### Mem0
Persistent memory layer with two-phase pipeline:
1. **Extraction**: LLM summarizes and extracts memories
2. **Update**: LLM determines add/modify/delete

#### Cognee
Semantic memory with dual-store architecture:
- Vector similarity search
- Graph relationships
- Hybrid retrieval combining both

### Memory Pipeline
1. Generate
2. Store
3. Retrieve
4. Integrate
5. Update
6. Forget (delete)

## Self-Improving Agents Pattern

A "knowledge agent" observes main conversation:
1. Identifies valuable information to save
2. Extracts and summarizes
3. Stores in knowledge base
4. Augments future queries with stored info

## Optimizations

- **Latency Management**: Use cheaper model to check if info is worth storing
- **Knowledge Base Maintenance**: Move cold data to cold storage

## MIRA Integration Notes

This lesson directly informs MIRA's:
- **Memory Mesh**: Long-term knowledge storage
- **Vector_Mesh**: Semantic memory and retrieval
- **Active Recall**: Proactive memory surfacing
- **Zettels**: Permanent knowledge artifacts

---
*Source: [Microsoft AI Agents for Beginners - Lesson 13](https://microsoft.github.io/ai-agents-for-beginners/13-agent-memory/)*
