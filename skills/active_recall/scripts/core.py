import os
import subprocess
import sys
import pickle
import re
from sklearn.metrics.pairwise import cosine_similarity

def active_recall_v2(query_terms):
    """
    Proactively surfaces relevant context using Hybrid Search (Keyword + Semantic).
    v2.0: Integrated TF-IDF Semantic Mesh.
    """
    system_path = "/home/sir-v/MiRA/ACCT_SYSTEM"
    manifest_path = os.path.join(system_path, "Knowledge_Base")
    db_path = os.path.join(system_path, "Laboratory/Vector_Mesh/db/semantic_mesh.pkl")
    
    query_string = " ".join(query_terms)
    results = {}

    # 1. KEYWORD SEARCH (Grep)
    for term in query_terms:
        try:
            grep_output = subprocess.check_output(
                ["grep", "-ril", term, manifest_path],
                stderr=subprocess.STDOUT, text=True
            ).splitlines()
            for path in grep_output:
                results[path] = results.get(path, 0) + 1.0 # Base keyword score
        except subprocess.CalledProcessError:
            continue

    # 2. SEMANTIC SEARCH (TF-IDF Cosine Similarity)
    if os.path.exists(db_path):
        with open(db_path, 'rb') as f:
            vectorizer, filenames, tfidf_matrix = pickle.load(f)
        
        query_vec = vectorizer.transform([query_string])
        similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
        
        for idx, score in enumerate(similarities):
            path = filenames[idx]
            if score > 0.1: # Only include significant semantic matches
                # Add semantic score to keyword results (Hybrid weight)
                results[path] = results.get(path, 0) + (score * 5.0) 

    # 3. RANK AND FILTER
    sorted_results = sorted(results.items(), key=lambda item: item[1], reverse=True)
    
    final_results = []
    seen_filenames = set()
    for path, score in sorted_results:
        filename = os.path.basename(path)
        if filename not in seen_filenames:
            final_results.append((path, score))
            seen_filenames.add(filename)
        if len(final_results) >= 5: break

    print("\n--- ACCT SEMANTIC PULSE: v2.0 ---")
    if not final_results:
        print("No significant matches found. Context isolation detected.")
    else:
        for path, score in final_results:
            try:
                with open(path, 'r', errors='ignore') as f:
                    snippet = " ".join(f.read(1000).split()[:35])
                
                rel_path = os.path.relpath(path, system_path)
                print(f"[*] RECALL: {os.path.basename(path)} (Hybrid Score: {score:.4f})")
                print(f"    Path: .../{rel_path}")
                print(f"    Spark: {snippet}...")
                print("-" * 25)
            except Exception: continue

if __name__ == "__main__":
    if len(sys.argv) > 1:
        active_recall_v2(sys.argv[1:])
    else:
        print("Usage: python3 core.py [terms...]")
