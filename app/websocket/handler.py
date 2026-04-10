"""
WebSocket Handler
Manages real-time communication between frontend and backend.
Handles voice input, text input, and audio playback coordination.
"""

import json
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from app.agent.brain import JarvisBrain
from app.voice.stt import SpeechToText
from app.voice.tts import TextToSpeech


from app.config import IS_CLOUD


class ConnectionManager:
    """Manages active WebSocket connections."""

    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.brain = JarvisBrain()
        self.stt = SpeechToText()
        self.tts = TextToSpeech()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print("[WS] Client connected")

        # Send server capabilities/info
        await self.send_json(websocket, {
            "type": "connection_info",
            "is_cloud": IS_CLOUD,
            "message": "Welcome to Jarvis Web Demo" if IS_CLOUD else "Jarvis is ready, Sir."
        })

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print("[WS] Client disconnected")

    async def send_json(self, websocket: WebSocket, data: dict):
        await websocket.send_json(data)

    async def handle_message(self, websocket: WebSocket, data: dict):
        """Process incoming WebSocket messages."""
        msg_type = data.get("type", "")

        if msg_type == "text_input":
            # User sent text via chat box — NO TTS (instant response)
            user_text = data.get("text", "").strip()
            if user_text:
                await self._process_query(websocket, user_text, speak=False)

        elif msg_type == "voice_input":
            # User pressed mic button — start listening, SPEAK response
            await self.send_json(websocket, {
                "type": "status",
                "status": "listening",
                "message": "Listening..."
            })

            # Run STT in a thread (it's blocking)
            loop = asyncio.get_event_loop()
            user_text = await loop.run_in_executor(None, self.stt.listen)

            if user_text:
                # Send the transcribed text to frontend
                await self.send_json(websocket, {
                    "type": "user_message",
                    "text": user_text
                })
                await self._process_query(websocket, user_text, speak=True)
            else:
                await self.send_json(websocket, {
                    "type": "status",
                    "status": "idle",
                    "message": "Didn't catch that. Try again."
                })

        elif msg_type == "reset_memory":
            self.brain.reset_memory()
            await self.send_json(websocket, {
                "type": "status",
                "status": "idle",
                "message": "Conversation memory cleared."
            })

    async def _process_query(self, websocket: WebSocket, query: str, speak: bool = False):
        """Process a user query through the AI brain and generate response."""
        try:
            # Show thinking state
            await self.send_json(websocket, {
                "type": "status",
                "status": "thinking",
                "message": "Processing..."
            })

            # Get AI response (runs Gemini with function calling)
            response_text = await self.brain.think(query)

            # Send the text response to frontend
            await self.send_json(websocket, {
                "type": "assistant_message",
                "text": response_text
            })

            # Only generate TTS audio if voice input was used
            if speak:
                await self.send_json(websocket, {
                    "type": "status",
                    "status": "speaking",
                    "message": "Speaking..."
                })

                audio_path = await self.tts.synthesize(response_text)

                if audio_path:
                    await self.send_json(websocket, {
                        "type": "play_audio",
                        "audio_url": audio_path
                    })

                self.tts.cleanup_old_files()

            # Return to idle
            await self.send_json(websocket, {
                "type": "status",
                "status": "idle",
                "message": ""
            })

        except Exception as e:
            print(f"[WS] Error processing query: {e}")
            await self.send_json(websocket, {
                "type": "error",
                "message": f"Error: {str(e)}"
            })
            await self.send_json(websocket, {
                "type": "status",
                "status": "idle",
                "message": ""
            })


# Global connection manager instance
manager = ConnectionManager()
