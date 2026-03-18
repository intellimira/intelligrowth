import os
import re
from collections import defaultdict

def project_synapse(mesh_dirs):
    """
    Analyzes the Memory Mesh to find 'Hidden Synapses' (cross-links and tags).
    v0.1: Connection Mapper
    """
    tag_map = defaultdict(list)
    link_map = defaultdict(list)
    orphans = []
    
    print("\n--- ACCT PROJECT SYNAPSE: MESH ANALYSIS ---")
    
    for mesh_dir in mesh_dirs:
        for root, _, files in os.walk(mesh_dir):
            for file in files:
                if file.endswith(".md"):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', errors='ignore') as f:
                            content = f.read()
                            
                            # Find all tags (#tag)
                            tags = re.findall(r'#(\w+)', content)
                            for tag in tags:
                                tag_map[tag.lower()].append(file)
                            
                            # Find all internal links ([[link]])
                            links = re.findall(r'\[\[(.*?)\]\]', content)
                            if not links and not tags:
                                orphans.append(file)
                            else:
                                for link in links:
                                    link_map[file].append(link)
                    except Exception:
                        continue

    # Identify 'Hidden Synapses' (Files sharing the same tags but not linked)
    print("\n[*] DISCOVERED SYNAPSES (Suggested Links):")
    synapse_count = 0
    for tag, files in tag_map.items():
        unique_files = list(set(files))
        if len(unique_files) > 1:
            for i in range(len(unique_files)):
                for j in range(i + 1, len(unique_files)):
                    f1, f2 = unique_files[i], unique_files[j]
                    # Check if these files are already linked
                    if f2.replace(".md", "") not in link_map[f1] and f1.replace(".md", "") not in link_map[f2]:
                        print(f"  [Synapse] '{f1}' <--> '{f2}' via #{tag}")
                        synapse_count += 1
        if synapse_count >= 15: break

    if orphans:
        print("\n[!] ORPHANED CONTEXT (No links or tags):")
        for orphan in orphans[:10]:
            print(f"  - {orphan}")

    print(f"\n--- Analysis Complete. {synapse_count} synapses proposed. ---")

if __name__ == "__main__":
    target_dirs = ["/home/sir-v/ACCT_CORE/Memory_Mesh", "/home/sir-v/MIRA_CORE/manifest"]
    project_synapse(target_dirs)
