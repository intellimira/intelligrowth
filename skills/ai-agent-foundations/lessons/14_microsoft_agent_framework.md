# Lesson 14: Microsoft Agent Framework (MAF)

## Introduction

Microsoft Agent Framework is a unified framework for building AI agents with flexibility for various use cases.

## Key Features

### Orchestration Types
- **Sequential**: Step-by-step workflows
- **Concurrent**: Parallel task completion
- **Group Chat**: Collaborative agents
- **Handoff**: Task transfer between agents
- **Magnetic**: Manager agent coordinates subagents

### Production Features
- **Observability**: OpenTelemetry, Microsoft Foundry dashboards
- **Security**: Role-based access, private data handling
- **Durability**: Pause, resume, recover from errors
- **Control**: Human-in-the-loop workflows

### Interoperability
- Cloud-agnostic (containers, on-prem, multi-cloud)
- Provider-agnostic (Azure OpenAI, OpenAI)
- Open standards (A2A, MCP)
- Connectors (Fabric, SharePoint, Pinecone, Qdrant)

## Key Concepts

### Agents
```python
agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    instructions="You are good at recommending trips...",
    name="TripRecommender"
)
```

### Agent Threads
Multi-turn conversations with persistence:
```python
thread = agent.get_new_thread()
response = await agent.run("Where would you like to go?", thread=thread)
```

### Middleware
- **Function Middleware**: Execute between agent and tool calls
- **Chat Middleware**: Execute between agent and LLM requests

### Memory
- In-memory storage
- Persistent messages
- Dynamic memory (Mem0 integration)

### Workflows
- **Executors**: Perform tasks (agents or custom logic)
- **Edges**: Define flow (direct, conditional, switch-case, fan-out/in)
- **Events**: Built-in execution events

## MIRA Integration Notes

This lesson informs MIRA's:
- **Architecture Patterns**: MAF-inspired orchestration
- **OpenJarvis Integration**: Framework compatibility
- **Sovereign Operation**: Durable, recoverable agent state

---
*Source: [Microsoft AI Agents for Beginners - Lesson 14](https://microsoft.github.io/ai-agents-for-beginners/14-microsoft-agent-framework/)*
