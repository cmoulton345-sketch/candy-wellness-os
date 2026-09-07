import json
import os
import sys
import math
import time
import requests
import eth_account
from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants

# ============================================================
#  FLOWSTATE AI MOONSHOT BOT v2
#  Managed moonshot positions with trailing stop
#  Usage: python moonshot_launcher.py <COIN> --amount <USD>
# ============================================================

# --- MAINNET for trading ---
TRADE_API_URL = "https://api.hyperliquid.xyz/info"

# --- MAINNET for price/candle data (better accuracy) ---
DATA_API_URL = "https://api.hyperliquid.xyz/info"

# --- Moonshot Parameters ---
TRAILING_STOP_PCT = 0.20        # 20% trailing stop — wide enough for moonshot volatility
CHECK_INTERVAL = 3600           # Check every hour (moonshots are longer plays)
THESIS_INVALIDATION_RSI = 30    # If RSI drops below 30 AND price is below entry, force exit


def round_to_tick(price):
    """Round price to 5 significant figures (Hyperliquid tick convention)."""
    if price <= 0:
        return price
    sig_figs = 5
    magnitude = math.floor(math.log10(abs(price)))
    factor = 10 ** (sig_figs - 1 - magnitude)
    return round(price * factor) / factor


def get_total_balance(info, account_address):
    """Get total equity: perps + spot."""
    try:
        total = 0.0
        user_state = info.user_state(account_address)
        perps_bal = float(user_state.get("marginSummary", {}).get("accountValue", 0))
        total += perps_bal
        
        spot_state = info.spot_user_state(account_address)
        for balance in spot_state.get("balances", []):
            if balance.get("coin") == "USDC":
                total += float(balance.get("total", 0))
        
        return total if total > 0 else 0.0
    except Exception as e:
        print(f"[!] Balance check error: {e}")
        return 0.0


def fetch_candles_for_rsi(coin, api_url):
    """Fetch candles for RSI calculation."""
    end_time = int(time.time() * 1000)
    start_time = end_time - (100 * 3600 * 1000)  # 100 hours
    payload = {
        "type": "candleSnapshot",
        "req": {"coin": coin, "interval": "1h", "startTime": start_time, "endTime": end_time}
    }
    try:
        response = requests.post(api_url, json=payload, timeout=10)
        candles = response.json()
        if not candles:
            return None
        return [float(c["c"]) for c in candles]
    except:
        return None


def calculate_rsi(prices, window=14):
    if len(prices) < window + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        gains.append(max(change, 0))
        losses.append(abs(min(change, 0)))
    avg_gain = sum(gains[:window]) / window
    avg_loss = sum(losses[:window]) / window
    for i in range(window, len(gains)):
        avg_gain = (avg_gain * (window - 1) + gains[i]) / window
        avg_loss = (avg_loss * (window - 1) + losses[i]) / window
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def save_state(state, filepath):
    """Persist moonshot state to disk."""
    with open(filepath, 'w') as f:
        json.dump(state, f, indent=4)


def load_state(filepath):
    """Load moonshot state from disk."""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None


