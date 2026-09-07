import os
import sys
import time
import json
import glob
import re
import asyncio
import requests
import threading
import tempfile
import ctypes
from ctypes import wintypes

try:
    import pyaudio
except ImportError:
    import pyaudiowpatch as pyaudio
    sys.modules['pyaudio'] = pyaudio

import speech_recognition as sr
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Hide Pygame welcome banner
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

# Initialize Pygame Mixer at high quality (48kHz stereo)
mixer.init(frequency=48000, buffer=1024)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# =========================================================
# SINGLE INSTANCE MUTEX (WINDOWS)
# =========================================================
def enforce_single_instance():
    """Ensure only one instance of Candy's voice_system.py runs at a time."""
    kernel32 = ctypes.windll.kernel32
    mutex_name = "FlowstateCandyVoiceSystemMutex"
    handle = kernel32.CreateMutexW(None, True, mutex_name)
    last_error = kernel32.GetLastError()
    if handle == 0 or last_error in (183, 5): # ERROR_ALREADY_EXISTS or ERROR_ACCESS_DENIED
        print("\n[Voice System] Another instance of Candy's voice system is already running. Exiting.")
        sys.exit(0)
    return handle

_mutex_handle = enforce_single_instance()

# =========================================================
# PERSONA & VOICE DEFINITIONS (30 PERSONAS)
# =========================================================
VOICE_MAP = {
    "default": "en-US-ChristopherNeural",
    "ax":                    "en-US-ChristopherNeural",  # Lead Architect
    "closer":                "en-US-AndrewNeural",       # Deal Architect / Closer
    "jarvis":                "en-GB-RyanNeural",         # Local OS Controller
    "pen":                   "en-US-EmmaNeural",         # Copy and content strategist
    "steward":              "en-GB-RyanNeural",         # Client delivery and retention
    "strategist":           "en-US-AndrewNeural",       # Positioning and strategic direction
    "warden":               "en-US-SteffanNeural",       # Governance and system audit
    "atlas":                 "en-US-SteffanNeural",      # CMO
    "keller":                "en-US-AndrewNeural",       # Executive Business Coach
    "uncle_g":               "en-US-RogerNeural",        # 10X Sales Coach
    "brunsen_2_0":           "en-US-BrianNeural",        # Direct Response Architect
    "voss":                  "en-US-ChristopherNeural",  # B2B Systems Architect
    "chairman":              "en-US-RogerNeural",        # Ads Architect
    "collect":               "en-US-EricNeural",         # Client Intake Specialist
    "jeeves":                "en-GB-RyanNeural",         # Client Delivery
    "navigator":             "en-US-BrianMultilingualNeural",
    "elder":                 "en-GB-ThomasNeural",       # Modern Mystic
    "psyche":                "en-US-MichelleNeural",     # Human Behavior OS
    "clarity":               "en-US-EmmaNeural",         # Intuitive Facilitator
    "socrates":              "en-US-AndrewMultilingualNeural",  # Legal Shadow
    "nate":                  "en-US-EricNeural",         # n8n Workflow Architect
    "web_builder":           "en-CA-LiamNeural",         # Full-Stack Builder
    "webbuilder":            "en-CA-LiamNeural",
    "information_architect": "en-NZ-MitchellNeural",
    "skeptical_researcher":  "en-AU-WilliamMultilingualNeural",
    "researcher":            "en-AU-WilliamMultilingualNeural",
    "distiller":             "en-IE-ConnorNeural",       # Master Distiller
    "foreman":               "en-US-SteffanNeural",      # General Contractor
    "crypto":                "en-US-GuyNeural",          # Crypto Trading Architect
    "bliss":                 "en-US-JennyNeural",        # Inner Peace / Presence
    "earl":                  "en-US-SteffanNeural",      # Goals Coach & Inner Architect
    "sentry":                "en-US-ChristopherNeural",  # EH&S Safety Shadow
    "soma":                  "en-US-AriaNeural",         # Health & Optimization
    "studio":                "en-US-GuyNeural",          # Visual Creative Director
    "wave":                  "en-US-GuyNeural",          # Audio & Music Creative
    "envoy":                 "en-ZA-LukeNeural",         # Cultural Consultant
    "erickson":              "en-US-BrianNeural"         # Trance Architect & Subconscious Release
}

