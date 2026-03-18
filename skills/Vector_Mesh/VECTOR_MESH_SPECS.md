# ACCT Quest: Live Vector Mesh (Technical Specs)

## 1. Objective: Beyond Keywords
Transition the ACCT Memory Mesh from a keyword-based retrieval system (grep) to a mathematical semantic similarity engine. This allows for "Intuitive Retrieval" where the system understands context even when exact words don't match.

## 2. Technical Architecture:
*   **Embedding Engine:** `sentence-transformers` (all-MiniLM-L6-v2) - chosen for its balance of speed and semantic accuracy.
*   **Vector Database:** Flat File Storage (`.npy`) for v0.1. We will store raw vectors in `/embeddings` and map them to Zettel UIDs.
*   **Search Logic:** Cosine Similarity. We calculate the mathematical "angle" between the user query and every Zettel in the mesh.

## 3. The Semantic Upgrade (active_recall v2.0):
*   **Process:**
    1.  **Index:** Read every `.md` file in the Knowledge Base and Memory Mesh.
    2.  **Vectorize:** Generate a 384-dimensional vector for each file.
    3.  **Search:** When queried, vectorize the query and find the "Nearest Neighbors" in the vector space.
*   **Demonstration:**
    *   Query: "How do I secure my agent?"
    *   Result: Surfacess files about "Risk Node," "Security Protocols," and "Agent-Zero Audits" even if "Secure" isn't explicitly used.

## 4. Maintenance (Recursive Grind):
*   **Re-indexing:** Every time a new Zettel is added, the Vector Mesh must be updated.
*   **Compaction Sync:** When `context_compactor` runs, it must also compact the corresponding vector entries.

---
**Status:** ARCHITECTING
**Engine:** Sentence-Transformers (Pending install completion)
