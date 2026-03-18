import json
import os

class ReputationManager:
    def __init__(self, db_path="reputation_db.json"):
        self.db_path = db_path
        self.reputation = self._load_db()

    def _load_db(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return {}

    def _save_db(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.reputation, f, indent=4)

    def update(self, successful_dids, failing_dids):
        """
        Updates reputation scores based on consensus results.
        """
        for did in successful_dids:
            score = self.reputation.get(did, 0)
            self.reputation[did] = score + 1
            print(f"Reputation Boost: {did} -> {self.reputation[did]}")

        for did in failing_dids:
            score = self.reputation.get(did, 0)
            self.reputation[did] = score - 10
            print(f"Reputation Penalty: {did} -> {self.reputation[did]}")

        self._save_db()

    def get_top_peers(self, count=3):
        """
        Returns the top N DIDs by reputation.
        """
        sorted_peers = sorted(self.reputation.items(), key=lambda x: x[1], reverse=True)
        return [peer[0] for peer in sorted_peers[:count]]

    def is_blacklisted(self, did, threshold=-50):
        return self.reputation.get(did, 0) <= threshold

if __name__ == "__main__":
    # Test Reputation logic
    rm = ReputationManager("test_reputation.json")
    rm.update(["N1", "N2"], ["N3"])
    print(f"Top Peers: {rm.get_top_peers()}")
    print(f"Is N3 Blacklisted? {rm.is_blacklisted('N3')}")
