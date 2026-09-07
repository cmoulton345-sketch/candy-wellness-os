import re, sys
sys.path.insert(0, '.')
from listen import detect_persona, normalize_recognized_text

test_phrases = [
    "ax", "Ax", "axe", "acts", "hey ax", "hey Ax", "hey axe",
    "x", "X", "ex", "hey ex", "hey x", "hacks", "hey",
    "hey Jarvis", "closer", "hey closer",
    "okay ax", "okay Bob"
]

for phrase in test_phrases:
    text = normalize_recognized_text(phrase)
    persona = detect_persona(text)
    print(f"  '{phrase}' -> normalized: '{text}' -> persona: {persona}")
