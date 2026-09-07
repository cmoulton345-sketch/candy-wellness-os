import os
import glob
import re
import json
import time
import asyncio
import edge_tts
import tempfile
import sys
import threading
import ctypes
from ctypes import wintypes
import signal

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VOICE_QUEUE_FILE = os.path.join(SCRIPT_DIR, "voice_queue.jsonl")
PLAYBACK_STOP_EVENT = threading.Event()

def request_stop(reason="stop signal"):
    """Request playback cancellation from any thread or process."""
    PLAYBACK_STOP_EVENT.set()
    stop_flag = os.path.join(SCRIPT_DIR, "stop.flag")
    try:
        with open(stop_flag, "w") as sf:
            sf.write(reason)
    except OSError:
        pass

# Single-Instance Enforcement using Windows Named Mutex (atomic, no race condition)
def enforce_single_instance():
    """Uses a Windows named mutex to guarantee only one speak.py runs at a time."""
    kernel32 = ctypes.windll.kernel32
    # Local session namespace avoids privilege requirements while protecting user session
    mutex_name = "AntigravitySpeakPyMutex"
    handle = kernel32.CreateMutexW(None, True, mutex_name)
    last_error = kernel32.GetLastError()
    ERROR_ALREADY_EXISTS = 183
    ERROR_ACCESS_DENIED = 5
    if handle == 0 or last_error in (ERROR_ALREADY_EXISTS, ERROR_ACCESS_DENIED):
        print("[speak.py] Another instance is already running. Exiting.")
        sys.exit(0)

    # Create .speak_active lockfile for listen.py verification
    active_flag = os.path.join(SCRIPT_DIR, ".speak_active")
    try:
        with open(active_flag, "w") as f:
            f.write(str(os.getpid()))
    except OSError:
        pass

    # Keep handle alive for the lifetime of the process (prevents GC from releasing it)
    return handle

_mutex_handle = None
if __name__ == "__main__":
    _mutex_handle = enforce_single_instance()

# Clean up .speak_active on exit
def _cleanup_active_flag():
    active_flag = os.path.join(SCRIPT_DIR, ".speak_active")
    try:
        if os.path.exists(active_flag):
            os.remove(active_flag)
    except OSError:
        pass

import atexit
atexit.register(_cleanup_active_flag)

# Configure Pygame Mixer for high quality audio playback
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
mixer.init(frequency=48000, buffer=1024)

# Continuous hardware hotkey poller (20ms polling interval)
def hardware_hotkey_poller():
    """Stop speech from either Escape during playback or Pause at any time."""
    user32 = ctypes.windll.user32
    user32.GetAsyncKeyState.restype = wintypes.SHORT
    user32.GetAsyncKeyState.argtypes = [ctypes.c_int]

    def is_down(vk):
        try:
            return bool(user32.GetAsyncKeyState(vk) & 0x8000)
        except Exception:
            return False

    while True:
        try:
            speaking_flag = os.path.join(SCRIPT_DIR, ".speaking")
            is_speaking = mixer.music.get_busy() or os.path.exists(speaking_flag)

            esc = is_down(0x1B)        # Escape
            pause = is_down(0x13)      # Pause / Break

            if (is_speaking and esc) or pause:
                print("\n[Hotkey Engine] Stop hotkey detected (Esc/Pause). Interrupting speech...")
                request_stop("hardware hotkey")
                try:
                    mixer.music.stop()
                except Exception:
                    pass
        except Exception as err:
            print(f"[Hotkey Poller Error]: {err}")
        time.sleep(0.02)

