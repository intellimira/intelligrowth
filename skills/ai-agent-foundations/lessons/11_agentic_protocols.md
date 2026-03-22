# Lesson 11: Agentic Protocols (MCP, A2A, NLWeb)

## Introduction

As AI agents grow, protocols ensure standardization, security, and open innovation.

## Model Context Protocol (MCP)

Open standard for applications to provide context and tools to LLMs.

### Core Components
- **Hosts**: LLM applications that start connections
- **Clients**: Components maintaining connections with servers
- **Servers**: Lightweight programs exposing capabilities

### Three Primitives
1. **Tools**: Discrete actions/functions (e.g., get weather)
2. **Resources**: Read-only data (files, database records)
3. **Prompts**: Predefined templates

### Benefits
- Dynamic tool discovery
- Interoperability across LLMs
- Standardized security

## Agent-to-Agent Protocol (A2A)

Enables communication between different AI agents.

### Components
- **Agent Card**: Name, description, skills, endpoint URL
- **Agent Executor**: Passes context to remote agent
- **Artifact**: Result of agent's work
- **Event Queue**: Handles updates and messages

### Benefits
- Enhanced collaboration across vendors
- Model selection flexibility per agent
- Built-in authentication

## Natural Language Web (NLWeb)

Brings natural language interfaces to websites.

### Components
- **NLWeb Application**: Core processing engine
- **NLWeb Protocol**: Basic rules for natural language interaction
- **MCP Server**: Shares tools and data
- **Embedding Models**: Convert content to vectors
- **Vector Database**: Stores embeddings

## MIRA Integration Notes

This lesson directly informs MIRA's:
- **MCP Compatibility**: Future MCP integration
- **A2A Patterns**: Agent-to-agent communication
- **Vector_Mesh**: Semantic search infrastructure

## Key Insight
> MCP connects LLMs to tools; A2A connects agents to agents; NLWeb connects agents to web content.

---
*Source: [Microsoft AI Agents for Beginners - Lesson 11](https://microsoft.github.io/ai-agents-for-beginners/11-agentic-protocols/)*
