/**
 * Jarvis AI Assistant — Main Application
 * Wires together WebSocket, Voice, UI, and Settings.
 */

(function () {
    'use strict';

    // --- Initialize 3D Background (Vanta.js) ---
    let vantaEffect = null;
    try {
        vantaEffect = VANTA.NET({
            el: "#vanta-bg",
            mouseControls: true,
            touchControls: true,
            gyroControls: false,
            minHeight: 200.00,
            minWidth: 200.00,
            scale: 1.00,
            scaleMobile: 1.00,
            color: 0x00d2ff,
            backgroundColor: 0x000000,
            points: 12.00,
            maxDistance: 22.00,
            spacing: 16.00
        });
    } catch (e) {
        console.warn('Vanta initialization failed:', e);
    }

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
                    // Hide demo banner on disconnect
                    document.getElementById('demoModeBanner').classList.add('hidden');
                }
                break;

            case 'connection_info':
                if (data.is_cloud) {
                    ui.setStatus('AI Assistant — Web Demo');
                    document.getElementById('demoModeBanner').classList.remove('hidden');
                } else {
                    ui.setStatus('AI Assistant — Connected');
                    document.getElementById('demoModeBanner').classList.add('hidden');
                }
                if (data.message) {
                    ui.showToast(data.message);
                }
                break;

            case 'status':
                ui.setOrbState(data.status);
                
                // Update 3D effect based on state
                if (vantaEffect) {
                    if (data.status === 'thinking' || data.status === 'speaking') {
                        vantaEffect.setOptions({
                            color: 0x97e9ff,
                            points: 18.00,
                            spacing: 14.00
                        });
                    } else {
                        vantaEffect.setOptions({
                            color: 0x00d2ff,
                            points: 12.00,
                            spacing: 16.00
                        });
                    }
                }

                if (data.message) {
                    ui.setStatus(`AI Assistant — ${data.message}`);
                }
                if (data.status === 'idle') {
                    ui.setStatus('AI Assistant — Ready');
                }
                break;

            case 'user_message':
                if (data.text === "voice_input_disabled") {
                    ui.showToast('Voice input is disabled in Web Demo. Please type your message.', 5000);
                    ui.setOrbState('idle');
                    ui.setStatus('AI Assistant — Web Demo');
                } else {
                    ui.addUserMessage(data.text);
                }
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
