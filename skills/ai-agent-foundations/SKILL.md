---
name: ai-agent-foundations
description: Comprehensive skill covering AI agent fundamentals, capabilities, architecture patterns, and implementation across education and enterprise workflows.
triggers: [ai-agent, agentic-ai, autonomous-agents, multi-agent, workflow-automation, llm-agents, agent-architecture, agent-implementation]
tools: [llm_infer, tool_calling, memory_management, orchestration_layer, rag_retrieval]
quality_gates: [agent_defined, tools_registered, memory_configured, workflow_validated]
persona: "🔬 Scientific Method — pattern extraction and systematic analysis"
mira_tier: 1
---

## Source Content Chained
1. 8allocate.com - Agentic AI in Education (use cases, implementation playbook)
2. Jotform - What are AI Agents (definition, capabilities)
3. Analytics Vidhya - LLM Workflow for Developers
4. Multiple ResearchGate sources on AI in enterprise/education
5. **Microsoft AI Agents for Beginners** - 14 lessons on agent frameworks, patterns, production

## What is an AI Agent?

An AI agent is **autonomous software** that:
- **Perceives** environment and inputs
- **Reasons** using LLMs for planning
- **Acts** using tools and APIs
- **Remembers** state across interactions
- **Iterates** until goal is achieved

### Agent vs Chatbot vs Copilot

| Capability | Chatbot | Copilot | AI Agent |
|------------|---------|---------|----------|
| Responds to prompts | ✅ | ✅ | ✅ |
| Handles simple tasks | ❌ | ✅ | ✅ |
| Suggests next steps | ❌ | ✅ | ✅ |
| **Plans autonomously** | ❌ | ❌ | ✅ |
| Uses external tools | ❌ | ❌ | ✅ |
| Maintains memory | ❌ | Partial | ✅ |

## Core Agent Architecture

### The Agent Loop
```
Perceive → Reason → Plan → Act → Observe → Repeat
```

### Key Components
1. **LLM Brain** - Reasoning, planning, decision-making
2. **Tools** - APIs, functions, code execution
3. **Memory** - Short-term (conversation), long-term (vector store)
4. **Orchestration** - Multi-step coordination, state management
5. **Guardrails** - Safety constraints, human oversight

### Agent Types (by Capability Level)

1. **Simple Reflex Agents** - Rule-based, no memory
2. **Model-Based Agents** - Maintain world model
3. **Goal-Based Agents** - Plan toward objectives
4. **Utility-Based Agents** - Optimize for outcomes
5. **Learning Agents** - Improve from experience
6. **Multi-Agent Systems** - Coordinate multiple specialized agents

## Multi-Agent Orchestration

### Why Multi-Agent?
- 70% of multi-agent systems by 2027
- Specialized agents for different tasks
- Parallel execution for speed
- Fault tolerance through redundancy

### Orchestration Patterns
- **Sequential** - Agent A → Agent B → Agent C
- **Parallel** - Agent A, B, C run simultaneously, merge results
- **Hierarchical** - Manager agent delegates to sub-agents
- **Swarm** - Dynamic collaboration based on task

## Agentic AI in Education

### Use Cases
1. **Personalized Learning Paths** - Adaptive content based on student progress
2. **Autonomous Tutoring** - 24/7 coaching and feedback
3. **Student Retention** - Early intervention when students struggle
4. **Administrative Automation** - Scheduling, grading, communications
5. **Content Generation** - Lesson plans, assessments, materials

### Implementation Architecture
```
Student Input → Agent Router → [Retriever Agent | Tutor Agent | Evaluator Agent] 
    ↓
[Human-in-the-Loop: Teacher Review] ← Feedback
    ↓
Output → Student
```

### Key Insights
- Teachers evolve to **orchestrators** of AI agents
- Human oversight remains critical
- Agent must flag when human intervention needed
- Cost range: $50K-$250K development, $4K-$25K/month run

## Enterprise Workflow Patterns

### LLM Agent Stack
```
┌─────────────────────────────────────┐
│         User Request                │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│      Planning Agent                  │
│  (decomposes task, creates plan)    │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│    Tool Execution Layer              │
│  (API calls, code, RAG, etc.)       │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│       Memory/Context                │
│  (conversation + vector store)       │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│         Response                     │
└─────────────────────────────────────┘
```

### Common Frameworks
- **LangChain/LangGraph** - Python orchestration
- **CrewAI** - Multi-agent role-playing
- **AutoGen** - Microsoft multi-agent
- **MASFactory** - Graph-centric (Vibe Graphing)
- **PydanticAI** - Production-grade, type-safe

## Hard Rules

1. **Always have exit conditions** - Prevent infinite loops
2. **Implement guardrails** - Safety constraints before deployment
3. **Human-in-the-loop** - Critical for high-stakes decisions
4. **Token budgets** - Control costs, prevent runaway usage
5. **Graceful failures** - Agents must fail predictably

## Quality Gates

- [ ] agent_defined - Clear role and objectives
- [ ] tools_registered - All capabilities exposed as tools
- [ ] memory_configured - Short + long term memory
- [ ] guardrails_active - Safety constraints in place
- [ ] workflow_validated - Tested end-to-end
- [ ] cost_budgeted - Token usage limits set

