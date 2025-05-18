from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ------------------ ENV variables ------------------
url = os.getenv("ODOO_URL")
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
        "id": 1
    }
    response = requests.post(jsonrpc_url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    if 'error' in data:
        raise Exception(data['error'])
    return data['result']

def get_uid():
    return jsonrpc_call("common", "authenticate", [db, username, password, {}])

# ------------------ Routes ------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/partners")
async def get_partners():
    try:
        uid = get_uid()
        partners = jsonrpc_call(
            "object",
            "execute_kw",
            [db, uid, password, 'res.partner', 'search_read', [[]],
             {'fields': ['id', 'name', 'email', 'image_1920'], 'limit': 10}]
        )
        return JSONResponse(partners)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/partners/search")
async def search_partners(name: str = ""):
    try:
        uid = get_uid()
        domain = [['name', 'ilike', name]] if name else []
        partners = jsonrpc_call(
            "object",
            "execute_kw",
            [db, uid, password, 'res.partner', 'search_read', [domain],
             {'fields': ['id', 'name', 'email', 'image_1920'], 'limit': 20}]
        )
        return JSONResponse(partners)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

class PartnerCreate(BaseModel):
    name: str
    email: str = None
    image_1920: str = None  # base64 encoded image (optional)

@app.post("/partners")
async def create_partner(partner: PartnerCreate):
    try:
        uid = get_uid()
        partner_data = {
            "name": partner.name,
        }
        if partner.email:
            partner_data["email"] = partner.email
        if partner.image_1920:
            partner_data["image_1920"] = partner.image_1920

        partner_id = jsonrpc_call(
            "object",
            "execute_kw",
            [db, uid, password, 'res.partner', 'create', [partner_data]]
        )
        return {"id": partner_id}
    
    except RequestValidationError as e:
        return JSONResponse(status_code=422, content={"error": str(e)})
    
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.delete("/partners/{partner_id}")
async def delete_partner(partner_id: int):
    try:
        uid = get_uid()
        result = jsonrpc_call(
            "object",
            "execute_kw",
            [db, uid, password, 'res.partner', 'unlink', [[partner_id]]]
        )
        return {"deleted": result}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
