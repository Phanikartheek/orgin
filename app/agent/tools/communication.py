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
    
    try:
        # Clean number - remove spaces, dashes
        clean_number = number.replace(" ", "").replace("-", "")
        if not clean_number.startswith("+"):
            clean_number = "+91" + clean_number  # Default to India
        
        # Try opening WhatsApp desktop app for call
        # First open the chat, then user can click call
        whatsapp_url = f"https://wa.me/{clean_number.replace('+', '')}"
        webbrowser.open(whatsapp_url)
        
        # Also try the WhatsApp desktop protocol
        try:
            os.startfile(f"whatsapp://send?phone={clean_number.replace('+', '')}")
        except Exception:
            pass
        
        return f"Opening WhatsApp for {to}. Please click the call button to start the voice call."
    except Exception as e:
        return f"Failed to open WhatsApp call: {str(e)}"


def make_whatsapp_video_call(to: str) -> str:
    """Start a WhatsApp video call."""
    number = _get_number(to)
    if IS_CLOUD:
        return f"[Cloud Demo Mode] I would have started a WhatsApp video call to {to}."
    
    try:
        clean_number = number.replace(" ", "").replace("-", "")
        if not clean_number.startswith("+"):
            clean_number = "+91" + clean_number
        
        whatsapp_url = f"https://wa.me/{clean_number.replace('+', '')}"
        webbrowser.open(whatsapp_url)
        
        try:
            os.startfile(f"whatsapp://send?phone={clean_number.replace('+', '')}")
        except Exception:
            pass
        
        return f"Opening WhatsApp for {to}. Please click the video call button to start."
    except Exception as e:
        return f"Failed to open WhatsApp video call: {str(e)}"


def make_phone_call(to: str) -> str:
    """Make a regular phone call using the default phone app."""
    number = _get_number(to)
    if IS_CLOUD:
        return f"[Cloud Demo Mode] I would have made a phone call to {to}."
    
    try:
        clean_number = number.replace(" ", "").replace("-", "")
        if not clean_number.startswith("+"):
            clean_number = "+91" + clean_number
        webbrowser.open(f"tel:{clean_number}")
        return f"Initiating phone call to {to}."
    except Exception as e:
        return f"Failed to make phone call: {str(e)}"


def send_sms(to: str, message: str) -> str:
    """Send a regular SMS/Text message."""
    number = _get_number(to)
    if IS_CLOUD:
        return f"[Cloud Demo Mode] I would have sent an SMS to {to}: '{message}'"
    
    try:
        clean_number = number.replace(" ", "").replace("-", "")
        if not clean_number.startswith("+"):
            clean_number = "+91" + clean_number
        webbrowser.open(f"sms:{clean_number}?body={message}")
        return f"Opening SMS for {to}."
    except Exception as e:
        return f"Failed to send SMS: {str(e)}"

