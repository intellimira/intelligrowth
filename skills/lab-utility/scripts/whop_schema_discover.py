import requests
import json

API_KEY = "apik_EDHYk8A6ZGypR_C4539121_C_ca37cc9553cd6e6ce38e1b889903941db1888d1434c5ff118cd08498cba802"
headers = {"Authorization": f"Bearer {API_KEY}"}

print("\n--- WHOP API: DISCOVERY PULSE ---")
# List businesses
r = requests.get("https://api.whop.com/v1/companies", headers=headers)
print(f"[*] Companies: {r.text}")

# Attempt creation with fixed nested payload if required by some API versions
def create_fixed(name, price):
    payload = {
        "name": name,
        "visibility": "public",
        "pricing_type": "one_time",
        "price": float(price)
    }
    # Testing direct endpoint
    res = requests.post("https://api.whop.com/v1/biz/products", json=payload, headers=headers)
    print(f"[*] Try {name}: {res.status_code} - {res.text}")

create_fixed("Test_Shadow_Audit", 29)
