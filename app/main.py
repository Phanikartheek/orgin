"""
Jarvis AI-Native Voice Assistant — FastAPI Server
Main application entry point that serves the frontend and WebSocket API.
"""

import os
import json
import sqlite3
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse

from app.config import FRONTEND_DIR, DB_PATH, HOST, PORT
from app.database.db import init_database, get_connection
from app.websocket.handler import manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # --- Startup ---
    print("\n" + "=" * 50)
    print("  🤖 JARVIS AI Assistant — Starting Up")
    print("=" * 50)
    
    try:
        # Ensure database directory exists
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        # Initialize database
        init_database()

        # Copy existing database if it exists in old location
        old_db = os.path.join(os.path.dirname(FRONTEND_DIR), "jarvis.db")
        if os.path.exists(old_db) and not os.path.exists(DB_PATH):
            import shutil
            shutil.copy2(old_db, DB_PATH)
            print("[DB] Migrated existing database.")
    except Exception as e:
        print(f"[Startup Error] Non-critical error during initialization: {e}")
        print("Continuing startup anyway...")

    print(f"  🌐 Open http://{HOST}:{PORT} in your browser")
    print("=" * 50 + "\n")

    yield

    # --- Shutdown ---
    print("\n[Server] Jarvis shutting down. Goodbye, Sir.")


# Create FastAPI app
app = FastAPI(
    title="Jarvis AI Assistant",
    description="AI-Native Voice Assistant powered by Gemini",
    version="2.0.0",
    lifespan=lifespan,
)

# Serve frontend static files
app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIR, "assets")), name="assets")
app.mount("/css", StaticFiles(directory=os.path.join(FRONTEND_DIR, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(FRONTEND_DIR, "js")), name="js")


# --- Pages ---

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Serve the main Jarvis UI."""
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


# --- WebSocket ---

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.handle_message(websocket, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"[WS] Connection error: {e}")
        manager.disconnect(websocket)


# --- REST API for Settings ---

@app.get("/api/personal-info")
async def get_personal_info():
    """Get user's personal information."""
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM info")
        result = cursor.fetchone()
        con.close()
        if result:
            return {"data": {"name": result[0], "designation": result[1], "mobileno": result[2], "email": result[3], "city": result[4]}}
        return {"data": None}
    except Exception:
        return {"data": None}


@app.post("/api/personal-info")
async def update_personal_info(request: Request):
    """Update user's personal information."""
    body = await request.json()
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("SELECT COUNT(*) FROM info")
        count = cursor.fetchone()[0]

        if count > 0:
            cursor.execute(
                "UPDATE info SET name=?, designation=?, mobileno=?, email=?, city=?",
                (body["name"], body["designation"], body["mobileno"], body["email"], body["city"]),
            )
        else:
            cursor.execute(
                "INSERT INTO info (name, designation, mobileno, email, city) VALUES (?, ?, ?, ?, ?)",
                (body["name"], body["designation"], body["mobileno"], body["email"], body["city"]),
            )
        con.commit()
        con.close()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/api/sys-commands")
async def get_sys_commands():
    """Get all system commands."""
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM sys_command")
        results = cursor.fetchall()
        con.close()
        return {"data": [{"id": r[0], "name": r[1], "path": r[2]} for r in results]}
    except Exception:
        return {"data": []}


@app.post("/api/sys-commands")
async def add_sys_command(request: Request):
    """Add a new system command."""
    body = await request.json()
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO sys_command VALUES (?, ?, ?)", (None, body["name"], body["path"]))
        con.commit()
        con.close()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.delete("/api/sys-commands/{command_id}")
async def delete_sys_command(command_id: int):
    """Delete a system command."""
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("DELETE FROM sys_command WHERE id = ?", (command_id,))
        con.commit()
        con.close()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/api/web-commands")
async def get_web_commands():
    """Get all web commands."""
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM web_command")
        results = cursor.fetchall()
        con.close()
        return {"data": [{"id": r[0], "name": r[1], "url": r[2]} for r in results]}
    except Exception:
        return {"data": []}


@app.post("/api/web-commands")
async def add_web_command(request: Request):
    """Add a new web command."""
    body = await request.json()
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO web_command VALUES (?, ?, ?)", (None, body["name"], body["url"]))
        con.commit()
        con.close()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.delete("/api/web-commands/{command_id}")
async def delete_web_command(command_id: int):
    """Delete a web command."""
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("DELETE FROM web_command WHERE id = ?", (command_id,))
        con.commit()
        con.close()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/api/contacts")
async def get_contacts():
    """Get all contacts."""
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM contacts")
        results = cursor.fetchall()
        con.close()
        return {"data": [{"id": r[0], "name": r[1], "mobile_no": r[2], "email": r[3], "city": r[4]} for r in results]}
    except Exception:
        return {"data": []}


@app.post("/api/contacts")
async def add_contact_api(request: Request):
    """Add a new contact."""
    body = await request.json()
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO contacts VALUES (?, ?, ?, ?, ?)",
            (None, body["name"], body["mobile_no"], body.get("email", ""), body.get("city", "")),
        )
        con.commit()
        con.close()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.delete("/api/contacts/{contact_id}")
async def delete_contact(contact_id: int):
    """Delete a contact."""
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        con.commit()
        con.close()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}
