"""
ADB Helper Functions
Utilities for Android device automation via ADB.
"""

import os
import time


def keyEvent(key_code: int):
    """Send a key event to the connected Android device."""
    os.system(f"adb shell input keyevent {key_code}")
    time.sleep(1)


def tapEvents(x: int, y: int):
    """Tap at specific coordinates on the Android device screen."""
    os.system(f"adb shell input tap {x} {y}")
    time.sleep(1)


def adbInput(message: str):
    """Type text on the connected Android device."""
    os.system(f'adb shell input text "{message}"')
    time.sleep(1)


def goback(key_code: int):
    """Press the back button multiple times."""
    for _ in range(6):
        keyEvent(key_code)
