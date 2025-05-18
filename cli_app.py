import typer
import xmlrpc.client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
url = os.getenv("ODOO_URL")
db = os.getenv("ODOO_DB")
username = os.getenv("ODOO_USERNAME")
password = os.getenv("ODOO_PASSWORD")

# Auth and connect to endpoints
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# CLI app
app = typer.Typer()

@app.command()
def list(limit: int = 10):
    """
    List the first N partners.
    """
    partners = models.execute_kw(
        db, uid, password,
        'res.partner', 'search_read',
        [[]],
        {'fields': ['id', 'name', 'email'], 'limit': limit}
    )
    for partner in partners:
        typer.echo(f"{partner['id']}: {partner['name']} ({partner.get('email', 'no email')})")

@app.command()
def search(name: str):
    """
    Search partners by name (partial match).
    """
    domain = [['name', 'ilike', name]]
    partners = models.execute_kw(
        db, uid, password,
        'res.partner', 'search_read',
        [domain],
        {'fields': ['id', 'name', 'email']}
    )
    if not partners:
        typer.echo("❌ No matching partners found.")
        return

    for partner in partners:
        typer.echo(f"{partner['id']}: {partner['name']} ({partner.get('email', 'no email')})")

@app.command()
def create(name: str, email: str = ""):
    """
    Create a new partner.
    """
    partner_id = models.execute_kw(
        db, uid, password,
        'res.partner', 'create',
        [{
            'name': name,
            'email': email
        }]
    )
    typer.echo(f"✅ Partner created with ID: {partner_id}")

@app.command()
def delete(id: int):
    """
    Delete a partner by ID.
    """
    result = models.execute_kw(
        db, uid, password,
        'res.partner', 'unlink',
        [[id]]
    )
    if result:
        typer.echo(f"🗑️ Partner with ID {id} deleted.")
    else:
        typer.echo("❌ Failed to delete partner. Check the ID and your permissions.")

if __name__ == "__main__":
    app()