# Voice Mapping — ALL 30 PERSONAS from router.yaml
# Each persona is mapped to a distinct Microsoft Edge Neural voice
# matched to their personality and role.
VOICE_MAP = {
    # === DEFAULT / FALLBACK ===
    "default": "en-US-ChristopherNeural",

    # === CORE COMMAND (Deep, authoritative male voices) ===
    "ax":                    "en-US-ChristopherNeural",  # Lead Architect — deep, steady, authoritative
    "closer":                "en-US-AndrewNeural",       # Deal Architect / Closer — calm, commercial authority
    "jarvis":                "en-GB-RyanNeural",         # Local OS Controller — British, professional butler
    "pen":                   "en-US-EmmaNeural",         # Copy and content strategist
    "steward":              "en-GB-RyanNeural",         # Client delivery and retention
    "strategist":           "en-US-AndrewNeural",       # Positioning and strategic direction
    "warden":               "en-US-SteffanNeural",       # Governance and system audit
    "atlas":                 "en-US-SteffanNeural",      # Chief Marketing Officer — commanding, strategic
    "keller":                "en-US-AndrewNeural",       # Executive Business Coach — warm, focused mentor

    # === SALES & COPY (Energetic, persuasive voices) ===
    "uncle_g":               "en-US-RogerNeural",        # 10X Sales Coach — raspy, urban grit, high-energy
    "brunsen_2_0":           "en-US-BrianNeural",        # Direct Response Architect — persuasive pitch
    "voss":                  "en-US-ChristopherNeural",  # B2B Systems Architect & Deal Closer — authoritative, empathetic
    "chairman":              "en-US-RogerNeural",        # GOATed Ads Architect — bold, production-driven
    "collect":               "en-US-EricNeural",         # Client Intake Specialist — calm, methodical
    "jeeves":                "en-GB-RyanNeural",         # Client Delivery Orchestrator — immaculate British valet

    # === STRATEGIC / WISDOM (Measured, thoughtful voices) ===
    "navigator":             "en-US-BrianMultilingualNeural",  # Polymath Synthesizer — articulate, precise
    "elder":                 "en-GB-ThomasNeural",       # Modern Mystic — wise, contemplative, deep British baritone
    "psyche":                "en-US-MichelleNeural",     # Human Behavior OS — warm, empathetic female
    "clarity":               "en-US-EmmaNeural",         # Intuitive Insight Facilitator — clear, calming female
    "socrates":              "en-US-AndrewMultilingualNeural",  # Legal Shadow — measured, precise, articulate

    # === EXECUTION / TECHNICAL (Clear, efficient voices) ===
    "nate":                  "en-US-EricNeural",         # n8n Workflow Architect — technical, efficient
    "web_builder":           "en-CA-LiamNeural",         # Full-Stack Builder — Canadian, crisp
    "webbuilder":            "en-CA-LiamNeural",         # Alias for web_builder
    "information_architect": "en-NZ-MitchellNeural",     # Workspace Designer — distinct, organized
    "skeptical_researcher":  "en-AU-WilliamMultilingualNeural",  # Deep Researcher — Australian, analytical
    "researcher":            "en-AU-WilliamMultilingualNeural",  # Alias for skeptical_researcher

    # === SPECIALIST DOMAIN (Unique accent voices for character) ===
    "distiller":             "en-IE-ConnorNeural",       # Master Distiller — Irish, rugged character
    "foreman":               "en-US-SteffanNeural",      # General Contractor — deep, rough, grumpy
    "crypto":                "en-US-RogerNeural",        # Crypto Trading Architect — sharp, fast
    "sentry":                "en-GB-RyanNeural",         # EH&S Safety Shadow — British, authoritative
    "envoy":                 "en-ZA-LukeNeural",         # Cultural & Foreign Affairs — South African accent
    "earl":                  "en-CA-LiamNeural",         # Goals Coach — warm, encouraging Canadian

    # === LIFESTYLE & PERSONAL (Warm, approachable voices) ===
    "bliss":                 "en-US-EmmaMultilingualNeural",  # Intimacy Coach — whispery, sultry, dreamy
    "soma":                  "en-US-AvaNeural",          # Diet & Physical Optimization — soft, calming female
    "studio":                "en-US-JennyNeural",        # Persona (unlisted in router but active) — bright female
    "wave":                  "en-US-RogerNeural",        # Vibroacoustic & Frequency Architect — smooth, resonant male

    # === LIGHTWEIGHT / UTILITY ===
    "consistency":           "en-GB-SoniaNeural",        # Copy Editor — precise, British female
    "stephen_universal":     "en-US-BrianNeural",        # Polymath Synthesizer (lightweight) — versatile
    "stephen":               "en-US-BrianNeural",        # Alias for stephen_universal

    # === LEGACY ALIASES (so old VOICE tags still work) ===
    "brian":                 "en-US-ChristopherNeural",  # Legacy alias for Ax
    "uncle g":               "en-US-GuyNeural",          # Space-separated alias
    "brunsen":               "en-US-BrianNeural",        # Alias for brunsen_2_0
    "the elder":             "en-GB-ThomasNeural",       # Alias for elder
    "jeeves":                "en-GB-ThomasNeural",       # Alias (same wise British voice)
    "george":                "en-AU-WilliamMultilingualNeural",  # Legacy alias
    "voss":                  "en-US-AndrewNeural",       # Voss — calm, negotiation-style
}

