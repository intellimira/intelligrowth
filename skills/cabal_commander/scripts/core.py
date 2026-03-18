import os
import sys
import pickle
from sklearn.metrics.pairwise import cosine_similarity

# Import existing spawner logic
sys.path.append("/home/sir-v/ACCT_SYSTEM/Skill_Vault/cabal_spawner/scripts")
from spawner_logic import ACCTCabalSpawner

class ACCTSovereignCommander:
    """
    Elevated ACCT Commander (v1.5).
    Uses Semantic Synapses to enrich sub-node directives.
    """
    def __init__(self, system_path):
        self.system_path = system_path
        self.spawner = ACCTCabalSpawner(os.path.join(system_path, "Laboratory"))
        self.db_path = os.path.join(system_path, "Laboratory/Vector_Mesh/db/semantic_mesh.pkl")
        self.active_missions = {}

    def _get_synapses(self, objective, top_k=2):
        """Finds legacy files semantically related to the task."""
        if not os.path.exists(self.db_path): return []
        
        with open(self.db_path, 'rb') as f:
            vectorizer, filenames, tfidf_matrix = pickle.load(f)
        
        query_vec = vectorizer.transform([objective])
        similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
        related_indices = similarities.argsort()[::-1][:top_k]
        
        return [os.path.basename(filenames[idx]) for idx in related_indices if similarities[idx] > 0.1]

    def delegate_quest(self, quest_name, tasks):
        print(f"\n--- ACCT SOVEREIGN COMMANDER: INITIATING [{quest_name}] ---")
        
        for task in tasks:
            label = task['label']
            node_type = task['node']
            objective = task['objective']
            
            # ENRICHMENT: Find Semantic Synapses for this specific objective
            synapses = self._get_synapses(objective)
            enriched_objective = f"{objective}\n\n**Semantic Context (Synapses):** {', '.join(synapses)}"
            
            # Spawn the specialized node with enriched data
            path = self.spawner.spawn_node(label, node_type, enriched_objective)
            self.active_missions[label] = {"status": "Active", "path": path}

    def synthesize(self):
        print("\n--- MISSION SYNTHESIS COMPLETE ---")
        print(f"Quest: All sub-nodes coordinated via Semantic Mesh.")

if __name__ == "__main__":
    commander = ACCTSovereignCommander("/home/sir-v/ACCT_SYSTEM")
    
    # Test Delegation with Semantic Enrichment
    commander.delegate_quest("Project-Vision-Alpha", [
        {"label": "Sensory Audit", "node": "Risk", "objective": "Analyze the visual event stream for security gaps."}
    ])
    commander.synthesize()
