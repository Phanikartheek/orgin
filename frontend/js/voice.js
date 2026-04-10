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

// Global instance
const voiceManager = new VoiceManager();
