"""
Database Manager
Handles Supabase connection and client initialization.
Replaced local SQLite with cloud-hosted Supabase for persistence.
"""

from supabase import create_client, Client
from app.config import SUPABASE_URL, SUPABASE_KEY

# Initialize Supabase client
# This client will be used for all database operations across the app
supabase_client: Client = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("[DB] Supabase client initialized successfully.")
    except Exception as e:
        print(f"[DB] Error initializing Supabase client: {e}")
else:
    print("[DB] Warning: SUPABASE_URL or SUPABASE_KEY missing from environment.")

def get_client() -> Client:
    """Get the initialized Supabase client."""
    return supabase_client

# Deprecated SQLite functions (kept for backward compatibility during migration)
def init_database():
    """No-op for Supabase; schema must be initialized via Supabase SQL Editor."""
    pass

def get_connection():
    """Deprecated: Use get_client() for Supabase operations."""
    raise DeprecatedAppError("get_connection() is deprecated for SQLite. Use Supabase client.")

class DeprecatedAppError(Exception):
    pass
