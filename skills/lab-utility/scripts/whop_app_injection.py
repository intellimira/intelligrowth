import requests
import json

API_KEY = "apik_lnITyVEbzdMtI_A2028519_C_e80ef7e27e436460307fc5cfb24332c8d0131306cc137f133a94fbf1f746d7"
APP_ID = "app_Cg90rT0pn7aJKA"
BASE_URL = "https://api.whop.com/v1"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def instantiate_monetization():
    products = [
        {"name": "Shadow Revenue Audit", "price": 29.00, "desc": "10-page deep-dive into your audience DNA and revenue leaks."},
        {"name": "Priority Launch Slot", "price": 49.00, "desc": "Bypass the 30-day waitlist and launch your vault within 7 days."},
        {"name": "White-Glove Vault Setup", "price": 199.00, "desc": "Full technical build of your 14-day monetization vault."}
    ]
    
    print("\n--- ACCT: NATIVE APP PRODUCT INJECTION ---")
    
    # First, let's find the company_id associated with this App Key
    # We use the 'Me' or 'Companies' endpoint with the new elevated key
    try:
        biz_req = requests.get(f"{BASE_URL}/companies", headers=headers)
        if biz_req.status_code == 200:
            companies = biz_req.json().get('companies', [])
            if not companies:
                print("[!] No companies found for this App Key.")
                return
            
            company_id = companies[0]['id']
            print(f"[+] Authorized Company Found: {companies[0]['name']} ({company_id})")
            
            for prod in products:
                print(f"[*] Instantiating: {prod['name']}...")
                payload = {
                    "company_id": company_id,
                    "name": prod["name"],
                    "description": prod["desc"],
                    "visibility": "public",
                    "pricing_type": "one_time",
                    "price": prod["price"]
                }
                # Using the standard creation endpoint
                res = requests.post(f"{BASE_URL}/plans", json=payload, headers=headers)
                if res.status_code in [200, 201]:
                    print(f"    [SUCCESS] {prod['name']} is LIVE.")
                else:
                    print(f"    [FAILED] {res.text}")
        else:
            print(f"[!] Access Denied: {biz_req.text}")
            
    except Exception as e:
        print(f"[!] Bridge Error: {e}")

if __name__ == "__main__":
    instantiate_monetization()
