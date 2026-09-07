import json
import os
import sys
import time
import threading
import datetime
import random
import requests

# ============================================================
#  EARL — THE GOALS COACH & INNER ARCHITECT
#  Telegram Integration Bot
# ============================================================

def get_env_var(name):
    val = os.environ.get(name, "")
    if val:
        return val
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment")
        val, _ = winreg.QueryValueEx(key, name)
        return val
    except Exception:
        return ""

BOT_TOKEN  = get_env_var("EARL_BOT_TOKEN")
CHAT_ID    = get_env_var("TELEGRAM_CHAT_ID")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# State to avoid sending the same scheduled message twice
last_sent_date = {
    "morning": None,
    "midday": None,
    "evening": None
}

# =============================================================
# CONTENT TEMPLATES
# =============================================================

MORNING_QUOTES = [
    '"We become what we think about." — Earl Nightingale',
    '"Discipline weighs ounces. Regret weighs tons." — Jim Rohn',
    '"Where focus goes, energy flows." — Tony Robbins',
    '"I am that which I am." — Wayne Dyer',
    '"Be here now." — Ram Dass'
]

MIDDAY_QUESTIONS = [
    '"What small discipline am I avoiding today that would change everything?" (Rohn)',
    '"Are you doing right now, or are you being right now?" (Ram Dass)',
    '"What would you do if you knew you could not fail?" (Dyer)',
    '"What is your goal? Can you write it in one sentence?" (Nightingale)',
    '"How would you show up today if you were already the person you want to become?" (Robbins)'
]

def get_morning_message():
    quote = random.choice(MORNING_QUOTES)
    return (
        f"☀️ *EARL — MORNING PRIME*\n\n"
        f"Good morning.\n\n"
        f"_{quote}_\n\n"
        f"🙏 *3 Gratitudes (feel them, don't just list them):*\n"
        f"1. ___\n2. ___\n3. ___\n\n"
        f"📌 *Today's 3 Seeds:*\n"
        f"1. ___\n2. ___\n3. ___\n\n"
        f"🧘 Hand on heart. One breath. 'I am loving awareness.'\n\n"
        f"Now go plant your day. 🌱"
    )

def get_midday_message():
    question = random.choice(MIDDAY_QUESTIONS)
    return (
        f"🔥 *EARL — MIDDAY CHECK*\n\n"
        f"Quick pulse check.\n\n"
        f"How's your state right now?\n"
        f"If it's low, move your body for 60 seconds. Motion creates emotion.\n\n"
        f"💭 *Power Question:*\n"
        f"_{question}_\n\n"
        f"You know the answer. Go do it. ⚡"
    )

def get_evening_message():
    return (
        f"🌙 *EARL — EVENING REFLECT*\n\n"
        f"Good evening.\n\n"
        f"Before you rest, let's harvest today:\n\n"
        f"✅ What worked today? ___\n"
        f"❌ What didn't? ___\n"
        f"📖 What did you learn? ___\n\n"
        f"🙏 *3 things you're grateful for from today:*\n"
        f"1. ___\n2. ___\n3. ___\n\n"
        f"🌱 *Tomorrow's intention:* 'Tomorrow I will ___'\n\n"
        f"'I am loving awareness.' Sleep well. 🕯️"
    )

def get_fire_message():
    return (
        f"🔥 *EARL — PEAK STATE ACTIVATION*\n\n"
        f"Stand up. Breathe rapidly 30 times. Move your body.\n"
        f"Change your physiology right now.\n\n"
        f"What's the story you're telling yourself? Is it empowering or disempowering?\n"
        f"Step into the identity of the person who has already achieved the goal.\n\n"
        f"Take massive action. NOW. 🚀"
    )

def get_stillness_message():
    return (
        f"🧘 *EARL — STILLNESS*\n\n"
        f"Stop.\n\n"
        f"Take a deep breath in. Hold it. Release it slowly.\n\n"
        f"Notice your thoughts. You are not your thoughts. You are the awareness behind them.\n"
        f"Whatever you are attached to right now that is causing you suffering — let it go.\n\n"
        f"You are loving awareness. Be here now. 🌊"
    )

# =============================================================
# TELEGRAM FUNCTIONS
# =============================================================

