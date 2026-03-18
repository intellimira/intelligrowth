import os
import json
import time
from datetime import datetime

class ACCTSensoryNode:
    """
    Programmatic foundation for the 👁️ Sensory Node.
    Monitors TITAN VISION OS events and triggers the Nodal Mesh.
    """
    def __init__(self, system_path):
        self.system_path = system_path
        self.sensory_log = os.path.join(system_path, "Memory_Mesh/Sensory_Logs/titan_events.log")
        os.makedirs(os.path.dirname(self.sensory_log), exist_ok=True)

    def log_event(self, event_type, data):
        """Simulates receiving a JSON event from TITAN."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event = {
            "timestamp": timestamp,
            "origin": "TITAN_VISION_OS",
            "type": event_type,
            "data": data,
            "nodal_trigger": self._determine_nodal_trigger(event_type)
        }
        
        with open(self.sensory_log, 'a') as f:
            f.write(json.dumps(event) + "\n")
        
        print(f"\n[👁️ SENSORY EVENT]: {event_type}")
        print(f"    Data: {json.dumps(data)}")
        print(f"    Triggering Node: {event['nodal_trigger']}")
        return event

    def _determine_nodal_trigger(self, event_type):
        """Maps visual events to Cognitive Nodes."""
        mapping = {
            "MOTION_DETECTED": "Risk Node",
            "OCR_TEXT_RECOGNIZED": "Analytic Node",
            "FACE_RECOGNIZED": "Philosophical Node",
            "SYSTEM_ERROR": "Pragmatic Node"
        }
        return mapping.get(event_type, "Analytic Node")

if __name__ == "__main__":
    sensory = ACCTSensoryNode("/home/sir-v/ACCT_SYSTEM")
    
    # Simulate Test 1: Security Event
    sensory.log_event("MOTION_DETECTED", {"location": "Front Door", "confidence": 0.98})
    
    # Simulate Test 2: Contextual Ingestion
    sensory.log_event("OCR_TEXT_RECOGNIZED", {"text": "Project Alpha: Confidential", "source": "User Screen"})
