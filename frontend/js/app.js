/**
 * Jarvis AI Assistant — Main Application
 * Wires together WebSocket, Voice, UI, and Settings.
 */

(function () {
    'use strict';

    // --- Initialize WebSocket ---
    jarvisWS.connect();

    // --- Handle incoming WebSocket messages ---
    jarvisWS.onMessage((data) => {
        switch (data.type) {
            case 'connection':
                if (data.status === 'connected') {
                    ui.setStatus('AI Assistant — Connected');
                    ui.showToast('Connected to Jarvis');
                } else {
                    ui.setStatus('AI Assistant — Disconnected');
                }
                break;

            case 'status':
                ui.setOrbState(data.status);
                if (data.message) {
                    ui.setStatus(`AI Assistant — ${data.message}`);
                }
                if (data.status === 'idle') {
                    ui.setStatus('AI Assistant — Ready');
                }
                break;

            case 'user_message':
                ui.addUserMessage(data.text);
                break;

            case 'assistant_message':
                ui.addAssistantMessage(data.text);
                break;

            case 'play_audio':
                voiceManager.playAudio(data.audio_url);
                break;

            case 'error':
                ui.showToast(data.message, 5000);
                ui.setOrbState('idle');
                break;
        }
    });

    // --- Voice playback end handler ---
    voiceManager.onPlaybackEnd = () => {
        ui.setOrbState('idle');
    };

    // --- Mic Button ---
    document.getElementById('micBtn').addEventListener('click', () => {
        if (!jarvisWS.isConnected) {
            ui.showToast('Not connected to server');
            return;
        }
        jarvisWS.sendVoiceRequest();
    });

    // --- Send Button ---
    document.getElementById('sendBtn').addEventListener('click', () => {
        sendTextMessage();
    });

    // --- Chat Input ---
    const chatInput = document.getElementById('chatInput');

    chatInput.addEventListener('input', () => {
        if (chatInput.value.trim().length > 0) {
            ui.showSendButton();
        } else {
            ui.showMicButton();
        }
    });

    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendTextMessage();
        }
    });

    // --- Send Text Message ---
    function sendTextMessage() {
        const text = chatInput.value.trim();
        if (!text) return;
        if (!jarvisWS.isConnected) {
            ui.showToast('Not connected to server');
            return;
        }

        ui.addUserMessage(text);
        jarvisWS.sendText(text);
        ui.clearInput();
    }

    // --- Clear Chat ---
    document.getElementById('clearChatBtn').addEventListener('click', () => {
        ui.clearChat();
        jarvisWS.sendResetMemory();
        ui.showToast('Chat cleared');
    });

    // --- Keyboard Shortcut: Win+J to activate mic ---
    document.addEventListener('keyup', (e) => {
        if (e.key === 'j' && e.metaKey) {
            if (jarvisWS.isConnected) {
                jarvisWS.sendVoiceRequest();
            }
        }
    });

    console.log('🤖 Jarvis AI Assistant initialized');
})();