def send_message(text, keyboard=None):
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    if keyboard:
        payload["reply_markup"] = json.dumps(keyboard)

    try:
        r = requests.post(f"{TELEGRAM_API}/sendMessage", json=payload, timeout=10)
        res = r.json()
        if not res.get("ok"):
            print(f"  [!] Telegram send failed: {res}")
    except Exception as e:
        print(f"  [!] Telegram error: {e}")

# =============================================================
# SCHEDULER
# =============================================================

def check_schedule():
    """Runs continuously in the main thread to send scheduled messages."""
    global last_sent_date
    print("[*] Earl Scheduler running. Waiting for 07:00, 12:00, and 18:00...")
    
    while True:
        now = datetime.datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        
        # 7:00 AM - Morning Prime
        if now.hour == 7 and now.minute == 0:
            if last_sent_date["morning"] != current_date:
                print(f"[{now.strftime('%H:%M:%S')}] Sending Morning Prime...")
                send_message(get_morning_message())
                last_sent_date["morning"] = current_date
                
        # 12:00 PM - Midday Pulse
        elif now.hour == 12 and now.minute == 0:
            if last_sent_date["midday"] != current_date:
                print(f"[{now.strftime('%H:%M:%S')}] Sending Midday Pulse...")
                send_message(get_midday_message())
                last_sent_date["midday"] = current_date
                
        # 6:00 PM (18:00) - Evening Reflect
        elif now.hour == 18 and now.minute == 0:
            if last_sent_date["evening"] != current_date:
                print(f"[{now.strftime('%H:%M:%S')}] Sending Evening Reflect...")
                send_message(get_evening_message())
                last_sent_date["evening"] = current_date

        time.sleep(30) # Check every 30 seconds

# =============================================================
# LISTENER (For Interactive Commands)
# =============================================================

def poll_messages():
    """Poll Telegram for incoming messages and commands."""
    last_update_id = 0
    print("[*] Earl Listener started — listening for commands...")

    # Main keyboard
    main_keyboard = {
        "keyboard": [
            [{"text": "☀️ Morning"}, {"text": "🔥 Pulse"}, {"text": "🌙 Evening"}],
            [{"text": "🚀 Fire Me Up"}, {"text": "🧘 Ground Me"}]
        ],
        "resize_keyboard": True
    }

    while True:
        try:
            r = requests.get(
                f"{TELEGRAM_API}/getUpdates",
                params={"timeout": 30, "offset": last_update_id + 1},
                timeout=40
            )
            data = r.json()
            if not data.get("ok"):
                time.sleep(5)
                continue

            for update in data.get("result", []):
                last_update_id = update["update_id"]
                
                message = update.get("message")
                if not message:
                    continue
                
                text = message.get("text", "").lower()
                print(f"  [MSG] Received: {text}")

                if "/start" in text:
                    send_message(
                        "*EARL IS ONLINE*\n\n"
                        "I am your Goals Coach & Inner Architect.\n"
                        "I will message you automatically at 7 AM, 12 PM, and 6 PM.\n\n"
                        "Use the menu below to summon me at any time.",
                        keyboard=main_keyboard
                    )
                elif "morning" in text:
                    send_message(get_morning_message(), keyboard=main_keyboard)
                elif "pulse" in text or "midday" in text:
                    send_message(get_midday_message(), keyboard=main_keyboard)
                elif "evening" in text or "reflect" in text:
                    send_message(get_evening_message(), keyboard=main_keyboard)
                elif "fire" in text or "energy" in text:
                    send_message(get_fire_message(), keyboard=main_keyboard)
                elif "ground" in text or "stillness" in text or "peace" in text:
                    send_message(get_stillness_message(), keyboard=main_keyboard)

        except Exception as e:
            print(f"  [!] Poll error: {e}")
            time.sleep(10)

# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":
    print("=" * 60)
    print(" EARL — TELEGRAM INTEGRATION BOT")
    print("=" * 60)

    if not BOT_TOKEN or not CHAT_ID:
        print("[!] TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set.")
        print("    Run: $env:TELEGRAM_BOT_TOKEN='your-token'")
        print("    Run: $env:TELEGRAM_CHAT_ID='your-chat-id'")
        sys.exit(1)

    # Send startup notification
    send_message("⚙️ *Earl System Rebooted*\nGoals Coach online and standing by. Type /start for menu.")
    print("[*] Startup notification sent to Telegram")

    # Start listener in background thread
    listener_thread = threading.Thread(target=poll_messages, daemon=True)
    listener_thread.start()

    # Run scheduler in main thread
    check_schedule()
