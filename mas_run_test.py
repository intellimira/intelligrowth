# mas_run_test.py  —  Shadow Ops × The Weave v4.0 Test Runner
# Usage: python mas_run_test.py --signal_id [SIGNAL_ID]

import argparse
import os
import sqlite3
import json
import logging
import sys
from masfactory        import NodeTemplate, RootGraph, VibeGraph, Model
from masfactory.adapters.model import ModelResponseType

# Setup logging
logging.basicConfig(level=logging.INFO)

class MockModel(Model):
    """Mock model for testing graph flow without external API calls."""
    def __init__(self, model_name="mock-model", **kwargs):
        super().__init__(model_name=model_name, **kwargs)

    def invoke(self, messages, tools=None, settings=None, **kwargs):
        prompt = messages[-1]["content"] if messages else ""
        print(f"\n [MOCK] Model invoked with prompt: {prompt[:100]}...")
        
        content = json.dumps({
            "signal_id": "test-uuid",
            "signal_type": "SIGNAL_B",
            "icp_hint": "Startup Founder"
        })

        return {
            "type": ModelResponseType.CONTENT,
            "content": content
        }

try:
    from mira              import init_control_plane
except ImportError:
    sys.path.append(".")
    from mira import init_control_plane

parser = argparse.ArgumentParser()
parser.add_argument("--signal_id", type=str, required=True)
args = parser.parse_args()

mira = init_control_plane(
    policy_dir  = ".mira/policies",
    scores_dir  = ".mira/scores",
    tier        = 1,
    kpis        = { "max_task_duration": 30 }
)

mock_model = MockModel()

cache_path = os.path.abspath(".brain/graph_design_simple.json")
print(f" [DEBUG] Using cache path: {cache_path}")

workflow = NodeTemplate(
    VibeGraph,
    invoke_model       = mock_model,
    build_model        = mock_model,
    build_instructions = "Run test signal through pipeline.",
    build_cache_path   = cache_path,
    attributes         = {"mira": mira},
)

root = RootGraph(name="ShadowOpsWeaveTest", nodes=[("task", workflow)])

print(f" [BUILDING] Graph...")
root.build()

print(f" [INVOKING] Testing...")
initial_state = {
    "raw_text": "Zapier pricing is insane. $300 for 10 zaps.",
    "platform": "reddit"
}
out, attrs = root.invoke(initial_state)
print(f" [DONE] Output: {out}")
