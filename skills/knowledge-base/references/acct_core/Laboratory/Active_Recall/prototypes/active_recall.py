import os
import subprocess
import sys

def active_recall(query_terms):
    """
    Proactively surfaces relevant context from the MIRA manifest.
    v0.1: Keyword-based Grepper (Strict File Diversity)
    """
    manifest_path = "/home/sir-v/MIRA_CORE/manifest/"
    results = {}

    for term in query_terms:
        try:
            grep_output = subprocess.check_output(
                ["grep", "-ril", term, manifest_path],
                stderr=subprocess.STDOUT,
                text=True
            ).splitlines()
            
            for file_path in grep_output:
                results[file_path] = results.get(file_path, 0) + 1
        except subprocess.CalledProcessError:
            continue

    # Rank results by the number of matching terms
    sorted_results = sorted(results.items(), key=lambda item: item[1], reverse=True)
    
    # Return top UNIQUE Filenames (to avoid multiple copies of the same doc)
    final_results = []
    seen_filenames = set()
    
    for path, score in sorted_results:
        filename = os.path.basename(path)
        if filename not in seen_filenames:
            final_results.append((path, score))
            seen_filenames.add(filename)
        if len(final_results) >= 5:
            break
    
    print("\n--- ACCT ACTIVE RECALL: MEMORY SPARKS ---")
    if not final_results:
        print("No direct matches found in Memory Mesh. Ingesting current context...")
    else:
        for path, score in final_results:
            try:
                with open(path, 'r', errors='ignore') as f:
                    content = f.read(1000).strip()
                    snippet = " ".join(content.split()[:35]) # First 35 words
                
                rel_path = os.path.relpath(path, manifest_path)
                print(f"[*] RECALL: {os.path.basename(path)} (Score: {score})")
                print(f"    Path: .../{rel_path}")
                print(f"    Spark: {snippet}...")
                print("-" * 20)
            except Exception:
                continue

if __name__ == "__main__":
    if len(sys.argv) > 1:
        unique_terms = list(set(sys.argv[1:]))
        active_recall(unique_terms)
    else:
        print("Usage: python active_recall.py [term1] [term2] ...")
