import os
import sys
import time
import json
import math
import threading
import requests
import subprocess
from datetime import datetime

try:
    from dotenv import load_dotenv
    # Load from workspace root .env if present
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        load_dotenv()
except ImportError:
    pass

BOT_TOKEN  = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID    = os.environ.get("TELEGRAM_CHAT_ID", "")
HL_KEY     = os.environ.get("HL_PRIVATE_KEY", "")
HL_ADDRESS = os.environ.get("HL_ACCOUNT_ADDRESS", "")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

BASE      = os.path.dirname(os.path.abspath(__file__))
DATA      = os.path.join(BASE, "data")
SCANNERS  = os.path.join(BASE, "scanners")
AGENTS    = os.path.join(BASE, "agents")

REGIME_FILE   = os.path.join(DATA, "market_regime.json")
QUALIFIED     = os.path.join(DATA, "qualified_pairs.json")
APPROVED      = os.path.join(DATA, "final_approved_pairs.json")
RANKED        = os.path.join(DATA, "ranked_pairs.json")
MOONSHOT_FILE = os.path.join(DATA, "moonshot_candidates.json")
SEEN_FILE     = os.path.join(DATA, "seen_listings.json")
HODL_DEPOSITS = os.path.join(DATA, "hodl_deposits.json")
STATE_FILE    = os.path.join(DATA, "orchestrator_state.json")

CORE_INTERVAL_HOURS     = 4
MOONSHOT_INTERVAL_HOURS = 1
MOONSHOT_WEEKLY_LIMIT   = 1

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def round_to_tick(price):
    """Round price to 5 significant figures + cap decimal places for Hyperliquid."""
    if price <= 0:
        return price
    sig_figs = 5
    magnitude = math.floor(math.log10(abs(price)))
    factor = 10 ** (sig_figs - 1 - magnitude)
    rounded = round(price * factor) / factor
    if price < 0.001:
        return round(rounded, 7)
    elif price < 0.01:
        return round(rounded, 6)
    elif price < 0.1:
        return round(rounded, 5)
    elif price < 1:
        return round(rounded, 4)
    elif price < 10:
        return round(rounded, 3)
    elif price < 100:
        return round(rounded, 2)
    else:
        return round(rounded, 1)

def get_sz_decimals(info, coin):
    """Get the szDecimals for a coin from Hyperliquid metadata."""
    try:
        meta = info.meta()
        for asset in meta.get("universe", []):
            if asset.get("name") == coin:
                return asset.get("szDecimals", 0)
    except Exception as e:
        log(f"szDecimals lookup error for {coin}: {e}")
    return 0

def get_total_balance(info, address):
    """Get total equity: perps account value + spot USDC. Returns (total, perps_val, spot_val, detail_str)."""
    total = 0.0
    perps_val = 0.0
    spot_val = 0.0
    detail_parts = []
    try:
        user_state = info.user_state(address)
        perps_val = float(user_state.get("marginSummary", {}).get("accountValue", 0))
        total += perps_val
        detail_parts.append(f"perps=${perps_val:.2f}")
    except Exception as e:
        detail_parts.append(f"perps=ERR({e})")
    try:
        spot_state = info.spot_user_state(address)
        for b in spot_state.get("balances", []):
            if b.get("coin") == "USDC":
                spot_val = float(b.get("total", 0))
                total += spot_val
                detail_parts.append(f"spot=${spot_val:.2f}")
    except Exception as e:
        detail_parts.append(f"spot=ERR({e})")
    return total, perps_val, spot_val, " + ".join(detail_parts)

def send_message(text, keyboard=None):
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    if keyboard:
        payload["reply_markup"] = json.dumps(keyboard)
    try:
        r = requests.post(f"{TELEGRAM_API}/sendMessage", json=payload, timeout=10)
        result = r.json()
        if result.get("ok"):
            return result["result"]["message_id"]
    except Exception as e:
        log(f"Telegram error: {e}")
    return None

def answer_callback(callback_id, text):
    try:
        requests.post(f"{TELEGRAM_API}/answerCallbackQuery",
            json={"callback_query_id": callback_id, "text": text}, timeout=5)
    except Exception:
        pass

