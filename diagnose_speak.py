import os, glob, json, ctypes

print("=== SPEAK.PY DIAGNOSTIC ===")
print()

# 1. Check transcript resolution
user_profile = os.environ.get("USERPROFILE", "")
pattern = os.path.join(user_profile, ".gemini", "antigravity*", "brain", "*", ".system_generated", "logs", "transcript.jsonl")
files = glob.glob(pattern)
files.sort(key=lambda f: os.path.getmtime(f) if os.path.exists(f) else 0, reverse=True)
latest = files[0] if files else None
print(f"1. Latest transcript file: {latest}")

if latest:
    with open(latest, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    print(f"   Total lines: {len(lines)}")
    for line in lines[-3:]:
        try:
            data = json.loads(line)
            src = data.get("source", "?")
            typ = data.get("type", "?")
            content = str(data.get("content", ""))[:60]
            print(f"   [{src}] [{typ}] {content}")
        except Exception:
            print("   (parse error)")

# 2. Check if GetAsyncKeyState works from this context
print()
print("2. Testing GetAsyncKeyState accessibility...")
try:
    result = ctypes.windll.user32.GetAsyncKeyState(0x1B)
    print(f"   GetAsyncKeyState(ESC) returned: {result} (0 = key not pressed, expected)")
    print("   GetAsyncKeyState IS accessible from this process context.")
except Exception as e:
    print(f"   GetAsyncKeyState FAILED: {e}")

# 3. Check if edge_tts and pygame work
print()
print("3. Testing edge_tts and pygame imports...")
try:
    import edge_tts
    print(f"   edge_tts: OK")
except ImportError as e:
    print(f"   edge_tts: FAILED - {e}")

try:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    from pygame import mixer
    mixer.init(frequency=48000, buffer=1024)
    print(f"   pygame mixer: OK")
except Exception as e:
    print(f"   pygame mixer: FAILED - {e}")

# 4. Check for orphan speak.py processes
print()
print("4. Current speak.py processes (should be just this diagnostic):")
import subprocess
result = subprocess.run(
    'powershell -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like \'*speak*\' } | Select-Object ProcessId, Name, CommandLine | Format-List"',
    shell=True, capture_output=True, text=True
)
print(result.stdout if result.stdout else "   (none found)")

# 5. Check stop.flag and speak.pid
print()
base = os.path.dirname(__file__)
stop_flag = os.path.join(base, "stop.flag")
pid_file = os.path.join(base, "speak.pid")
print(f"5. stop.flag exists: {os.path.exists(stop_flag)}")
print(f"   speak.pid exists: {os.path.exists(pid_file)}")
if os.path.exists(pid_file):
    with open(pid_file, "r") as f:
        print(f"   speak.pid content: {f.read().strip()}")

print()
print("=== DIAGNOSTIC COMPLETE ===")
