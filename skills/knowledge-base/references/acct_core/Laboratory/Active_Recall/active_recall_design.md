# Laboratory Project: Active Recall v0.1

## 1. Objective: The "Proactive Second Brain"
Traditional RAG (Retrieval-Augmented Generation) is reactive—it waits for a query. **Active Recall** aims to be proactive. It will continuously scan the ACCT environment (current Quest, user input, Memory Mesh) to identify and surface relevant historical "Zettels" from the 401 local MIRA files.

## 2. Functional Requirements:
*   **Semantic Keying:** Automatically extract key entities, concepts, and personas from the current context.
*   **Deep Manifest Search:** Scan `/home/sir-v/MIRA_CORE/manifest/` for keyword matches and semantic overlaps.
*   **Nodal Synthesis:** Filter results based on the active Cognitive Node (e.g., if "Empirical" is active, prioritize technical logs).
*   **Proactive Snippets:** Provide 1-2 sentence "Memory Sparks" to the ACCT reasoning stream.

## 3. Prototype Architecture (v0.1 - The "Grepper"):
*   **Input:** Current user prompt or `TODO.md` task.
*   **Process:**
    1.  Parse input for "High-Signal" terms.
    2.  Execute a recursive `grep` across the manifest.
    3.  Rank results by frequency and recentness (if possible).
*   **Output:** A list of the top 5 most relevant Zettel paths and a brief "Spark" from each.

## 4. Test Case:
**Input:** "How do we integrate TITAN Vision into ACCT?"
**Expected Recall:** `TITAN_INTEGRATION_ARCHITECTURE.md`, `mira_titan_events.log` references, and any persona definitions related to "Optic Nerve."
