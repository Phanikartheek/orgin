"""
Jarvis AI-Native Voice Assistant
Entry point — starts the FastAPI server.
"""

import os
import webbrowser
import threading
import uvicorn
from app.config import HOST, PORT


def open_browser():
    """Open the browser after a short delay to let the server start."""
    import time
    time.sleep(2)
    webbrowser.open(f"http://{HOST}:{PORT}")


if __name__ == "__main__":
    # Open browser in a separate thread (LOCAL ONLY)
    if not os.getenv("RENDER") and not os.getenv("PORT") and not os.getenv("K_SERVICE"):
        threading.Thread(target=open_browser, daemon=True).start()

    # Start the FastAPI server
    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=False,
        log_level="info",
    )