PERSONA_TRIGGERS = {
    "ax": ["ax", "bring up ax", "hey ax"],
    "bliss": ["bliss", "bring up bliss", "hey bliss"],
    "closer": ["closer", "the closer", "deal closer", "hey closer"],
    "crypto": ["crypto", "hey crypto"],
    "distiller": ["distiller", "hey distiller"],
    "earl": ["earl", "bring up earl", "hey earl"],
    "elder": ["the elder", "elder", "seek the elder"],
    "envoy": ["envoy", "bring up envoy", "hey envoy"],
    "erickson": ["erickson", "bring up erickson", "hey erickson", "dr erickson"],
    "foreman": ["foreman", "bring up foreman", "hey foreman"],
    "jarvis": ["jarvis", "bring up jarvis", "hey jarvis"],
    "pen": ["pen", "the pen", "hey pen"],
    "psyche": ["psyche", "bring up psyche", "hey psyche"],
    "sentry": ["sentry", "bring up sentry", "hey sentry"],
    "socrates": ["socrates", "bring up socrates", "hey socrates"],
    "soma": ["soma", "bring up soma", "hey soma", "selma", "hey selma"],
    "steward": ["steward", "the steward", "hey steward"],
    "strategist": ["strategist", "the strategist", "hey strategist"],
    "studio": ["studio", "bring up studio", "hey studio"],
    "warden": ["warden", "the warden", "hey warden"],
    "wave": ["wave", "bring up wave", "hey wave"]
}

PERSONA_ALIASES = {
    "ax": ["axe", "hey axe", "x", "hey x", "ex", "hey ex", "acts", "hey acts",
           "hacks", "play x", "play ax", "plate x", "ask", "hey ask", "ox",
           "hey ox", "aks", "hey aks", "axle", "hey axle", "acs", "hey acs",
           "8", "hey 8", "axi", "hey axi", "acc", "hey acc"],
    "erickson": ["ericsson", "hey ericsson", "erikson", "hey erikson", "airickson", "erick"],
    "pen": ["pain", "hey pain", "pan", "hey pan", "pin", "hey pin", "penn", "hey penn"],
    "socrates": ["socratis", "sock rates", "sockrates", "hey socrates"],
    "psyche": ["sike", "syke", "psychee", "psych", "hey psyche"],
    "soma": ["selma", "hey selma", "sumo"],
    "foreman": ["four man", "for man", "4 man"],
    "steward": ["stewart", "stew"],
    "sentry": ["century", "centry"],
    "warden": ["warren"],
    "wave": ["waive", "wayv"],
    "closer": ["closure"],
}

