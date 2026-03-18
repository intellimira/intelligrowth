import requests
import json

API_KEY = "apik_EDHYk8A6ZGypR_C4539121_C_ca37cc9553cd6e6ce38e1b889903941db1888d1434c5ff118cd08498cba802"
BIZ_ID = "biz_wJSN9AZSnng2vT"
URL = "https://api.whop.com/graphql"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Query to list products for a specific company
query = """
query GetProducts($companyId: ID!) {
  company(id: $companyId) {
    name
    products {
      edges {
        node {
          id
          name
          visibility
        }
      }
    }
  }
}
"""

def run_audit():
    print("\n--- ACCT: GRAPHQL DATABASE AUDIT ---")
    variables = {"companyId": BIZ_ID}
    try:
        response = requests.post(URL, json={'query': query, 'variables': variables}, headers=headers)
        if response.status_code == 200:
            data = response.json()
            products = data.get('data', {}).get('company', {}).get('products', {}).get('edges', [])
            print(f"[*] Found {len(products)} products in the database:")
            for p in products:
                node = p['node']
                print(f"    - [{node['id']}] {node['name']} ({node['visibility']})")
        else:
            print(f"[!] FAILED: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    run_audit()
