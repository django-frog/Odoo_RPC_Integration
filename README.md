
# Odoo Partners Integration Projects

This repository contains multiple example projects demonstrating integration with Odoo's JSON-RPC API to manage partner records. The projects showcase different approaches: a simple FastAPI backend, a CLI tool using Typer, and a full-featured web app with create, search, and delete functionality using FastAPI, Alpine.js, and Tailwind CSS.

---

## Project Overview

### 1. Simple FastAPI Partners API

A minimal FastAPI application that connects to an Odoo instance and retrieves partner records via JSON-RPC. It exposes a single endpoint `/partners` that returns a JSON list of partners with basic fields such as `id`, `name`, `email`, and `image_1920`.

- Demonstrates JSON-RPC calls to Odoo
- Uses environment variables for Odoo connection configuration
- Returns partner data as JSON

---

### 2. CLI Tool using Typer

A command-line interface tool built with [Typer](https://typer.tiangolo.com/) that interacts with the Odoo partners data via JSON-RPC. It allows you to:

- List all partners
- Create new partners
- Delete partners by ID

This tool is useful for quick partner management from the terminal without a UI.

---

### 3. Full Web Application (CRUD)

A more advanced web app using:

- **FastAPI** backend exposing RESTful endpoints for partner CRUD operations
- **Alpine.js** (via CDN) for frontend reactivity and API calls
- **Tailwind CSS** (via CDN) for styling and responsive UI

Features include:

- Display partner list with images and emails
- Search partners by name
- Create new partners (with optional base64-encoded image)
- Delete partners

This app demonstrates building a lightweight but functional full-stack application with minimal dependencies.

---

## Prerequisites

- Python 3.8+
- An accessible Odoo instance (with URL, DB, username, and password)
- `requests`, `fastapi`, `uvicorn`, `typer`, `jinja2` Python packages installed (see Installation)
- Internet connection for CDN scripts (Alpine.js and Tailwind CSS)

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/django-frog/Odoo_RPC_Integration.git
   cd odoo-partners-integration
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your Odoo credentials:

   ```env
   ODOO_URL=https://your-odoo-instance.com
   ODOO_DB=your_database
   ODOO_USERNAME=your_username
   ODOO_PASSWORD=your_password
   ```

---

## Usage

### 1. Run the Simple Partners API Version

#### For XML-RPC Version

```bash
python rpc_xml.py
```

#### For JSON-RPC Version

```bash
python rpc_json.py
```

---

### 2. Use the CLI Tool

Run the CLI Typer app:

```bash
python cli_app.py [command]
```

Commands:

- `list` - List all partners
- `create --name NAME --email EMAIL` - Create a new partner
- `delete --id PARTNER_ID` - Delete a partner by ID

Example:

```bash
python cli_app.py create --name "New Partner" --email "partner@example.com"
python cli_app.py list
python cli_app.py delete --id 5
```

---

### 3. Run the Full Web Application

```bash
uvicorn web_app:app --reload
```

Open in your browser:

```
http://localhost:8000/
```

Features:

- View partners list with images
- Search partners by name
- Create new partner with optional base64 image input
- Delete partners

---

## Project Structure

```
├── rpc_xml.py           # Simple XML-RPC Integration returning partners
├── rpc_json.py          # Simple XML-JSON Integration returning partners
├── cli_app.py           # Typer CLI app for managing partners
├── web_app.py           # Full FastAPI web app with CRUD
├── templates/
│   └── index.html       # Jinja2 template for web app frontend
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---


## License

GPL License © Mohammad Hamdan

---

Feel free to open issues or submit pull requests to improve the projects!

---

**Enjoy managing your Odoo partners easily with these integration examples!**
