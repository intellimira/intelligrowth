# mas_run_test_simple.py
import os
import json
import logging
from masfactory import Agent, Model
from masfactory.adapters.model import ModelResponseType
from mira import init_control_plane

logging.basicConfig(level=logging.INFO)

class MockModel(Model):
    def __init__(self, model_name="mock-model", **kwargs):
        super().__init__(model_name=model_name, **kwargs)
    def invoke(self, messages, tools=None, settings=None, **kwargs):
        return {
            "type": ModelResponseType.CONTENT,
            "content": json.dumps({
                "signal_id": "test-uuid",
                "signal_type": "SIGNAL_B",
                "icp_hint": "Startup Founder"
            })
        }

mira = init_control_plane()

agent = Agent(
    name="sentry",
    model=MockModel(),
    instructions="SENTRY ROLE",
    push_keys={"signal_id": "", "signal_type": "", "icp_hint": ""}
)

# Test mira hook directly
print(" [TEST] Writing lineage...")
mira.write_lineage("sentry", "mock-model", "test-path")

# Test agent
print(" [TEST] Invoking agent...")
# Agent._forward is used via step
out = agent._forward({"raw_text": "Zapier is expensive", "platform": "reddit"})
print(f" [DONE] Output: {out}")
