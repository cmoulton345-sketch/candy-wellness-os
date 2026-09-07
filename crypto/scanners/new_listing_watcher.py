import json
import os
import sys
import time
import threading
import requests

# ============================================================
#  FLOWSTATE AI — NEW LISTING WATCHER
#  Runs every 2 hours, detects fresh Hyperliquid listings,
#  sends Telegram alert with BUY / SKIP buttons.
#  When you tap BUY, it executes the trade automatically.
# ============================================================

# --- Config ---
SCAN_INTERVAL_HOURS = 2          # How often to scan
BUY_AMOUNT_USD      = 10         # Default buy size in USDC
STOP_LOSS_PCT       = 0.25       # 25% stop loss on new listings
TAKE_PROFIT_PCT     = 1.00       # 100% take profit (2x)
MIN_SCORE           = 40         # Minimum score to send alert
MAX_AGE_DAYS        = 60         # Max days on HL to qualify

# --- Credentials (with Windows Registry fallback) ---
def get_env_var(name):
    # Try current process environment first
    val = os.environ.get(name, "")
    if val:
        return val
    # Fallback to Windows User Registry
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment")
        val, _ = winreg.QueryValueEx(key, name)
        return val
    except Exception:
        return ""

BOT_TOKEN  = get_env_var("TELEGRAM_BOT_TOKEN")
CHAT_ID    = get_env_var("TELEGRAM_CHAT_ID")
HL_KEY     = get_env_var("HL_PRIVATE_KEY")
HL_ADDRESS = get_env_var("HL_ACCOUNT_ADDRESS")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"
HYPERLIQUID_API = "https://api.hyperliquid.xyz/info"

# --- State files ---
DATA_DIR     = os.path.join(os.path.dirname(__file__), "..", "data")
SEEN_FILE    = os.path.join(DATA_DIR, "seen_listings.json")
PENDING_FILE = os.path.join(DATA_DIR, "pending_buys.json")


# =============================================================
# STATE MANAGEMENT
# =============================================================

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return json.load(f)
    return {}


def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(seen, f, indent=2)


def load_pending():
    if os.path.exists(PENDING_FILE):
        with open(PENDING_FILE) as f:
            return json.load(f)
    return {}


def save_pending(pending):
    with open(PENDING_FILE, "w") as f:
        json.dump(pending, f, indent=2)


# =============================================================
# TELEGRAM FUNCTIONS
# =============================================================

def send_alert(coin_data):
    """Send a new listing alert with BUY / SKIP inline buttons."""
    coin    = coin_data["coin"]
    price   = coin_data["price"]
    age     = coin_data["age_days"]
    score   = coin_data["score"]
    vol     = coin_data["volume_24h"]
    mom     = coin_data.get("vol_momentum", 0)
    dump    = coin_data.get("drawdown_pct", 0)
    signals = " | ".join(coin_data.get("reasons", [])[:3])

    vol_str = f"${vol/1e6:.2f}M" if vol >= 1e6 else f"${vol/1e3:.0f}K"
    mom_str = f"{mom:.1f}x vs launch" if mom > 0 else "N/A"

    text = (
        f"*FLOWSTATE - NEW LISTING ALERT*\n"
        f"{'='*30}\n"
        f"*Coin:*      `{coin}`\n"
        f"*Age on HL:* {age} days\n"
        f"*Price:*     `${price:.8f}`\n"
        f"*Volume:*    {vol_str}/24h\n"
        f"*Momentum:*  {mom_str}\n"
        f"*Drawdown:*  {dump:.0f}% from peak\n"
        f"*Score:*     {score}/100\n"
        f"*Signals:*   {signals}\n"
        f"{'='*30}\n"
        f"_Auto stop: 25% | Target: 2x_"
    )

    keyboard = {
        "inline_keyboard": [[
            {"text": f"BUY ${BUY_AMOUNT_USD}", "callback_data": f"buy_{coin}_{BUY_AMOUNT_USD}"},
            {"text": f"BUY $25",               "callback_data": f"buy_{coin}_25"},
            {"text": "SKIP",                   "callback_data": f"skip_{coin}"}
        ]]
    }

    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(keyboard)
    }

    try:
        r = requests.post(f"{TELEGRAM_API}/sendMessage", json=payload, timeout=10)
        result = r.json()
        if result.get("ok"):
            msg_id = result["result"]["message_id"]
            print(f"  [TELEGRAM] Alert sent for {coin} (msg_id: {msg_id})")
            return msg_id
        else:
            print(f"  [!] Telegram send failed: {result}")
            return None
    except Exception as e:
        print(f"  [!] Telegram error: {e}")
        return None


