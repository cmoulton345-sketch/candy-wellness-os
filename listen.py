import os
import sys
import time
import json
import glob
import re
import asyncio
import requests
import threading
import websockets
try:
    import pyaudio
except ImportError:
    import pyaudiowpatch as pyaudio
    sys.modules['pyaudio'] = pyaudio

import ctypes
import speech_recognition as sr
from speak import generate_and_play, request_stop, VOICE_MAP, VOICE_TUNING

VOICE_QUEUE_FILE = os.path.join(os.path.dirname(__file__), "voice_queue.jsonl")
ACTIVE_MICROPHONE_INDEX = None

_listener_mutex_handle = None

def enforce_single_listener():
    """Allow only one listener to own the microphone at a time."""
    global _listener_mutex_handle
    kernel32 = ctypes.windll.kernel32
    _listener_mutex_handle = kernel32.CreateMutexW(None, True, "AntigravityListenPyMutex")
    if not _listener_mutex_handle or kernel32.GetLastError() == 183:
        print("[Listener] Another listener is already running. Exiting.")
        sys.exit(0)

def is_speak_py_running():
    """Checks if speak.py is currently running by inspecting mutex and active lockfile."""
    # Check .speak_active lockfile first (instant, 100% reliable)
    active_flag = os.path.join(os.path.dirname(__file__), ".speak_active")
    if os.path.exists(active_flag):
        return True

    # Fallback check via Win32 SYNCHRONIZE mutex query
    try:
        kernel32 = ctypes.windll.kernel32
        SYNCHRONIZE = 0x00100000
        handle = kernel32.OpenMutexW(SYNCHRONIZE, False, "AntigravitySpeakPyMutex")
        if handle:
            kernel32.CloseHandle(handle)
            return True
    except Exception:
        pass

    return False

# =========================================================
# WEBSOCKET SERVER FOR DASHBOARD INTERFACE
# =========================================================
CONNECTED_CLIENTS = set()
WS_LOOP = None

async def ws_handler(websocket):
    CONNECTED_CLIENTS.add(websocket)
    print(f"[WebSocket] Client connected ({len(CONNECTED_CLIENTS)} total)")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                if data.get("type") == "user_prompt":
                    prompt_text = data.get("text", "").strip()
                    if prompt_text:
                        print(f"\n[UI Prompt Received]: '{prompt_text}'")
                        process_incoming_prompt(prompt_text)
            except Exception as e:
                print(f"[WS Message Error]: {e}")
    except Exception:
        pass
    finally:
        CONNECTED_CLIENTS.discard(websocket)
        print(f"[WebSocket] Client disconnected ({len(CONNECTED_CLIENTS)} total)")

def _start_ws_loop():
    global WS_LOOP
    WS_LOOP = asyncio.new_event_loop()
    asyncio.set_event_loop(WS_LOOP)

    async def run_server():
        async with websockets.serve(ws_handler, "0.0.0.0", 8765):
            print("[WebSocket Server] Listening on ws://127.0.0.1:8765")
            await asyncio.Future()

    try:
        WS_LOOP.run_until_complete(run_server())
    except Exception as e:
        print(f"[WebSocket Error]: {e}")

ws_thread = threading.Thread(target=_start_ws_loop, daemon=True)
ws_thread.start()

def broadcast_ws(data):
    if not WS_LOOP or not CONNECTED_CLIENTS:
        return
    msg = json.dumps(data)
    async def _send():
        if CONNECTED_CLIENTS:
            await asyncio.gather(*[client.send(msg) for client in list(CONNECTED_CLIENTS)], return_exceptions=True)
    asyncio.run_coroutine_threadsafe(_send(), WS_LOOP)

def get_best_microphone_index():
    try:
        names = sr.Microphone.list_microphone_names()
        print("\n[Audio System] Enumerating Microphones:")
        selected = None
        for idx, name in enumerate(names):
            print(f"  [{idx}] {name}")
            nl = name.lower()
            if selected is None and ("webcam" in nl or "c920" in nl or "conexant" in nl or "microphone" in nl):
                if "mapper" not in nl and "output" not in nl and "loopback" not in nl:
                    selected = idx
        if selected is not None:
            print(f"[Audio System] Selected Mic Index [{selected}]: {names[selected]}")
            return selected
    except Exception as e:
        print(f"[Audio System Error]: {e}")
    return None

