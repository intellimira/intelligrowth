# Consensus Engine: Byzantine Fault Tolerant Inference (Laboratory v0.1)

## Objective: 
To implement a "Consensus Engine" that ensures the integrity of decentralized LLM inference by sharding tasks across multiple untrusted nodes and validating results via a 2/3 majority (pBFT-inspired) mechanism.

## Core Pillars:
1.  **Triple Dispatch (Redundancy):** Each inference chunk (layer or activation tensor) is sent to 3 independent Peer DIDs.
2.  **Consensus Verification:** Output tensors are hashed (SHA-256) and compared. 2/3 match = Success.
3.  **Reputation & Blacklisting:** Nodes that consistently fail consensus are flagged and eventually blacklisted from the personal mesh.
4.  **Effort-Aware Throttling:** Integration with `llama.cpp-effort` to respect host resource limits during verification.

## Native Effort Profile (Sovereign Sentinel v1.6.3):
For nodes running the `llama-server` variant, the following CLI flags MUST be enforced to ensure mesh stability:
- `--bucket-mul`: Enables dynamic effort scaling.
- `--bucket-mul-cpu-threshold 80`: Triggers throttling at 80% CPU usage.

## Architecture:

### 1. Mesh Dispatcher (`dispatcher.py`)
- **Input:** LLM Layer ID, Input Tensors, Peer Pool (DIDs).
- **Function:** Selects 3 Peers (prioritizing high-reputation nodes) and dispatches the task.
- **Protocol:** Uses `Chaincraft` (mDNS/P2P) for transport.

### 2. Consensus Verifier (`verifier.py`)
- **Input:** 3 Received Output Tensors.
- **Logic:**
    - Generate SHA-256 hashes of the received tensors.
    - If `hash(N1) == hash(N2)`: Return N1 Result. Mark N3 as "Failed".
    - If all 3 differ: Trigger "Full Recalculation" on trusted local nodes and flag all 3 Peers.
    - If all 3 match: Reward all 3 Peers with Reputation points.

### 3. Reputation Manager (`reputation.py`)
- **Storage:** SQLite or JSON-based DID-Reputation Map.
- **Logic:**
    - **Success:** +1 Point.
    - **Failure:** -10 Points.
    - **Blacklist Threshold:** -50 Points.
- **Integration:** Feeds the Peer Pool for the Dispatcher.

### 4. Byzantine Mock Node (`mock_node.py`)
- **Modes:** 
    - `HONEST`: Returns the correct tensor.
    - `LAZY`: Returns a cached or slightly delayed correct tensor.
    - `MALICIOUS`: Returns a random/tampered tensor (Byzantine).

## Roadmap:
- [ ] **Phase 1:** Python Prototype with Mock Nodes (Local Simulation).
- [ ] **Phase 2:** Integration with `llama.cpp` RPC splitting (Experimental).
- [ ] **Phase 3:** Integration with `Chaincraft` P2P Transport.
- [ ] **Phase 4:** Live Mesh Test on TITAN OS DIDs.

---
Tags: #consensus #byzantine #mesh #p2p
