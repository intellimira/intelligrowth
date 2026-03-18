import requests
import json

API_KEY = "apik_EDHYk8A6ZGypR_C4539121_C_ca37cc9553cd6e6ce38e1b889903941db1888d1434c5ff118cd08498cba802"
GRAPHQL_URL = "https://api.whop.com/graphql"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Query to find the 'Me' context and Company IDs in GraphQL
query = """
query {
  me {
    id
    username
    companies {
      edges {
        node {
          id
          name
        }
      }
    }
  }
}
"""

def run_query():
    print("\n--- WHOP AGENTIC MAPPING: GRAPHQL PROBE ---")
    try:
        response = requests.post(GRAPHQL_URL, json={'query': query}, headers=headers)
        print(f"[*] GraphQL Response Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"[!] DATA: {json.dumps(data, indent=2)}")
        else:
            print(f"[!] FAILED: {response.text}")
    except Exception as e:
        print(f"[!] Connection Error: {e}")

if __name__ == "__main__":
    run_query()
