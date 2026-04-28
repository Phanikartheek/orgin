/**
 * UI Manager
 * Handles all DOM manipulations, animations, and visual states.
 */

class UIManager {
    constructor() {
        this.orbSection = document.getElementById('orbSection');
        this.aiOrb = document.getElementById('aiOrb');
        this.orbLabel = document.getElementById('orbLabel');
        this.chatContainer = document.getElementById('chatContainer');
        this.chatMessages = document.getElementById('chatMessages');
        this.statusText = document.getElementById('statusText');
        this.chatInput = document.getElementById('chatInput');
        this.micBtn = document.getElementById('micBtn');
        this.sendBtn = document.getElementById('sendBtn');
        this.toast = document.getElementById('toast');
        this.toastMessage = document.getElementById('toastMessage');

        this.hasMessages = false;
    }

    // --- Orb State Management ---

    setOrbState(state) {
        // Remove all states
        this.aiOrb.classList.remove('listening', 'thinking', 'speaking');

        switch (state) {
            case 'listening':
                this.aiOrb.classList.add('listening');
                this.orbLabel.textContent = 'Listening...';
                this.micBtn.classList.add('recording');
                break;
            case 'thinking':
                this.aiOrb.classList.add('thinking');
                this.orbLabel.textContent = 'Processing...';
                this.micBtn.classList.remove('recording');
                break;
            case 'speaking':
                this.aiOrb.classList.add('speaking');
                this.orbLabel.textContent = 'Speaking...';
                this.micBtn.classList.remove('recording');
                break;
            default: // idle
                this.orbLabel.textContent = 'Listening for your command...';
                this.micBtn.classList.remove('recording');
                break;
        }
    }

    // --- Status Bar ---

    setStatus(text) {
        this.statusText.textContent = text;
    }

    // --- Chat Messages ---

    addUserMessage(text) {
        this._ensureChatVisible();
        const msgEl = this._createMessage('user', text);
        this.chatMessages.appendChild(msgEl);
        this._scrollToBottom();
    }

    addAssistantMessage(text) {
        this._ensureChatVisible();
        const msgEl = this._createMessage('assistant', text);
        this.chatMessages.appendChild(msgEl);
        this._scrollToBottom();
    }

    clearChat() {
        this.chatMessages.innerHTML = '';
        this.hasMessages = false;
        this.orbSection.classList.remove('minimized');
    }

    _createMessage(role, text) {
        const msg = document.createElement('div');
        msg.className = `message ${role}`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = role === 'user' ? 'U' : 'J';

        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        bubble.textContent = text;

        msg.appendChild(avatar);
        msg.appendChild(bubble);
        return msg;
    }

    _ensureChatVisible() {
        if (!this.hasMessages) {
            this.hasMessages = true;
            this.orbSection.classList.add('minimized');
        }
    }

    _scrollToBottom() {
        requestAnimationFrame(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        });
    }

    // --- Input Controls ---

    showSendButton() {
        this.micBtn.classList.add('hidden');
        this.sendBtn.classList.remove('hidden');
    }

    showMicButton() {
        this.sendBtn.classList.add('hidden');
        this.micBtn.classList.remove('hidden');
    }

    clearInput() {
        this.chatInput.value = '';
        this.showMicButton();
    }

    // --- Toast Notifications ---

    showToast(message, duration = 3000) {
        this.toastMessage.textContent = message;
        this.toast.classList.remove('hidden');
        this.toast.classList.add('show');

        setTimeout(() => {
            this.toast.classList.remove('show');
            setTimeout(() => this.toast.classList.add('hidden'), 300);
        }, duration);
    }
}

// Global instance
const ui = new UIManager();
