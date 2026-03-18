import requests
import base64
import os

def beam_image():
    # Updated Master Relay URL
    relay_url = "https://script.google.com/macros/s/AKfycbyMwZzxw67LVGYhAlWWepb14HPIjUyxTerAk43qZ0t_pIa5GBPuYjfN8vcSLmS87fP6/exec"
    access_key = "SOVEREIGN_KEY_123"
    img_path = "/home/sir-v/ACCT_SYSTEM/Workspace/Experiment_ShadowOps/AETHERIC_SNAPSHOT.png"
    
    if not os.path.exists(img_path):
        print("[!] Snapshot not found. Re-capturing...")
        return

    with open(img_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    payload = {
        "action": "SEND_IMAGE",
        "access_key": access_key,
        "to": "randolphdube@gmail.com",
        "subject": "AETHERIC TERMINAL: S-RANK VISUAL STATUS",
        "image_base64": img_base64
    }
    
    print("[*] Beaming Visual Dashboard via Master Relay...")
    try:
        r = requests.post(relay_url, json=payload, timeout=60)
        print(f"[+] BEAM STATUS: {r.text}")
    except Exception as e:
        print(f"[!] Beam Error: {e}")

if __name__ == "__main__":
    beam_image()