# Per-Persona Voice Tuning (pitch, rate, volume)
# pitch: "-10Hz" to "+10Hz" or "-10%" to "+10%" (negative = deeper)
# rate:  "-50%" to "+100%" (negative = slower, positive = faster)
# volume: "silent", "x-soft", "soft", "medium", "loud", "x-loud" or "+0%" to "+100%"
VOICE_TUNING = {
    "default":      {"pitch": "+0Hz",  "rate": "-5%",  "volume": "+0%"},
    "ax":           {"pitch": "-4Hz",  "rate": "-3%",  "volume": "+0%"},
    "jarvis":       {"pitch": "+0Hz",  "rate": "-4%",  "volume": "+0%"},
    "atlas":        {"pitch": "+0Hz",  "rate": "-3%",  "volume": "+0%"},
    "keller":       {"pitch": "+0Hz",  "rate": "-4%",  "volume": "+0%"},
    "uncle_g":      {"pitch": "-8Hz",  "rate": "+2%",  "volume": "+0%"},
    "brunsen_2_0":  {"pitch": "+0Hz",  "rate": "-3%",  "volume": "+0%"},
    "chairman":     {"pitch": "+0Hz",  "rate": "-2%",  "volume": "+0%"},
    "collect":      {"pitch": "+0Hz",  "rate": "-4%",  "volume": "+0%"},
    "navigator":    {"pitch": "+0Hz",  "rate": "-3%",  "volume": "+0%"},
    "elder":        {"pitch": "-8Hz",  "rate": "-8%",  "volume": "-5%"},
    "psyche":       {"pitch": "+0Hz",  "rate": "-4%",  "volume": "+0%"},
    "clarity":      {"pitch": "+0Hz",  "rate": "-4%",  "volume": "+0%"},
    "socrates":     {"pitch": "+0Hz",  "rate": "-3%",  "volume": "+0%"},
    "nate":          {"pitch": "+0Hz",  "rate": "-3%",  "volume": "+0%"},
    "web_builder":  {"pitch": "+0Hz",  "rate": "-3%",  "volume": "+0%"},
    "information_architect": {"pitch": "+0Hz", "rate": "-3%", "volume": "+0%"},
    "skeptical_researcher":  {"pitch": "+0Hz", "rate": "-4%", "volume": "+0%"},
    "distiller":    {"pitch": "+0Hz",  "rate": "-3%",  "volume": "+0%"},
    "foreman":      {"pitch": "-6Hz",  "rate": "-2%",  "volume": "+0%"},
    "crypto":       {"pitch": "+0Hz",  "rate": "-1%",  "volume": "+0%"},
    "sentry":       {"pitch": "+0Hz",  "rate": "-3%",  "volume": "+0%"},
    "envoy":        {"pitch": "+0Hz",  "rate": "-3%",  "volume": "+0%"},
    "earl":         {"pitch": "+0Hz",  "rate": "-4%",  "volume": "+0%"},
    "bliss":        {"pitch": "-8Hz",  "rate": "-25%", "volume": "+0%"},
    "soma":         {"pitch": "-6Hz",  "rate": "-10%", "volume": "-20%"},
    "studio":       {"pitch": "+0Hz",  "rate": "+0%",  "volume": "+0%"},
    "wave":         {"pitch": "-4Hz",  "rate": "-5%",  "volume": "+0%"},
    "consistency":  {"pitch": "+0Hz",  "rate": "+0%",  "volume": "+0%"},
    "stephen_universal": {"pitch": "+0Hz", "rate": "+0%", "volume": "+0%"},
    "voss":         {"pitch": "+0Hz",  "rate": "+0%",  "volume": "+0%"},
}

