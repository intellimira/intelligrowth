from mock_node import MockNode
from verifier import ConsensusVerifier
from reputation import ReputationManager
from effort_engine import EffortEngine
from p2p_transport import P2PTransport
import time

class MeshDispatcherV2:
    def __init__(self):
        self.verifier = ConsensusVerifier()
        self.reputation = ReputationManager("mesh_reputation.json")
        self.effort = EffortEngine()
        self.transport = P2PTransport()
        
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
        
        # Phase 2: Effort Check
        throttle_status = self.effort.regulate_effort()
        if throttle_status == "THROTTLED":
            print("[ORCHESTRATOR] Host Node Throttling Down (Effort Axiom).")

        # 1. Select 3 nodes
        available_dids = [did for did in self.nodes.keys() if not self.reputation.is_blacklisted(did)]
        if len(available_dids) < 3:
            print("[CRITICAL] Not enough trusted nodes in the mesh!")
            return None

        selected_dids = available_dids[:3]
        print(f"[ORCHESTRATOR] Selected Peers: {selected_dids}")

        # Phase 3: P2P Transport Simulation
        results = []
        for did in selected_dids:
            # Send (Mocked)
            self.transport.send_tensor(did, layer_id, input_data)
            
            # Receive (Mocked wait + result)
            p2p_status = self.transport.receive_result(did)
            if p2p_status:
                node = self.nodes[did]
                result = node.compute_layer(layer_id, input_data)
                results.append(result)
            else:
                 # Timeout/Packet Loss -> Treat as failure for this round
                 print(f"[P2P] Failed to receive from {did}")
                 results.append({"did": did, "tensor_hash": None, "status": "TIMEOUT"})

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
    dispatcher = MeshDispatcherV2()
    
    # Phase 4: Lazy Loading Simulation (Sequential Layers)
    print("--- STARTING LAZY LOADING INFERENCE CHAIN ---")
    layers = ["L1", "L2", "L3", "L4", "L5"]
    
    previous_hash = "input_seed"
    
    for layer in layers:
        # The input to the next layer is the hash/output of the previous one
        result_hash = dispatcher.dispatch_inference(layer, previous_hash)
        
        if result_hash:
            previous_hash = result_hash # Chain the context
            print(f"[CHAIN] Layer {layer} Complete. Moving to next...")
        else:
            print(f"[CHAIN] BROKEN at {layer}. Aborting Inference.")
            break
            
    print("\n--- Final Reputation Summary ---")
    print(dispatcher.reputation.reputation)
