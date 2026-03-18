from mock_node import MockNode
from verifier import ConsensusVerifier
from reputation import ReputationManager
import time

class MeshDispatcher:
    def __init__(self):
        self.verifier = ConsensusVerifier()
        self.reputation = ReputationManager("mesh_reputation.json")
        # Initialize some mock nodes
        self.nodes = {
            "DID:NODE:001": MockNode("DID:NODE:001", mode="HONEST"),
            "DID:NODE:002": MockNode("DID:NODE:002", mode="HONEST"),
            "DID:NODE:003": MockNode("DID:NODE:003", mode="MALICIOUS"),
            "DID:NODE:004": MockNode("DID:NODE:004", mode="HONEST"),
            "DID:NODE:005": MockNode("DID:NODE:005", mode="MALICIOUS")
        }

    def dispatch_inference(self, layer_id, input_data):
        print(f"\n[ORCHESTRATOR] Dispatching Layer {layer_id}...")
        
        # 1. Select 3 nodes (In real life, this would use DID discovery)
        available_dids = [did for did in self.nodes.keys() if not self.reputation.is_blacklisted(did)]
        if len(available_dids) < 3:
            print("[CRITICAL] Not enough trusted nodes in the mesh!")
            return None

        # Simple selection: pick first 3 available
        selected_dids = available_dids[:3]
        print(f"[ORCHESTRATOR] Selected Peers: {selected_dids}")

        # 2. Parallel "Computation"
        results = []
        for did in selected_dids:
            node = self.nodes[did]
            result = node.compute_layer(layer_id, input_data)
            results.append(result)

        # 3. Consensus Verification
        winner_hash, successful_dids, failing_dids = self.verifier.verify(results)

        if winner_hash:
            print(f"[CONSENSUS] Match Found! Result Hash: {winner_hash[:10]}...")
            print(f"[CONSENSUS] Honest Nodes: {successful_dids}")
            print(f"[CONSENSUS] Byzantine Nodes Detected: {failing_dids}")
            
            # 4. Update Reputation
            self.reputation.update(successful_dids, failing_dids)
            return winner_hash
        else:
            print("[CRITICAL] Consensus Failed! 3 different results received.")
            self.reputation.update([], selected_dids) # Penalty for all
            return None

if __name__ == "__main__":
    dispatcher = MeshDispatcher()
    
    # Simulate multiple inference steps
    for i in range(1, 6):
        layer_name = f"L{i}"
        input_v = f"v_state_{i}"
        dispatcher.dispatch_inference(layer_name, input_v)
        time.sleep(0.5)

    print("\n--- Final Reputation Summary ---")
    print(dispatcher.reputation.reputation)
