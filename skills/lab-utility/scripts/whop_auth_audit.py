import requests
import json

API_KEY = "apik_EDHYk8A6ZGypR_C4539121_C_ca37cc9553cd6e6ce38e1b889903941db1888d1434c5ff118cd08498cba802"
headers = {"Authorization": f"Bearer {API_KEY}"}

print("\n--- WHOP API: IDENTITY AUDIT ---")
# Check 'Me' endpoint to find Business/User ID
r = requests.get("https://api.whop.com/v1/me", headers=headers)
print(f"[*] Identity: {r.text}")

# List available plans (common endpoint for product discovery)
r2 = requests.get("https://api.whop.com/v1/plans", headers=headers)
print(f"[*] Plans: {r2.text}")