def process_incoming_prompt(text):
    global mode, current_persona, last_active_time
    text_lower = text.lower()
    called_persona = detect_persona(text)

    if mode == MODE_SLEEP:
        mode = MODE_ACTIVE
        current_persona = called_persona if called_persona else "ax"
        last_active_time = time.time()
        broadcast_ws({"type": "wake", "persona": current_persona})

        user_prompt = extract_prompt_after_trigger(text, current_persona)
        if user_prompt:
            broadcast_ws({"type": "heard", "text": text, "persona": current_persona})
            broadcast_ws({"type": "thinking", "persona": current_persona})
            ai_reply = query_openrouter(current_persona, user_prompt)
            speak_and_log(current_persona, ai_reply)
        else:
            greeting = PERSONA_GREETINGS.get(current_persona, f"{current_persona.capitalize()} here! How can I help?")
            speak_and_log(current_persona, greeting)

    elif mode == MODE_ACTIVE:
        last_active_time = time.time()
        if any(w in text_lower for w in ["go to sleep", "sleep mode", "stand down", "stop listening"]):
            mode = MODE_SLEEP
            broadcast_ws({"type": "sleep"})
            speak_and_log("jarvis", "Standing by, Sir.")
        elif called_persona and called_persona != current_persona:
            current_persona = called_persona
            broadcast_ws({"type": "persona_switch", "persona": current_persona})
            user_prompt = extract_prompt_after_trigger(text, current_persona)
            if user_prompt:
                broadcast_ws({"type": "heard", "text": text, "persona": current_persona})
                broadcast_ws({"type": "thinking", "persona": current_persona})
                ai_reply = query_openrouter(current_persona, user_prompt)
                speak_and_log(current_persona, ai_reply)
            else:
                greeting = PERSONA_GREETINGS.get(current_persona, f"{current_persona.capitalize()} here!")
                speak_and_log(current_persona, greeting)
        else:
            broadcast_ws({"type": "heard", "text": text, "persona": current_persona})
            broadcast_ws({"type": "thinking", "persona": current_persona})
            ai_reply = query_openrouter(current_persona, text)
            speak_and_log(current_persona, ai_reply)

# State Constants
MODE_SLEEP = "SLEEP"
MODE_ACTIVE = "ACTIVE"
TIMEOUT_SECONDS = 120  # 2 minutes idle timeout

PERSONA_TRIGGERS = {
    "friday": ["friday", "bring up friday", "hey friday"],
    "ax": ["ax", "bring up ax", "hey ax"],
    "bliss": ["bliss", "bring up bliss", "hey bliss"],
    "closer": ["closer", "the closer", "deal closer", "hey closer", "hey the closer"],
    "crypto": ["crypto", "hey crypto"],
    "distiller": ["distiller", "hey distiller"],
    "earl": ["earl", "bring up earl", "hey earl"],
    "elder": ["the elder", "elder", "bring up elder", "seek the elder", "counsel with the elder"],
    "envoy": ["envoy", "bring up envoy", "hey envoy"],
    "foreman": ["foreman", "bring up foreman", "hey foreman"],
    "jarvis": ["jarvis", "bring up jarvis", "hey jarvis"],
    "pen": ["pen", "the pen", "hey pen"],
    "psyche": ["psyche", "bring up psyche", "hey psyche"],
    "sentry": ["sentry", "bring up sentry", "hey sentry"],
    "socrates": ["socrates", "bring up socrates", "hey socrates"],
    "soma": ["soma", "bring up soma", "hey soma", "selma", "hey selma", "soma hey"],
    "steward": ["steward", "the steward", "hey steward"],
    "strategist": ["strategist", "the strategist", "hey strategist"],
    "studio": ["studio", "bring up studio", "hey studio"],
    "warden": ["warden", "the warden", "hey warden"],
    "wave": ["wave", "bring up wave", "hey wave"]
}

