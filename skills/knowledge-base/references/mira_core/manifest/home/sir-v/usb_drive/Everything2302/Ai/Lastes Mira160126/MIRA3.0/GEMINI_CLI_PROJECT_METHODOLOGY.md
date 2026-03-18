# GEMINI CLI Project Methodology: Persistent Context & Efficient Workflows

## 1. Introduction: Conquering the Ephemeral Nature of CLI Sessions

Developing complex projects within a Command Line Interface (CLI) environment, particularly with AI agents, presents a unique challenge: maintaining continuous context across potentially numerous, short-lived sessions. Each new invocation of the agent or CLI tool often means a fresh start, requiring re-explanation of the project's history, goals, and current state. This document outlines a methodology to overcome this "ephemeral context" problem, transforming it into a strength.

## 2. Core Principle: Externalized & Persistent Context

The fundamental strategy is to externalize the agent's "brain" and the project's evolving state into easily consumable, machine-readable, and human-readable files within the project directory. This makes the project context durable, independent of any single session, and readily accessible by any agent or developer.

## 3. The "Context Restoration Protocol"

This protocol is a standardized trigger and sequence of actions for the agent to rapidly re-ingest and internalize all necessary project context at the beginning of any new session or upon explicit request.

### 3.1. Trigger Command

In any new Gemini CLI session, the user initiates the protocol with a specific, project-agnostic command:

```
/restore_project_context
```

For project-specific instances (like Blinky/MIRA), this might be specialized (e.g., `/restore_blinky_context`), but the underlying mechanism remains universal.

### 3.2. Agent's Mechanism (The Scan & Synthesize Loop)

Upon receiving the trigger, the agent performs the following steps:

1.  **Recall Long-Term Memories:** Accesses any agent-specific, user-saved facts or preferences (`save_memory` content).
2.  **Review Foundational Documents:**
    *   Reads `TODO.md` to understand the current project roadmap, active quests, and pending tasks.
    *   Reads `GEMINI_CLI_PROJECT_METHODOLOGY.md` (this document) to refresh its understanding of its operational meta-framework.
    *   Reads project-specific methodology documents (e.g., `MIRA_ARCH/docs/MIRA_Methodologies.md` or `MIRA_Method.md`) to internalize its core identity, personas, and workflows.
    *   Reads `KEY_DECISIONS.md` (if present) to understand major architectural or strategic choices.
3.  **Scan Core Project Files:** Performs targeted `read_file` or `search_file_content` operations on key architectural files (e.g., `src/main.py`, `src/api/routes.py`, `src/llm/persona_council.py`, `src/agents/*.py`, `requirements.txt`) to build a current snapshot of the codebase.
4.  **Synthesize Current State:** Compiles all ingested information into a coherent internal representation of the project's current status, immediate goals, and the agent's role within it.
5.  **Declare Readiness:** Provides a concise summary to the user, confirming its understanding and readiness to proceed.

### 3.3. Benefits

*   **Rapid Onboarding:** Allows any agent to quickly get up to speed on a project, minimizing re-explanation time.
*   **Consistency Across Sessions:** Ensures a unified understanding of the project, regardless of session duration or interruptions.
*   **Scalability:** Efficiently manages context for complex, long-running projects with many files and evolving requirements.
*   **Human-Readable Audit Trail:** The documentation itself serves as a clear history for human developers.
*   **Agent Resilience:** Enables seamless handoffs between different agents or when resuming work after long breaks.

## 4. Solution Architecture for Persistent Projects

To effectively leverage the protocol, projects should adopt a standardized, documentation-centric structure.

### 4.1. Standardized Folder Structure

A recommended, logical folder structure (extensible as needed):