def run_script(script_path, timeout=300):
    try:
        result = subprocess.run([sys.executable, script_path],
            capture_output=True, text=True, timeout=timeout)
        if result.returncode == 0:
            log(f"OK: {os.path.basename(script_path)}")
            return True
        else:
            log(f"FAIL: {os.path.basename(script_path)} (code={result.returncode})")
            log(f"STDERR: {result.stderr[-400:]}")
            try:
                with open('/tmp/last_error.txt', 'w') as ef:
                    ef.write(f"Script: {script_path}\nCode: {result.returncode}\nSTDERR:\n{result.stderr}\nSTDOUT:\n{result.stdout}")
            except Exception:
                pass
            return False
    except subprocess.TimeoutExpired:
        log(f"TIMEOUT: {os.path.basename(script_path)} exceeded {timeout}s")
        return False
    except Exception as e:
        log(f"Script error: {e}")
        return False

def load_json(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_state():
    state = load_json(STATE_FILE)
    if not state:
        state = {
            "moonshots_this_week": 0,
            "week_start": time.time(),
            "last_core_scan": 0,
            "last_moonshot_scan": 0
        }
    return state

def save_state(state):
    save_json(STATE_FILE, state)

def run_core_scan():
    log("CORE SCAN STARTING")
    # Clear final approved pairs at the start of a new scan cycle
    save_json(APPROVED, [])
    
    if not run_script(f"{SCANNERS}/regime_scanner.py"):
        send_message("Warning: Regime scanner failed")
        return
    regime_data = load_json(REGIME_FILE)
    regime = regime_data.get("regime", "CHOP") if regime_data else "CHOP"
    log(f"Regime: {regime}")
    scanner_map = {
        "BULL": f"{SCANNERS}/bull_scanner.py",
        "BEAR": f"{SCANNERS}/bear_scanner.py",
        "CHOP": f"{SCANNERS}/chop_scanner.py"
    }
    scanner = scanner_map.get(regime, f"{SCANNERS}/chop_scanner.py")
    if not run_script(scanner):
        send_message(f"Warning: {regime} scanner failed")
        return
    qualified = load_json(QUALIFIED)
    if not qualified:
        send_message(f"Scan complete - {regime} market. No qualifying pairs found.")
        return
    if not run_script(f"{AGENTS}/fa_agent.py", timeout=900):
        send_message("Warning: FA agent failed")
        return
    # Decoupled: Check fa_approved_pairs.json instead of final_approved_pairs.json
    approved = load_json(os.path.join(DATA, "fa_approved_pairs.json"))
    if not approved:
        send_message(f"Scan complete - {regime} market. No pairs passed FA filter.")
        return
    if not run_script(f"{AGENTS}/pair_ranker.py"):
        return
    ranked = load_json(RANKED)
    if not ranked:
        return
    send_core_alert(regime, ranked[:3])

def send_core_alert(regime, top3):
    regime_emoji = {"BULL": "green", "BEAR": "red", "CHOP": "yellow"}.get(regime, "white")
    lines = [f"*FLOWSTATE SCAN COMPLETE*", f"Regime: {regime}\n"]
    medals = ["1", "2", "3"]
    for i, p in enumerate(top3):
        lines.append(f"{medals[i]}. *{p['coin']}* Score:{p['score']} BBW:{p['bbw']}% Vol:${p['volume']}M")
    lines.append("\nTap a coin to enter:")
    text = "\n".join(lines)
    buttons = []
    for p in top3:
        buttons.append([{"text": f"{p['coin']}", "callback_data": f"trade_{p['coin']}"}])
    buttons.append([{"text": "SKIP this cycle", "callback_data": "trade_skip"}])
    keyboard = {"inline_keyboard": buttons}
    send_message(text, keyboard)
    log(f"Core alert sent: {[p['coin'] for p in top3]}")

def run_moonshot_scan(state):
    week_elapsed = time.time() - state.get("week_start", 0)
    if week_elapsed > 7 * 24 * 3600:
        state["moonshots_this_week"] = 0
        state["week_start"] = time.time()
    if state.get("moonshots_this_week", 0) >= MOONSHOT_WEEKLY_LIMIT:
        log("Weekly moonshot limit reached")
        return state
    log("Running moonshot scanner...")
    run_script(f"{SCANNERS}/unified_moonshot_scanner.py")
    candidates = load_json(MOONSHOT_FILE)
    if not candidates:
        log("No moonshot candidates")
        return state
    seen = load_json(SEEN_FILE) or {}
    for candidate in candidates[:1]:
        coin = candidate.get("coin")
        if not coin or coin in seen:
            continue
        score = candidate.get("score", 0)
        price = candidate.get("price", 0)
        vol   = candidate.get("volume_24h", 0)
        age   = candidate.get("age_days", 0)
        vol_str = f"${vol/1e6:.1f}M" if vol >= 1e6 else f"${vol/1e3:.0f}K"
        text = (
            f"*MOONSHOT DETECTED*\n"
            f"Coin: {coin}\n"
            f"Score: {score}/100\n"
            f"Price: ${price:.8f}\n"
            f"Volume: {vol_str}/24h\n"
            f"Age: {age} days\n"
            f"Stop: 40% | Target: 10x"
        )
        keyboard = {"inline_keyboard": [[
            {"text": "$5",   "callback_data": f"moon_{coin}_5"},
            {"text": "$10",  "callback_data": f"moon_{coin}_10"},
            {"text": "$20",  "callback_data": f"moon_{coin}_20"},
            {"text": "SKIP", "callback_data": f"moon_skip_{coin}"}
        ]]}
        msg_id = send_message(text, keyboard)
        if msg_id:
            seen[coin] = {"alerted": time.time(), "action": "pending"}
            save_json(SEEN_FILE, seen)
            log(f"Moonshot alert sent: {coin}")
    return state

def execute_core_trade(coin):
    log(f"Core trade selected: {coin}")
    qualified = load_json(QUALIFIED)
    coin_data = None
    if qualified:
        for p in qualified:
            if p.get("coin") == coin:
                coin_data = p
                break
    
    if not coin_data:
        regime_data = load_json(REGIME_FILE)
        regime = regime_data.get("regime", "CHOP") if regime_data else "CHOP"
        scan_mode = "chop_opportunity" if regime == "CHOP" else "bear_short" if regime == "BEAR" else "standard"
        coin_data = {"coin": coin, "fa_score": 1, "metrics": {"scan_mode": scan_mode}}
        
    current_approved = load_json(APPROVED) or []
    current_approved = [p for p in current_approved if p.get("coin") != coin]
    current_approved.append(coin_data)
    save_json(APPROVED, current_approved)

    # --- Immediate Execution on Telegram Approval ---
    try:
        from hyperliquid.exchange import Exchange
        from hyperliquid.info import Info
        from hyperliquid.utils import constants
        import eth_account

        account  = eth_account.Account.from_key(HL_KEY)
        info     = Info(constants.MAINNET_API_URL, skip_ws=True)
        exchange = Exchange(account, constants.MAINNET_API_URL, account_address=HL_ADDRESS)
        log(f"  HL Account: {HL_ADDRESS} | Signer Wallet: {account.address}")

        # --- Get price ---
        mids  = info.all_mids()
        price = float(mids.get(coin, 0))
        if price == 0:
            send_message(f"❌ *{coin} FAILED*\nCould not get price from Hyperliquid (coin not found in mids)")
            return
        log(f"  Price for {coin}: ${price}")

        # --- Check if position is ALREADY open for this coin to prevent duplicate fills ---
        try:
            user_state = info.user_state(HL_ADDRESS)
            for pos in user_state.get("assetPositions", []):
                position = pos.get("position", {})
                if position.get("coin") == coin and float(position.get("szi", 0)) != 0:
                    sz_existing = position.get("szi")
                    log(f"  [SAFETY] Position already open for {coin} ({sz_existing}). Aborting duplicate trade execution.")
                    send_message(f"ℹ️ *{coin} ALREADY ACTIVE*\nPosition is already open on Hyperliquid ({sz_existing} {coin}). Skipping duplicate trade execution.")
                    return
        except Exception as check_err:
            log(f"  [SAFETY WARNING] Existing position check error: {check_err}")

        # --- Get balance (perps + spot) ---
        balance, perps_val, spot_val, balance_detail = get_total_balance(info, HL_ADDRESS)
        log(f"  Balance: ${balance:.2f} ({balance_detail})")
        if balance <= 0:
            send_message(f"❌ *{coin} FAILED*\nZero balance detected ({balance_detail}). Deposit USDC first.")
            return

        # --- Auto-transfer Spot USDC to Perps Margin if needed ---
        if spot_val > 0.5 and perps_val < 1.0:
            log(f"  Auto-transferring ${spot_val:.2f} USDC from Spot to Perps Margin...")
            try:
                transfer_res = exchange.usd_class_transfer(spot_val, True)
                log(f"  USD class transfer result: {transfer_res}")
                time.sleep(1)
            except Exception as te:
                log(f"  USD class transfer warning: {te}")

        # --- Position sizing: 88% margin allocation with dynamic leverage to clear Hyperliquid $10 min ---
        # Leaving 12% margin buffer prevents initial margin rejection from 0.5% limit slippage & taker fees.
        margin_alloc = balance * 0.88
        leverage = 3.0
        notional_target = margin_alloc * leverage
        if notional_target < 10.50:
            if (margin_alloc * 10.0) >= 10.50:
                leverage = round(10.50 / margin_alloc, 1)
                notional_target = margin_alloc * leverage
            else:
                send_message(
                    f"❌ *{coin} FAILED: BALANCE TOO LOW*\n"
                    f"Balance: ${balance:.2f} — cannot reach Hyperliquid's $10 minimum even at 10x.\n"
                    f"Deposit more USDC and try again."
                )
                return
        raw_size = notional_target / price
        mode_str = f"⚡ 100% ALL-IN ({leverage:.1f}x) | Margin: ~${margin_alloc:.2f} | Position Value: ~${notional_target:.2f}"
        log(f"  ALL-IN MODE: ~${margin_alloc:.2f} margin @ {leverage:.1f}x leverage (notional: ${notional_target:.2f})")

        # --- Round to correct size decimals ---
        sz_dec = get_sz_decimals(info, coin)
        size = round(raw_size, sz_dec)
        if sz_dec == 0:
            size = int(size)
        log(f"  Size: {size} (raw={raw_size:.6f}, decimals={sz_dec})")

        if size <= 0:
            send_message(
                f"❌ *{coin} FAILED*\nCalculated size is 0\n"
                f"Balance: ${balance:.2f} | Price: ${price} | Raw: {raw_size:.8f} | Decimals: {sz_dec}"
            )
            return

        # --- Hyperliquid Exchange Minimum Check ($10 minimum order value) ---
        order_value = size * price
        if order_value < 10.0:
            shortfall = 10.0 - balance
            add_str = f"Deposit ~${shortfall + 1.0:.2f} USDC" if shortfall > 0 else "Deposit a small amount of USDC"
            send_message(
                f"⚠️ *{coin} FAILED: BALANCE BELOW HYPERLIQUID $10 MINIMUM*\n"
                f"Current Balance: *${balance:.2f}*\n"
                f"Calculated Order Value: *${order_value:.2f}*\n\n"
                f"Hyperliquid protocol requires a **minimum order value of $10.00** per trade.\n\n"
                f"💡 *Action:* {add_str} to your wallet to meet the $10 minimum."
            )
            return

        # --- Place order using proven IOC pattern (same as master_trader.py) ---
        limit_price = round_to_tick(price * 1.005)  # 0.5% slippage allowance
        log(f"  Placing IOC order: {size} {coin} @ limit ${limit_price}")

        order_result = exchange.order(
            coin,
            True,          # is_buy = True (long)
            size,
            limit_price,
            {"limit": {"tif": "Ioc"}}
        )
        log(f"  Order response: {order_result}")

        # --- Check if the order actually filled ---
        response = order_result.get("response", {}) if isinstance(order_result, dict) else {}
        data = response.get("data", {}) if isinstance(response, dict) else {}
        statuses = data.get("statuses", []) if isinstance(data, dict) else []
        has_fill = any("filled" in str(s).lower() or "resting" in str(s).lower() for s in statuses)

        if has_fill:
            # ── STEP 1: Get ACTUAL filled position size from on-chain ─────────────────
            # IOC orders can partially fill. Always use real on-chain size for the stop,
            # never the estimated size — wrong size on a stop can leave you exposed.
            time.sleep(1.5)  # Brief wait for Hyperliquid to post the position
            actual_size = size  # fallback to intended size
            actual_entry = price  # fallback to quote price
            try:
                us = info.user_state(HL_ADDRESS)
                for pos in us.get("assetPositions", []):
                    p_data = pos.get("position", {})
                    if p_data.get("coin") == coin and float(p_data.get("szi", 0)) > 0:
                        actual_size = abs(float(p_data.get("szi", 0)))
                        actual_entry = float(p_data.get("entryPx", price))
                        log(f"  Actual on-chain size: {actual_size} {coin} @ ${actual_entry}")
                        break
            except Exception as sz_err:
                log(f"  Could not verify actual position size (using estimated): {sz_err}")

            # ── STEP 2: Place native Hyperliquid trigger stop-loss order ──────────────
            # This stop lives on Hyperliquid's servers. It fires 24/7 even if the VPS
            # is offline, restarting, or the bot crashes. This is the core protection.
            stop_price = round_to_tick(actual_entry * 0.96)   # 4% below entry
            stop_limit = round_to_tick(stop_price * 0.90)     # 10% below trigger = guarantee fill
            native_stop_placed = False
            native_stop_status = "❌ STOP NOT PLACED"
            try:
                stop_result = exchange.order(
                    coin,
                    False,       # is_buy=False → SELL to close long
                    actual_size,
                    stop_limit,
                    {"trigger": {"triggerPx": stop_price, "isMarket": True, "tpsl": "sl"}},
                    reduce_only=True
                )
                log(f"  Native stop-loss result: {stop_result}")
                # Verify the stop was accepted
                stop_resp = stop_result.get("response", {}) if isinstance(stop_result, dict) else {}
                stop_data = stop_resp.get("data", {}) if isinstance(stop_resp, dict) else {}
                stop_statuses = stop_data.get("statuses", []) if isinstance(stop_data, dict) else []
                stop_ok = any(
                    "resting" in str(s).lower() or "success" in str(s).lower()
                    for s in stop_statuses
                )
                if stop_ok:
                    native_stop_placed = True
                    native_stop_status = f"🛡️ Native HL Stop: ${stop_price:.4f} (-4%) — ACTIVE on exchange"
                    log(f"  ✅ Native stop CONFIRMED active at ${stop_price}")
                else:
                    native_stop_status = f"⚠️ STOP ORDER UNCERTAIN — check HL open orders! (response: {str(stop_statuses)[:100]})"
                    log(f"  ⚠️ Stop placement response uncertain: {stop_statuses}")
            except Exception as stop_err:
                log(f"  ❌ Native stop placement FAILED: {stop_err}")
                native_stop_status = f"🚨 STOP FAILED — POSITION UNPROTECTED! Error: {str(stop_err)[:80]}"

            # ── STEP 3: Send Telegram confirmation with full status ───────────────────
            send_message(
                f"✅ *CORE TRADE FILLED: {coin}*\n"
                f"{mode_str}\n"
                f"Size: {actual_size} @ ${actual_entry:.4f}\n"
                f"Position Value: ~${actual_size * actual_entry:.2f}\n\n"
                f"{native_stop_status}\n"
                f"📈 Trailing Stop: 50% of peak profit\n"
                f"⏱️ Exits: 4h stale / 24h compound"
            )

            # ── STEP 4: If stop failed, send a separate urgent alert ─────────────────
            if not native_stop_placed:
                send_message(
                    f"🚨 *URGENT: {coin} POSITION HAS NO STOP LOSS*\n"
                    f"The native stop order could not be placed on Hyperliquid.\n"
                    f"master_trader.py will attempt to re-place it on next loop (60s).\n"
                    f"If the bot is not running, CLOSE THIS POSITION MANUALLY NOW!"
                )

        else:
            raw_resp = statuses if (statuses and len(statuses) > 0) else order_result
            resp_str = str(raw_resp).replace("*", "").replace("_", "")[:200]
            send_message(
                f"⚠️ *{coin} ORDER NOT FILLED*\n"
                f"{mode_str}\n"
                f"Size: {size} @ limit ${limit_price}\n"
                f"Response: {resp_str}\n"
                f"Check Hyperliquid balance/margin."
            )

    except Exception as e:
        log(f"Core trade execution error: {e}")
        import traceback
        traceback.print_exc()
        send_message(f"❌ *{coin} EXECUTION ERROR*\n{str(e)[:300]}")

def execute_moonshot_trade(coin, amount_usd):
    log(f"Moonshot trade: {coin} ${amount_usd}")
    try:
        from hyperliquid.exchange import Exchange
        from hyperliquid.info import Info
        from hyperliquid.utils import constants
        import eth_account
        account  = eth_account.Account.from_key(HL_KEY)
        info     = Info(constants.MAINNET_API_URL, skip_ws=True)
        exchange = Exchange(account, constants.MAINNET_API_URL, account_address=HL_ADDRESS)
        mids     = info.all_mids()
        price    = float(mids.get(coin, 0))
        if price == 0:
            send_message(f"❌ *MOONSHOT FAILED: {coin}*\nCould not get price from Hyperliquid")
            return

        sz_dec = get_sz_decimals(info, coin)
        raw_size = amount_usd / price
        size = round(raw_size, sz_dec)
        if sz_dec == 0:
            size = int(size)
        if size <= 0:
            send_message(f"❌ *MOONSHOT FAILED: {coin}*\nSize too small: ${amount_usd} / ${price} = {raw_size:.8f} (decimals={sz_dec})")
            return

        limit_price = round_to_tick(price * 1.005)
        log(f"  Moonshot IOC order: {size} {coin} @ limit ${limit_price}")

        order_result = exchange.order(
            coin,
            True,
            size,
            limit_price,
            {"limit": {"tif": "Ioc"}}
        )
        log(f"  Moonshot response: {order_result}")

        response = order_result.get("response", {}) if isinstance(order_result, dict) else {}
        data = response.get("data", {}) if isinstance(response, dict) else {}
        statuses = data.get("statuses", []) if isinstance(data, dict) else []
        has_fill = any("filled" in str(s).lower() or "resting" in str(s).lower() for s in statuses)

        if has_fill:
            send_message(
                f"✅ *MOONSHOT FILLED: {coin}*\n"
                f"Size: {size} @ ${price:.6f}\n"
                f"Cost: ${amount_usd}\n"
                f"Stop: ${price*0.60:.6f} (-40%)\n"
                f"Target: ${price*10:.6f} (10x)"
            )
        else:
            send_message(
                f"⚠️ *MOONSHOT NOT FILLED: {coin}*\n"
                f"Size: {size} @ limit ${limit_price}\n"
                f"Response: {str(statuses)[:200]}"
            )
    except Exception as e:
        log(f"Moonshot execution error: {e}")
        import traceback
        traceback.print_exc()
        send_message(f"❌ *MOONSHOT ERROR: {coin}*\n{str(e)[:300]}")

def process_hodl_sweeps():
    deposits = load_json(HODL_DEPOSITS)
    if not deposits:
        return
    pending = [d for d in deposits if not d.get("processed")]
    if not pending:
        return
    total = sum(d.get("amount", 0) for d in pending)
    log(f"Processing HODL sweep: ${total:.2f}")
    try:
        from hyperliquid.exchange import Exchange
        from hyperliquid.info import Info
        from hyperliquid.utils import constants
        import eth_account
        account   = eth_account.Account.from_key(HL_KEY)
        info      = Info(constants.MAINNET_API_URL, skip_ws=True)
        exchange  = Exchange(account, constants.MAINNET_API_URL, account_address=HL_ADDRESS)
        mids      = info.all_mids()
        btc_price = float(mids.get("BTC", 0))
        sol_price = float(mids.get("SOL", 0))
        if btc_price == 0 or sol_price == 0:
            return
        btc_usd  = total * 0.60
        sol_usd  = total * 0.40

        btc_sz_dec = get_sz_decimals(info, "BTC")
        sol_sz_dec = get_sz_decimals(info, "SOL")
        btc_size = round(btc_usd / btc_price, btc_sz_dec)
        sol_size = round(sol_usd / sol_price, sol_sz_dec)
        if btc_sz_dec == 0: btc_size = int(btc_size)
        if sol_sz_dec == 0: sol_size = int(sol_size)

        btc_limit = round_to_tick(btc_price * 1.005)
        sol_limit = round_to_tick(sol_price * 1.005)
        exchange.order("BTC", True, btc_size, btc_limit, {"limit": {"tif": "Ioc"}})
        exchange.order("SOL", True, sol_size, sol_limit, {"limit": {"tif": "Ioc"}})

        for d in deposits:
            d["processed"] = True
        save_json(HODL_DEPOSITS, deposits)
        send_message(
            f"*HODL SWEEP COMPLETE*\n"
            f"Total: ${total:.2f}\n"
            f"BTC: {btc_size} (${btc_usd:.2f})\n"
            f"SOL: {sol_size} (${sol_usd:.2f})"
        )
    except Exception as e:
        log(f"HODL sweep error: {e}")

def poll_callbacks(state_ref):
    last_update_id = 0
    log("Callback listener started")
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
                cb_id   = cb["id"]
                cb_data = cb.get("data", "")
                
                # Security check: verify callback query is from the authorized user/chat
                message = cb.get("message", {})
                chat = message.get("chat", {})
                sender_id = str(chat.get("id", ""))
                from_user = cb.get("from", {})
                user_id = str(from_user.get("id", ""))
                
                if sender_id != str(CHAT_ID) and user_id != str(CHAT_ID):
                    log(f"[SECURITY WARNING] Ignored callback from unauthorized user/chat: {user_id}/{sender_id}")
                    continue

                log(f"Button: {cb_data}")
                if cb_data.startswith("trade_"):
                    coin = cb_data.replace("trade_", "")
                    if coin == "skip":
                        answer_callback(cb_id, "Skipped")
                        save_json(APPROVED, [])
                        send_message("Skipped - watching for next opportunity")
                    else:
                        answer_callback(cb_id, f"Entering {coin}...")
                        execute_core_trade(coin)
                elif cb_data.startswith("moon_"):
                    parts = cb_data.split("_")
                    if parts[1] == "skip":
                        coin = parts[2]
                        answer_callback(cb_id, f"Skipped {coin}")
                        send_message(f"Skipped {coin}")
                    else:
                        coin   = parts[1]
                        amount = float(parts[2])
                        answer_callback(cb_id, f"Buying ${amount} of {coin}...")
                        execute_moonshot_trade(coin, amount)
                        state_ref["moonshots_this_week"] = state_ref.get("moonshots_this_week", 0) + 1
                        save_state(state_ref)
        except Exception as e:
            log(f"Callback error: {e}")
            time.sleep(10)

def main():
    print("=" * 50)
    print(" FLOWSTATE AI ORCHESTRATOR")
    print("=" * 50)
    if not BOT_TOKEN or not CHAT_ID:
        print("ERROR: Telegram credentials missing")
        sys.exit(1)
    state = load_state()
    send_message("*FlowState Orchestrator ONLINE*\nCore: every 4h | Moonshot: every 1h\nAll systems go")
    cb_thread = threading.Thread(target=poll_callbacks, args=(state,), daemon=True)
    cb_thread.start()
    log("First scan in 10 seconds...")
    time.sleep(10)
    while True:
        now = time.time()
        if now - state.get("last_core_scan", 0) >= CORE_INTERVAL_HOURS * 3600:
            run_core_scan()
            # process_hodl_sweeps()  # DISABLED until properly rebuilt
            state["last_core_scan"] = now
            save_state(state)
        if now - state.get("last_moonshot_scan", 0) >= MOONSHOT_INTERVAL_HOURS * 3600:
            state = run_moonshot_scan(state)
            state["last_moonshot_scan"] = now
            save_state(state)
        time.sleep(60)

if __name__ == "__main__":
    main()