PERSONA_GREETINGS = {
    "ax": "Ax here! System architect ready. What are we building next?",
    "bliss": "Well hello there, darling. Bliss is here. What is on your mind?",
    "closer": "Closer here. Bring me the deal, the objection, or the decision in front of you.",
    "crypto": "Crypto here. Markets, risk, and execution are ready for review.",
    "distiller": "Distiller here. Let us refine the raw material into something precise.",
    "earl": "Hey Joe! Earl here. Ready to align your core pillars and execute on your goals?",
    "elder": "Peace be with you, my friend. The Elder is here. Speak, seeker.",
    "envoy": "Howzit, Joe! Envoy here. Ready for global diplomacy and cultural protocol.",
    "erickson": "Erickson here. Trance architecture and subconscious transformation ready, Joe.",
    "foreman": "Alright Joe, Foreman on site. Let us get to work and build it right.",
    "jarvis": "Good evening, Sir. Jarvis here. All systems operational. How may I serve you?",
    "pen": "Pen here. Give me the idea, the audience, and the action we need to create.",
    "psyche": "I am here with you, Joe. Psyche here. How are you feeling right now?",
    "sentry": "Good day, Joe. Sentry here. Safety, compliance, and risk controls ready.",
    "socrates": "Good day, Joe. Socrates here. Legal shadow and contract risk analysis ready.",
    "soma": "Hello Joe. Soma here. Let us focus on your health, energy, and recovery.",
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

# State Constants
MODE_SLEEP = "SLEEP"
MODE_ACTIVE = "ACTIVE"
TIMEOUT_SECONDS = 120

# =========================================================
# UNIFIED VOICE ENGINE CLASS
# =========================================================
class VoiceEngine:
    def __init__(self):
        self.mode = MODE_SLEEP
        self.current_persona = "ax"
        self.active_speaker = "candy" # Default to Candy in Candy's OS
        self.last_active_time = time.time()
        self.is_speaking = False
        self.stop_requested = False
        self.active_mic_index = None
        self.energy_threshold = 95.0
        self.connected_ws_clients = set()
        self.ws_loop = None

        # Lock for thread-safe state operations
        self.state_lock = threading.Lock()

    # -----------------------------------------------------
    # WEBSOCKET SUBSYSTEM
    # -----------------------------------------------------
    def start_websocket_server(self):
        def _run_server():
            self.ws_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.ws_loop)

            async def handler(websocket):
                self.connected_ws_clients.add(websocket)
                print(f"[WebSocket] Client connected ({len(self.connected_ws_clients)} total)")
                try:
                    async for message in websocket:
                        try:
                            data = json.loads(message)
                            if data.get("type") == "user_prompt":
                                text = data.get("text", "").strip()
                                if text:
                                    print(f"\n[UI Prompt Received]: '{text}'")
                                    self.handle_incoming_text(text)
                        except Exception as err:
                            print(f"[WS Error]: {err}")
                finally:
                    self.connected_ws_clients.discard(websocket)
                    print(f"[WebSocket] Client disconnected ({len(self.connected_ws_clients)} total)")

            async def main_server():
                async with websockets.serve(handler, "0.0.0.0", 8765):
                    print("[WebSocket Server] Listening on ws://127.0.0.1:8765")
                    await asyncio.Future()

            try:
                self.ws_loop.run_until_complete(main_server())
            except Exception as e:
                print(f"[WebSocket Loop Failed]: {e}")

        import websockets
        ws_thread = threading.Thread(target=_run_server, daemon=True)
        ws_thread.start()

    def broadcast_ws(self, data):
        if not self.ws_loop or not self.connected_ws_clients:
            return
        msg = json.dumps(data)
        async def _send():
            if self.connected_ws_clients:
                await asyncio.gather(*[client.send(msg) for client in list(self.connected_ws_clients)], return_exceptions=True)
        asyncio.run_coroutine_threadsafe(_send(), self.ws_loop)

    # -----------------------------------------------------
    # HARDWARE HOTKEY POLLER THREAD
    # -----------------------------------------------------
    def start_hotkey_poller(self):
        user32 = ctypes.windll.user32
        user32.GetAsyncKeyState.restype = wintypes.SHORT
        user32.GetAsyncKeyState.argtypes = [ctypes.c_int]

        def is_down(vk):
            try:
                return bool(user32.GetAsyncKeyState(vk) & 0x8000)
            except Exception:
                return False

        def poller_loop():
            while True:
                try:
                    esc = is_down(0x1B)        # Escape
                    pause = is_down(0x13)      # Pause / Break
                    ctrl = is_down(0x11)
                    shift = is_down(0x10)
                    s_key = is_down(0x53)
                    ctrl_shift_s = ctrl and shift and s_key

                    if (self.is_speaking and esc) or pause or ctrl_shift_s:
                        if self.is_speaking:
                            print("\n🛑 [HOTKEY INTERRUPT] Stop hotkey pressed! Halting speech instantly...")
                            self.stop_requested = True
                            try:
                                mixer.music.stop()
                            except Exception:
                                pass
                            self.is_speaking = False
                            time.sleep(0.3)
                except Exception as e:
                    print(f"[Hotkey Poller Error]: {e}")
                time.sleep(0.015)

        t = threading.Thread(target=poller_loop, daemon=True)
        t.start()

    # -----------------------------------------------------
    # SPEECH SYNTHESIS & PLAYBACK (IN-MEMORY CONTROLLER)
    # -----------------------------------------------------
    def speak(self, persona, text):
        """Synthesize text via Edge-TTS and play audio while enforcing mic pause and instant cancellation."""
        if not text or not text.strip():
            return

        self.stop_requested = False
        self.is_speaking = True
        self.broadcast_ws({"type": "speaking", "text": text, "persona": persona})
        self.log_to_transcript(persona, text)

        voice = VOICE_MAP.get(persona.lower(), VOICE_MAP["default"])

        # Create temporary audio file
        tmp_fd, tmp_path = tempfile.mkstemp(suffix=".mp3")
        os.close(tmp_fd)

        try:
            # Generate Edge-TTS audio file synchronously
            async def _gen():
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(tmp_path)

            asyncio.run(_gen())

            if self.stop_requested:
                print("[Speech] Cancelled before playback started.")
                return

            # Play audio file via Pygame Mixer
            mixer.music.load(tmp_path)
            mixer.music.play()

            # Monitor playback until finished or interrupted
            while mixer.music.get_busy():
                if self.stop_requested:
                    mixer.music.stop()
                    print("[Speech] Interrupted during playback.")
                    break
                time.sleep(0.02)

        except Exception as err:
            print(f"[Speech Generation/Playback Error]: {err}")
        finally:
            self.is_speaking = False
            self.broadcast_ws({"type": "speech_ended", "persona": persona})
            try:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except OSError:
                pass

    def log_to_transcript(self, persona, text):
        user_profile = os.environ.get("USERPROFILE", "")
        pattern = os.path.join(user_profile, ".gemini", "antigravity*", "brain", "*", ".system_generated", "logs", "transcript.jsonl")
    def log_to_transcript(self, persona, text):
        user_profile = os.environ.get("USERPROFILE", "")
        pattern = os.path.join(user_profile, ".gemini", "antigravity*", "brain", "*", ".system_generated", "logs", "transcript.jsonl")
        files = glob.glob(pattern)
        if files:
            files.sort(key=os.path.getmtime, reverse=True)
            latest_file = files[0]
            entry = {
                "step_index": int(time.time()),
                "source": "MODEL",
                "type": "PLANNER_RESPONSE",
                "status": "DONE",
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "content": f"<!-- VOICE ({self.active_speaker.upper()}): {persona} -->\n{text}"
            }
            try:
                with open(latest_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(entry) + "\n")
            except Exception:
                pass

        if self.active_speaker == "candy":
            candy_mem = os.path.join(SCRIPT_DIR, "memory", "active", "candy_session_memory.md")
            try:
                timestamp = time.strftime("%Y-%m-%d %H:%M", time.localtime())
                with open(candy_mem, "a", encoding="utf-8") as cm:
                    cm.write(f"\n- **{timestamp}** ({persona.upper()}): {text}")
            except Exception:
                pass

    # -----------------------------------------------------
    # OPENROUTER LLM QUERY
    # -----------------------------------------------------
    def query_openrouter(self, persona, prompt):
        api_key = None
        env_path = os.path.join(SCRIPT_DIR, ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("OPENROUTER_API_KEY="):
                        api_key = line.strip().split("=", 1)[1].strip()

        if not api_key:
            api_key = os.environ.get("OPENROUTER_API_KEY")

        if not api_key or api_key == "YOUR_OPENROUTER_KEY_HERE":
            return "I hear you! Please add your OPENROUTER_API_KEY to the .env file."

        protocol_path = os.path.join(SCRIPT_DIR, ".agent", "rules", f"{persona}.md")
        protocol = ""
        try:
            with open(protocol_path, "r", encoding="utf-8") as pf:
                protocol = pf.read()
        except OSError:
            pass

        protocol_section = protocol[:2000] if protocol else "No protocol file found."
        
        if self.active_speaker == "candy":
            speaker_instr = "CURRENT SPEAKER: CANDY (Joe's wife).\nAddress her warmly and respectfully as Candy or Ma'am. Do NOT call her Joe."
        else:
            speaker_instr = "CURRENT SPEAKER: JOE MOULTON (Founder).\nAddress him as Joe or Sir."

        system_prompt = f"""You are the {persona.upper()} persona speaking directly by voice.
{speaker_instr}

Speak naturally, concisely (2-3 sentences max), and stay strictly in character. Do not include markdown codeblocks or quotes.

Governing Protocol Summary:
{protocol_section}"""

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://radicalsimplicity.ai",
            "X-Title": "Antigravity AI OS"
        }

        for model_name in ["meta-llama/llama-3.1-8b-instruct", "openai/gpt-4o-mini", "deepseek/deepseek-chat"]:
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 80
            }
            try:
                res = requests.post(url, headers=headers, json=payload, timeout=4)
                if res.status_code == 200:
                    return res.json()["choices"][0]["message"]["content"].strip()
            except Exception as e:
                print(f"[LLM Query Warning] {model_name} failed: {e}")

        return "I am right here, Sir. How can I assist you?"

    # -----------------------------------------------------
    # TEXT NORMALIZATION & PERSONA SWITCHING
    # -----------------------------------------------------
    def normalize_text(self, text):
        normalized = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
        ax_rewrites = [
            r"(?:play|plate|played|plae) (?:x|ax|axe|ex|acts)",
            r"(?:hey|hay|he|hei|a) (?:ax|axe|x|ex|acts|ask|ox|aks|acc|axi|axle|8)",
            r"(?:hey|hay) (?:ax|axe)\b",
        ]
        for pattern in ax_rewrites:
            if re.fullmatch(pattern, normalized):
                return "hey ax"
        ax_singles = {"ask", "ox", "aks", "axle", "axi", "acc", "acs", "8", "axe", "acts", "hacks"}
        if normalized in ax_singles:
            return "ax"
        return text

    def detect_persona(self, text):
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

    def extract_prompt_after_trigger(self, text, persona):
        text_lower = text.lower().strip()
        words_to_strip = [
            "hey ax", "hey x", "hacks", "alexa", "hey acts", "acts", "hey ex", "hey axe", "axe",
            "bring up", "switch to", "talk to", "can you", "please", "i want to talk to", "counsel with"
        ]
        triggers = PERSONA_TRIGGERS.get(persona, []) + [persona, persona.replace("_", " ")]
        aliases = PERSONA_ALIASES.get(persona, [])
        words_to_strip.extend(triggers)
        words_to_strip.extend(aliases)
        for a in aliases:
            words_to_strip.append(f"hey {a}")
            words_to_strip.append(f"bring up {a}")
            words_to_strip.append(f"switch to {a}")

        cleaned = text_lower
        for w in sorted(set(words_to_strip), key=len, reverse=True):
            pattern = r'\b' + re.escape(w) + r'\b'
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)

        cleaned = re.sub(r'^\s*[,.!:-]+\s*', '', cleaned).strip()
        if len(cleaned) >= 4:
            return text.strip()
        return None

    # -----------------------------------------------------
    # CORE INPUT PROCESSOR
    # -----------------------------------------------------
    def handle_incoming_text(self, raw_text):
        if self.is_speaking:
            # Self-echo protection: ignore incoming text while speaking
            return

        try:
            text = self.normalize_text(raw_text)
            text_lower = text.lower()
            print(f"\n[Heard]: '{raw_text}'" + (f" -> normalized: '{text}'" if text != raw_text else ""))

            # Speaker identity detection
            candy_triggers = ["this is candy", "i'm candy", "i am candy", "candy speaking", "candy here", "it's candy", "candy joe's wife", "hi this is candy"]
            joe_triggers = ["this is joe", "i'm joe", "i am joe", "joe speaking", "joe here", "it's joe"]

            if any(t in text_lower for t in candy_triggers):
                if self.active_speaker != "candy":
                    self.active_speaker = "candy"
                    print("\n[SPEAKER SWITCH] Active speaker set to Candy (Ma'am)!")
            elif any(t in text_lower for t in joe_triggers):
                if self.active_speaker != "joe":
                    self.active_speaker = "joe"
                    print("\n[SPEAKER SWITCH] Active speaker set to Joe!")

            called_persona = self.detect_persona(text)

            if self.mode == MODE_SLEEP:
                if called_persona or "hey" in text_lower or "ax" in text_lower:
                    self.mode = MODE_ACTIVE
                    self.current_persona = called_persona if called_persona else "ax"
                    self.last_active_time = time.time()
                    print(f"\n[WAKE DETECTED] Switched to ACTIVE mode as '{self.current_persona}'!")
                    self.broadcast_ws({"type": "wake", "persona": self.current_persona})

                    user_prompt = self.extract_prompt_after_trigger(raw_text, self.current_persona)
                    if user_prompt:
                        self.broadcast_ws({"type": "heard", "text": raw_text, "persona": self.current_persona})
                        self.broadcast_ws({"type": "thinking", "persona": self.current_persona})
                        ai_reply = self.query_openrouter(self.current_persona, user_prompt)
                        self.speak(self.current_persona, ai_reply)
                    else:
                        if self.active_speaker == "candy":
                            greeting = f"Hello Candy! {self.current_persona.capitalize()} here. How can I assist you today, Ma'am?"
                        else:
                            greeting = PERSONA_GREETINGS.get(self.current_persona, f"{self.current_persona.capitalize()} here!")
                        self.speak(self.current_persona, greeting)

            elif self.mode == MODE_ACTIVE:
                self.last_active_time = time.time()

                if any(w in text_lower for w in ["go to sleep", "sleep mode", "stand down", "stop listening"]):
                    self.mode = MODE_SLEEP
                    print("[SLEEP COMMAND] Returning to SLEEP mode.")
                    self.broadcast_ws({"type": "sleep"})
                    goodbye = "Standing by, Ma'am." if self.active_speaker == "candy" else "Standing by, Sir."
                    self.speak("jarvis", goodbye)

                elif called_persona and called_persona != self.current_persona:
                    self.current_persona = called_persona
                    print(f"\n[PERSONA SWITCH] Handing over to '{self.current_persona}'!")
                    self.broadcast_ws({"type": "persona_switch", "persona": self.current_persona})
                    user_prompt = self.extract_prompt_after_trigger(raw_text, self.current_persona)
                    if user_prompt:
                        self.broadcast_ws({"type": "heard", "text": raw_text, "persona": self.current_persona})
                        self.broadcast_ws({"type": "thinking", "persona": self.current_persona})
                        ai_reply = self.query_openrouter(self.current_persona, user_prompt)
                        self.speak(self.current_persona, ai_reply)
                    else:
                        if self.active_speaker == "candy":
                            greeting = f"Hello Candy! {self.current_persona.capitalize()} here. How can I assist you today, Ma'am?"
                        else:
                            greeting = PERSONA_GREETINGS.get(self.current_persona, f"{self.current_persona.capitalize()} here!")
                        self.speak(self.current_persona, greeting)

                else:
                    self.broadcast_ws({"type": "heard", "text": raw_text, "persona": self.current_persona})
                    self.broadcast_ws({"type": "thinking", "persona": self.current_persona})
                    print(f"\n[THINKING as {self.current_persona}]...")
                    ai_reply = self.query_openrouter(self.current_persona, raw_text)
                    self.speak(self.current_persona, ai_reply)
        except Exception as err:
            print(f"[Input Processing Exception]: {err}")

    # -----------------------------------------------------
    # MAIN MICROPHONE LISTENING LOOP
    # -----------------------------------------------------
    def start_listening_loop(self):
        # Find best webcam / microphone
        try:
            names = sr.Microphone.list_microphone_names()
            print("\n[Audio System] Enumerating Microphones:")
            for idx, name in enumerate(names):
                print(f"  [{idx}] {name}")
                nl = name.lower()
                if self.active_mic_index is None and ("webcam" in nl or "c920" in nl or "conexant" in nl or "microphone" in nl):
                    if "mapper" not in nl and "output" not in nl and "loopback" not in nl:
                        self.active_mic_index = idx
            if self.active_mic_index is not None:
                print(f"[Audio System] Selected Microphone Index [{self.active_mic_index}]: {names[self.active_mic_index]}")
        except Exception as e:
            print(f"[Audio System Error]: {e}")

        recognizer = sr.Recognizer()

        # Initial mic calibration with high-sensitivity static threshold
        print("\nCalibrating microphone for room background noise...")
        with sr.Microphone(device_index=self.active_mic_index) as source:
            recognizer.adjust_for_ambient_noise(source, duration=1.0)
            # Force high-sensitivity energy threshold (60.0) so conversational speech is always caught
            self.energy_threshold = 60.0
            recognizer.energy_threshold = self.energy_threshold
            recognizer.dynamic_energy_threshold = False
            recognizer.pause_threshold = 0.75
            recognizer.non_speaking_duration = 0.35
            print(f"Mic Calibrated! High-sensitivity threshold set to: {self.energy_threshold:.1f}\n")

        print("=========================================================")
        print("  Antigravity Unified Voice Engine Online")
        print("=========================================================")
        print("  Booting up in SLEEP mode.")
        print("  Say 'Hey Ax' or any persona name to wake up.")
        print("  Hotkeys: Press 'Esc' during speech or 'Pause' anytime to interrupt.")
        print("=========================================================\n")

        with sr.Microphone(device_index=self.active_mic_index) as source:
            while True:
                # 1. Idle timeout check
                if self.mode == MODE_ACTIVE and (time.time() - self.last_active_time > TIMEOUT_SECONDS):
                    print("\n[IDLE TIMEOUT] 2 minutes of silence elapsed. Returning to SLEEP mode.")
                    self.mode = MODE_SLEEP
                    self.broadcast_ws({"type": "sleep"})
                    self.speak("jarvis", "Standing by, Sir.")
                    continue

                # 2. Hard Mic Pause during speech playback
                if self.is_speaking:
                    time.sleep(0.1)
                    continue

                # 3. Listen for mic input
                try:
                    mode_str = f"MODE: ACTIVE ({self.current_persona}) | Timeout in {int(TIMEOUT_SECONDS - (time.time() - self.last_active_time))}s" if self.mode == MODE_ACTIVE else "MODE: SLEEP | Listening for 'Hey Ax'..."
                    print(f"[{mode_str}] Listening...", end="\r", flush=True)

                    audio = recognizer.listen(source, timeout=1.5, phrase_time_limit=10.0)

                    # Re-verify is_speaking after listen returns
                    if self.is_speaking:
                        continue

                    try:
                        recognized = recognizer.recognize_google(audio).strip()
                        if recognized:
                            print("\n") # Clear carriage return
                            self.handle_incoming_text(recognized)
                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError as e:
                        print(f"\n[STT Service Error]: {e}")
                        time.sleep(1)

                except sr.WaitTimeoutError:
                    pass
                except Exception as exc:
                    print(f"\n[Listener Loop Error]: {exc}")
                    time.sleep(0.5)

# =========================================================
# MAIN ENTRY POINT
# =========================================================
if __name__ == "__main__":
    engine = VoiceEngine()
    engine.start_websocket_server()
    engine.start_hotkey_poller()
    engine.start_listening_loop()
