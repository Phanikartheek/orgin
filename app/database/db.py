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
    if not SUPABASE_URL or not SUPABASE_KEY or "supabase.co" not in SUPABASE_URL:
        print(f"[DB] Warning: SUPABASE_URL or SUPABASE_KEY is missing or invalid. Check your environment settings.")
        _supabase_client = None
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
