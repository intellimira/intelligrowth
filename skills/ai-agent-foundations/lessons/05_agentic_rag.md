# Lesson 05: Agentic RAG

## Introduction

Agentic RAG is an emerging AI paradigm where large language models (LLMs) autonomously plan their next steps while pulling information from external sources. Unlike static retrieval-then-read patterns, Agentic RAG involves iterative calls to the LLM, interspersed with tool or function calls and structured outputs.

## Key Concepts

### What is Agentic RAG?
- **Iterative Maker-Checker Style**: Loop of iterative calls to LLM interspersed with tool calls
- **Owning the Reasoning Process**: Agent autonomously determines sequence of steps
- **Self-Correction**: Agent can rewrite queries that fail and try different retrieval methods

### The Core Loop
1. **Initial Call**: User's goal presented to LLM
2. **Tool Invocation**: Model selects retrieval methods
3. **Assessment & Refinement**: Model evaluates results
4. **Repeat Until Satisfied**: Cycle continues until high-quality result

### Handling Failure Modes
- Iterate and re-query
- Use diagnostic tools
- Fallback on human oversight

## MIRA Integration Notes

This lesson directly maps to MIRA's:
- **Vector_Mesh Skill**: Agentic RAG pattern for semantic search
- **Memory Mesh**: Long-term memory and retrieval
- **PathRAG**: Dynamic retrieval strategies

## Key Insight
> "The distinguishing quality of an agentic system is its ability to own its reasoning process."

---
*Source: [Microsoft AI Agents for Beginners - Lesson 05](https://microsoft.github.io/ai-agents-for-beginners/05-agentic-rag/)*
