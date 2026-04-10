"""
Conversation Memory Manager
Stores conversation history so Jarvis can maintain context across turns.
"""

from app.config import MAX_MEMORY_TURNS


class ConversationMemory:
    """Manages conversation history for multi-turn context."""

    def __init__(self):
        self.messages: list[dict] = []

    def add_message(self, role: str, content: str):
        """Add a message to the conversation history."""
        self.messages.append({"role": role, "content": content})

        # Trim to max turns (keep recent context)
        if len(self.messages) > MAX_MEMORY_TURNS * 2:
            self.messages = self.messages[-(MAX_MEMORY_TURNS * 2):]

    def get_gemini_contents(self) -> list:
        """Convert memory to Gemini API format."""
        contents = []
        for msg in self.messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}],
            })
        return contents

    def clear(self):
        """Clear all conversation history."""
        self.messages = []

    def get_last_exchange(self) -> tuple[str, str]:
        """Get the last user message and assistant response."""
        user_msg = ""
        assistant_msg = ""
        for msg in reversed(self.messages):
            if msg["role"] == "assistant" and not assistant_msg:
                assistant_msg = msg["content"]
            elif msg["role"] == "user" and not user_msg:
                user_msg = msg["content"]
            if user_msg and assistant_msg:
                break
        return user_msg, assistant_msg
