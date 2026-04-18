"""
Database Manager
Handles Supabase connection and client initialization.
Replaced local SQLite with cloud-hosted Supabase for persistence.
"""

from supabase import create_client, Client
from app.config import SUPABASE_URL, SUPABASE_KEY

# Global client holder
_supabase_client: Client = None

def init_client():
    """Explicitly initialize the Supabase client. Called during app startup."""
    global _supabase_client
    
    # Check for missing OR placeholder strings
    placeholders = ["your_project_url_here", "your_service_role_key_here", "your_project_id", ""]
    
    if not SUPABASE_URL or SUPABASE_URL in placeholders or not SUPABASE_KEY or SUPABASE_KEY in placeholders:
        print("[DB] Warning: SUPABASE_URL or SUPABASE_KEY missing or invalid placeholder. Client not initialized.")
        return

    try:
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("[DB] Supabase client initialized successfully.")
    except Exception as e:
        print(f"[DB] Error initializing Supabase client: {e}")

def get_client() -> Client:
    """Get the initialized Supabase client."""
    return _supabase_client

# Deprecated SQLite functions (kept for backward compatibility during migration)
def init_database():
    """No-op for Supabase; schema must be initialized via Supabase SQL Editor."""
    pass

def get_connection():
    """Deprecated: Use get_client() for Supabase operations."""
    raise DeprecatedAppError("get_connection() is deprecated for SQLite. Use Supabase client.")

class DeprecatedAppError(Exception):
    pass