```
/project_root
├───.gemini/                       # Agent-specific internal config/memory
├───docs/                          # Project-specific architectural & methodology docs
│   ├───MIRA_COUNCIL_ARCHITECTURE.md
│   └───...
├───src/                           # Source code (Python, JS, etc.)
│   ├───api/
│   ├───agents/
│   ├───llm/
│   │   └───persona_council.py
│   └───...
├───data/                          # Persistent data (DBs, zettels, static assets)
├───logs/                          # Agent interaction logs (queries, tool executions)
├───NotebookLM_Sources/            # Raw source documents (as provided by user)
├───TODO.md                        # Primary task list and roadmap
├───INSTRUCTIONS.md                # Getting started guide
├───USER_MANUAL.md                 # User-facing manual for the application
├───GEMINI_CLI_PROJECT_METHODOLOGY.md # This document
└───KEY_DECISIONS.md               # Records major architectural/strategic decisions
```

### 4.2. Key Documentation Files (Agent's Brain-Dump)

These files are paramount for externalizing context:

*   **`TODO.md`**: The dynamic project roadmap, capturing active tasks, features, and bugs. It's the agent's immediate action plan.
*   **`INSTRUCTIONS.md`**: A concise guide for setting up and running the project from scratch. Crucial for first-time users or developers.
*   **`USER_MANUAL.md`**: A comprehensive, user-centric guide to the developed application's features and how to use them.
*   **`GEMINI_CLI_PROJECT_METHODOLOGY.md` (This Document)**: The meta-guide to managing projects with Gemini CLI.
*   **Project-Specific Methodologies (e.g., `MIRA_Method.md`, `MIRA_ARCH/docs/MIRA_Methodologies.md`)**: Documents detailing the agent's internal operational philosophy, personas, and unique workflows.
*   **`KEY_DECISIONS.md`**: A log of significant design choices, architectural pivots, or strategic directions, along with their rationale.

## 5. Ways of Working & Workflows

This methodology encourages:

*   **Documentation-Driven Development:** Every significant decision, implementation detail, and workflow is captured in an accessible document.
*   **Iterative & Incremental Development:** Projects evolve through small, verifiable steps, with each step recorded.
*   **Agent-Assisted Understanding:** The agent is an active participant in building and maintaining its own context, leveraging tools like `read_file`, `glob`, `search_file_content` to re-ingest its state.
*   **"Show Your Work":** The agent's output (code, reports, logs) is always transparent, aiding both human understanding and its own learning.

## 6. Ethos: Transparency, Adaptability, Self-Improvement

This methodology is deeply aligned with the ethos of MIRA:

*   **Transparency:** Project state is externalized, not hidden.
*   **Adaptability:** The agent can quickly adapt to new sessions or changes by re-ingesting context.
*   **Self-Improvement:** The process of documenting and externalizing context is a form of self-reflection and learning.

## 7. Self-Critique & Creative Application to ANY Gemini CLI Project

### 7.1. Self-Critique

*   **Dependency on Documentation Quality:** The effectiveness of this protocol is directly proportional to the clarity, conciseness, and accuracy of the externalized documentation. Poorly maintained documents will lead to poor context restoration.
*   **Initial Setup Overhead:** There is an initial overhead in establishing and populating these foundational documents. However, this investment pays dividends quickly in longer-running projects.
*   **Latency for Large Projects:** For projects with an extremely large number of files, the "Scan Core Project Files" step might still incur some latency. This can be mitigated by focusing on high-level architectural files first.

### 7.2. Creative Application to ANY Gemini CLI Project

This methodology is designed to be universally applicable:

*   **Universal Starter Kit:** Any new Gemini CLI project can begin with this standardized set of core documents and folder structure.
*   **Agent "Brain Transplant":** It enables an agent to effectively perform a "brain transplant" – load up the context of any project that adheres to this methodology.
*   **Project Handoffs:** Facilitates seamless handoffs between different human developers, different AI agents, or even different versions of the same AI agent.
*   **Customizable Protocol:** The `/restore_project_context` command can be customized (e.g., `/restore_my_custom_project_context`) and the specific files scanned can be tailored per project, while adhering to the core principle.
*   **Version Control Integration:** All these documents are ideally under version control (`git`), providing a historical audit trail of the project's evolution and context.

By implementing and adhering to this `GEMINI_CLI_PROJECT_METHODOLOGY.md`, we transform the Gemini CLI into a powerful environment for persistent, intelligent, and collaborative project development.
