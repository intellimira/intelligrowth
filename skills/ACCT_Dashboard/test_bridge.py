import websocket
import json
import time

def test_bridge():
    try:
        ws = websocket.create_connection("ws://127.0.0.1:4000/ws")
        print("[Test] Connected to Bridge.")
        
        # Send a test pulse
        payload = {
            "type": "PULSE_EVENT",
            "kind": "PROMPT",
            "model": "test-model",
            "content": "BRIDGE_VALIDATION_PULSE"
        }
        ws.send(json.dumps(payload))
        print("[Test] Pulse sent.")
        
        # Send a test node event
        node_event = {
            "type": "NODE_EVENT",
            "node": "pain_miner",
            "event": "start"
        }
        ws.send(json.dumps(node_event))
        print("[Test] Node event sent.")
        
        ws.close()
        print("[Test] Connection closed.")
    except Exception as e:
        print(f"[Test Error] {e}")

if __name__ == "__main__":
    test_bridge()
