"""
Communication Tools — WhatsApp, Phone Calls, SMS
Gemini calls these for messaging and calling.
"""

import os
import time
import subprocess
import sqlite3
from urllib.parse import quote
try:
    import pyautogui
    HAS_GUI = True
except ImportError:
    HAS_GUI = False

from app.config import DB_PATH, IS_CLOUD


def _find_contact_number(name: str) -> str | None:
    """Internal helper to look up a contact's phone number."""
    try:
        con = sqlite3.connect(DB_PATH)
        cursor = con.cursor()
        cursor.execute(
            "SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?",
            (f"%{name.lower()}%", f"{name.lower()}%"),
        )
        results = cursor.fetchall()
        con.close()

        if results:
            mobile = str(results[0][0])
            if not mobile.startswith("+91"):
                mobile = "+91" + mobile
            return mobile
    except Exception:
        pass
    return None


def send_whatsapp_message(contact_name: str, message: str) -> str:
    """Send a WhatsApp message to a contact.
    Use this when the user wants to send a message via WhatsApp.

    Args:
        contact_name: The name of the contact to message
        message: The message text to send
    """
    mobile_no = _find_contact_number(contact_name)
    if not mobile_no:
        return f"Contact '{contact_name}' not found in your contacts."

    if IS_CLOUD or not HAS_GUI:
        return f"[Cloud Demo Mode] I would have sent a WhatsApp message to {contact_name} with: '{message}'"

    try:
        encoded_message = quote(message)
        whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
        full_command = f'start "" "{whatsapp_url}"'

        subprocess.run(full_command, shell=True)
        time.sleep(5)
        subprocess.run(full_command, shell=True)

        # Navigate to send button
        pyautogui.hotkey("ctrl", "f")
        time.sleep(0.5)
        for _ in range(11):
            pyautogui.hotkey("tab")
            time.sleep(0.1)
        pyautogui.hotkey("enter")

        return f"Message sent to {contact_name} on WhatsApp."
    except Exception as e:
        return f"Failed to send WhatsApp message: {str(e)}"


def make_whatsapp_call(contact_name: str) -> str:
    """Make a WhatsApp voice call to a contact.
    Use this when the user wants to make a voice/audio call via WhatsApp.

    Args:
        contact_name: The name of the contact to call
    """
    mobile_no = _find_contact_number(contact_name)
    if not mobile_no:
        return f"Contact '{contact_name}' not found in your contacts."

    if IS_CLOUD or not HAS_GUI:
        return f"[Cloud Demo Mode] I would have started a WhatsApp voice call with {contact_name}."

    try:
        whatsapp_url = f"whatsapp://send?phone={mobile_no}"
        full_command = f'start "" "{whatsapp_url}"'

        subprocess.run(full_command, shell=True)
        time.sleep(5)
        subprocess.run(full_command, shell=True)

        # Navigate to call button
        pyautogui.hotkey("ctrl", "f")
        time.sleep(0.5)
        for _ in range(6):
            pyautogui.hotkey("tab")
            time.sleep(0.1)
        pyautogui.hotkey("enter")

        return f"Calling {contact_name} on WhatsApp."
    except Exception as e:
        return f"Failed to make WhatsApp call: {str(e)}"


def make_whatsapp_video_call(contact_name: str) -> str:
    """Make a WhatsApp video call to a contact.
    Use this when the user wants to make a video call via WhatsApp.

    Args:
        contact_name: The name of the contact to video call
    """
    mobile_no = _find_contact_number(contact_name)
    if not mobile_no:
        return f"Contact '{contact_name}' not found in your contacts."

    if IS_CLOUD or not HAS_GUI:
        return f"[Cloud Demo Mode] I would have started a WhatsApp video call with {contact_name}."

    try:
        whatsapp_url = f"whatsapp://send?phone={mobile_no}"
        full_command = f'start "" "{whatsapp_url}"'

        subprocess.run(full_command, shell=True)
        time.sleep(5)
        subprocess.run(full_command, shell=True)

        # Navigate to video call button
        pyautogui.hotkey("ctrl", "f")
        time.sleep(0.5)
        for _ in range(5):
            pyautogui.hotkey("tab")
            time.sleep(0.1)
        pyautogui.hotkey("enter")

        return f"Starting video call with {contact_name} on WhatsApp."
    except Exception as e:
        return f"Failed to start video call: {str(e)}"


def make_phone_call(contact_name: str) -> str:
    """Make a phone call to a contact via connected Android device (ADB).
    Use this when the user wants to make a regular phone call (not WhatsApp).

    Args:
        contact_name: The name of the contact to call
    """
    mobile_no = _find_contact_number(contact_name)
    if not mobile_no:
        return f"Contact '{contact_name}' not found in your contacts."

    if IS_CLOUD:
        return f"[Cloud Demo Mode] I would have made a phone call to {contact_name} via ADB."

    try:
        clean_number = mobile_no.replace(" ", "")
        command = f"adb shell am start -a android.intent.action.CALL -d tel:{clean_number}"
        os.system(command)
        return f"Calling {contact_name} via phone."
    except Exception as e:
        return f"Failed to make phone call: {str(e)}"


def send_sms(contact_name: str, message: str) -> str:
    """Send an SMS text message to a contact via connected Android device (ADB).
    Use this when the user wants to send a regular SMS (not WhatsApp).

    Args:
        contact_name: The name of the contact to message
        message: The SMS text to send
    """
    mobile_no = _find_contact_number(contact_name)
    if not mobile_no:
        return f"Contact '{contact_name}' not found in your contacts."

    if IS_CLOUD:
        return f"[Cloud Demo Mode] I would have sent an SMS to {contact_name} with: '{message}'"

    try:
        from app.agent.tools._adb_helpers import goback, keyEvent, tapEvents, adbInput

        formatted_msg = message.replace(" ", "%s")
        formatted_no = mobile_no.replace(" ", "%s")

        goback(4)
        time.sleep(1)
        keyEvent(3)
        tapEvents(136, 2220)
        tapEvents(819, 2192)
        adbInput(formatted_no)
        tapEvents(601, 574)
        tapEvents(390, 2270)
        adbInput(formatted_msg)
        tapEvents(957, 1397)

        return f"SMS sent to {contact_name}."
    except Exception as e:
        return f"Failed to send SMS: {str(e)}"