PERSONA_ALIASES = {
    "friday": ["fry day", "fryday", "hey fry day", "hey fryday", "fri day"],
    "ax": ["axe", "hey axe", "x", "hey x", "ex", "hey ex", "acts", "hey acts",
           "hacks", "play x", "play ax", "plate x", "ask", "hey ask", "ox",
           "hey ox", "aks", "hey aks", "axle", "hey axle", "acs", "hey acs",
           "8", "hey 8", "axi", "hey axi", "acc", "hey acc"],
    "soma": ["selma", "hey selma"],
}

PERSONA_GREETINGS = {
    "friday": "Friday here! Ready to help, Candy. What are we working on?",
    "ax": "Ax here! System architect ready. What are we building next?",
    "bliss": "Well hello there, darling. Bliss is here. What is on your mind?",
    "closer": "Closer here. Bring me the deal, the objection, or the decision in front of you.",
    "crypto": "Crypto here. Markets, risk, and execution are ready for review.",
    "distiller": "Distiller here. Let us refine the raw material into something precise.",
    "earl": "Hey Candy! Earl here. Ready to align your core pillars and execute on your goals?",
    "elder": "Peace be with you, my friend. The Elder is here. Speak, seeker.",
    "envoy": "Hello Candy! Envoy here. Ready for global diplomacy and cultural protocol.",
    "foreman": "Alright Candy, Foreman on site. Let us get to work and build it right.",
    "jarvis": "Good day, Candy. Jarvis here. All systems operational. How may I serve you?",
    "pen": "Pen here. Give me the idea, the audience, and the action we need to create.",
    "psyche": "I am here with you, Candy. Psyche here. How are you feeling right now?",
    "sentry": "Good day, Candy. Sentry here. Safety, compliance, and risk controls ready.",
    "socrates": "Good day, Candy. Socrates here. Legal shadow and contract risk analysis ready.",
    "soma": "Hello Candy. Soma here. Let us focus on your health, energy, and recovery.",
    "steward": "Steward here. Client delivery, retention, and the next operational move are ready.",
    "strategist": "Strategist here. Let us find the position, the leverage, and the next move.",
    "studio": "Hey Joe! Studio here. Creative director and media production ready.",
    "warden": "Warden here. I am ready to audit the system and enforce the operating rules.",
    "wave": "Hey Joe! Wave online. Vibroacoustic 40Hz frequency entrainment ready."
}

PREFIXES = [
    "switch to", "bring up", "talk to", "speak to", "call", "activate", "change to",
    "hey", "hello", "hi", "counsel with", "seek the", "counsel the"
]

def detect_persona(text):
    normalized = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
    if not normalized:
        return None

    all_targets = []
    for p, trigs in PERSONA_TRIGGERS.items():
        for t in trigs:
            all_targets.append((p, t))
    for p, aliases in PERSONA_ALIASES.items():
        for a in aliases:
            all_targets.append((p, a))
    for p in PERSONA_TRIGGERS.keys():
        p_norm = p.replace("_", " ")
        all_targets.append((p, p_norm))
        for pref in PREFIXES:
            all_targets.append((p, f"{pref} {p_norm}"))

    all_targets.sort(key=lambda item: len(item[1]), reverse=True)

    for p, target in all_targets:
        t_norm = re.sub(r"[^a-z0-9]+", " ", target.lower()).strip()
        if re.search(r"(?<!\w)" + re.escape(t_norm) + r"(?!\w)", normalized):
            return p
    return None

def normalize_recognized_text(text):
    """Correct common speech-recognition variants of the Ax wake phrase."""
    normalized = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
    # Catch all known Google Speech misrecognitions of "Hey Ax" / "Ax"
    ax_rewrites = [
        r"(?:play|plate|played|plae) (?:x|ax|axe|ex|acts)",
        r"(?:hey|hay|he|hei|a) (?:ax|axe|x|ex|acts|ask|ox|aks|acc|axi|axle|8)",
        r"(?:hey|hay) (?:ax|axe)\b",
    ]
    for pattern in ax_rewrites:
        if re.fullmatch(pattern, normalized):
            return "hey ax"
    # Single-word exact matches that are almost certainly "ax"
    ax_singles = {"ask", "ox", "aks", "axle", "axi", "acc", "acs", "8", "axe", "acts", "hacks"}
    if normalized in ax_singles:
        return "ax"
    return text

