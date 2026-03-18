import requests
import json

API_KEY = "apik_EDHYk8A6ZGypR_C4539121_C_ca37cc9553cd6e6ce38e1b889903941db1888d1434c5ff118cd08498cba802"
BIZ_ID = "biz_wJSN9AZSnng2vT"
URL = "https://api.whop.com/graphql"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# The exact mutation required to create a product in Whop's GraphQL mesh
mutation = """
mutation CreateProduct($input: CreateProductInput!) {
  createProduct(input: $input) {
    product {
      id
      name
    }
  }
}
"""

def create_product(name, price):
    variables = {
        "input": {
            "companyId": BIZ_ID,
            "name": name,
            "visibility": "PUBLIC"
        }
    }
    print(f"[*] AGENT: GraphQL Injecting {name}...")
    try:
        response = requests.post(URL, json={'query': mutation, 'variables': variables}, headers=headers)
        if response.status_code == 200:
            print(f"    [SUCCESS] {name} Instantiated.")
            return response.json()
        else:
            print(f"    [!] FAILED: {response.text}")
    except Exception as e:
        print(f"    [!] Error: {e}")

if __name__ == "__main__":
    create_product("Shadow Revenue Audit", 29)
    create_product("Priority Launch Slot", 49)
    create_product("White-Glove Vault Setup", 199)
