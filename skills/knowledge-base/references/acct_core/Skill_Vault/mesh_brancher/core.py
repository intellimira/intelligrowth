import os
import json
import time
from datetime import datetime

class ACCTBranchingHistory:
    """
    Implements Tree-Structured History for ACCT.
    Each turn is a Zettel with a Parent-Child relationship.
    """
    def __init__(self, mesh_path):
        self.mesh_path = mesh_path
        self.history_dir = os.path.join(mesh_path, "History_Tree")
        os.makedirs(self.history_dir, exist_ok=True)

    def create_turn(self, content, parent_uid=None):
        """Creates a new turn (Zettel) in the tree."""
        # Use microseconds for uniqueness in high-speed simulation
        uid = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        filename = f"TURN_{uid}.md"
        filepath = os.path.join(self.history_dir, filename)
        
        zettel_content = f"""---
UID: {uid}
Parent: {parent_uid}
Tags: #history #turn
---
# Turn {uid}

{content}

---
Links: [[{parent_uid if parent_uid else 'ROOT'}]]
"""
        with open(filepath, 'w') as f:
            f.write(zettel_content)
        
        print(f"[*] TURN CREATED: {uid} (Parent: {parent_uid})")
        return uid

    def list_branches(self):
        """Lists all turns and their parents to visualize the tree."""
        turns = []
        for f in os.listdir(self.history_dir):
            if f.endswith(".md"):
                with open(os.path.join(self.history_dir, f), 'r') as file:
                    lines = file.readlines()
                    # Basic metadata parsing
                    uid = ""
                    parent = ""
                    for line in lines:
                        if line.startswith("UID: "): uid = line.split(": ")[1].strip()
                        if line.startswith("Parent: "): parent = line.split(": ")[1].strip()
                    turns.append((uid, parent))
        
        print("\n--- ACCT HISTORY TREE ---")
        # Simple tree visualization
        for uid, parent in sorted(turns):
            indent = "  " if parent != "None" else ""
            print(f"{indent}{parent} -> {uid}")

if __name__ == "__main__":
    history = ACCTBranchingHistory("/home/sir-v/ACCT_CORE/Memory_Mesh")
    # Simulate a root turn
    root = history.create_turn("Commander initialized the Pi-Refactor Side Quest.")
    time.sleep(0.1)
    # Simulate branches
    b1 = history.create_turn("Pragmatic Node proposed branching history.", root)
    time.sleep(0.1)
    b2 = history.create_turn("Alternative path: Philosophical Node proposed caution.", root)
    
    history.list_branches()
