import os
import json
import time
from datetime import datetime
from pathlib import Path

class MiraControlPlane:
    def __init__(self, policy_dir, scores_dir, tier=1, kpis=None):
        self.policy_dir = Path(policy_dir)
        self.scores_dir = Path(scores_dir)
        self.tier = tier
        self.kpis = kpis or {}
        self.lineage_path = self.scores_dir / "lineage.json"
        
        # Ensure directories exist
        self.policy_dir.mkdir(parents=True, exist_ok=True)
        self.scores_dir.mkdir(parents=True, exist_ok=True)

    def write_lineage(self, node_id, model, output_path, dm_score=None, tokens_used=0, cost=0.0):
        print(f" [MIRA] Writing lineage for {node_id}...")
        record = {
            "timestamp": datetime.now().isoformat(),
            "node": node_id,
            "model": model,
            "tier": self.tier,
            "dm_score": dm_score or {"content": 0.0, "provenance": 0.0, "total": 0.0},
            "output": str(output_path),
            "tokens_used": tokens_used,
            "cost_estimate_gbp": cost
        }
        
        with open(self.lineage_path, "a") as f:
            f.write(json.dumps(record) + "\n")

    def check_policy(self, agent_name, tool_name):
        policy_path = self.policy_dir / "agent_tool_policy.json"
        if not policy_path.exists():
            return True
            
        with open(policy_path, "r") as f:
            policies = json.load(f)
            
        agent_policy = policies.get(agent_name, policies.get("default", {}))
        allowed = agent_policy.get("allowed", agent_policy.get("allowed_tools", []))
        denied = agent_policy.get("deny", agent_policy.get("deny_tools", []))
        
        if tool_name in denied:
            return False
        if allowed and tool_name not in allowed:
            return False
            
        return True

def init_control_plane(policy_dir=".mira/policies", scores_dir=".mira/scores", tier=1, kpis=None):
    return MiraControlPlane(policy_dir, scores_dir, tier, kpis)
