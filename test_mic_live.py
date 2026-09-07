"""Quick mic diagnostic - listens for 10 seconds and reports what it hears."""
import speech_recognition as sr
import time

try:
    import pyaudio
except ImportError:
    import pyaudiowpatch as pyaudio

recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True  # Let it auto-adjust
recognizer.pause_threshold = 1.2  # Very generous
recognizer.non_speaking_duration = 0.5

# Find the webcam mic
names = sr.Microphone.list_microphone_names()
mic_idx = None
for idx, name in enumerate(names):
    nl = name.lower()
    if ("webcam" in nl or "c920" in nl) and "loopback" not in nl and "output" not in nl and "mapper" not in nl:
        mic_idx = idx
        break

print(f"Using mic index: {mic_idx}")
print(f"Calibrating...")

with sr.Microphone(device_index=mic_idx) as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)
    print(f"Energy threshold after calibration: {recognizer.energy_threshold:.1f}")
    
    for attempt in range(6):
        print(f"\n--- Attempt {attempt+1}/6: SAY SOMETHING (5 sec window) ---")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print(f"  Audio captured! Duration: {len(audio.frame_data) / (audio.sample_rate * audio.sample_width):.2f}s")
            try:
                text = recognizer.recognize_google(audio)
                print(f"  >>> Google heard: '{text}'")
            except sr.UnknownValueError:
                print(f"  >>> Google could NOT understand the audio (UnknownValueError)")
            except sr.RequestError as e:
                print(f"  >>> Google API error: {e}")
        except sr.WaitTimeoutError:
            print(f"  >>> No speech detected (WaitTimeoutError) - threshold too high or mic not picking up")

print("\nDone!")
