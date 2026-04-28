/**
 * Jarvis AI Assistant — Main Application
 * Voice-first: auto-greet, auto-listen, voice-to-voice loop.
 */

(function () {
    'use strict';

    // --- Initialize 3D Background (Vanta.js) ---
    let vantaEffect = null;
    let isCloudMode = false;
    let autoListenEnabled = true; // Voice-to-voice mode ON by default
    let isProcessing = false;

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
                    document.getElementById('demoModeBanner').classList.add('hidden');
                }
                break;

            case 'connection_info':
                isCloudMode = !!data.is_cloud;
                if (isCloudMode) {
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
                    isProcessing = false;
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

            case 'auto_listen':
                // After Jarvis finishes speaking, auto-listen for next command
                // Wait for audio to finish first
                if (autoListenEnabled) {
                    waitForAudioThenListen();
                }
                break;

            case 'error':
                ui.showToast(data.message, 5000);
                ui.setOrbState('idle');
                isProcessing = false;
                break;
        }
    });

    // --- Wait for TTS audio to finish, then start listening ---
    function waitForAudioThenListen() {
        // Check if audio is currently playing
        const checkInterval = setInterval(() => {
            if (!voiceManager.isPlaying) {
                clearInterval(checkInterval);
                // Small delay after audio ends before listening
                setTimeout(() => {
                    if (autoListenEnabled && !isProcessing) {
                        startListening();
                    }
                }, 500);
            }
        }, 200);

        // Safety timeout - don't wait forever
        setTimeout(() => clearInterval(checkInterval), 30000);
    }

    // --- Start Listening (Browser Speech Recognition) ---
    function startListening() {
        if (!jarvisWS.isConnected) return;
        if (isProcessing) return;

        // Always use browser speech recognition for speed
        speechRecognizer.start();
    }

    // --- Voice Recognition Setup ---
    voiceManager.onPlaybackEnd = () => {
        ui.setOrbState('idle');
    };

    speechRecognizer.onStart = () => {
        ui.setOrbState('listening');
        ui.setStatus('AI Assistant — Listening...');
    };

    speechRecognizer.onEnd = () => {
        if (!isProcessing) {
            ui.setOrbState('idle');
            ui.setStatus('AI Assistant — Ready');
        }
    };

    speechRecognizer.onResult = (text) => {
        if (text && text.trim()) {
            isProcessing = true;
            ui.addUserMessage(text);
            // Send as browser_voice_input for voice-to-voice flow
            jarvisWS.send({ type: 'browser_voice_input', text: text });
        }
    };

    // --- Mic Button (manual trigger) ---
    document.getElementById('micBtn').addEventListener('click', () => {
        if (!jarvisWS.isConnected) {
            ui.showToast('Not connected to server');
            return;
        }
        startListening();
    });

    // --- Send Button (text fallback) ---
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

        isProcessing = true;
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
                startListening();
            }
        }
    });

    console.log('Jarvis AI Assistant initialized — Voice Mode Active');
})();
