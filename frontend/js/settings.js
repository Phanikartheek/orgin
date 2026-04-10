/**
 * Settings Panel
 * Handles the slide-out settings panel and CRUD operations.
 */

class SettingsManager {
    constructor() {
        this.panel = document.getElementById('settingsPanel');
        this.overlay = document.getElementById('settingsOverlay');
        this.isOpen = false;

        this._bindEvents();
    }

    _bindEvents() {
        // Open/Close
        document.getElementById('settingsBtn').addEventListener('click', () => this.open());
        document.getElementById('closeSettingsBtn').addEventListener('click', () => this.close());
        this.overlay.addEventListener('click', () => this.close());

        // Tabs
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this._switchTab(e.target.dataset.tab));
        });

        // Save Profile
        document.getElementById('saveProfileBtn').addEventListener('click', () => this._saveProfile());

        // Add App
        document.getElementById('addAppBtn').addEventListener('click', () => this._addApp());

        // Add Website
        document.getElementById('addWebBtn').addEventListener('click', () => this._addWebsite());

        // Add Contact
        document.getElementById('addContactBtn').addEventListener('click', () => this._addContact());
    }

    open() {
        this.panel.classList.add('open');
        this.overlay.classList.remove('hidden');
        this.isOpen = true;
        this._loadAllData();
    }

    close() {
        this.panel.classList.remove('open');
        this.overlay.classList.add('hidden');
        this.isOpen = false;
    }

    _switchTab(tabId) {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

        document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');
        document.getElementById(`tab-${tabId}`).classList.add('active');
    }

    async _loadAllData() {
        await Promise.all([
            this._loadProfile(),
            this._loadApps(),
            this._loadWebsites(),
            this._loadContacts(),
        ]);
    }

    // --- Profile ---

    async _loadProfile() {
        try {
            const res = await fetch('/api/personal-info');
            const json = await res.json();
            if (json.data) {
                document.getElementById('profileName').value = json.data.name || '';
                document.getElementById('profileDesignation').value = json.data.designation || '';
                document.getElementById('profileMobile').value = json.data.mobileno || '';
                document.getElementById('profileEmail').value = json.data.email || '';
                document.getElementById('profileCity').value = json.data.city || '';
            }
        } catch (e) {
            console.error('Failed to load profile:', e);
        }
    }

    async _saveProfile() {
        const data = {
            name: document.getElementById('profileName').value,
            designation: document.getElementById('profileDesignation').value,
            mobileno: document.getElementById('profileMobile').value,
            email: document.getElementById('profileEmail').value,
            city: document.getElementById('profileCity').value,
        };

        if (!data.name || !data.mobileno) {
            ui.showToast('Name and Mobile are required');
            return;
        }

        try {
            await fetch('/api/personal-info', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
            ui.showToast('Profile saved successfully!');
        } catch (e) {
            ui.showToast('Failed to save profile');
        }
    }

    // --- Apps ---

    async _loadApps() {
        try {
            const res = await fetch('/api/sys-commands');
            const json = await res.json();
            const list = document.getElementById('appsList');
            list.innerHTML = json.data.map(item => `
                <div class="list-item">
                    <div class="list-item-info">
                        <span class="list-item-name">${item.name}</span>
                        <span class="list-item-detail">${item.path}</span>
                    </div>
                    <button class="delete-btn" onclick="settings._deleteApp(${item.id})">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                    </button>
                </div>
            `).join('');
        } catch (e) {
            console.error('Failed to load apps:', e);
        }
    }

    async _addApp() {
        const name = document.getElementById('appName').value.trim();
        const path = document.getElementById('appPath').value.trim();
        if (!name || !path) { ui.showToast('Both fields are required'); return; }

        try {
            await fetch('/api/sys-commands', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, path }),
            });
            document.getElementById('appName').value = '';
            document.getElementById('appPath').value = '';
            ui.showToast('App added!');
            this._loadApps();
        } catch (e) {
            ui.showToast('Failed to add app');
        }
    }

    async _deleteApp(id) {
        try {
            await fetch(`/api/sys-commands/${id}`, { method: 'DELETE' });
            this._loadApps();
        } catch (e) {
            ui.showToast('Failed to delete');
        }
    }

    // --- Websites ---

    async _loadWebsites() {
        try {
            const res = await fetch('/api/web-commands');
            const json = await res.json();
            const list = document.getElementById('websList');
            list.innerHTML = json.data.map(item => `
                <div class="list-item">
                    <div class="list-item-info">
                        <span class="list-item-name">${item.name}</span>
                        <span class="list-item-detail">${item.url}</span>
                    </div>
                    <button class="delete-btn" onclick="settings._deleteWebsite(${item.id})">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                    </button>
                </div>
            `).join('');
        } catch (e) {
            console.error('Failed to load websites:', e);
        }
    }

    async _addWebsite() {
        const name = document.getElementById('webName').value.trim();
        const url = document.getElementById('webUrl').value.trim();
        if (!name || !url) { ui.showToast('Both fields are required'); return; }

        try {
            await fetch('/api/web-commands', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, url }),
            });
            document.getElementById('webName').value = '';
            document.getElementById('webUrl').value = '';
            ui.showToast('Website added!');
            this._loadWebsites();
        } catch (e) {
            ui.showToast('Failed to add website');
        }
    }

    async _deleteWebsite(id) {
        try {
            await fetch(`/api/web-commands/${id}`, { method: 'DELETE' });
            this._loadWebsites();
        } catch (e) {
            ui.showToast('Failed to delete');
        }
    }

    // --- Contacts ---

    async _loadContacts() {
        try {
            const res = await fetch('/api/contacts');
            const json = await res.json();
            const list = document.getElementById('contactsList');
            list.innerHTML = json.data.map(item => `
                <div class="list-item">
                    <div class="list-item-info">
                        <span class="list-item-name">${item.name}</span>
                        <span class="list-item-detail">${item.mobile_no}${item.email ? ' • ' + item.email : ''}</span>
                    </div>
                    <button class="delete-btn" onclick="settings._deleteContact(${item.id})">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                    </button>
                </div>
            `).join('');
        } catch (e) {
            console.error('Failed to load contacts:', e);
        }
    }

    async _addContact() {
        const name = document.getElementById('contactName').value.trim();
        const mobile = document.getElementById('contactMobile').value.trim();
        const email = document.getElementById('contactEmail').value.trim();
        const city = document.getElementById('contactCity').value.trim();
        if (!name || !mobile) { ui.showToast('Name and Mobile are required'); return; }

        try {
            await fetch('/api/contacts', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, mobile_no: mobile, email, city }),
            });
            ['contactName', 'contactMobile', 'contactEmail', 'contactCity'].forEach(
                id => document.getElementById(id).value = ''
            );
            ui.showToast('Contact added!');
            this._loadContacts();
        } catch (e) {
            ui.showToast('Failed to add contact');
        }
    }

    async _deleteContact(id) {
        try {
            await fetch(`/api/contacts/${id}`, { method: 'DELETE' });
            this._loadContacts();
        } catch (e) {
            ui.showToast('Failed to delete');
        }
    }
}

// Global instance
const settings = new SettingsManager();
