# mas_run_test_graph.py
import os
import json
import logging
import re
from masfactory import RootGraph, Agent, Model, NodeTemplate
from masfactory.adapters.model import ModelResponseType
from mira import init_control_plane

logging.basicConfig(level=logging.INFO)

class MockModel(Model):
    def __init__(self, model_name="mock-model", **kwargs):
        super().__init__(model_name=model_name, **kwargs)
    def invoke(self, messages, tools=None, settings=None, **kwargs):
        prompt = messages[-1]["content"] if messages else ""
        print(f"\n [MOCK] Prompt: {prompt[:200]}...")
        
        if "SCORER" in prompt or "pain_score" in prompt:
             content = json.dumps({"pain_score": 100})
        else:
             content = json.dumps({"signal_id": "test-uuid"})
        
        return {
            "type": ModelResponseType.CONTENT,
            "content": content
        }

mira = init_control_plane()
model = MockModel()

sentry_tmpl = NodeTemplate(
    Agent,
    instructions="SENTRY ROLE",
    push_keys={"signal_id": ""},
    model=model
)

scorer_tmpl = NodeTemplate(
    Agent,
    instructions="SCORER ROLE",
    push_keys={"pain_score": ""},
    model=model
)

root = RootGraph(
    name="TestGraph",
    nodes=[
        ("sentry", sentry_tmpl),
        ("scorer", scorer_tmpl)
    ],
    edges=[
        ("ENTRY", "sentry", {"raw_text": ""}),
        ("sentry", "scorer", {"signal_id": ""}),
        ("scorer", "EXIT", {"pain_score": ""})
    ]
)

print(" [BUILDING] Graph...")
root.build()

print(" [INVOKING] Graph...")
out, attrs = root.invoke({"raw_text": "Zapier is expensive"})
print(f" [DONE] Output: {out}")
