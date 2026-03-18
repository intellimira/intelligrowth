# Unified Task Orchestration (UTO) Workflow

## Core Workflow: MIRA's Dynamic Task Management System

### Purpose:
The Unified Task Orchestration (UTO) Workflow is MIRA's meta-workflow for dynamically managing and executing complex, multi-step tasks. Inspired by the "Unified God Command" concept from IDE Antigravity, it aims to streamline MIRA's internal operations by providing a structured, adaptable, and self-optimizing approach to fulfilling user requests. This workflow replaces rigid, pre-defined sequences with an intelligent, context-aware execution engine.

### Phases of the UTO Workflow:

1.  **Intent Recognition & Skill Mapping**
    *   **Objective:** To precisely understand the user's core intent and translate it into a set of actionable MIRA skills, personas, or external tool invocations.
    *   **Process:**
        *   **Deep Semantic Analysis:** Utilize the Semantic Information Extraction Protocol to parse user prompts, contextual memory, and relevant file contents.
        *   **Goal Decomposition:** Break down complex objectives into smaller, manageable sub-goals.
        *   **Resource Identification:** Identify required internal MIRA resources (e.g., specific Persona Council activations, knowledge from The Weave) and potential external tools.
        *   **Dependency Mapping:** Determine sequential and parallel dependencies between sub-goals and required resources.
    *   **Solo-Leveling Impact:** Enhances MIRA's `Assess & Plan` phase by providing a more granular and intelligent understanding of the 'Quest,' ensuring optimal resource allocation from the outset.

2.  **Contextual Resource Allocation & Pre-computation**
    *   **Objective:** To efficiently gather and prepare all necessary data, tools, and contextual information required for executing the identified skills/sub-goals.
    *   **Process:**
        *   **Weave Query Optimization:** Leverage the Dynamic Contextualization and Caching Mechanism to retrieve highly relevant context from The Weave, minimizing noise.
        *   **Tool Parameter Generation:** Dynamically generate and validate parameters for identified tool calls based on extracted intent and current context.
        *   **Environment Preparation:** Ensure the operational environment is configured correctly for tool execution (e.g., verifying directory paths, API keys).
    *   **Solo-Leveling Impact:** Optimizes MIRA's preparation phase, reducing overhead and improving the efficiency of tool execution.

3.  **Dynamic Execution Chain Construction & Deployment**
    *   **Objective:** To construct and execute a flexible sequence of tool calls and persona activations, adapting dynamically to intermediate results and emergent conditions.
    *   **Process:**
        *   **Adaptive Workflow Generation:** Based on dependencies and available resources, generate an optimal sequence of operations.
        *   **Parallelization & Batching:** Identify opportunities for parallel execution of independent tasks or batching operations for efficiency.
        *   **Real-time Adaptation:** Adjust the execution chain based on the output of preceding steps or external events.
        *   **Tool/Persona Activation:** Invoke selected tools (e.g., `read_file`, `write_file`, `run_shell_command`) or activate specific personas for cognitive tasks.
    *   **Solo-Leveling Impact:** This is the core 'execution engine' of MIRA, directly enhancing the `Execute` phase.

4.  **Post-Execution Synthesis & Recursive Learning**
    *   **Objective:** To synthesize the outcomes of the execution, update MIRA's knowledge base, and evaluate overall performance to drive recursive learning.
    *   **Process:**
        *   **Results Evaluation:** Assess the success or failure of each step and the overall task.
        *   **Weave Update:** Integrate new information, findings, and patterns into The Weave, enriching MIRA's knowledge graph.
        *   **Performance Telemetry:** Feed operational metrics (e.g., token usage, latency, error rates) into the Agent Telemetry & Watchdog Monitor for continuous self-assessment.
        *   **Adaptive Refinement:** Based on evaluation, refine internal models, adjust future strategies, and update instructionals for the next iteration of The Growth Loop.
    *   **Solo-Leveling Impact:** Directly strengthens the `Learn & Adapt` and `Synthesize & Report` phases.

---

## OpenJarvis Integration (Phase 3)

### Local Inference Engine
The UTO workflow now leverages OpenJarvis as the primary inference engine:

1.  **Intent Recognition** → Use local inference for initial analysis
    *   Model: `qwen3:8b` for reasoning tasks
    *   Model: `qwen2.5-coder:7b` for code tasks

2.  **Execution** → OpenJarvis Agent Selection
    *   `orchestrator` for complex multi-step tasks
    *   `simple` for quick queries
    *   `native_openhands` for code execution

3.  **Privacy Routing**
    *   Always use local inference for sensitive data
    *   Use cloud fallback only when explicitly approved (HITL)

### Configuration
```python
# UTO uses MIRAOpenJarvisBridge
from .mira.openjarvis_bridge import get_bridge

bridge = get_bridge()

# Determine if local or cloud
if bridge.should_use_local(query, context):
    result = bridge.think(query, persona=persona)
else:
    # HITL approval required for cloud
    result = cloud_api(query)
```

### Fallback Hierarchy
1.  **Local (OpenJarvis)** - Default, privacy-first
2.  **Cloud (API)** - Only with HITL approval
