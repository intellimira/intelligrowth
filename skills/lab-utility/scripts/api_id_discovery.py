import requests
import json

API_KEY = "apik_EDHYk8A6ZGypR_C4539121_C_ca37cc9553cd6e6ce38e1b889903941db1888d1434c5ff118cd08498cba802"
headers = {"Authorization": f"Bearer {API_KEY}"}

print("\n--- WHOP API: COMPANY DISCOVERY ---")
# Whop API v2 uses different endpoints
endpoints = [
    "https://api.whop.com/v1/companies",
    "https://api.whop.com/v2/companies",
    "https://api.whop.com/v1/biz/companies"
]

for url in endpoints:
    try:
        r = requests.get(url, headers=headers)
        print(f"[*] Endpoint {url}: {r.status_code}")
        if r.status_code == 200:
            print(f"    [+] DATA: {r.text}")
    except:
        pass