def main():
    # Parse arguments
    if len(sys.argv) < 2:
        print("=" * 60)
        print(" FLOWSTATE AI MOONSHOT BOT v2")
        print(" Managed moonshot with trailing stop")
        print("=" * 60)
        print()
        print("Usage: python moonshot_launcher.py <COIN> --amount <USD>")
        print("Example: python moonshot_launcher.py PENDLE --amount 50")
        print()
        
        # Show approved moonshots
        approved_file = os.path.join(os.path.dirname(__file__), "..", "data", "moonshot_approved.json")
        if os.path.exists(approved_file):
            with open(approved_file, 'r') as f:
                approved = json.load(f)
            if approved:
                print("Approved moonshots from FA Agent:")
                for m in approved:
                    print(f"  {m['coin']:>10} | FA: {m['fa_score']}/5 | Scanner: {m['score']}/100")
        return
    
    coin = sys.argv[1].upper()
    
    # Parse --amount flag
    custom_amount = None
    if "--amount" in sys.argv:
        idx = sys.argv.index("--amount")
        if idx + 1 < len(sys.argv):
            try:
                custom_amount = float(sys.argv[idx + 1])
            except ValueError:
                print("[!] Invalid amount. Use: --amount 50")
                return
    
    if not custom_amount:
        print("[!] You must specify --amount <USD>")
        print("    Example: python moonshot_launcher.py PENDLE --amount 50")
        return
    
    # Check env vars
    private_key = os.environ.get("HL_PRIVATE_KEY")
    account_address = os.environ.get("HL_ACCOUNT_ADDRESS")
    
    if not private_key or not account_address:
        print("[!] Set HL_PRIVATE_KEY and HL_ACCOUNT_ADDRESS first.")
        return
    
    # Initialize
    wallet = eth_account.Account.from_key(private_key)
    info = Info(constants.MAINNET_API_URL, skip_ws=True)
    exchange = Exchange(wallet, constants.MAINNET_API_URL, account_address=account_address)
    
    state_file = os.path.join(os.path.dirname(__file__), "..", "data", f"moonshot_state_{coin.lower()}.json")
    
    print("=" * 60)
    print(f" MOONSHOT BOT v2 — {coin}")
    print(f" Trailing Stop: {TRAILING_STOP_PCT*100:.0f}% | Check: {CHECK_INTERVAL//60}min")
    print("=" * 60)
    
    # Check for existing state (resume after crash)
    state = load_state(state_file)
    
    if state and state.get("in_position"):
        # Resuming existing position
        print(f"\n[*] Resuming {coin} moonshot from saved state")
        print(f"    Entry: ${state['entry_price']} | Peak: ${state['peak_price']} | Stop: ${state['stop_price']}")
    else:
        # New position — open it
        balance = get_total_balance(info, account_address)
        if balance <= 0:
            print("[!] No balance available.")
            return
        
        # Get current price
        try:
            all_mids = info.all_mids()
            current_price = float(all_mids.get(coin, 0))
        except:
            print(f"[!] Could not get price for {coin}.")
            return
        
        if current_price <= 0:
            print(f"[!] {coin} not found on Hyperliquid mainnet.")
            return
        
        # Calculate position
        leverage = 1
        raw_size = custom_amount / current_price
        size = max(1, round(raw_size))
        actual_cost = size * current_price
        limit_price = round_to_tick(current_price * 1.01)
        stop_price = round(current_price * (1 - TRAILING_STOP_PCT), 6)
        
        print(f"\n  Account Balance:   ${balance:.2f}")
        print(f"  Moonshot Budget:   ${custom_amount:.2f}")
        print(f"  Coin:              {coin}")
        print(f"  Price:             ${current_price}")
        print(f"  Size:              {size} {coin}")
        print(f"  Position Value:    ~${actual_cost:.2f}")
        print(f"  Leverage:          1x")
        print(f"  Trailing Stop:     {TRAILING_STOP_PCT*100:.0f}% (${stop_price})")
        print(f"  Target:            10x+ (${current_price * 10:.6f})")
        
        print(f"\n  [!] This is a MOONSHOT. You could lose the entire ${actual_cost:.2f}.")
        confirm = input(f"\n  Type 'MOON' to launch {coin}: ").strip()
        
        if confirm != "MOON":
            print("  [ABORT] Cancelled.")
            return
        
        # Place the order
        try:
            exchange.update_leverage(leverage, coin)
            
            order_result = exchange.order(
                coin,
                True,
                size,
                limit_price,
                {"limit": {"tif": "Gtc"}}
            )
            
            print(f"\n  [RAW] {order_result}")
            
            response = order_result.get("response", {})
            data = response.get("data", {})
            statuses = data.get("statuses", [])
            
            filled = any(isinstance(s, dict) and "filled" in s for s in statuses)
            errored = any(isinstance(s, dict) and "error" in s for s in statuses)
            
            if errored and not filled:
                error_msg = [s.get("error", "") for s in statuses if isinstance(s, dict) and "error" in s]
                print(f"\n  [REJECTED] {error_msg}")
                return
            
            print(f"\n  [FILLED] Moonshot position opened!")
            
            # Save state
            state = {
                "coin": coin,
                "entry_price": current_price,
                "peak_price": current_price,
                "stop_price": stop_price,
                "position_size": size,
                "cost_basis": actual_cost,
                "in_position": True,
                "opened_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            save_state(state, state_file)
            
        except Exception as e:
            print(f"\n  [ERROR] Order failed: {e}")
            return
    
    # --- Main monitoring loop ---
    print(f"\n{'='*60}")
    print(f" MONITORING {coin} — Check every {CHECK_INTERVAL//60} minutes")
    print(f" Trailing Stop: {TRAILING_STOP_PCT*100:.0f}% | Press Ctrl+C to stop")
    print(f"{'='*60}\n")
    
    try:
        while True:
            try:
                # Get current price from mainnet (where our position lives)
                current_price = float(info.all_mids().get(coin, 0))
                if current_price <= 0:
                    print(f"  [!] Could not get {coin} price, retrying next cycle...")
                    time.sleep(CHECK_INTERVAL)
                    continue
                
                entry = state["entry_price"]
                peak = state["peak_price"]
                stop = state["stop_price"]
                size = state["position_size"]
                
                # Update peak and trailing stop
                if current_price > peak:
                    state["peak_price"] = current_price
                    # Trail the stop: entry + (peak - entry) * (1 - trailing_pct)
                    # Simpler: stop = peak * (1 - trailing_pct)
                    state["stop_price"] = round(current_price * (1 - TRAILING_STOP_PCT), 6)
                    print(f"  [TRAIL] New peak ${current_price:.6f} -> Stop ${state['stop_price']:.6f}")
                
                # P&L calculation
                pnl = (current_price - entry) * size
                pnl_pct = ((current_price - entry) / entry) * 100
                peak_pnl_pct = ((peak - entry) / entry) * 100
                
                # Status print
                timestamp = time.strftime("%H:%M:%S")
                print(f"  [{timestamp}] {coin} ${current_price:.6f} | Entry: ${entry:.6f} | Peak: ${peak:.6f} | Stop: ${state['stop_price']:.6f} | P&L: {pnl_pct:+.1f}%")
                
                # --- EXIT CHECK 1: Trailing stop ---
                if current_price <= state["stop_price"]:
                    print(f"\n  [EXIT] TRAILING STOP HIT at ${current_price:.6f} (stop: ${state['stop_price']:.6f})")
                    self_close_position(exchange, info, account_address, coin, current_price, entry, size, pnl, state_file)
                    break
                
                # --- EXIT CHECK 2: Thesis invalidation ---
                prices = fetch_candles_for_rsi(coin, TRADE_API_URL)
                if prices:
                    rsi = calculate_rsi(prices)
                    if rsi and rsi < THESIS_INVALIDATION_RSI and current_price < entry:
                        print(f"\n  [EXIT] THESIS INVALIDATED — RSI {rsi:.1f} < {THESIS_INVALIDATION_RSI} and price below entry")
                        self_close_position(exchange, info, account_address, coin, current_price, entry, size, pnl, state_file)
                        break
                
                # Save state each cycle
                save_state(state, state_file)
                
            except Exception as e:
                print(f"  [!] Cycle error: {e}")
            
            time.sleep(CHECK_INTERVAL)
    
    except KeyboardInterrupt:
        print(f"\n[*] Bot stopped by user.")
        if state.get("in_position"):
            pnl_pct = ((current_price - state["entry_price"]) / state["entry_price"]) * 100
            print(f"  [WARNING] {coin} position still open: ${current_price:.6f} ({pnl_pct:+.1f}%)")
            print(f"  State saved. Restart this script to resume monitoring.")


def self_close_position(exchange, info, account_address, coin, current_price, entry, size, pnl, state_file):
    """Close the moonshot position and clean up state."""
    try:
        # Verify position exists on-chain
        user_state = info.user_state(account_address)
        actual_size = 0.0
        for pos in user_state.get("assetPositions", []):
            position = pos.get("position", {})
            if position.get("coin") == coin:
                actual_size = float(position.get("szi", 0))
                break
        
        if actual_size <= 0:
            print(f"  [!] No position found on-chain for {coin}")
        else:
            sell_price = round_to_tick(current_price * 0.99)  # 1% slippage
            result = exchange.order(coin, False, actual_size, sell_price, {"limit": {"tif": "Ioc"}})
            print(f"  [RAW] {result}")
        
        pnl_pct = ((current_price - entry) / entry) * 100
        print(f"\n  {'='*50}")
        print(f"  MOONSHOT CLOSED: {coin}")
        print(f"  Entry: ${entry:.6f} | Exit: ${current_price:.6f}")
        print(f"  P&L: ${pnl:.2f} ({pnl_pct:+.1f}%)")
        print(f"  {'='*50}")
        
        # Clear state file
        state = {"coin": coin, "in_position": False, "closed_at": time.strftime("%Y-%m-%d %H:%M:%S"), "final_pnl": round(pnl, 2)}
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=4)
        
    except Exception as e:
        print(f"  [ERROR] Close failed: {e}")
        print(f"  Close manually on Hyperliquid UI!")


if __name__ == "__main__":
    main()
