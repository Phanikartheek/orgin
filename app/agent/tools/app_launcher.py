"""
App & Website Launcher Tools
Gemini calls these to open applications and websites.
Now using Supabase for custom app and bookmark lookups.
"""

import os
import webbrowser
from app.config import IS_CLOUD
from app.database.db import get_client


def open_application(app_name: str) -> str:
    """Open a desktop application by name.
    Use this when the user wants to open a program like Notepad, Calculator,
    Word, Excel, VS Code, Chrome, or any other installed application.

    Args:
        app_name: The name of the application to open (e.g., 'notepad', 'calculator', 'chrome')
    """
    if IS_CLOUD:
        return f"[Cloud Demo Mode] I would have opened the '{app_name}' application on your computer."

    # Common Windows applications mapping
    common_apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "explorer": "explorer.exe",
        "file explorer": "explorer.exe",
        "cmd": "cmd.exe",
        "command prompt": "cmd.exe",
        "terminal": "wt.exe",
        "powershell": "powershell.exe",
        "task manager": "taskmgr.exe",
        "control panel": "control.exe",
        "settings": "ms-settings:",
        "snipping tool": "snippingtool.exe",
    }

    app_lower = app_name.lower().strip()

    # Check common apps first
    if app_lower in common_apps:
        try:
            os.startfile(common_apps[app_lower])
            return f"Opened {app_name} successfully."
        except Exception as e:
            return f"Failed to open {app_name}: {str(e)}"

    # Check database for custom app paths
    try:
        client = get_client()
        if client:
            response = client.table("sys_command").select("path").ilike("name", f"%{app_lower}%").execute()
            if response.data:
                os.startfile(response.data[0]["path"])
                return f"Opened {app_name} successfully."
    except Exception:
        pass

    # Try to open directly via system
    try:
        os.system(f'start {app_name}')
        return f"Attempting to open {app_name}."
    except Exception as e:
        return f"Could not find application '{app_name}'. Error: {str(e)}"


def open_website(url: str) -> str:
    """Open a website URL in the default web browser.
    Use this when the user wants to open a specific website or URL.

    Args:
        url: The website URL to open (e.g., 'https://google.com', 'github.com')
    """
    if IS_CLOUD:
        return f"[Cloud Demo Mode] I would have opened the website '{url}' in your browser."

    # Add https:// if not present
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # Check database for saved bookmarks
    try:
        client = get_client()
        if client:
            url_query = url.lower().replace("https://", "").replace("http://", "").replace("www.", "")
            response = client.table("web_command").select("url").ilike("name", f"%{url_query}%").execute()
            if response.data:
                url = response.data[0]["url"]
    except Exception:
        pass

    try:
        os.system(f'start "" "{url}"')
        return f"Opened {url} in the browser."
    except Exception as e:
        return f"Failed to open website: {str(e)}"