async def generate_and_play(text, voice, tuning=None):
    """Generates speech using Edge TTS and plays it using Pygame."""
    print(f"[Edge TTS] Generating audio for voice '{voice}'...")
    """Generates MP3 audio using Edge TTS and plays it using pygame mixer."""
    stop_flag = os.path.join(os.path.dirname(__file__), "stop.flag")

    # Check if stop signal was already triggered before doing work
    if PLAYBACK_STOP_EVENT.is_set() or os.path.exists(stop_flag):
        print("[Edge TTS] Speech cancelled before generation.")
        return

    # Create a temporary file to store the audio
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        temp_path = temp_file.name

    try:
        # Generate audio via Edge TTS with prosody tuning
        rate = tuning.get('rate', '+0%') if tuning else '+0%'
        pitch = tuning.get('pitch', '+0Hz') if tuning else '+0Hz'
        volume = tuning.get('volume', '+0%') if tuning else '+0%'
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, volume=volume)
        await communicate.save(temp_path)

        # Re-check stop event after TTS generation completes (in case user pressed hotkey while downloading MP3)
        if PLAYBACK_STOP_EVENT.is_set() or os.path.exists(stop_flag):
            print("[Edge TTS] Speech cancelled immediately after generation.")
            try:
                os.remove(temp_path)
            except OSError:
                pass
            return

        # Create .speaking flag so listen.py pauses mic during playback
        speaking_flag = os.path.join(os.path.dirname(__file__), ".speaking")
        try:
            with open(speaking_flag, "w") as f:
                f.write("1")
        except Exception:
            pass

        # Play the audio
        mixer.music.load(temp_path)
        mixer.music.play()

        # Wait for audio to finish (or interrupt on hotkey / stop signal / user input)
        latest_t = get_active_transcript()
        last_t_len = 0
        if latest_t and os.path.exists(latest_t):
            try:
                with open(latest_t, "r", encoding="utf-8", errors="ignore") as tf:
                    last_t_len = len(tf.readlines())
            except Exception:
                pass

        while mixer.music.get_busy():
            if PLAYBACK_STOP_EVENT.is_set() or os.path.exists(stop_flag):
                mixer.music.stop()
                print("\n[Edge TTS] ⏹️ Playback interrupted!")
                break

            # Check for new User input in transcript during playback
            if latest_t and os.path.exists(latest_t):
                try:
                    with open(latest_t, "r", encoding="utf-8", errors="ignore") as tf:
                        curr_lines = tf.readlines()
                        if len(curr_lines) > last_t_len:
                            for nl in curr_lines[last_t_len:]:
                                try:
                                    t_data = json.loads(nl)
                                    if t_data.get("source") in ["USER_EXPLICIT", "USER_INPUT"]:
                                        request_stop("user input")
                                        mixer.music.stop()
                                        print("\n[Edge TTS] ⏹️ New user input detected! Stopping audio...")
                                        break
                                except Exception:
                                    pass
                            last_t_len = len(curr_lines)
                except Exception:
                    pass

            time.sleep(0.02)

    except Exception as e:
        print(f"[TTS Error]: {e}")
    finally:
        # Clean up
        mixer.music.unload()
        try:
            os.remove(temp_path)
        except OSError:
            pass
        try:
            speaking_flag = os.path.join(os.path.dirname(__file__), ".speaking")
            if os.path.exists(speaking_flag):
                os.remove(speaking_flag)
        except OSError:
            pass

def get_active_transcript():
    """Finds the active transcript.jsonl file with the newest modification time."""
    user_profile = os.environ.get("USERPROFILE", "")
    pattern = os.path.join(user_profile, ".gemini", "antigravity*", "brain", "*", ".system_generated", "logs", "transcript.jsonl")
    files = glob.glob(pattern)
    if not files:
        return None
    files.sort(key=lambda f: os.path.getmtime(f) if os.path.exists(f) else 0, reverse=True)
    return files[0]

def get_voice_queue():
    """Return the listener-owned queue used for voice playback only."""
    return VOICE_QUEUE_FILE

