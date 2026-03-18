import requests
import json

API_KEY = "apik_EDHYk8A6ZGypR_C4539121_C_ca37cc9553cd6e6ce38e1b889903941db1888d1434c5ff118cd08498cba802"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def probe_whop():
    endpoints = [
        "https://api.whop.com/v1/me",
        "https://api.whop.com/v1/companies",
        "https://api.whop.com/v2/me",
        "https://api.whop.com/v1/biz/me",
        "https://api.whop.com/api/v2/companies"
    ]
    
    print("\n--- WHOP AGENTIC MAPPING: PROBE START ---")
    for url in endpoints:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            print(f"[*] PROBING {url} -> Status: {r.status_code}")
            if r.status_code == 200:
                print(f"    [!] SUCCESS: Endpoint Active. Data: {r.text[:200]}")
                return r.json()
        except Exception as e:
            print(f"    [!] Error: {e}")
    return None

if __name__ == "__main__":
    probe_whop()