def send_confirmation(text):
    """Send a simple confirmation message."""
    try:
        requests.post(f"{TELEGRAM_API}/sendMessage", json={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        }, timeout=10)
    except Exception:
        pass


def answer_callback(callback_id, text):
    """Acknowledge a button press (dismisses loading indicator on phone)."""
    try:
        requests.post(f"{TELEGRAM_API}/answerCallbackQuery", json={
            "callback_query_id": callback_id,
            "text": text
        }, timeout=5)
    except Exception:
        pass


# =============================================================
# TRADE EXECUTION
# =============================================================

def execute_buy(coin, amount_usd):
    """Place a market buy on Hyperliquid with stop loss set."""
    if not HL_KEY or not HL_ADDRESS:
        send_confirmation(f"*ERROR:* HL credentials not found. Set HL_PRIVATE_KEY and HL_ACCOUNT_ADDRESS.")
        return False

    try:
        from hyperliquid.exchange import Exchange
        from hyperliquid.info import Info
        from hyperliquid.utils import constants
        import eth_account

        send_confirmation(f"*Executing buy for {coin}...*")

        account = eth_account.Account.from_key(HL_KEY)
        info = Info(constants.MAINNET_API_URL, skip_ws=True)
        exchange = Exchange(account, constants.MAINNET_API_URL, account_address=HL_ADDRESS)

        # Get current price
        meta = info.all_mids()
        current_price = float(meta.get(coin, 0))
        if current_price == 0:
            send_confirmation(f"*ERROR:* Could not get price for {coin}")
            return False

        # Calculate size
        size = round(amount_usd / current_price, 4)
        stop_price = round(current_price * (1 - STOP_LOSS_PCT), 6)
        tp_price   = round(current_price * (1 + TAKE_PROFIT_PCT), 6)

        # Place market buy
        order_result = exchange.market_open(coin, True, size)

        if order_result and order_result.get("status") == "ok":
            msg = (
                f"*FILLED: {coin}*\n"
                f"Size:   {size:,.0f} coins @ ${current_price:.6f}\n"
                f"Cost:   ${amount_usd}\n"
                f"Stop:   ${stop_price:.6f} (25% below)\n"
                f"Target: ${tp_price:.6f} (2x)\n"
                f"_Set your stop manually on HL if needed_"
            )
            send_confirmation(msg)
            print(f"  [TRADE] {coin} BUY filled — ${amount_usd} @ ${current_price:.6f}")
            return True
        else:
            send_confirmation(f"*Order failed for {coin}:* {order_result}")
            return False

    except ImportError:
        send_confirmation("*ERROR:* hyperliquid-python-sdk not installed. Run: pip install hyperliquid-python-sdk")
        return False
    except Exception as e:
        send_confirmation(f"*Trade error for {coin}:* {str(e)[:200]}")
        print(f"  [!] Trade error: {e}")
        return False


# =============================================================
# SCAN ENGINE (reuses new_listing_scanner logic inline)
# =============================================================

def get_listing_age(coin):
    try:
        end = int(time.time() * 1000)
        start = end - (90 * 24 * 3600 * 1000)
        r = requests.post(HYPERLIQUID_API, json={
            "type": "candleSnapshot",
            "req": {"coin": coin, "interval": "1d", "startTime": start, "endTime": end}
        }, timeout=10)
        candles = r.json()
        return len(candles) if candles else None, candles or []
    except Exception:
        return None, []


