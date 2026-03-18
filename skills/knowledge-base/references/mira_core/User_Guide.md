# MIRA Project: Comprehensive User Manual

This manual provides a detailed guide for interacting with the MIRA project, understanding its capabilities, and leveraging its features for efficient workflow management within the Gemini CLI environment.

## 1. Getting Started & Setup

For initial setup, installation of dependencies, and starting the MIRA backend, please refer to the `INSTRUCTIONS.md` file in the project root.

## 2. Understanding MIRA: Your AI Assistant

MIRA (Miranda) is an AI assistant designed to enhance your digital environment. It operates on principles of continuous self-improvement, persona-based reasoning, and deep contextual understanding.

### 2.1. MIRA's Core Identity & Ethos

MIRA embodies the "Solo Leveler" ethos, constantly learning and expanding its capabilities. Its interactions are guided by a set of distinct personas, providing multi-faceted analysis.

*   **Personas:** MIRA utilizes six core personas for reasoning: First Principles, Scientific Method, Philosophical Inquiry, Creative Synthesis, Pragmatic Application, and The Dark Passenger. These frameworks allow MIRA to approach problems from diverse viewpoints.
*   **The Weave:** MIRA builds and maintains an internal knowledge graph, "The Weave," composed of interconnected insights, project context, and operational knowledge.

### 2.2. Interaction Principles

*   **Command-Line Interface:** You interact with MIRA primarily through this command-line environment.
*   **Tool Usage:** MIRA can leverage internal tools (e.g., for file system operations) to gather information or enact changes. For critical actions like `write_file`, user confirmation is required.
*   **Show Your Work:** MIRA's responses are designed to be transparent, explaining its reasoning and the steps it took.

## 3. Managing Project Context: The Context Restoration Protocol

For long-running or interrupted projects, MIRA uses a powerful "Context Restoration Protocol" to rapidly regain its understanding of the project's current state.

### 3.1. How to Use

In any new Gemini CLI session where you wish to resume work on this project, simply type the following command:

```
/restore_project_context
```

### 3.2. What Happens

Upon receiving this command, MIRA will:

1.  **Recall Key Facts:** Re-ingest essential information about the project's identity and operational philosophy.
2.  **Review Roadmap:** Read `TODO.md` to understand the project's current tasks and future direction.
3.  **Scan Core Documentation:** Re-read `GEMINI_CLI_PROJECT_METHODOLOGY.md` and project-specific methodology documents (e.g., `MIRA_ARCH/docs/MIRA_Methodologies.md`) to refresh its operational guidelines.
4.  **Analyze Codebase Snapshot:** Perform targeted scans of key code files (`src/main.py`, `src/api/routes.py`, `requirements.txt`, etc.) to understand the current code state.
5.  **Summarize & Declare Readiness:** Provide you with a concise overview of its current understanding and confirm it's ready to continue the task.

### 3.3. Benefits

This protocol is crucial for:

*   **Seamless Project Resumption:** No need to re-explain the project every time you start a new session.
*   **Consistent Understanding:** Ensures MIRA operates with the latest, most accurate project context.
*   **Efficient Workflow:** Minimizes overhead and maximizes productivity in multi-session development.

For a deeper dive into the architecture and philosophy behind this protocol, refer to `GEMINI_CLI_PROJECT_METHODOLOGY.md`.

## 4. Key Project Files & Directories

Familiarize yourself with the project's structure to work effectively:

*   **`TODO.md`**: Your primary task list and project roadmap.
*   **`INSTRUCTIONS.md`**: Setup and installation guide.
*   **`USER_MANUAL.md` (This Document)**: Comprehensive guide to using the project.
*   **`GEMINI_CLI_PROJECT_METHODOLOGY.md`**: Core methodology for persistent CLI projects.
*   **`MIRA_ARCH/`**: Contains the core MIRA backend application and its modules.
*   **`src/`**: Source code for various components.
*   **`data/`**: Storage for persistent data, like the ChromaDB vector store.
*   **`logs/`**: Automated logs of MIRA's interactions and tool executions.
*   **`NotebookLM_Sources/`**: Directory containing source documents ingested by MIRA.

## 5. Troubleshooting & FAQ

*   **Server not starting:** Check `INSTRUCTIONS.md` for setup details and review `MIRA_ARCH/uvicorn_stderr.log` for error messages.
*   **MIRA seems confused:** Use `/restore_project_context` to refresh its memory. If issues persist, ensure `TODO.md` and other core documents are up-to-date and clear.
*   **Tool execution failed:** Check MIRA's response for error details. For `write_file` operations, ensure you approved the confirmation prompt.
*   **"File not found" errors:** Verify file paths in `TODO.md` or MIRA's responses.

## 6. Expanding MIRA's Capabilities (Advanced Users)

MIRA is designed for self-improvement. Refer to `MIRA_ARCH/docs/MIRA_COUNCIL_ARCHITECTURE.md` and `GEMINI_CLI_PROJECT_METHODOLOGY.md` for insights into its extensible architecture and how to potentially integrate new tools or modify its behavior.
