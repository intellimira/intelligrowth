import requests
import json

API_KEY = "apik_EDHYk8A6ZGypR_C4539121_C_ca37cc9553cd6e6ce38e1b889903941db1888d1434c5ff118cd08498cba802"
BASE_URL = "https://api.whop.com/v1"

def create_product(name, price, desc):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    # Whop API v1 uses 'plans' and 'visibility' structures
    payload = {
        "name": name,
        "description": desc,
        "visibility": "public",
        "pricing_type": "one_time",
        "price": float(price)
    }
    
    print(f"[*] API: Creating {name} (£{price})...")
    try:
        # Note: We use the /products endpoint as per standard API patterns
        response = requests.post(f"{BASE_URL}/products", json=payload, headers=headers)
        if response.status_code in [200, 201]:
            print(f"    [+] SUCCESS: {name} is now LIVE.")
            return response.json()
        else:
            print(f"    [!] FAILED: {response.text}")
            return None
    except Exception as e:
        print(f"    [!] Error: {e}")
        return None

if __name__ == "__main__":
    products = [
        {"name": "Shadow Revenue Audit", "price": "29", "desc": "10-page deep-dive into your audience DNA and revenue leaks."},
        {"name": "Priority Launch Slot", "price": "49", "desc": "Bypass the 30-day waitlist and launch your vault within 7 days."},
        {"name": "White-Glove Vault Setup", "price": "199", "desc": "Full technical build of your 14-day monetization vault."}
    ]
    
    print("\n--- ACCT: API-DIRECT MONETIZATION INJECTION ---")
    for p in products:
        create_product(p["name"], p["price"], p["desc"])