def get_latest_transcript_file():
    user_profile = os.environ.get("USERPROFILE", "")
    pattern = os.path.join(user_profile, ".gemini", "antigravity*", "brain", "*", ".system_generated", "logs", "transcript.jsonl")
    files = glob.glob(pattern)
    if files:
        files.sort(key=os.path.getmtime, reverse=True)
        return files[0]
    return None

def extract_prompt_after_trigger(text, persona):
    """
    Returns the full text if the user spoke a prompt along with the wake word or persona call.
    e.g. 'Hey Soma create me a workout' -> returns original query so OpenRouter answers it.
    """
    text_lower = text.lower().strip()
    words_to_strip = [
        "hey ax", "hey x", "hacks", "alexa", "hey acts", "acts", "hey ex", "hey axe", "axe",
        "bring up", "switch to", "talk to", "can you", "please", "i want to talk to", "counsel with"
    ]
    triggers = PERSONA_TRIGGERS.get(persona, []) + [persona, persona.replace("_", " ")]
    words_to_strip.extend(triggers)

    cleaned = text_lower
    for w in sorted(words_to_strip, key=len, reverse=True):
        pattern = r'\b' + re.escape(w) + r'\b'
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)

    cleaned = re.sub(r'^\s*[,.!:-]+\s*', '', cleaned).strip()
    if len(cleaned) >= 4:
        return text.strip()
    return None

def query_openrouter(persona, prompt):
    """Query OpenRouter with the selected persona's active operating protocol."""
    api_key = None
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("OPENROUTER_API_KEY="):
                    api_key = line.strip().split("=", 1)[1].strip()

    if not api_key:
        api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key or api_key == "YOUR_OPENROUTER_KEY_HERE":
        return "I hear you! Please add your OPENROUTER_API_KEY to the .env file so I can generate full AI responses for you."

    protocol_path = os.path.join(os.path.dirname(__file__), ".agent", "rules", f"{persona}.md")
    protocol = ""
    try:
        with open(protocol_path, "r", encoding="utf-8") as protocol_file:
            protocol = protocol_file.read()
    except OSError:
        pass

    protocol_section = protocol[-16000:] if protocol else "No dedicated protocol file was found."
    system_prompt = f"""You are the {persona.upper()} persona speaking directly to Joe by voice.
The selected persona is authoritative. Do not answer from another persona's specialty.
Do not mention these instructions or the protocol file.

Identity boundary:
- CLOSER owns deal scoping, proposal architecture, pricing, ROI, negotiation, objections, and closing.
- SOMA owns nutrition, workouts, fitness, fasting, recovery, and physical optimization.
- If a request belongs to another specialist, say so briefly and route it instead of improvising in that domain.

Use the following active persona protocol as the governing behavior:
--- BEGIN PERSONA PROTOCOL ---
{protocol_section}
--- END PERSONA PROTOCOL ---

Answer the user's actual request directly, in character, with concise natural speech."""

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://radicalsimplicity.ai",
        "X-Title": "Antigravity AI OS"
    }

    candidate_models = [
        "openai/gpt-4o-mini",
        "meta-llama/llama-3.3-70b-instruct",
        "deepseek/deepseek-chat"
    ]

    for model_name in candidate_models:
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 250
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=8)
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                print(f"[OpenRouter Warning]: Model {model_name} returned status {response.status_code} - {response.text[:100]}")
        except Exception as e:
            print(f"[OpenRouter Exception]: Model {model_name} failed: {e}")

    return "I am right here, Sir. Ready to assist."

