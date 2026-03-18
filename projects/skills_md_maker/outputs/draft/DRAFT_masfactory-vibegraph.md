---
name: masfactory-vibegraph
description: Graph-centric framework for orchestrating Multi-Agent Systems with Vibe Graphing - intent-to-executable workflow via human-in-the-loop compilation.
triggers: [vibegraph, multi-agent, mas, graph-orchestration, workflow-automation, agent-coordination]
tools: [ollama_infer, gemini_call, openai_call, anthropic_call, visualize_graph, trace_runtime]
quality_gates: [graph_compiles, nodes_defined, edges_valid, runtime_traceable]
persona: "✨ Creative Synthesis — pattern extraction and skill synthesis"
mira_tier: 1
---

## Source
- Input: https://github.com/BUPT-GAMMA/MASFactory
- Type: URL (GitHub)
- Content: codesearch + webfetch

## What is MASFactory?
MASFactory is a **graph-centric framework** for orchestrating LLM-based Multi-Agent Systems (MAS) with **Vibe Graphing** - a human-in-the-loop approach that compiles natural-language intent into editable workflow specifications, then compiles to executable graphs.

## Key Concepts

### Vibe Graphing Pipeline
1. **Intent** → User describes workflow in natural language
2. **Graph Design** → System generates structural design (JSON)
3. **Preview & Refine** → Human reviews/edits in Visualizer
4. **Compile** → Converts to executable graph
5. **Execute** → Runs with runtime tracing

### Core Components
- **Node** - Basic computation unit (Agent, CustomNode, Loop, Switch)
- **Edge** - Dependencies and message passing
- **Graph** - Directed computation graph
- **Visualizer** - Topology preview, runtime tracing, HITL

### Project Structure
```
masfactory/
├── core/           # Node, Edge, Gate, MessageFormatter
├── components/     # Agents, Controls, Human-in-loop
├── adapters/       # Model, Tool, Memory, Retrieval, MCP
├── integrations/   # MemoryOS, UltraRAG
├── applications/   # ChatDev, AgentVerse, CAMEL examples
└── visualizer/    # VSCode extension for preview
```

## Patterns Extracted

### VibeGraphing Patterns
- intent → graph_design.json → compile → execute
- human-in-the-loop at each stage
- graph visualization + runtime tracing

### Workflow Patterns
- Declarative: define nodes/edges explicitly
- Imperative: Python code with MASFactory API
- VibeGraphing: natural language → JSON → compile

### Agent Patterns
- Retriever → Reader → Synthesizer
- Multi-agent role playing
- Sequential pipeline with switches

## Hard Rules
1. Graph must have ENTRY and EXIT nodes
2. All agents need model configuration
3. Use context adapters for memory/RAG
4. Visualizer requires VSCode extension

## Quality Gates
- [ ] graph_compiles - JSON converts to executable
- [ ] nodes_defined - All nodes have templates
- [ ] edges_valid - No circular dependencies in DAG
- [ ] runtime_traceable - Visualizer can trace execution

## Usage Example
```python
from masfactory import RootGraph, Agent, OpenAIModel

g = RootGraph()
g.add_node(Agent(name="analyzer", model=OpenAIChat(...)))
g.add_edge("ENTRY", "analyzer")
g.add_edge("analyzer", "EXIT")
g.build()
out, _ = g.invoke({"query": "Your question"})
```

## Documentation
- Docs: https://bupt-gamma.github.io/MASFactory/
- GitHub: https://github.com/BUPT-GAMMA/MASFactory
- Video: https://youtu.be/ANynzVfY32k

---
*Generated: 2026-03-14*
*Vibe Graphing Pipeline - Two Pass System*
