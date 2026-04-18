/**
 * Voice Module
 * Handles TTS audio playback.
 * Mic input is handled server-side via WebSocket.
 */

class VoiceManager {
    constructor() {
        this.audioElement = document.getElementById('ttsAudio');
        this.isPlaying = false;

        if (this.audioElement) {
            this.audioElement.addEventListener('ended', () => {
                this.isPlaying = false;
                this.onPlaybackEnd();
            });

            this.audioElement.addEventListener('error', () => {
                this.isPlaying = false;
                this.onPlaybackEnd();
            });
        }

        // --- Mic Button ---
        const micBtn = document.getElementById('micBtn');
        let isCloudMode = false;

        // Handle incoming WebSocket messages
        jarvisWS.onMessage((data) => {
            if (data.type === 'connection_info') {
                isCloudMode = data.is_cloud;
            }
            // ... rest of the handler logic will be merged by the tool ...
        });

        this.onPlaybackEnd = () => {}; // Override in app.js
    }

    playAudio(audioUrl) {
        if (!this.audioElement) return;

        // Add cache-buster to avoid stale audio
        const url = audioUrl + '?t=' + Date.now();
        this.audioElement.src = url;
        this.isPlaying = true;

        this.audioElement.play().catch(err => {
            console.error('[Voice] Playback error:', err);
            this.isPlaying = false;
        });
    }

    stopAudio() {
        if (this.audioElement) {
            this.audioElement.pause();
            this.audioElement.currentTime = 0;
            this.isPlaying = false;
        }
    }
}

/**
 * Browser Speech Recognition Module
 * Uses Web Speech API for Cloud Demo mode.
 */
class BrowserSpeechRecognizer {
    constructor() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';

            this.onResult = (text) => {};
            this.onStart = () => {};
            this.onEnd = () => {};

            this.recognition.onstart = () => this.onStart();
            this.recognition.onend = () => this.onEnd();
            this.recognition.onerror = (e) => {
                console.error('[Speech] Error:', e);
                this.onEnd();
            };
            this.recognition.onresult = (event) => {
                const text = event.results[0][0].transcript;
                this.onResult(text);
            };
        } else {
            this.recognition = null;
        }
    }

    start() {
        if (this.recognition) {
            try {
                this.recognition.start();
            } catch (e) {
                console.warn('[Speech] Already started');
            }
        } else {
            ui.showToast('Speech recognition not supported in this browser.', 5000);
        }
    }

    stop() {
        if (this.recognition) this.recognition.stop();
    }
}

// Global instances
const voiceManager = new VoiceManager();
const speechRecognizer = new BrowserSpeechRecognizer();
