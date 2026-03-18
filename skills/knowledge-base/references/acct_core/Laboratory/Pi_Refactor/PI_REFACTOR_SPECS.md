# Side Quest: Project Pi-Refactor (Pragmatic Node)

## 1. Concept: Tree-Structured Memory (Branching)
Pi stores history as a tree. ACCT will adapt this by using our **Zettelkasten Memory Mesh** as the tree structure.
*   **Axiom:** Every "turn" in a conversation is a Zettel.
*   **Logic:** Instead of a linear log, we allow a Zettel to have multiple "Child" Zettels (branches).
*   **ACCT Implementation:** We will use the `[[UID]]` system in our Semantic Weave to allow a user to say "Go back to UID-X and try a different approach." ACCT will create a new branch from that UID.

## 2. Concept: Context Compaction (Active Summarization)
Pi uses customizable compaction to manage token limits. ACCT will adapt this as a **Maintenance Protocol**.
*   **Axiom:** High-fidelity context is expensive; summarized context is efficient.
*   **Logic:** When a branch or project folder exceeds a specific size threshold, ACCT triggers a "Compressor" skill.
*   **ACCT Implementation:**
    *   **L0 (Raw):** The full interaction log.
    *   **L1 (Compacted):** An auto-generated summary Zettel that replaces the L0 files in the active reasoning stream.
    *   **Archiving:** L0 is moved to `/manifest/archive/`, L1 remains in `Memory_Mesh`.

## 3. End-to-End Reasoning (The Pragmatic Goal)
By the end of this side quest, ACCT will be able to:
1.  **Branch:** `/branch [UID]` -> Creates a new reasoning stream from a historical point.
2.  **Compact:** `/compact [Folder]` -> Reduces a project's documentation footprint by 70% while retaining semantic meaning.
3.  **Navigate:** Proactively suggest branching if a reasoning path leads to a low-score Cognitive Health check.

---
**Status:** SPECS DRAFTED
**Cognitive Node:** ⚙️ Pragmatic (Elevated)