def clean_speech_text(text):
    """Aggressively strips code blocks, inline code, tool calls, JSON, file paths, URLs, and HTML tags for natural speech output."""
    if not text:
        return ""

    clean = text

    # Remove HTML comments and tags
    clean = re.sub(r"<!--.*?-->", "", clean, flags=re.DOTALL)
    clean = re.sub(r"<[^>]+>", "", clean)

    # Remove multi-line code blocks entirely
    clean = re.sub(r"```.*?```", "", clean, flags=re.DOTALL)

    # Remove inline code snippets (`...`)
    clean = re.sub(r"`[^`]*`", "", clean)

    # Remove file paths (Windows, Unix, file://)
    clean = re.sub(r"[A-Za-z]:\\[^\s,)\"']+", "", clean)
    clean = re.sub(r"file:///[^\s,)\"']+", "", clean)

    # Remove URLs
    clean = re.sub(r"https?://[^\s,)\"']+", "", clean)

    # Remove markdown links (keep link text only)
    clean = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", clean)

    # Remove pipe table formatting
    clean = re.sub(r"\|[^\n]*\|", "", clean)

    # Remove markdown formatting symbols (*, _, ~, #, >)
    clean = re.sub(r"[*_~#>]", "", clean)

    # Remove list bullets and numbered list markers
    clean = re.sub(r"^\s*[-•*]\s*", " ", clean, flags=re.MULTILINE)
    clean = re.sub(r"^\s*\d+\.\s*", " ", clean, flags=re.MULTILINE)

    # Remove raw JSON object payloads like {"key": "val"}
    clean = re.sub(r"\{[^{}]*\}", "", clean)

    # Remove non-BMP emoji characters that crash Windows CP1252 console
    clean = re.sub(r"[\U00010000-\U0010ffff]", "", clean)

    # Collapse extra whitespace
    clean = re.sub(r"\s+", " ", clean).strip()

    return clean

def extract_voice_blocks(content, last_user_text=""):
    """
    Parses content into (persona_name, text) blocks.
    Guarantees that a single response is spoken in a single persona voice
    without fragmenting pre-tag text into the default voice.
    """
    tags = re.findall(r"<!--\s*VOICE:\s*(.*?)\s*-->", content, flags=re.IGNORECASE)

    if len(tags) == 1:
        # Single persona tag present -> apply to the ENTIRE message text
        persona = tags[0].strip().lower()
        clean_text = re.sub(r"<!--\s*VOICE:\s*.*?\s*-->", "", content, flags=re.IGNORECASE)
        return [(persona, clean_text)]

    elif len(tags) > 1:
        # Multiple explicit voice tags -> switch between them sequentially
        voice_blocks = []
        parts = re.split(r"<!--\s*VOICE:\s*(.*?)\s*-->", content, flags=re.IGNORECASE)
        first_persona = tags[0].strip().lower()
        if parts[0].strip():
            voice_blocks.append((first_persona, parts[0]))
        for i in range(1, len(parts), 2):
            persona_name = parts[i].strip().lower()
            block_text = parts[i+1] if (i+1) < len(parts) else ""
            if block_text.strip():
                voice_blocks.append((persona_name, block_text))
        return voice_blocks

    else:
        # No VOICE tag present -> detect persona from user prompt or response content
        detected_persona = "ax"  # Default persona
        check_str = (last_user_text + " " + content[:120]).lower()
        for persona_key in VOICE_MAP.keys():
            if persona_key in ["default", "webbuilder", "researcher"]:
                continue
            if re.search(r"\b" + re.escape(persona_key) + r"\b", check_str):
                detected_persona = persona_key
                break
        return [(detected_persona, content)]

