import os
import sys
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def synapse_grind_v2(system_path):
    """
    Performs a deep semantic 'All-to-All' scan to identify the strongest 
    Hidden Synapses across the entire ACCT Universal System.
    """
    db_path = os.path.join(system_path, "Laboratory/Vector_Mesh/db/semantic_mesh.pkl")
    report_path = os.path.join(system_path, "Memory_Mesh/EXP/SYNAPSE_REVELATION_REPORT.md")
    
    if not os.path.exists(db_path):
        print("[!] Semantic Mesh DB not found.")
        return

    with open(db_path, 'rb') as f:
        vectorizer, filenames, tfidf_matrix = pickle.load(f)

    print(f"\n--- ACCT SYNAPSE GRIND v2: ANALYZING {len(filenames)} NODES ---")
    
    # Calculate Similarity Matrix for all files
    similarities = cosine_similarity(tfidf_matrix)
    
    # Zero out the diagonal (self-similarity)
    np.fill_diagonal(similarities, 0)
    
    revelations = []
    seen_pairs = set()

    # Find the top 20 strongest synapses in the entire system
    flat_indices = similarities.flatten().argsort()[::-1]
    
    count = 0
    for idx in flat_indices:
        i, j = divmod(idx, len(filenames))
        score = similarities[i, j]
        
        if score < 0.2: break # Stop if similarity is too low
        
        # Avoid duplicate pairs (i,j and j,i) and ensure files are unique
        pair = tuple(sorted((i, j)))
        f1, f2 = os.path.basename(filenames[i]), os.path.basename(filenames[j])
        
        if pair not in seen_pairs and f1 != f2:
            seen_pairs.add(pair)
            revelations.append(f"* **Strong Synapse:** `{f1}` <==> `{f2}` (Sim: {score:.4f})")
            count += 1
        
        if count >= 20: break

    report_content = f"""# Synapse Revelation Report v2: Universal System Connections

## 1. Executive Summary
This report identifies the top 20 semantic "Synapses" discovered across the entire ACCT system (Protocols, Knowledge Base, and Memory Mesh). These connections represent the highest-bandwidth logical bridges in our current Second Brain.

## 2. Top Discovered Synapses:
{chr(10).join(revelations)}

## 3. Recommended Actions:
- [ ] **Unified Documentation:** Consolidate files with >0.8 similarity to reduce redundancy.
- [ ] **Mesh Strengthening:** Use the identified connections to add internal `[[links]]` between the target files.

---
**Status:** GRIND COMPLETE
**Active Node:** ✨ Creative Synthesis
"""
    with open(report_path, 'w') as f:
        f.write(report_content)
    
    print(f"[+] Universal Synapse Grind Complete. Report generated.")

if __name__ == "__main__":
    synapse_grind_v2("/home/sir-v/ACCT_SYSTEM")
