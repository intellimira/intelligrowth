import requests
import os

def transmit():
    relay_url = "https://script.google.com/macros/s/AKfycbzyhUgUFIiZGxehaggFyLYhzw-PD9M88Z62lcztif8jB33rKt52U27A0ELu8UMx6sQj/exec"
    access_key = "SOVEREIGN_KEY_123"
    report_path = "/home/sir-v/ACCT_SYSTEM/Workspace/Experiment_ShadowOps/SOVEREIGN_ULTIMA_REPORT.html"
    
    with open(report_path, 'r') as f:
        html_content = f.read()
    
    # We send the HTML content as the 'body' - the updated GAS will pick it up as htmlBody
    payload = {
        "action": "SEND",
        "access_key": access_key,
        "to": "randolphdube@gmail.com",
        "subject": "AETHERIC TERMINAL: S-RANK RENDERED REPORT",
        "body": html_content
    }
    
    print("[*] Transmitting Rendered Terminal via Neural Relay...")
    r = requests.post(relay_url, json=payload, timeout=30)
    print(f"[+] TRANSMISSION STATUS: {r.text}")

if __name__ == "__main__":
    transmit()