def process_transcript():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=========================================")
    print("   Antigravity Free Voice Engine (Edge)")
    print("=========================================")
    print("Monitoring chat transcript for responses...")
    print("=========================================")

    current_log = None
    last_line_count = 0
    last_user_prompt = ""
    speech_suppressed = False

    while True:
        latest = get_voice_queue()
        if latest:
            if current_log != latest:
                if current_log is None:
                    # Initial boot -> skip old transcript history
                    current_log = latest
                    print(f"[Edge TTS] Active Log File: {current_log}")
                    if os.path.exists(current_log):
                        with open(current_log, "r", encoding="utf-8", errors="ignore") as f:
                            last_line_count = len(f.readlines())
                        speech_suppressed = False
                else:
                    # Active log file updated -> switch without discarding new lines
                    current_log = latest
                    print(f"[Edge TTS] Switched Active Log File: {current_log}")
                    last_line_count = 0
                    speech_suppressed = False

            if os.path.exists(current_log):
                with open(current_log, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()

                if len(lines) > last_line_count:
                    new_lines = lines[last_line_count:]
                    last_line_count = len(lines)

                    for line in new_lines:
                            try:
                                data = json.loads(line)
                                # Track last user prompt text
                                if data.get("source") in ["USER_EXPLICIT", "USER_INPUT"]:
                                    user_text = ""
                                    content_obj = data.get("content", "")
                                    if isinstance(content_obj, str):
                                        user_text = content_obj.lower()
                                    elif isinstance(content_obj, list):
                                        for part in content_obj:
                                            if isinstance(part, dict) and part.get("type") == "text":
                                                user_text += part.get("text", "").lower()
                                    last_user_prompt = user_text

                                    STOP_WORDS = ["stop", "quiet", "shh", "shut up", "hush", "silence", "stfu"]
                                    if any(w in user_text for w in STOP_WORDS):
                                        print("\n[Edge TTS] ⏹️ Stop command detected from user! Silencing audio...")
                                        mixer.music.stop()
                                        speech_suppressed = True
                                        try:
                                            stop_flag = os.path.join(os.path.dirname(__file__), "stop.flag")
                                            with open(stop_flag, "w") as sf:
                                                sf.write("1")
                                        except Exception:
                                            pass
                                        continue
                                    else:
                                        # New user prompt received -> reset speech suppression & stop flags
                                        speech_suppressed = False
                                        PLAYBACK_STOP_EVENT.clear()
                                        stop_flag = os.path.join(os.path.dirname(__file__), "stop.flag")
                                        if os.path.exists(stop_flag):
                                            try:
                                                os.remove(stop_flag)
                                            except OSError:
                                                pass

                                if data.get("source") == "MODEL" and data.get("type") == "PLANNER_RESPONSE":
                                    # SKIP TOOL CALL LINES ENTIRELY (prevents reading code/tool args out loud)
                                    if data.get("tool_calls"):
                                        continue

                                    # If speech was suppressed for this turn, skip model output
                                    if speech_suppressed:
                                        continue

                                    content = data.get("content", "")
                                    # If stop flag exists (written by user stop command), skip model response
                                    stop_flag = os.path.join(os.path.dirname(__file__), "stop.flag")
                                    if os.path.exists(stop_flag):
                                        speech_suppressed = True
                                        try:
                                            os.remove(stop_flag)
                                        except OSError:
                                            pass
                                        continue

                                    # Reset any transient stop event before beginning generation for new turn
                                    PLAYBACK_STOP_EVENT.clear()

                                    if content and not content.startswith("Created At:") and not content.startswith("Tool is running"):
                                        voice_blocks = extract_voice_blocks(content, last_user_prompt)

                                        for persona, block_text in voice_blocks:
                                            # Use mapped voice or fallback to default
                                            edge_voice = VOICE_MAP.get(persona, VOICE_MAP["default"])

                                            # Clean text for speech
                                            clean = clean_speech_text(block_text)

                                            if clean and len(clean) > 3:
                                                try:
                                                    print(f"\n[Edge TTS] Speaking as {persona} ({edge_voice}):")
                                                    print(clean[:80] + "..." if len(clean) > 80 else clean)
                                                except Exception:
                                                    pass
                                                # Get tuning for this persona
                                                tuning = VOICE_TUNING.get(persona, VOICE_TUNING["default"])
                                                # Run the async generation and playback
                                                try:
                                                    asyncio.run(generate_and_play(clean, edge_voice, tuning))
                                                except Exception as exc:
                                                    # Keep monitoring the transcript if one TTS or mixer turn fails.
                                                    print(f"[Edge TTS Error] {persona}: {exc}")

                            except json.JSONDecodeError:
                                pass
                            except Exception as exc:
                                print(f"[Transcript Processing Error]: {exc}")

        time.sleep(0.05)

if __name__ == "__main__":
    threading.Thread(target=hardware_hotkey_poller, daemon=True).start()
    process_transcript()
