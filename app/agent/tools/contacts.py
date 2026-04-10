"""
Contact Management Tools
Gemini calls these to manage the user's contact list.
"""

import sqlite3
from app.config import DB_PATH


def find_contact(name: str) -> str:
    """Search for a contact by name in the phone book.
    Use this when the user asks to look up a contact's information.

    Args:
        name: The name of the contact to search for
    """
    try:
        con = sqlite3.connect(DB_PATH)
        cursor = con.cursor()
        cursor.execute(
            "SELECT name, mobile_no, email, address FROM contacts WHERE LOWER(name) LIKE ?",
            (f"%{name.lower()}%",),
        )
        results = cursor.fetchall()
        con.close()

        if not results:
            return f"No contact found matching '{name}'."

        contacts_info = []
        for r in results:
            info = f"Name: {r[0]}, Phone: {r[1]}"
            if r[2]:
                info += f", Email: {r[2]}"
            if r[3]:
                info += f", City: {r[3]}"
            contacts_info.append(info)

        return "Found contacts:\n" + "\n".join(contacts_info)
    except Exception as e:
        return f"Error searching contacts: {str(e)}"


def add_contact(name: str, mobile_no: str, email: str = "", city: str = "") -> str:
    """Add a new contact to the phone book.
    Use this when the user wants to save a new contact.

    Args:
        name: The contact's full name
        mobile_no: The contact's phone number
        email: The contact's email address (optional)
        city: The contact's city (optional)
    """
    try:
        con = sqlite3.connect(DB_PATH)
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO contacts VALUES (?, ?, ?, ?, ?)",
            (None, name, mobile_no, email, city),
        )
        con.commit()
        con.close()
        return f"Contact '{name}' added successfully."
    except Exception as e:
        return f"Failed to add contact: {str(e)}"


def list_contacts() -> str:
    """List all contacts in the phone book.
    Use this when the user wants to see all their saved contacts.
    """
    try:
        con = sqlite3.connect(DB_PATH)
        cursor = con.cursor()
        cursor.execute("SELECT name, mobile_no FROM contacts ORDER BY name")
        results = cursor.fetchall()
        con.close()

        if not results:
            return "No contacts saved yet."

        contacts_list = [f"{i+1}. {r[0]} — {r[1]}" for i, r in enumerate(results)]
        return "Your contacts:\n" + "\n".join(contacts_list)
    except Exception as e:
        return f"Error listing contacts: {str(e)}"
