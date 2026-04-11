"""
Jarvis AI Assistant — Configuration
Loads settings from .env file and provides type-safe access.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- API Keys ---
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

# --- Assistant Settings ---
ASSISTANT_NAME: str = os.getenv("ASSISTANT_NAME", "Jarvis")

# --- Voice Settings ---
TTS_VOICE: str = "en-US-GuyNeural"  # Microsoft Edge TTS voice (male, natural)
TTS_RATE: str = "+10%"              # Speech rate adjustment
STT_LANGUAGE: str = "en-in"         # Speech recognition language

# --- Server Settings ---
# We use 0.0.0.0 in cloud environments to allow external connections
HOST: str = os.getenv("HOST", "0.0.0.0") if (os.getenv("RENDER") or os.getenv("PORT") or os.getenv("K_SERVICE")) else "localhost"
PORT: int = int(os.getenv("PORT", 8000))

# --- Cloud Detection (For Recruiter Demo) ---
# We detect if we are on Render or similar to disable desktop-only features
IS_CLOUD: bool = True if (os.getenv("RENDER") or os.getenv("PORT") or os.getenv("K_SERVICE")) else False

# --- Paths ---
BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR: str = os.path.join(BASE_DIR, "frontend")
DATA_DIR: str = os.path.join(BASE_DIR, "data")
DB_PATH: str = os.path.join(DATA_DIR, "jarvis.db")
AUDIO_OUTPUT_DIR: str = os.path.join(FRONTEND_DIR, "assets", "audio")

# --- Face Auth ---
FACE_AUTH_ENABLED: bool = True
HAARCASCADE_PATH: str = os.path.join(BASE_DIR, "legacy", "engine", "auth", "haarcascade_frontalface_default.xml")
TRAINER_PATH: str = os.path.join(BASE_DIR, "legacy", "engine", "auth", "trainer", "trainer.yml")
FACE_NAMES: list = ["", "Kartheek"]  # Names for face IDs

# --- Conversation Memory ---
MAX_MEMORY_TURNS: int = 20  # Number of conversation turns to remember
