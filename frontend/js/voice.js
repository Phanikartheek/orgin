/**
 * Voice Module
 * Handles TTS audio playback and Browser Speech Recognition.
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
            this.onPlaybackEnd();
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
 * Uses Web Speech API for voice input.
 */
class BrowserSpeechRecognizer {
    constructor() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-IN'; // English India for better recognition

            this.onResult = (text) => {};
            this.onStart = () => {};
            this.onEnd = () => {};

            this.recognition.onstart = () => {
                console.log('[Speech] Recognition started');
                this.onStart();
            };
            this.recognition.onend = () => {
                console.log('[Speech] Recognition ended');
                this.onEnd();
            };
            this.recognition.onerror = (e) => {
                console.error('[Speech] Error:', e.error);
                // Don't trigger onEnd for 'no-speech' - just retry
                if (e.error === 'no-speech') {
                    console.log('[Speech] No speech detected, ready for retry');
                }
                this.onEnd();
            };
            this.recognition.onresult = (event) => {
                const text = event.results[0][0].transcript;
                console.log('[Speech] Heard:', text);
                this.onResult(text);
            };
        } else {
            this.recognition = null;
            console.warn('[Speech] Web Speech API not supported in this browser');
        }
    }

    start() {
        if (this.recognition) {
            try {
                this.recognition.start();
                console.log('[Speech] Attempting to start...');
            } catch (e) {
                console.warn('[Speech] Already started or error:', e);
            }
        } else {
            console.error('[Speech] Speech recognition not available');
            if (typeof ui !== 'undefined') {
                ui.showToast('Speech recognition not supported. Use Chrome browser.', 5000);
            }
        }
    }

    stop() {
        if (this.recognition) this.recognition.stop();
    }
}

// Global instances
const voiceManager = new VoiceManager();
const speechRecognizer = new BrowserSpeechRecognizer();