## Implementation Checklist

### Phase 1: Foundation
- [ ] Select LLM (GPT-4, Claude, Gemini)
- [ ] Define agent role/persona
- [ ] Register core tools

### Phase 2: Memory
- [ ] Conversation history
- [ ] Vector store for context
- [ ] Preference memory

### Phase 3: Orchestration
- [ ] Multi-step planning
- [ ] Tool selection logic
- [ ] Error handling

### Phase 4: Safety
- [ ] Guardrails
- [ ] Human override
- [ ] Audit logging

### Phase 5: Production
- [ ] Monitoring
- [ ] Cost tracking
- [ ] Performance metrics

## LearnAgents.dev Integration

### Course: Build First AI Agent in 60 Minutes

**Access:** https://learnagents.dev/lessons/introduction  
**Email:** intellimira@gmail.com  
**Note:** Site is client-side rendered - requires manual browser signup

#### Lessons (Pending Extraction)
| # | Lesson | MIRA Integration |
|---|--------|-----------------|
| 01 | What are AI Agents | Core concepts |
| 02 | Agent Architecture | PRPAL loop |
| 03 | Tools and Tool Calling | MIRA-OJ tool system |
| 04 | Memory and State | Memory Mesh |
| 05 | Planning and Reasoning | Persona Council |
| 06 | Multi-Agent Systems | ACCT multi-node |
| 07 | Production Considerations | Monitoring/logging |
| 08 | What's Next | Roadmap |

### Extracted Patterns

#### PRPAL Loop (LearnAgents)
```
Perceive → Reason → Plan → Act → Learn
```

Every agent follows this loop. MIRA implements:
- **Perceive**: User input + Memory context
- **Reason**: Persona Council deliberation
- **Plan**: Task decomposition
- **Act**: Tool execution
- **Learn**: Weave updates + training

---

## Microsoft AI Agents Course

**Source:** https://microsoft.github.io/ai-agents-for-beginners/  
**Format:** 14 lessons + code samples (Python, .NET)  
**Framework:** Microsoft Agent Framework (MAF)

### Course Curriculum (All 14 Lessons Extracted)

| # | Lesson | MIRA Integration | File |
|---|--------|------------------|------|
| 01 | Intro to AI Agents | Core concepts, agent types | `lessons/01_intro_to_ai_agents.md` |
| 02 | Exploring AI Agentic Frameworks | MAF patterns | `lessons/02_agentic_frameworks.md` |
| 03 | AI Agentic Design Principles | Design patterns | `lessons/03_agentic_design_patterns.md` |
| 04 | Tool Use Design Pattern | Function calling | `lessons/04_tool_use_design_pattern.md` |
| 05 | Agentic RAG | Vector_Mesh, PathRAG | `lessons/05_agentic_rag.md` |
| 06 | Building Trustworthy AI Agents | Security, trust | `lessons/06_building_trustworthy_agents.md` |
| 07 | Planning Design Pattern | Task decomposition | `lessons/07_planning_design_pattern.md` |
| 08 | Multi-Agent Design Patterns | Cabal spawner/commander | `lessons/08_multi_agent_patterns.md` |
| 09 | Metacognition in AI Agents | Self-anneal watchdog | `lessons/09_metacognition.md` |
| 10 | AI Agents in Production | Observability, eval | `lessons/10_ai_agents_production.md` |
| 11 | Agentic Protocols (MCP, A2A, NLWeb) | Future MCP support | `lessons/11_agentic_protocols.md` |
| 12 | Context Engineering | Context compactor | `lessons/12_context_engineering.md` |
| 13 | Managing Agent Memory | Memory Mesh | `lessons/13_agent_memory.md` |
| 14 | Microsoft Agent Framework | MAF patterns | `lessons/14_microsoft_agent_framework.md` |

### Key Takeaways from Microsoft Course

#### Agentic Design Principles
1. **Transparency** - Inform user AI is involved
2. **Control** - Enable customization
3. **Consistency** - Multi-modal experiences

#### Agentic RAG Pattern
- Iterative maker-checker style
- Self-correction capabilities
- Tool integration for retrieval

#### Multi-Agent Patterns
- Group chat, handoff, collaborative filtering
- Agent communication protocols
- Visibility and monitoring

#### Context Engineering Failures
| Failure | Solution |
|---------|----------|
| Poisoning | Validation + quarantine |
| Distraction | Context summarization |
| Confusion | Tool loadout management |
| Clash | Context pruning |

#### Production Observability
- **Traces**: Complete task from start to finish
- **Spans**: Individual steps within trace
- **Metrics**: Latency, costs, errors, feedback, accuracy

## References
- 8allocate Agentic AI Playbook
- Jotform AI Agents Guide
- Analytics Vidhya LLM Workflows
- MASFactory Vibe Graphing
- n8n, Make.com agent platforms
- LearnAgents.dev (pending - client-side rendered)
- **Microsoft AI Agents for Beginners** (14 lessons extracted)

---
*Generated: 2026-03-14*
*Updated: 2026-03-22*
*Chained from 20+ sources including Microsoft AI Agents Course*
*Vibe Graphing Pipeline*
