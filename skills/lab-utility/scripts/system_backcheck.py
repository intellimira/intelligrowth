import os
import subprocess
import json

class ACCTDiagnostic:
    def __init__(self, system_path):
        self.system_path = system_path
        self.results = {"skills": {}, "protocols": {}, "nodes": {}, "mesh": {}}

    def test_skill(self, name, command_args=[]):
        print(f"[*] Testing Skill: {name}...")
        script_path = os.path.join(self.system_path, f"Skill_Vault/{name}/scripts/core.py")
        if not os.path.exists(script_path):
            self.results["skills"][name] = "MISSING SCRIPT"
            return
        
        try:
            cmd = ["python3", script_path] + command_args
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.results["skills"][name] = "PASS"
            else:
                self.results["skills"][name] = f"FAIL (Code {result.returncode})"
        except Exception as e:
            self.results["skills"][name] = f"ERROR: {str(e)}"

    def check_protocols(self):
        print("[*] Verifying Protocol Density...")
        protocol_dir = os.path.join(self.system_path, "Core_Protocols")
        files = [f for f in os.listdir(protocol_dir) if f.endswith(".md")]
        self.results["protocols"]["count"] = len(files)
        # Check for Hub
        self.results["protocols"]["hub_presence"] = "PASS" if "ACCT_PROTOCOL_HUB.md" in files else "FAIL"

    def check_nodes(self):
        print("[*] Validating Nodal Mesh Implementation...")
        # Mapping Nodes to their programmatic anchors
        node_anchors = {
            "Analytic": "Skill_Vault/active_recall",
            "Empirical": "Skill_Vault/context_compactor",
            "Pragmatic": "Skill_Vault/cabal_commander",
            "Risk": "Skill_Vault/stream_monitor",
            "Sensory": "Laboratory/sensory_listener.py"
        }
        for node, anchor in node_anchors.items():
            path = os.path.join(self.system_path, anchor)
            self.results["nodes"][node] = "TECHNICAL" if os.path.exists(path) else "CONCEPTUAL ONLY"

    def run_full_check(self):
        print("\n--- ACCT SYSTEM: INITIALIZING VERBOSE BACK-TEST ---")
        
        # Test Core Skills
        self.test_skill("active_recall", ["test"])
        self.test_skill("mesh_brancher")
        self.test_skill("context_compactor", [os.path.join(self.system_path, "Memory_Mesh/History_Tree")])
        self.test_skill("cabal_spawner", ["DiagNode", "Analytic", "Diagnostic Objective"])
        self.test_skill("stream_monitor")
        
        # Check Protocols & Nodes
        self.check_protocols()
        self.check_nodes()
        
        print("\n--- DIAGNOSTIC SUMMARY ---")
        print(json.dumps(self.results, indent=2))

if __name__ == "__main__":
    diag = ACCTDiagnostic("/home/sir-v/ACCT_SYSTEM")
    diag.run_full_check()
