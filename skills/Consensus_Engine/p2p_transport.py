import time
import random

class P2PTransport:
    def __init__(self, network_latency_ms=50):
        self.latency = network_latency_ms / 1000.0

    def send_tensor(self, target_did, layer_id, tensor_data):
        """
        Simulates sending a tensor over the mesh network.
        """
        # Simulate network hop
        time.sleep(self.latency + random.uniform(0, 0.1))
        #print(f"[P2P] Sent Layer {layer_id} chunk to {target_did}")
        return True

    def receive_result(self, source_did, timeout=2.0):
        """
        Simulates waiting for a result from a peer.
        """
        start = time.time()
        # Mock wait
        time.sleep(self.latency)
        
        if random.random() < 0.05: # 5% packet loss simulation
            print(f"[P2P] Timeout waiting for {source_did}")
            return None
            
        return "RECEIVED_OK"

if __name__ == "__main__":
    p2p = P2PTransport()
    p2p.send_tensor("DID:TEST:123", "L1", "data...")
    res = p2p.receive_result("DID:TEST:123")
    print(f"Transport Result: {res}")
