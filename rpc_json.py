import requests
from dotenv import load_dotenv
import os

# ------------------- Load environment variables -------------------
load_dotenv()

url = os.getenv("ODOO_URL")  # e.g. "http://localhost:8069"
db = os.getenv("ODOO_DB")
username = os.getenv("ODOO_USERNAME")
password = os.getenv("ODOO_PASSWORD")

jsonrpc_url = f"{url}/jsonrpc"
headers = {"Content-Type": "application/json"}

def jsonrpc_call(service, method, args):
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": service,
            "method": method,
            "args": args
        },
        "id": 1,
    }
    response = requests.post(jsonrpc_url, json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    if 'error' in result:
        raise Exception(result['error'])
    return result.get("result")

# ------------------- Step 1: Authenticate -------------------
uid = jsonrpc_call("common", "authenticate", [db, username, password, {}])

if uid:
    print(f"Authenticated as {username} (uid: {uid})")
else:
    print("Failed to authenticate.")
    exit()

# ------------------- Step 2: Fetch Partners -------------------
partners = jsonrpc_call(
    "object",
    "execute_kw",
    [
        db,
        uid,
        password,
        'res.partner',
        'search_read',
        [[]],  # domain: all records
        {'fields': ['id', 'name', 'email'], 'limit': 10}
    ]
)

# ------------------- Step 3: Display Partners -------------------
print("\nPartner List:")
for partner in partners:
    print(f"{partner['id']}: {partner['name']} ({partner.get('email', 'no email')})")
