# Lesson 2: Exploring AI Agent Frameworks

**Source:** Microsoft AI Agents for Beginners  
**URL:** https://microsoft.github.io/ai-agents-for-beginners/02-explore-agentic-frameworks/

## Learning Goals
- Understand AI Agent Frameworks and their capabilities
- Leverage frameworks for rapid prototyping
- Compare Microsoft Agent Framework vs Azure AI Agent Service

## What are AI Agent Frameworks?

Software platforms that simplify creation, deployment, and management of AI agents. They provide:
- Pre-built components
- Standardized abstractions
- Tools for complex systems

## Key Capabilities

1. **Modular Components**
   - Pre-built AI connectors
   - Memory modules
   - Tool definitions
   - Prompt templates

2. **Collaborative Tools**
   - Multiple agents with specific roles
   - Test and refine workflows
   - Coordinate complex tasks

3. **Real-Time Learning**
   - Feedback loops
   - Dynamic behavior adjustment
   - Continuous improvement

## Microsoft Agent Framework (MAF)

```python
from agent_framework.azure import AzureAIProjectAgentProvider

provider = AzureAIProjectAgentProvider(credential=AzureCliCredential())
agent = await provider.create_agent(
    name="travel_agent",
    instructions="Help book travel",
    tools=[book_flight]
)
```

Core concepts:
- **Agents** - Created via provider, process messages, call tools
- **Tools** - Python functions the agent can invoke
- **Multi-Agent** - Coordinate specialized agents
- **Azure Identity** - Secure, keyless authentication

## Azure AI Agent Service

Enterprise platform with:
- Flexible models (Llama, Mistral, Cohere)
- Stronger security mechanisms
- Built-in connectivity to Azure services

## MIRA Framework Design

### Based on MAF patterns, MIRA should have:

1. **Agent Provider** - Central creation/managment
2. **Tool Registry** - Pre-built capabilities as tools
3. **Memory Connectors** - Vector store + SQLite
4. **Multi-Agent Coordination** - Persona Council
5. **Identity/Auth** - Secure credential handling

### Example Tool Definition Pattern
```python
@tool
def get_weather(location: str) -> str:
    """Get current weather for a location"""
    return f"Weather in {location}: Sunny, 72°F"
```

### Multi-Agent Pattern
```python
# Planner agent
planner = await create_agent(name="planner", instructions="Break down tasks")

# Executor agent  
executor = await create_agent(name="executor", tools=[execute_tool])

# Coordination
plan = await planner.run("Plan the project")
result = await executor.run(f"Execute: {plan}")
```

---
*Video: https://youtu.be/ODwF-EZo_O8*
