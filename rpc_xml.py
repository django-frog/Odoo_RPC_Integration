import xmlrpc.client
from dotenv import load_dotenv
import os


# ------------------- Load environment variables -------------------
load_dotenv()

url = os.getenv("ODOO_URL")
db = os.getenv("ODOO_DB")
username = os.getenv("ODOO_USERNAME")
password = os.getenv("ODOO_PASSWORD")

# ------------------- Step 1: Authenticate -------------------
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

if uid:
    print(f"Authenticated as {username} (uid: {uid})")
else:
    print("Failed to authenticate.")
    exit()

# ------------------- Step 2: Connect to Object Endpoint -------------------
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# ------------------- Step 3: Fetch Partners -------------------
partners = models.execute_kw(
    db, uid, password,
    'res.partner', 'search_read',
    [[]],  # Empty domain = all records
    {'fields': ['id', 'name', 'email'], 'limit': 10}
)

# ------------------- Step 4: Display Partners -------------------
print("\nPartner List:")
for partner in partners:
    print(f"{partner['id']}: {partner['name']} ({partner.get('email', 'no email')})")
