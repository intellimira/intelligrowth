# Laboratory Project: Project Synapse v0.1

## 1. Objective: The "Cross-Mesh Synapse"
Current ACCT tools (like Active Recall) are driven by specific queries. **Project Synapse** aims to be an autonomous discovery engine. It will scan the Memory Mesh to find non-obvious connections (Synapses) between disparate projects and archived files.

## 2. Functional Requirements:
*   **Recursive Cross-Linking:** Automatically scan all `.md` files in `/home/sir-v/ACCT_CORE/Memory_Mesh/` and `/home/sir-v/MIRA_CORE/manifest/`.
*   **Clustering Logic:** Identify "Context Clusters" (groups of files sharing 3+ unique tags or high-frequency keywords).
*   **Proactive Synthesis:** Propose a new "Consolidated Zettel" when a Synapse is found between two previously unrelated directories.

## 3. Prototype Architecture (v0.1 - The "Linker"):
1.  **Input:** The entire Memory Mesh.
2.  **Process:**
    *   Map every tag (`#tag`) and internal link (`[[link]]`) into a temporary graph.
    *   Identify "Orphan Nodes" (no links) and "Island Clusters" (small groups of linked files not connected to the main mesh).
    *   Suggest "Bridge Links" to the Commander to unify the mesh.
3.  **Output:** A `SYNAPSE_REPORT.md` detailing discovered connections.

## 4. Test Case:
**Scenario:** A legal file in the MIRA archive mentioned "IP Coverage." A technical file in ACCT mentions "Master Skill Integration."
**Expected Synapse:** ACCT identifies that Master Skills are covered under the "MiRA + TITAN Legal Doc" found in the manifest.
