"""
Speech-to-Text Module
Uses Google Speech Recognition for converting speech to text.
"""

import speech_recognition as sr
from app.config import STT_LANGUAGE


class SpeechToText:
    """Handles microphone input and speech recognition."""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 1
        self.recognizer.energy_threshold = 300

    def listen(self, timeout: int = 10, phrase_limit: int = 8) -> str:
        """
        Listen to microphone and return transcribed text.

        Args:
            timeout: Max seconds to wait for speech to start
            phrase_limit: Max seconds of speech to capture

        Returns:
            Transcribed text or empty string if failed
        """
        try:
            with sr.Microphone() as source:
                print("[STT] Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("[STT] Listening...")

                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_limit,
                )

            print("[STT] Recognizing...")
            text = self.recognizer.recognize_google(audio, language=STT_LANGUAGE)
            print(f"[STT] Heard: {text}")
            return text.lower()

        except sr.WaitTimeoutError:
            print("[STT] Timeout — no speech detected")
            return ""
        except sr.UnknownValueError:
            print("[STT] Could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"[STT] API error: {e}")
            return ""
        except Exception as e:
            print(f"[STT] Error: {e}")
            return ""
