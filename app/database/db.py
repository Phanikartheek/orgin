"""
Database Manager
Handles SQLite database operations and initialization.
"""

import sqlite3
from app.config import DB_PATH


def init_database():
    """Initialize the database with required tables if they don't exist."""
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()

    # System commands table (app paths)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sys_command (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100),
            path VARCHAR(1000)
        )
    """)

    # Web commands table (bookmarked URLs)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS web_command (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100),
            url VARCHAR(1000)
        )
    """)

    # Contacts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY,
            name VARCHAR(200),
            mobile_no VARCHAR(255),
            email VARCHAR(255),
            address VARCHAR(255)
        )
    """)

    # Personal info table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS info (
            name VARCHAR(200),
            designation VARCHAR(200),
            mobileno VARCHAR(50),
            email VARCHAR(255),
            city VARCHAR(200)
        )
    """)

    # Conversation history table (for persistent memory)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_log (
            id INTEGER PRIMARY KEY,
            role VARCHAR(20),
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    con.commit()
    con.close()
    print("[DB] Database initialized successfully.")


def get_connection():
    """Get a new database connection."""
    return sqlite3.connect(DB_PATH)
