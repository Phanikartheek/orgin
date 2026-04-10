"""
System Control Tools
Gemini calls these for system-level operations.
"""

import os
import datetime


def get_current_time() -> str:
    """Get the current time.
    Use this when the user asks what time it is.
    """
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%I:%M %p')}."


def get_current_date() -> str:
    """Get today's date.
    Use this when the user asks what the date is or what day it is.
    """
    now = datetime.datetime.now()
    return f"Today is {now.strftime('%A, %B %d, %Y')}."


def set_system_volume(level: int) -> str:
    """Set the system volume to a specific level (0-100).
    Use this when the user wants to change the system volume.

    Args:
        level: Volume level from 0 (mute) to 100 (maximum)
    """
    try:
        # Clamp to valid range
        level = max(0, min(100, level))
        # Convert 0-100 to 0-65535 range for Windows
        volume_value = int(level * 655.35)

        # Use nircmd for volume control (common on Windows)
        os.system(f"nircmd.exe setsysvolume {volume_value}")
        return f"System volume set to {level}%."
    except Exception as e:
        return f"Failed to set volume: {str(e)}"


def take_screenshot() -> str:
    """Take a screenshot of the current screen.
    Use this when the user wants to capture their screen.
    """
    try:
        import pyautogui
        from app.config import DATA_DIR

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(DATA_DIR, f"screenshot_{timestamp}.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        return f"Screenshot saved to {filepath}."
    except Exception as e:
        return f"Failed to take screenshot: {str(e)}"
