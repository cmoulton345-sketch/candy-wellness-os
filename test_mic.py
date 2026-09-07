import sys
try:
    import pyaudio
except ImportError:
    import pyaudiowpatch as pyaudio
    sys.modules['pyaudio'] = pyaudio

import speech_recognition as sr
import time

print("=========================================")
print("     Microphone Energy & Speech Test     ")
print("=========================================")

r = sr.Recognizer()

with sr.Microphone() as source:
    print("\n1. Calibrating for ambient room noise... Please remain quiet for 1 second.")
    r.adjust_for_ambient_noise(source, duration=1.0)
    print(f"-> Calibrated Ambient Energy Threshold: {r.energy_threshold:.2f}")

    print("\n2. Now speak out loud (e.g. say 'Hey Ax')...")
    try:
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        print("-> Audio captured! Transcribing with Google...")
        text = r.recognize_google(audio)
        print(f"\nSUCCESS! Heard: '{text}'")
    except sr.WaitTimeoutError:
        print("\n[X] Timeout: No speech detected above energy threshold.")
    except sr.UnknownValueError:
        print("\n[X] Speech was captured but could not be understood.")
    except Exception as e:
        print(f"\n[X] Error: {e}")
