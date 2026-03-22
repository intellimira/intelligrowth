# Lesson 12: Context Engineering for AI Agents

## Introduction

Context Engineering is the practice of ensuring AI Agents have the right information to complete tasks. It's about managing a dynamic set of information in a limited context window.

## Prompt vs Context Engineering

| Prompt Engineering | Context Engineering |
|-------------------|---------------------|
| Single static instructions | Dynamic information management |
| Fixed rules | Repeatable and reliable processes |
| One-time setup | Ongoing management |

## Types of Context

1. **Instructions**: Prompts, system messages, few-shot examples, tool descriptions
2. **Knowledge**: Facts, database info, long-term memories
3. **Tools**: Function definitions, API schemas, MCP servers
4. **Conversation History**: Ongoing dialogue
5. **User Preferences**: Learned likes/dislikes

## Strategies

### Planning Strategies
1. Define clear results
2. Map the context (what info needed?)
3. Create context pipelines

### Practical Strategies
- **Agent Scratchpad**: Notes during single session
- **Memories**: Cross-session information
- **Compressing Context**: Summarization, trimming
- **Multi-Agent Systems**: Separate context windows per agent
- **Sandbox Environments**: Run code externally
- **Runtime State Objects**: Containers for subtask results

## Common Context Failures

### Context Poisoning
Hallucinated info entered context, causing wrong actions.
**Solution**: Validation and quarantine before adding to memory

### Context Distraction
Large context causes model to focus on history over training.
**Solution**: Context summarization, periodic compression

### Context Confusion
Too many tools causes model to call irrelevant ones.
**Solution**: Tool loadout management with RAG (limit to <30 tools)

### Context Clash
Conflicting info in context causes inconsistent reasoning.
**Solution**: Context pruning, scratchpad workspace

## MIRA Integration Notes

This lesson directly informs MIRA's:
- **Topic Sealer**: Consolidating reasoning
- **Memory Mesh**: Context management across sessions
- **Context Compactor**: Lean context maintenance

---
*Source: [Microsoft AI Agents for Beginners - Lesson 12](https://microsoft.github.io/ai-agents-for-beginners/12-context-engineering/)*
