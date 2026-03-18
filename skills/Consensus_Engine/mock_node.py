import hashlib
import json
import random

class MockNode:
    def __init__(self, did, mode="HONEST"):
        self.did = did
        self.mode = mode

    def compute_layer(self, layer_id, input_tensor):
        """
        Simulates the computation of an LLM layer.
        In a real scenario, this would involve llama.cpp inference.
        """
        # Base "correct" computation (Mocked as a hash of input + layer)
        base_data = f"{layer_id}:{input_tensor}".encode()
        correct_hash = hashlib.sha256(base_data).hexdigest()

        if self.mode == "HONEST":
            return {"did": self.did, "tensor_hash": correct_hash, "status": "SUCCESS"}
        
        elif self.mode == "LAZY":
            # Simulate a slight delay or cached result (still correct)
            return {"did": self.did, "tensor_hash": correct_hash, "status": "SUCCESS"}
            
        elif self.mode == "MALICIOUS":
            # Byzantine behavior: Return a tampered hash
            tampered_data = f"TAMPERED:{random.random()}".encode()
            bad_hash = hashlib.sha256(tampered_data).hexdigest()
            return {"did": self.did, "tensor_hash": bad_hash, "status": "SUCCESS"}

        else:
            return {"did": self.did, "tensor_hash": None, "status": "ERROR"}

if __name__ == "__main__":
    # Quick test
    node1 = MockNode("DID:TRUSTED:001", mode="HONEST")
    node2 = MockNode("DID:EVIL:666", mode="MALICIOUS")
    
    print(f"Honest Node Result: {node1.compute_layer('L1', 'input_vector_x')}")
    print(f"Malicious Node Result: {node2.compute_layer('L1', 'input_vector_x')}")
