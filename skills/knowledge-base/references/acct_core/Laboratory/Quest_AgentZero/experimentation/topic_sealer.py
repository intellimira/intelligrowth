import os
import json
from datetime import datetime

class ACCTTopicSealer:
    """
    Implements Topic-Based Context Sealing (Inspired by Agent-Zero).
    When a sub-task is done, the 'Topic' is sealed and summarized to save space.
    """
    def __init__(self, mesh_path):
        self.history_dir = os.path.join(mesh_path, "History_Tree")
        self.sealed_dir = os.path.join(mesh_path, "Sealed_Topics")
        os.makedirs(self.sealed_dir, exist_ok=True)

    def seal_topic(self, topic_id, turn_uids):
        """
        Gathers a group of turns, summarizes them, and moves them to the sealed vault.
        """
        print(f"\n--- ACCT TOPIC SEALER: {topic_id} ---")
        
        gathered_content = []
        for uid in turn_uids:
            turn_path = os.path.join(self.history_dir, f"TURN_{uid}.md")
            if os.path.exists(turn_path):
                with open(turn_path, 'r') as f:
                    gathered_content.append(f.read())
                # In a real scenario, we'd delete/archive the original TURN file here.
        
        if not gathered_content:
            print("[!] No content found for topic sealing.")
            return None

        # Create the Sealed Topic Zettel
        seal_uid = f"SEALED_{topic_id}_{datetime.now().strftime('%Y%m%d')}"
        seal_path = os.path.join(self.sealed_dir, f"{seal_uid}.md")
        
        # Simplified summary for prototype
        summary = f"""---
UID: {seal_uid}
Topic: {topic_id}
Turn_Count: {len(turn_uids)}
Tags: #sealed #compaction #exp
---
# Sealed Topic: {topic_id}

## Cognitive Summary:
This node represents a sealed and consolidated logic-stream for the sub-task: {topic_id}.
The primary reasoning path was validated and is now stored as permanent Experience (EXP).

## Historical Turn References:
{', '.join(['[['+uid+']]' for uid in turn_uids])}

---
Links: [[ACCT_PROTOCOL_HUB]], [[EXP_VAULT]]
"""
        with open(seal_path, 'w') as f:
            f.write(summary)
        
        print(f"[+] TOPIC SEALED: {seal_uid}.md (Consolidated {len(turn_uids)} turns).")
        return seal_uid

if __name__ == "__main__":
    sealer = ACCTTopicSealer("/home/sir-v/ACCT_CORE/Memory_Mesh")
    # Simulate sealing the Pi-Refactor turns
    turns = ["20260303-164658-505638", "20260303-164658-605836", "20260303-164658-706076"]
    sealer.seal_topic("Pi-Refactor-Sidequest", turns)