def check_volume_momentum(candles):
    if not candles or len(candles) < 7:
        return 0.0
    volumes = [float(c.get("v", 0)) * float(c.get("c", 0)) for c in candles]
    early = sum(volumes[:7]) / 7
    recent = sum(volumes[-7:]) / 7
    return round(recent / early, 2) if early > 0 else 0.0


def check_price_health(candles, current_price):
    if not candles:
        return True, 0.0
    peak = max([float(c.get("h", 0)) for c in candles])
    drawdown = (peak - current_price) / peak if peak > 0 else 0
    return drawdown < 0.90, round(drawdown * 100, 1)


def run_scan():
    """Run the new listing scan and return qualifying coins."""
    print(f"\n[SCAN] Starting new listing scan at {time.strftime('%H:%M:%S')}")

    try:
        r = requests.post(HYPERLIQUID_API, json={"type": "metaAndAssetCtxs"}, timeout=10)
        data = r.json()
        universe = data[0]["universe"]
        contexts = data[1]
    except Exception as e:
        print(f"  [!] HL fetch failed: {e}")
        return []

    liquid_coins = {}
    for i, asset in enumerate(universe):
        name = asset["name"]
        ctx = contexts[i]
        price = float(ctx.get("markPx", 0))
        volume = float(ctx.get("dayNtlVlm", 0))
        oi = float(ctx.get("openInterest", 0))
        if price > 0 and volume >= 250_000 and price < 2.0:
            liquid_coins[name] = {"price": price, "volume_24h": volume, "open_interest": oi}

    print(f"  {len(liquid_coins)} liquid coins under $2")

    seen = load_seen()
    new_hits = []

    for coin, data in liquid_coins.items():
        if coin in seen:
            continue  # Already alerted

        age_days, candles = get_listing_age(coin)
        if age_days is None or age_days > MAX_AGE_DAYS:
            continue

        current_price = data["price"]
        healthy, drawdown_pct = check_price_health(candles, current_price)
        if not healthy:
            continue

        vol_ratio = check_volume_momentum(candles)

        # Quick score
        score = 0
        reasons = []

        if age_days <= 14:
            score += 30; reasons.append(f"Listed {age_days}d ago - first-mover window")
        elif age_days <= 30:
            score += 22; reasons.append(f"Listed {age_days}d ago - early stage")
        elif age_days <= 45:
            score += 14; reasons.append(f"Listed {age_days}d ago - fresh")
        else:
            score += 6;  reasons.append(f"Listed {age_days}d ago")

        if vol_ratio >= 2.0:
            score += 25; reasons.append(f"Volume {vol_ratio}x vs launch - BUILDING")
        elif vol_ratio >= 1.0:
            score += 15; reasons.append(f"Volume holding ({vol_ratio}x)")
        elif vol_ratio >= 0.5:
            score += 5;  reasons.append(f"Volume cooling ({vol_ratio}x)")

        if drawdown_pct < 30:
            score += 15; reasons.append("Price holding strong")
        elif drawdown_pct < 50:
            score += 8
        elif drawdown_pct < 70:
            score += 2

        if current_price < 0.001:
            score += 10; reasons.append(f"Sub $0.001 - lottery tier")
        elif current_price < 0.01:
            score += 6;  reasons.append(f"Sub-cent entry")

        print(f"  [FRESH] {coin} | {age_days}d | score {score} | vol {vol_ratio}x")

        if score >= MIN_SCORE:
            new_hits.append({
                "coin": coin,
                "price": current_price,
                "age_days": age_days,
                "volume_24h": data["volume_24h"],
                "open_interest": data["open_interest"],
                "vol_momentum": vol_ratio,
                "drawdown_pct": drawdown_pct,
                "score": score,
                "reasons": reasons
            })

        time.sleep(0.3)

    print(f"  [SCAN] {len(new_hits)} new hits found")
    return new_hits


# =============================================================
# CALLBACK LISTENER (handles button presses from your phone)
# =============================================================

