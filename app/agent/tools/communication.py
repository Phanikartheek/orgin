"""
Communication Tools
Gemini calls these to send messages and make calls.
Now using Supabase for contact lookup if only name is provided.
"""

import os
import webbrowser
from app.config import IS_CLOUD
from app.database.db import get_client


def _get_number(name_or_number: str) -> str:
    """Helper to lookup a number in Supabase if a name is provided."""
    # If it looks like a number already, just return it
    if name_or_number.startswith('+') or (name_or_number.isdigit() and len(name_or_number) >= 10):
        return name_or_number
    
    # Otherwise, search in Supabase contacts
    try:
        client = get_client()
        if client:
            response = client.table("contacts").select("mobile_no").ilike("name", f"%{name_or_number}%").execute()
            if response.data:
                return response.data[0]["mobile_no"]
    except Exception:
        pass
        
    return name_or_number


def send_whatsapp_message(to: str, message: str) -> str:
    """Send a WhatsApp message.
    
    Args:
        to: The name or phone number of the recipient
        message: The message content
    """
    number = _get_number(to)
    
    if IS_CLOUD:
        return f"[Cloud Demo Mode] I would have sent a WhatsApp to {to} ({number}): '{message}'"

    try:
        import pywhatkit
        # Using pywhatkit (instantly opens web.whatsapp.com)
        pywhatkit.sendwhatmsg_instantly(number, message, wait_time=10, tab_close=True)
        return f"Sending WhatsApp message to {to} now."
    except Exception as e:
        return f"Failed to send WhatsApp: {str(e)}"


def make_whatsapp_call(to: str) -> str:
    """Start a WhatsApp audio call."""
    number = _get_number(to)
    if IS_CLOUD:
        return f"[Cloud Demo Mode] I would have started a WhatsApp audio call to {to}."
    
    # Simplified logic for demo
    return f"Attempting to call {to} on WhatsApp..."


def make_whatsapp_video_call(to: str) -> str:
    """Start a WhatsApp video call."""
    number = _get_number(to)
    if IS_CLOUD:
        return f"[Cloud Demo Mode] I would have started a WhatsApp video call to {to}."
    
    return f"Attempting video call to {to} on WhatsApp..."


def make_phone_call(to: str) -> str:
    """Make a regular phone call."""
    number = _get_number(to)
    if IS_CLOUD:
        return f"[Cloud Demo Mode] I would have made a phone call to {to}."
    
    return f"Calling {to}..."


def send_sms(to: str, message: str) -> str:
    """Send a regular SMS/Text message."""
    number = _get_number(to)
    if IS_CLOUD:
        return f"[Cloud Demo Mode] I would have sent an SMS to {to}: '{message}'"
    
    return f"Sending SMS to {to}: {message[:20]}..."
