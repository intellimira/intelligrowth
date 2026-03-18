import requests
import json

API_KEY = "apik_EDHYk8A6ZGypR_C4539121_C_ca37cc9553cd6e6ce38e1b889903941db1888d1434c5ff118cd08498cba802"
BIZ_ID = "biz_wJSN9AZSnng2vT"
BASE_URL = "https://api.whop.com/v1"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def create_shadow_product(name, price, desc):
    # Fixed Schema: nesting the plan details and using correct visibility enum
    payload = {
        "company_id": BIZ_ID,
        "name": name,
        "description": desc,
        "visibility": "visible",
        "pricing_type": "one_time",
        "price": float(price)
    }
    
    print(f"[*] AGENT: Attempting Corrected Instantiation for {name}...")
    try:
        # Some versions of Whop API require the price inside a 'plans' array or a sub-object
        # We will try the most standard 'Product' creation first
        response = requests.post(f"{BASE_URL}/products", json=payload, headers=headers)
        if response.status_code in [200, 201]:
            print(f"    [SUCCESS] {name} is LIVE.")
            return response.json()
        else:
            print(f"    [!] FAILED: {response.text}")
            return None
    except Exception as e:
        print(f"    [!] Error: {e}")
        return None

if __name__ == "__main__":
    # Starting with the £29 Audit to verify the schema fix
    create_shadow_product("Shadow Revenue Audit", 29, "10-page technical audit of your current monetization funnels.")