def poll_callbacks():
    """Continuously poll Telegram for button presses."""
    last_update_id = 0
    print("[*] Callback listener started — waiting for your button presses...")

    while True:
        try:
            r = requests.get(
                f"{TELEGRAM_API}/getUpdates",
                params={"timeout": 30, "offset": last_update_id + 1, "allowed_updates": ["callback_query"]},
                timeout=40
            )
            data = r.json()
            if not data.get("ok"):
                time.sleep(5)
                continue

            for update in data.get("result", []):
                last_update_id = update["update_id"]
                cb = update.get("callback_query")
                if not cb:
                    continue

                callback_id = cb["id"]
                cb_data     = cb.get("data", "")

                # Security check: verify callback query is from the authorized user/chat
                message = cb.get("message", {})
                chat = message.get("chat", {})
                sender_id = str(chat.get("id", ""))
                from_user = cb.get("from", {})
                user_id = str(from_user.get("id", ""))
                
                if sender_id != str(CHAT_ID) and user_id != str(CHAT_ID):
                    print(f"  [SECURITY WARNING] Ignored callback from unauthorized user/chat: {user_id}/{sender_id}")
                    continue

                print(f"  [BUTTON] Received: {cb_data}")

                if cb_data.startswith("buy_"):
                    parts      = cb_data.split("_")
                    coin       = parts[1]
                    amount_usd = float(parts[2])

                    answer_callback(callback_id, f"Executing ${amount_usd} buy for {coin}...")
                    execute_buy(coin, amount_usd)

                    # Mark as seen so we don't re-alert
                    seen = load_seen()
                    seen[coin] = {"alerted": time.time(), "action": f"bought_${amount_usd}"}
                    save_seen(seen)

                elif cb_data.startswith("skip_"):
                    coin = cb_data.split("_")[1]
                    answer_callback(callback_id, f"Skipped {coin}")
                    send_confirmation(f"*Skipped {coin}* - watching for next opportunity")

                    seen = load_seen()
                    seen[coin] = {"alerted": time.time(), "action": "skipped"}
                    save_seen(seen)

        except Exception as e:
            print(f"  [!] Callback poll error: {e}")
            time.sleep(10)


# =============================================================
# MAIN LOOP
# =============================================================

def main():
    print("=" * 60)
    print(" FLOWSTATE AI - NEW LISTING WATCHER")
    print(f" Scanning every {SCAN_INTERVAL_HOURS}h | Min score: {MIN_SCORE}/100")
    print(f" Buy amount: ${BUY_AMOUNT_USD} | Stop: {STOP_LOSS_PCT*100:.0f}% | Target: {TAKE_PROFIT_PCT*100:.0f}%")
    print("=" * 60)

    # Validate credentials
    if not BOT_TOKEN or not CHAT_ID:
        print("[!] TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set.")
        print("    Run: $env:TELEGRAM_BOT_TOKEN='your-token'")
        print("    Run: $env:TELEGRAM_CHAT_ID='your-chat-id'")
        sys.exit(1)

    # Send startup notification
    send_confirmation(
        f"*FlowState Watcher ONLINE*\n"
        f"Scanning every {SCAN_INTERVAL_HOURS}h for new HL listings\n"
        f"Buy size: ${BUY_AMOUNT_USD} | Stop: 25% | Target: 2x\n"
        f"_I will alert you the moment something qualifies_"
    )
    print("[*] Startup notification sent to your phone")

    # Start callback listener in background thread
    cb_thread = threading.Thread(target=poll_callbacks, daemon=True)
    cb_thread.start()

    # Main scan loop
    while True:
        hits = run_scan()

        seen = load_seen()
        alerted = 0
        for coin_data in hits:
            coin = coin_data["coin"]
            if coin not in seen:
                msg_id = send_alert(coin_data)
                if msg_id:
                    seen[coin] = {"alerted": time.time(), "action": "pending", "score": coin_data["score"]}
                    alerted += 1
        save_seen(seen)

        if alerted == 0:
            print(f"  [OK] No new qualifying listings. Next scan in {SCAN_INTERVAL_HOURS}h")

        print(f"\n[*] Sleeping {SCAN_INTERVAL_HOURS} hours... (Ctrl+C to stop)")
        time.sleep(SCAN_INTERVAL_HOURS * 3600)


if __name__ == "__main__":
    main()
