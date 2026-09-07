# Voice Engine & Listener SOP (Standard Operating Procedure)

## Overview
The Antigravity Voice System consists of two lightweight, asynchronous python scripts running on Windows:
1. **`speak.py`**: Monitors active `transcript.jsonl` log files, parses persona tags (e.g. `<!-- VOICE: jarvis -->`), synthesizes natural speech using Edge TTS, and plays audio aloud via `pygame.mixer`. It also runs a 20ms hardware hotkey listener for instant speech interruption.
2. **`listen.py`**: Monitors local microphone audio for wake words (*"Hey Ax"*, *"Jarvis"*, etc.), handles real-time speech recognition via Google Speech Recognition API, queries OpenRouter for AI persona responses, and broadcasts events via WebSocket (`ws://127.0.0.1:8765`).

---

## ⚡ Hotkey Interruption Rules
Hotkeys are polled in `hardware_hotkey_poller()` inside `speak.py` using direct Win32 `GetAsyncKeyState` kernel queries:
- **`Escape` (`0x1B`)**: Interrupts speech immediately when audio is actively playing (`is_speaking`). Outside of active audio playback, Esc is ignored to avoid interfering with IDE/browser typing.
- **`Pause / Break` (`0x13`)**: Interrupts speech at any time.

> **CRITICAL RULE**: Do not alter `hardware_hotkey_poller()` to re-introduce complex Win32 `RegisterHotKey` callbacks or un-scoped `was_triggered` variable references. The `GetAsyncKeyState` loop must strictly check `st & 0x8000`.

---

## 🤖 OpenRouter API Candidate Models
`listen.py` uses an automatic fallback array when querying OpenRouter for persona responses:
1. `openai/gpt-4o-mini` (Primary — ultra fast, 200 OK)
2. `meta-llama/llama-3.3-70b-instruct` (Secondary fallback)
3. `deepseek/deepseek-chat` (Tertiary fallback)

> **CRITICAL RULE**: Do not revert to deprecated model slugs like `google/gemini-2.0-flash-lite-001` or `google/gemini-2.0-flash-001` which return HTTP 404 on OpenRouter.

---

## 🚀 How to Run & Maintain
- **Standard Launcher**: Run `start_voice.bat` (cleans stale lock files and launches speaker + listener).
- **Silent Background Launcher**: Double-click `start_voice_silent.vbs`.
- **Termination Script**: Run `kill_speak.ps1` to cleanly terminate processes and release audio/mic handles.
