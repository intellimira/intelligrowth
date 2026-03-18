from collections import Counter

class ConsensusVerifier:
    def __init__(self):
        self.total_processed = 0
        self.total_byzantine_detected = 0

    def verify(self, results):
        """
        Input: List of result dictionaries from 3 nodes.
        Output: (Winning Hash, Successful DIDs, Failing DIDs)
        """
        self.total_processed += 1
        
        # Extract hashes and DIDs
        hashes = [res['tensor_hash'] for res in results if res['status'] == "SUCCESS"]
        did_map = {res['tensor_hash']: res['did'] for res in results if res['status'] == "SUCCESS"}
        all_dids = [res['did'] for res in results]

        if not hashes:
            return None, [], all_dids

        # Count occurrences of each hash
        hash_counts = Counter(hashes)
        
        # Find the winner (majority hash)
        winner_hash, count = hash_counts.most_common(1)[0]

        successful_dids = [res['did'] for res in results if res['tensor_hash'] == winner_hash]
        failing_dids = [res['did'] for res in results if res['tensor_hash'] != winner_hash]

        if count >= 2:
            # Consensus reached (2/3 or 3/3)
            self.total_byzantine_detected += len(failing_dids)
            return winner_hash, successful_dids, failing_dids
        else:
            # No consensus (3 different hashes)
            return None, [], all_dids

if __name__ == "__main__":
    # Test cases
    v = ConsensusVerifier()
    
    # 2/3 Consensus Case
    results_2_3 = [
        {"did": "N1", "tensor_hash": "AAA", "status": "SUCCESS"},
        {"did": "N2", "tensor_hash": "AAA", "status": "SUCCESS"},
        {"did": "N3", "tensor_hash": "BBB", "status": "SUCCESS"}
    ]
    print(f"2/3 Result: {v.verify(results_2_3)}")
    
    # No Consensus Case (Byzantine Overload)
    results_0_3 = [
        {"did": "N1", "tensor_hash": "AAA", "status": "SUCCESS"},
        {"did": "N2", "tensor_hash": "BBB", "status": "SUCCESS"},
        {"did": "N3", "tensor_hash": "CCC", "status": "SUCCESS"}
    ]
    print(f"No Consensus Result: {v.verify(results_0_3)}")
