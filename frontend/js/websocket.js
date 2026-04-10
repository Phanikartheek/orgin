/**
 * WebSocket Client
 * Manages real-time connection to the Jarvis backend.
 */

class JarvisWebSocket {
    constructor() {
        this.ws = null;
        this.isConnected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 10;
        this.reconnectDelay = 2000;
        this.messageHandlers = [];
    }

    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;

        this.ws = new WebSocket(wsUrl);

        this.ws.onopen = () => {
            console.log('[WS] Connected to Jarvis');
            this.isConnected = true;
            this.reconnectAttempts = 0;
            this._emit({ type: 'connection', status: 'connected' });
        };

        this.ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                this._emit(data);
            } catch (e) {
                console.error('[WS] Failed to parse message:', e);
            }
        };

        this.ws.onclose = () => {
            console.log('[WS] Disconnected');
            this.isConnected = false;
            this._emit({ type: 'connection', status: 'disconnected' });
            this._tryReconnect();
        };

        this.ws.onerror = (error) => {
            console.error('[WS] Error:', error);
        };
    }

    send(data) {
        if (this.ws && this.isConnected) {
            this.ws.send(JSON.stringify(data));
        } else {
            console.warn('[WS] Not connected. Message not sent.');
        }
    }

    sendText(text) {
        this.send({ type: 'text_input', text });
    }

    sendVoiceRequest() {
        this.send({ type: 'voice_input' });
    }

    sendResetMemory() {
        this.send({ type: 'reset_memory' });
    }

    onMessage(handler) {
        this.messageHandlers.push(handler);
    }

    _emit(data) {
        this.messageHandlers.forEach(handler => handler(data));
    }

    _tryReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`[WS] Reconnecting (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
            setTimeout(() => this.connect(), this.reconnectDelay);
        }
    }
}

// Global instance
const jarvisWS = new JarvisWebSocket();
