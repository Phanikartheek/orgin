"""
Contact Management Tools
Gemini calls these to manage the user's contact list.
Now using Supabase for cloud persistence.
"""

from app.database.db import get_client

def find_contact(name: str) -> str:
    """Search for a contact by name in the phone book.
    Use this when the user asks to look up a contact's information.

    Args:
        name: The name of the contact to search for
    """
    try:
        client = get_client()
        if not client:
            return "Error: Supabase client not initialized."

        # Search using case-insensitive ilike
        response = client.table("contacts").select("*").ilike("name", f"%{name}%").execute()
        results = response.data

        if not results:
            return f"No contact found matching '{name}'."

        contacts_info = []
        for r in results:
            info = f"Name: {r['name']}, Phone: {r['mobile_no']}"
            if r.get('email'):
                info += f", Email: {r['email']}"
            if r.get('city'):
                info += f", City: {r['city']}"
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
        client = get_client()
        if not client:
            return "Error: Supabase client not initialized."

        client.table("contacts").insert({
            "name": name,
            "mobile_no": mobile_no,
            "email": email,
            "city": city
        }).execute()
        
        return f"Contact '{name}' added successfully."
    except Exception as e:
        return f"Failed to add contact: {str(e)}"


def list_contacts() -> str:
    """List all contacts in the phone book.
    Use this when the user wants to see all their saved contacts.
    """
    try:
        client = get_client()
        if not client:
            return "Error: Supabase client not initialized."

        response = client.table("contacts").select("name, mobile_no").order("name").execute()
        results = response.data

        if not results:
            return "No contacts saved yet."

        contacts_list = [f"{i+1}. {r['name']} — {r['mobile_no']}" for i, r in enumerate(results)]
        return "Your contacts:\n" + "\n".join(contacts_list)
    except Exception as e:
        return f"Error listing contacts: {str(e)}"
