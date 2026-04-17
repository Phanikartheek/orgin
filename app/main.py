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

from app.config import FRONTEND_DIR, HOST, PORT, IS_CLOUD
from app.database.db import get_client
from app.websocket.handler import manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # --- Startup ---
    print("\n" + "=" * 50)
    print("  🤖 JARVIS AI Assistant — Starting Up")
    print("=" * 50)
    
    try:
        # Check Supabase connection
        client = get_client()
        if client:
            print("[DB] Supabase connected.")
        else:
            print("[DB] Warning: Supabase client not initialized.")
    except Exception as e:
        print(f"[Startup Error] Database connectivity issue: {e}")
        print("Continuing startup anyway...")

    print(f"  🌐 Server running on: http://{HOST}:{PORT}")
    if IS_CLOUD:
        print("  ☁️  Cloud environment detected (Render/Production)")
    else:
        print("  🏠 Local environment detected")
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
        client = get_client()
        response = client.table("info").select("*").limit(1).execute()
        if response.data:
            r = response.data[0]
            return {"data": {"name": r.get("name"), "designation": r.get("designation"), "mobileno": r.get("mobileno"), "email": r.get("email"), "city": r.get("city")}}
        return {"data": None}
    except Exception as e:
        print(f"[API Error] get_personal_info: {e}")
        return {"data": None}


@app.post("/api/personal-info")
async def update_personal_info(request: Request):
    """Update user's personal information."""
    body = await request.json()
    try:
        client = get_client()
        # Since we only have one user/info row in this simple version, 
        # we check for existing or just upsert if ID is known. 
        # For simplicity, we'll fetch existing first or just assume ID 1.
        response = client.table("info").select("id").limit(1).execute()
        
        data = {
            "name": body["name"],
            "designation": body["designation"],
            "mobileno": body["mobileno"],
            "email": body["email"],
            "city": body["city"]
        }

        if response.data:
            client.table("info").update(data).eq("id", response.data[0]["id"]).execute()
        else:
            client.table("info").insert(data).execute()
            
        return {"success": True}
    except Exception as e:
        print(f"[API Error] update_personal_info: {e}")
        return {"success": False, "error": str(e)}


@app.get("/api/sys-commands")
async def get_sys_commands():
    """Get all system commands."""
    try:
        client = get_client()
        response = client.table("sys_command").select("*").execute()
        return {"data": response.data or []}
    except Exception as e:
        print(f"[API Error] get_sys_commands: {e}")
        return {"data": []}


@app.post("/api/sys-commands")
async def add_sys_command(request: Request):
    """Add a new system command."""
    body = await request.json()
    try:
        client = get_client()
        client.table("sys_command").insert({"name": body["name"], "path": body["path"]}).execute()
        return {"success": True}
    except Exception as e:
        print(f"[API Error] add_sys_command: {e}")
        return {"success": False, "error": str(e)}


@app.delete("/api/sys-commands/{command_id}")
async def delete_sys_command(command_id: int):
    """Delete a system command."""
    try:
        client = get_client()
        client.table("sys_command").delete().eq("id", command_id).execute()
        return {"success": True}
    except Exception as e:
        print(f"[API Error] delete_sys_command: {e}")
        return {"success": False, "error": str(e)}


@app.get("/api/web-commands")
async def get_web_commands():
    """Get all web commands."""
    try:
        client = get_client()
        response = client.table("web_command").select("*").execute()
        return {"data": response.data or []}
    except Exception as e:
        print(f"[API Error] get_web_commands: {e}")
        return {"data": []}


@app.post("/api/web-commands")
async def add_web_command(request: Request):
    """Add a new web command."""
    body = await request.json()
    try:
        client = get_client()
        client.table("web_command").insert({"name": body["name"], "url": body["url"]}).execute()
        return {"success": True}
    except Exception as e:
        print(f"[API Error] add_web_command: {e}")
        return {"success": False, "error": str(e)}


@app.delete("/api/web-commands/{command_id}")
async def delete_web_command(command_id: int):
    """Delete a web command."""
    try:
        client = get_client()
        client.table("web_command").delete().eq("id", command_id).execute()
        return {"success": True}
    except Exception as e:
        print(f"[API Error] delete_web_command: {e}")
        return {"success": False, "error": str(e)}


@app.get("/api/contacts")
async def get_contacts():
    """Get all contacts."""
    try:
        client = get_client()
        response = client.table("contacts").select("*").execute()
        return {"data": response.data or []}
    except Exception as e:
        print(f"[API Error] get_contacts: {e}")
        return {"data": []}


@app.post("/api/contacts")
async def add_contact_api(request: Request):
    """Add a new contact."""
    body = await request.json()
    try:
        client = get_client()
        client.table("contacts").insert({
            "name": body["name"],
            "mobile_no": body["mobile_no"],
            "email": body.get("email", ""),
            "city": body.get("city", "")
        }).execute()
        return {"success": True}
    except Exception as e:
        print(f"[API Error] add_contact_api: {e}")
        return {"success": False, "error": str(e)}


@app.delete("/api/contacts/{contact_id}")
async def delete_contact(contact_id: int):
    """Delete a contact."""
    try:
        client = get_client()
        client.table("contacts").delete().eq("id", contact_id).execute()
        return {"success": True}
    except Exception as e:
        print(f"[API Error] delete_contact: {e}")
        return {"success": False, "error": str(e)}