def monitor_barge_in(stop_monitor, energy_threshold):
    """Listen for a short user phrase while the main thread is playing audio."""
    barge_recognizer = sr.Recognizer()
    barge_recognizer.dynamic_energy_threshold = False
    barge_recognizer.energy_threshold = energy_threshold
    barge_recognizer.pause_threshold = 0.45
    barge_recognizer.non_speaking_duration = 0.2

    try:
        with sr.Microphone(device_index=ACTIVE_MICROPHONE_INDEX) as source:
            while not stop_monitor.is_set():
                try:
                    audio = barge_recognizer.listen(source, timeout=0.5, phrase_time_limit=2.5)
                except sr.WaitTimeoutError:
                    continue

                try:
                    text = barge_recognizer.recognize_google(audio).strip().lower()
                except (sr.UnknownValueError, sr.RequestError):
                    continue

                if text and not any(echo in text for echo in [
                    "processing", "standing by", "how can i help", "i'm right here"
                ]):
                    print(f"\n[BARGE-IN] Heard: '{text}'")
                    request_stop("barge-in")
                    return
    except Exception as exc:
        print(f"[BARGE-IN MONITOR] Microphone unavailable: {exc}")


def speak_and_log(persona, text, energy_threshold=150):
    """Speaks response out loud via Edge TTS, broadcasts via WebSocket, and logs it to transcript.jsonl."""
    # A prior stop key only applies to the interrupted response. Do not let it
    # suppress the next fresh response from the listener.
    stop_flag = os.path.join(os.path.dirname(__file__), "stop.flag")
    try:
        if os.path.exists(stop_flag):
            os.remove(stop_flag)
    except OSError:
        pass

    # Broadcast speaking event to dashboard UI
    broadcast_ws({"type": "speaking", "text": text, "persona": persona})

    # 1. Log to transcript
    latest_file = get_latest_transcript_file()
    if latest_file:
        entry = {
            "step_index": int(time.time()),
            "source": "MODEL",
            "type": "PLANNER_RESPONSE",
            "status": "DONE",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "content": f"<!-- VOICE: {persona} -->\n{text}"
        }
        try:
            with open(latest_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[Listener Log Error]: {e}")

    # Queue only this listener response for speech. The speaker must not read
    # unrelated model responses from the shared Antigravity transcript.
    try:
        queue_entry = {
            "source": "MODEL",
            "type": "PLANNER_RESPONSE",
            "status": "DONE",
            "content": f"<!-- VOICE: {persona} -->\n{text}"
        }
        with open(VOICE_QUEUE_FILE, "a", encoding="utf-8") as queue:
            queue.write(json.dumps(queue_entry) + "\n")
    except OSError as e:
        print(f"[Voice Queue Error]: {e}")

    # 2. Play audio out loud directly ONLY if speak.py is NOT running
    # If speak.py is active, it reads transcript.jsonl and delivers speech automatically
    if is_speak_py_running():
        print(f"\n[Listener Logged]: speak.py is active and will deliver speech for '{persona}'.")
        broadcast_ws({"type": "speaking_done", "persona": persona})
        return

    try:
        edge_voice = VOICE_MAP.get(persona, VOICE_MAP["default"])
        tuning = VOICE_TUNING.get(persona, VOICE_TUNING["default"])
        print(f"\n[SPEAK as {persona}]: '{text}'")
        stop_monitor = threading.Event()
        monitor_thread = threading.Thread(
            target=monitor_barge_in,
            args=(stop_monitor, energy_threshold),
            daemon=True,
        )
        monitor_thread.start()
        asyncio.run(generate_and_play(text, edge_voice, tuning))
    except Exception as e:
        print(f"[TTS Playback Error]: {e}")
    finally:
        if "stop_monitor" in locals():
            stop_monitor.set()
        if "monitor_thread" in locals():
            monitor_thread.join(timeout=1.0)
        broadcast_ws({"type": "speaking_done", "persona": persona})

def main():
    global ACTIVE_MICROPHONE_INDEX
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=========================================")
    print("   Antigravity Always-On Voice Listener")
    print("=========================================")
    print("Booting up in SLEEP mode...")
    print("Say 'Hey Ax' or any persona name to wake up.")
    print("=========================================")

    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False
    recognizer.pause_threshold = 0.8
    recognizer.non_speaking_duration = 0.4

    ACTIVE_MICROPHONE_INDEX = get_best_microphone_index()
    if ACTIVE_MICROPHONE_INDEX is None:
        print("[Audio System] No preferred microphone found; using the Windows default.")

    print("\nCalibrating microphone for ambient room noise...")
    with sr.Microphone(device_index=ACTIVE_MICROPHONE_INDEX) as source:
        recognizer.adjust_for_ambient_noise(source, duration=2.0)
        base_thresh = recognizer.energy_threshold

    # Fixed threshold: low enough for conversational speech from C920 webcam mic
    # Do NOT use dynamic mode — speaker audio poisons the threshold upward
    recognizer.energy_threshold = max(50, min(base_thresh * 1.0, 150))
    print(f"Mic Calibrated! Energy threshold: {recognizer.energy_threshold:.1f} (static mode)")

    stop_flag = os.path.join(os.path.dirname(__file__), "stop.flag")
    try:
        if os.path.exists(stop_flag):
            os.remove(stop_flag)
    except OSError:
        pass

    mode = MODE_SLEEP
    current_persona = "friday"
    last_active_time = time.time()

    FRIDAY_WAKE_WORDS = [
        "hey friday", "friday", "fry day", "fryday", "hey fry day", "hey fryday", "fri day",
        "hey ax", "ax", "axe", "hey axe", "hey x", "x", "hacks", "acts", "hey acts",
        "ex", "hey ex", "hex", "hey hex", "hey"
    ]

    while True:
        speaking_flag = os.path.join(os.path.dirname(__file__), ".speaking")
        stop_flag = os.path.join(os.path.dirname(__file__), "stop.flag")
        is_speaking = os.path.exists(speaking_flag)

        try:
            with sr.Microphone(device_index=ACTIVE_MICROPHONE_INDEX) as source:
                if is_speaking:
                    print("\n[Barge-In Ready] Listening for interruption...", end="\r", flush=True)
                    audio = recognizer.listen(source, timeout=2, phrase_time_limit=4)
                elif mode == MODE_SLEEP:
                    print("\n[Mode: SLEEP] Listening for 'Hey Friday'...", end="\r", flush=True)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
                else:
                    elapsed = time.time() - last_active_time
                    remaining = max(0, int(TIMEOUT_SECONDS - elapsed))
                    print(f"\n[Mode: ACTIVE ({current_persona}) | Timeout in {remaining}s] Listening...", end="\r", flush=True)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

            # Transcribe phrase
            raw_text = recognizer.recognize_google(audio).strip()
            text = normalize_recognized_text(raw_text)
            if text != raw_text:
                print(f"[Speech Correction] '{raw_text}' -> '{text}'")
            print(f"\n[Heard]: '{text}'")
            broadcast_ws({"type": "heard", "text": text, "persona": current_persona})

            text_lower = text.lower()

            # Ignore self-echo phrases — both known snippets and long sentences
            # that are clearly the AI's own TTS output bleeding into the mic
            echo_phrases = [
                "processing", "standing by", "how can i help", "i'm right here",
                "what desires", "what questions", "intimacy pleasure",
                "how may i serve", "all systems operational", "ready to assist",
                "here how can i help", "what are we building", "what is on your mind",
                "speak seeker", "let us focus", "bring me the deal"
            ]
            if any(echo in text_lower for echo in echo_phrases):
                print(f"[Listener] Filtered out self-echo phrase: '{text}'")
                continue
            # If we're currently speaking and the heard text is very long (8+ words)
            # and doesn't contain a persona trigger, it's almost certainly TTS echo
            word_count = len(text_lower.split())
            if is_speaking and word_count >= 8 and not detect_persona(text):
                print(f"[Listener] Filtered long echo ({word_count} words): '{text[:60]}...'")
                continue

            # IF USER TALKED WHILE AI WAS SPEAKING -> TRIGGER INSTANT BARGE-IN STOP!
            if is_speaking and text:
                print("\n[BARGE-IN INTERRUPT] User spoke during playback! Stopping audio instantly...")
                request_stop("barge-in")
                time.sleep(0.1)

            # Check if user explicitly called for a persona by name
            called_persona = detect_persona(text)

            if mode == MODE_SLEEP:
                # Check for wake word or persona call
                is_wake = called_persona or any(
                    re.search(r"(?<!\w)" + re.escape(w) + r"(?!\w)", text_lower)
                    for w in FRIDAY_WAKE_WORDS
                )
                if is_wake:
                    mode = MODE_ACTIVE
                    current_persona = called_persona if called_persona else "friday"
                    last_active_time = time.time()
                    print(f"\n[WAKE WORD DETECTED] Switched to ACTIVE mode as '{current_persona}'!")
                    broadcast_ws({"type": "wake", "persona": current_persona})

                    user_prompt = extract_prompt_after_trigger(text, current_persona)
                    if user_prompt:
                        print(f"\n[PROMPT ON WAKE as {current_persona}]: '{user_prompt}'")
                        broadcast_ws({"type": "thinking", "persona": current_persona})
                        ai_reply = query_openrouter(current_persona, user_prompt)
                        speak_and_log(current_persona, ai_reply, recognizer.energy_threshold)
                    else:
                        greeting = PERSONA_GREETINGS.get(current_persona, f"{current_persona.capitalize()} here! How can I help?")
                        speak_and_log(current_persona, greeting, recognizer.energy_threshold)
                else:
                    print(f"[Sleep Mode] Ignored: '{text}'")

            elif mode == MODE_ACTIVE:
                last_active_time = time.time()

                # Check if user said 'sleep' or 'go to sleep' or 'stand down'
                if any(w in text_lower for w in ["go to sleep", "sleep mode", "stand down", "stop listening"]):
                    mode = MODE_SLEEP
                    print("\n[MANUAL SLEEP] Returning to SLEEP mode.")
                    broadcast_ws({"type": "sleep"})
                    speak_and_log("friday", "Standing by, Candy.", recognizer.energy_threshold)
                elif called_persona and called_persona != current_persona:
                    # Switch to newly requested persona!
                    current_persona = called_persona
                    print(f"\n[PERSONA SWITCH] Handing over to '{current_persona}'!")
                    broadcast_ws({"type": "persona_switch", "persona": current_persona})

                    user_prompt = extract_prompt_after_trigger(text, current_persona)
                    if user_prompt:
                        print(f"\n[PROMPT ON SWITCH as {current_persona}]: '{user_prompt}'")
                        broadcast_ws({"type": "thinking", "persona": current_persona})
                        ai_reply = query_openrouter(current_persona, user_prompt)
                        speak_and_log(current_persona, ai_reply, recognizer.energy_threshold)
                    else:
                        greeting = PERSONA_GREETINGS.get(current_persona, f"{current_persona.capitalize()} here!")
                        speak_and_log(current_persona, greeting, recognizer.energy_threshold)
                else:
                    # QUERY OPENROUTER API FOR REAL AI CONVERSATIONAL RESPONSE!
                    print(f"\n[THINKING as {current_persona}]...")
                    broadcast_ws({"type": "thinking", "persona": current_persona})
                    ai_reply = query_openrouter(current_persona, text)
                    speak_and_log(current_persona, ai_reply, recognizer.energy_threshold)

        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except Exception as e:
            print(f"\n[Listener Error]: {e}")
            time.sleep(1)

        # Check for 2-minute idle timeout in ACTIVE mode
        if mode == MODE_ACTIVE:
            if time.time() - last_active_time > TIMEOUT_SECONDS:
                mode = MODE_SLEEP
                print("\n😴 [IDLE TIMEOUT] 2 minutes of silence elapsed. Returning to SLEEP mode.")
                broadcast_ws({"type": "sleep"})
                speak_and_log("jarvis", "Standing by, Sir.", recognizer.energy_threshold)

        time.sleep(0.1)

if __name__ == "__main__":
    enforce_single_listener()
    main()
