import requests
import os

def transmit():
    relay_url = "https://script.google.com/macros/s/AKfycbzyhUgUFIiZGxehaggFyLYhzw-PD9M88Z62lcztif8jB33rKt52U27A0ELu8UMx6sQj/exec"
    access_key = "SOVEREIGN_KEY_123"
    report_path = "/home/sir-v/ACCT_SYSTEM/Workspace/Experiment_ShadowOps/SOVEREIGN_ULTIMA_REPORT.html"
    
    with open(report_path, 'r') as f:
        html_content = f.read()
    
    payload = {
        "action": "SEND",
        "access_key": access_key,
        "to": "randolphdube@gmail.com",
        "subject": "AETHERIC TERMINAL: S-RANK STATUS UPDATE",
        "body": "The Aetheric Terminal v2.0 is live. (Embedded HTML data below)\n\n" + html_content
    }
    
    r = requests.post(relay_url, json=payload, timeout=30)
    print(f"[+] AETHERIC TRANSMISSION SUCCESS: {r.text}")

if __name__ == "__main__":
    transmit()
