"""
YouTube Tools
Gemini calls these to play videos and music on YouTube.
"""

import os
import pywhatkit


def play_youtube(search_query: str) -> str:
    """Play a video or music on YouTube by searching for it.
    Use this when the user wants to watch a video, listen to music,
    or play any content on YouTube.

    Args:
        search_query: What to search for on YouTube (e.g., 'lofi hip hop music', 'Python tutorial')
    """
    try:
        # Use pywhatkit to find and play the first video matching the query directly
        pywhatkit.playonyt(search_query)

        return f"Playing '{search_query}' on YouTube."
    except Exception as e:
        return f"Failed to open YouTube: {str(e)}"
