import requests
import json

def check_replies():
    relay_url = "https://script.google.com/macros/s/AKfycbzyhUgUFIiZGxehaggFyLYhzw-PD9M88Z62lcztif8jB33rKt52U27A0ELu8UMx6sQj/exec"
    payload = {"action": "MONITOR", "access_key": "SOVEREIGN_KEY_123"}
    
    print("\n--- ACCT: LIVE REPLY AUDIT ---")
    try:
        r = requests.post(relay_url, json=payload, timeout=30)
        replies = r.json()
        if replies:
            print(f"[!!!] POSITIVE REPLIES DETECTED: {len(replies)}")
            for rep in replies:
                print(f"    - From: {rep['from']} | Subject: {rep['subject']}")
        else:
            print("[*] No unread 'YES' or 'DNA' replies yet. The lures are still being digested.")
    except Exception as e:
        print(f"[!] Audit Error: {e}")

if __name__ == "__main__":
    check_replies()
