# 🤖 JARVIS — AI-Native Voice Assistant

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://orgin-qeol.onrender.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat&logo=supabase)](https://supabase.com)
[![Gemini](https://img.shields.io/badge/Google_Gemini-8E75C2?style=flat&logo=googlegemini)](https://ai.google.dev/)

**Jarvis** is a state-of-the-art AI-Native personal assistant inspired by Iron Man's JARVIS. Built with a modern tech stack, it combines high-performance web architecture with Google's most capable AI models to provide a seamless, voice-first experience.

---

## 🚀 Two Ways to Experience Jarvis

### 1. The Cloud Demo (For Recruiters & Developers)
**Link:** [https://orgin-qeol.onrender.com](https://orgin-qeol.onrender.com)

Jarvis is hosted on **Render** with a "Cloud Demo Mode." In this mode:
- **Voice Interaction**: Jarvis listens and speaks via the browser (STT & TTS).
- **Tool Simulation**: Since he can't access your laptop from the cloud, Jarvis **simulates** desktop actions (like opening WhatsApp, changing volume, or taking screenshots) and explains what he would do.
- **Cloud Persistence**: Jarvis uses **Supabase** (PostgreSQL) to store your preferences and contacts persistently.

### 2. Local Control (For Full PC Automation)
Run Jarvis locally to give him full control over your machine:
- **Desktop Automation**: Open any app, control system volume, and take screenshots.
- **Communication**: Automatically send WhatsApp messages and initiate calls.
- **Synced Knowledge**: Because it's connected to the same Supabase instance, all your cloud-saved settings are instantly available locally.

---

## 🏗️ Technical Architecture

- **AI Brain**: Powered by **Google Gemini 1.5 Flash**, utilizing advanced **Function Calling** to translate natural language into system commands.
- **Backend**: **FastAPI** provides a high-concurrency WebSocket server for real-time audio and text streaming.
- **Database**: **Supabase (PostgreSQL)** handles persistent storage for contacts, personal info, and custom commands.
- **Voice Pipeline**: 
  - **Speech-to-Text**: Google Recognition API.
  - **Text-to-Speech**: **Edge-TTS** (Microsoft Neural voices) for premium, lifelike audio output.
- **Frontend**: A custom, "premium" dark-mode interface built with Vanilla JS for maximum speed and responsiveness.

---

## 🛠️ Local Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Phanikartheek/orgin.git
   cd orgin
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   Create a `.env` file with your keys:
   ```env
   GEMINI_API_KEY=your_key_here
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_service_role_key
   ```

4. **Run Jarvis:**
   ```bash
   python run.py
   ```

---

## 📜 Repository Structure
- `app/main.py`: The core FastAPI server.
- `app/agent/brain.py`: The Gemini Agent logic and tool definitions.
- `app/database/db.py`: Supabase client integration.
- `frontend/`: The premium Web UI.
- `app/agent/tools/`: Custom Python tools for system control and communication.

---

*“Jarvis is ready, Sir. How may I assist you today?”*
