"""
Text-to-Speech Module
Uses edge-tts (Microsoft Neural TTS) for natural-sounding voice output.
Free, fast, and supports 300+ voices.
"""

import asyncio
import os
import uuid
import edge_tts
from app.config import TTS_VOICE, TTS_RATE, AUDIO_OUTPUT_DIR


class TextToSpeech:
    """Generates speech audio from text using Microsoft Edge TTS."""

    def __init__(self):
        self.voice = TTS_VOICE
        self.rate = TTS_RATE
        # Ensure output directory exists
        os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)

    async def synthesize(self, text: str) -> str:
        """
        Convert text to speech and save as audio file.

        Args:
            text: The text to convert to speech

        Returns:
            Relative path to the generated audio file (for frontend playback)
        """
        try:
            # Generate unique filename
            filename = f"tts_{uuid.uuid4().hex[:8]}.mp3"
            filepath = os.path.join(AUDIO_OUTPUT_DIR, filename)

            # Generate speech using edge-tts
            communicate = edge_tts.Communicate(
                text=text,
                voice=self.voice,
                rate=self.rate,
            )
            await communicate.save(filepath)

            # Return the relative path for the frontend
            return f"/assets/audio/{filename}"

        except Exception as e:
            print(f"[TTS] Error: {e}")
            return ""

    def cleanup_old_files(self, keep_latest: int = 10):
        """Remove old TTS audio files to save disk space."""
        try:
            files = []
            for f in os.listdir(AUDIO_OUTPUT_DIR):
                if f.startswith("tts_") and f.endswith(".mp3"):
                    filepath = os.path.join(AUDIO_OUTPUT_DIR, f)
                    files.append((filepath, os.path.getmtime(filepath)))

            # Sort by modification time (newest first)
            files.sort(key=lambda x: x[1], reverse=True)

            # Remove files beyond the keep limit
            for filepath, _ in files[keep_latest:]:
                os.remove(filepath)
        except Exception:
            pass
