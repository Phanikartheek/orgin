"""
App & Website Launcher Tools
Gemini calls these to open applications and websites.
"""

import os
import webbrowser
import sqlite3
from app.config import DB_PATH


def open_application(app_name: str) -> str:
    """Open a desktop application by name.
    Use this when the user wants to open a program like Notepad, Calculator,
    Word, Excel, VS Code, Chrome, or any other installed application.

    Args:
        app_name: The name of the application to open (e.g., 'notepad', 'calculator', 'chrome')
    """
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
        con = sqlite3.connect(DB_PATH)
        cursor = con.cursor()
        cursor.execute("SELECT path FROM sys_command WHERE LOWER(name) LIKE ?", (f"%{app_lower}%",))
        results = cursor.fetchall()
        con.close()

        if results:
            os.startfile(results[0][0])
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
    # Add https:// if not present
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # Check database for saved bookmarks
    try:
        con = sqlite3.connect(DB_PATH)
        cursor = con.cursor()
        url_lower = url.lower().replace("https://", "").replace("http://", "").replace("www.", "")
        cursor.execute("SELECT url FROM web_command WHERE LOWER(name) LIKE ?", (f"%{url_lower}%",))
        results = cursor.fetchall()
        con.close()

        if results:
            url = results[0][0]
    except Exception:
        pass

    try:
        os.system(f'start "" "{url}"')
        return f"Opened {url} in the browser."
    except Exception as e:
        return f"Failed to open website: {str(e)}"
