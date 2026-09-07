import json
import os
import time
import math
import datetime
import requests
import eth_account

try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        load_dotenv()
except ImportError:
    pass

from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants

# ============================================================
#  FLOWSTATE AI TRADING BOT v2 — MAINNET (Multi-Coin)
#  Strategy: Option B — Pullback Entry + Trend Following
#  Platform: Hyperliquid Mainnet
# ============================================================

API_URL = "https://api.hyperliquid.xyz/info"

# --- Indicator Calculations ---

def calculate_ema(prices, window):
    if len(prices) < window: return None
    multiplier = 2 / (window + 1)
    ema = sum(prices[:window]) / window
    for price in prices[window:]:
        ema = (price - ema) * multiplier + ema
    return ema

def calculate_rsi(prices, window=14):
    if len(prices) < window + 1: return None
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
    if avg_loss == 0: return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculate_bollinger(prices, window=20, num_std=2):
    if len(prices) < window: return None, None, None
    recent = prices[-window:]
    mean = sum(recent) / window
    variance = sum((p - mean) ** 2 for p in recent) / window
    std_dev = math.sqrt(variance)
    upper = mean + (num_std * std_dev)
    lower = mean - (num_std * std_dev)
    return upper, mean, lower

def fetch_candles(coin, interval="1h", lookback_hours=100):
    end_time = int(time.time() * 1000)
    start_time = end_time - (lookback_hours * 3600 * 1000)
    payload = {"type": "candleSnapshot", "req": {"coin": coin, "interval": interval, "startTime": start_time, "endTime": end_time}}
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        candles = response.json()
        if not candles: return None
        return [{'high': float(c['h']), 'low': float(c['l']), 'close': float(c['c']), 'volume': float(c.get('v', 0))} for c in candles]
    except Exception as e:
        print(f"  [!] Candle fetch error for {coin}: {e}")
        return None


def round_to_tick(price):
    """Round price to 5 significant figures + cap decimal places for Hyperliquid."""
    if price <= 0:
        return price
    import math
    sig_figs = 5
    magnitude = math.floor(math.log10(abs(price)))
    factor = 10 ** (sig_figs - 1 - magnitude)
    rounded = round(price * factor) / factor
    # Cap decimal places based on price magnitude (Hyperliquid tick convention)
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

# --- Per-Coin Position Tracker ---

class CoinPosition:
    """Tracks the state of a single coin's position."""
    def __init__(self, coin):
        self.coin = coin
        self.entry_price = None
        self.stop_price = None
        self.peak_price = None
        self.peak_pnl = 0.0             # Track highest PnL in dollars
        self.position_size = None
        self.entry_time = None          # [IMPROVEMENT 6] Track when position opened
        self.in_position = False
        self.is_long = True             # [PHASE 4] Track if position is long or short


# --- Core Bot Logic ---

class TradingBot:
    def __init__(self, private_key, account_address, coins, size_multipliers=None, scan_modes=None):
        self.coins = coins  # List of coin tickers
        self.wallet = eth_account.Account.from_key(private_key)
        self.account_address = account_address
        self.info = Info(constants.MAINNET_API_URL, skip_ws=True)
        self.exchange = Exchange(self.wallet, constants.MAINNET_API_URL, account_address=account_address)
        
        # Strategy parameters
        self.leverage = 3
        self.risk_per_trade = 0.02       # 2% of capital per trade
        self.stop_loss_pullback = 0.04   # 4% stop for pullback entries
        self.stop_loss_momentum = 0.03   # 3% stop for momentum entries (room to survive chop)
        self.stop_loss_deep_value = 0.05  # 5% stop for deep value entries (oversold bounces)
        self.daily_loss_limit = 0.10     # 10% daily kill switch
        self.trailing_retracement = 0.50 # 50% trailing stop
        # NEW: Trail floor + entry edge filter (added to fix no-edge trades and tiny-peak whipsaws)
        self.min_peak_pnl_for_trail = 1.50   # Don't activate trail until peak clears $1.50 (~3x round-trip fees)
        self.min_reward_distance = 0.012     # Skip chop entry if upper BB is < 1.2% away from price
        self.max_concurrent = len(coins) # Max simultaneous positions
        
        # [IMPROVEMENT 1] Min gain before trailing activates (use fixed stop until then)
        self.min_gain_for_trail = 0.015  # 1.5% gain required before trailing stop kicks in
        
        # [IMPROVEMENT 2] Cooldown after stop-out (seconds)
        self.cooldown_seconds = 3600     # 60 minutes (was 30 — increased to avoid chop)
        
        # [IMPROVEMENT 3] Max re-entries per coin per time window
        self.max_entries_per_window = 3  # Max 3 entries
        self.entry_window_seconds = 7200 # per 2-hour window
        
        # [IMPROVEMENT 6] Time-based exit & Compounding Rules
        self.max_hold_hours = 4                 # Close if no 1.5% gain after 4 hours
        self.compounding_max_hold_hours = 24.0 # Max 24h hold for profitable trades to release capital for larger sizing
        self.compounding_profit_target_pct = 0.50 # 50% profit target to lock gains and scale position size
        
        self.approved_for_entry = []     # Tracks coins currently allowed for NEW entries
        
        # Per-coin size multipliers (1.0 = full, 0.5 = half position)
        self.size_multipliers = size_multipliers or {}
        self.scan_modes = scan_modes or {}
        
        # Per-coin state tracking
        self.positions = {coin: CoinPosition(coin) for coin in coins}
        
        # [IMPROVEMENT 2 & 3] Cooldown and re-entry tracking
        self.last_stopout_time = {coin: 0 for coin in coins}   # timestamp of last stop-out
        self.entry_timestamps = {coin: [] for coin in coins}   # list of entry timestamps
        self.coin_daily_losses = {coin: 0 for coin in coins}   # [v3.2] per-coin daily loss counter
        
        # Global state
        self.daily_pnl = 0.0
        self.starting_balance = None
        
        # [IMPROVEMENT 5] Weekend mode detection
        self.is_weekend = datetime.datetime.utcnow().weekday() in (5, 6)  # Sat=5, Sun=6

        # Get szDecimals for each coin from Hyperliquid meta
        self.coin_decimals = {}
        try:
            meta = self.info.meta()
            for asset in meta.get("universe", []):
                self.coin_decimals[asset["name"]] = asset["szDecimals"]
        except Exception as e:
            print(f"[!] Error fetching size decimals: {e}")

        # Persistent daily kill switch state
        self.kill_state_file = os.path.join(os.path.dirname(__file__), "..", "data", "daily_kill_state.json")
        self.kill_switch_triggered_today = False
        self.load_daily_kill_state()
        
        print(f"[*] Bot initialized for {', '.join(coins)} on MAINNET")
        print(f"[*] Wallet: {self.wallet.address}")
        print(f"[*] Max concurrent positions: {self.max_concurrent}")
        print(f"[*] Min gain before trailing: {self.min_gain_for_trail*100}%")
        print(f"[*] Cooldown after stop-out: {self.cooldown_seconds//60} min")
        print(f"[*] Max entries per coin: {self.max_entries_per_window} per {self.entry_window_seconds//3600}h")
        print(f"[*] Deep Value mode: RSI < 25 + EMA50 slope rising (5% stop)")
        if self.is_weekend:
            print(f"[*] WEEKEND MODE: Stricter entry conditions active")
        for coin in coins:
            mult = self.size_multipliers.get(coin, 1.0)
            if mult != 1.0:
                print(f"[*] {coin}: {mult}x position size (half position)")
        
    def get_account_balance(self):
        """Get total equity: perps account value + spot USDC."""
        try:
            total = 0.0
            
            # Perps equity (includes margin + unrealized P&L)
            user_state = self.info.user_state(self.account_address)
            perps_bal = float(user_state.get("marginSummary", {}).get("accountValue", 0))
            total += perps_bal
            
            # Spot USDC balance (remaining cash not in margin)
            spot_state = self.info.spot_user_state(self.account_address)
            for balance in spot_state.get("balances", []):
                if balance.get("coin") == "USDC":
                    total += float(balance.get("total", 0))
            
            return total if total > 0 else 0.0
        except Exception as e:
            print(f"[!] Balance check error (API hiccup, retrying next cycle): {e}")
            return -1  # Return -1 to signal API error, not zero balance
    
    def get_current_price(self, coin):
        try:
            all_mids = self.info.all_mids()
            return float(all_mids.get(coin, 0))
        except:
            return 0.0
    
    def get_peak_price_since_entry(self, coin, entry_price, is_long):
        """Fetch historical candles since entry to reconstruct the peak price."""
        try:
            fills = self.info.user_fills(self.account_address)
            entry_time_ms = None
            for fill in fills:
                is_fill_long = fill.get("dir", "").lower() == "open long"
                if fill.get("coin") == coin and is_fill_long == is_long:
                    entry_time_ms = fill.get("time")
                    break
            
            if not entry_time_ms:
                # Fallback: look back 48 hours
                entry_time_ms = int((time.time() - 48 * 3600) * 1000)
                
            # Fetch hourly candles from entry time to now
            payload = {
                "type": "candleSnapshot",
                "req": {
                    "coin": coin,
                    "interval": "1h",
                    "startTime": entry_time_ms,
                    "endTime": int(time.time() * 1000)
                }
            }
            r = requests.post("https://api.hyperliquid.xyz/info", json=payload)
            candles = r.json()
            
            prices = [entry_price]
            for c in candles:
                prices.append(float(c['h'] if is_long else c['l']))
                
            # Current mid-price as well
            current_price = self.get_current_price(coin)
            if current_price > 0:
                prices.append(current_price)
                
            peak = max(prices) if is_long else min(prices)
            print(f"  [*] Reconstructed peak price for {coin} since entry: ${peak:.4f}")
            return peak
        except Exception as e:
            print(f"  [!] Failed to reconstruct peak price for {coin}: {e}")
            return entry_price

    def get_entry_time_from_fills(self, coin):
        """Fetch actual fill timestamp for position from Hyperliquid user_fills API."""
        try:
            user_fills = self.info.user_fills(self.account_address)
            for fill in user_fills:
                if fill.get("coin") == coin:
                    fill_time = float(fill.get("time", 0)) / 1000.0
                    if fill_time > 0:
                        return fill_time
        except Exception as e:
            print(f"  [!] Fills lookup error for {coin}: {e}")
        # Default to 48 hours ago if fill lookup fails, so old restored positions are evaluated as mature
        return time.time() - 172800.0

    def check_existing_positions(self):
        try:
            user_state = self.info.user_state(self.account_address)
            positions = user_state.get("assetPositions", [])
            for pos in positions:
                position = pos.get("position", {})
                coin = position.get("coin")
                size = float(position.get("szi", 0))
                if size != 0:
                    # Dynamically add the coin to monitoring if we have an active on-chain position
                    if coin not in self.positions:
                        print(f"[*] Dynamically adding active on-chain position coin to monitoring: {coin}")
                        self.coins.append(coin)
                        self.positions[coin] = CoinPosition(coin)
                        self.last_stopout_time[coin] = 0
                        self.entry_timestamps[coin] = []
                        self.coin_daily_losses[coin] = 0
                        
                    p = self.positions[coin]
                    p.in_position = True
                    p.is_long = (size > 0)
                    p.entry_price = float(position.get("entryPx", 0))
                    p.position_size = abs(size)
                    p.peak_price = self.get_peak_price_since_entry(coin, p.entry_price, p.is_long)
                    
                    # Reconstruct stop loss based on the peak price achieved
                    if p.is_long:
                        p.stop_price = round(p.entry_price * (1 - self.stop_loss_pullback), 6)
                        gain_pct = (p.peak_price - p.entry_price) / p.entry_price
                        if gain_pct >= self.min_gain_for_trail:
                            gain = p.peak_price - p.entry_price
                            new_stop = p.entry_price + (gain * self.trailing_retracement)
                            if new_stop > p.stop_price:
                                p.stop_price = new_stop
                    else:
                        p.stop_price = round(p.entry_price * (1 + self.stop_loss_pullback), 6)
                        gain_pct = (p.entry_price - p.peak_price) / p.entry_price
                        if gain_pct >= self.min_gain_for_trail:
                            gain = p.entry_price - p.peak_price
                            new_stop = p.entry_price - (gain * self.trailing_retracement)
                            if new_stop < p.stop_price:
                                p.stop_price = new_stop
                                
                    p.entry_time = self.get_entry_time_from_fills(coin)
                    hours_held = (time.time() - p.entry_time) / 3600
                    m_str = "LONG" if p.is_long else "SHORT"
                    print(f"[*] Found existing {m_str} position: {abs(size)} {coin} @ ${p.entry_price} (stop: ${p.stop_price:.4f}, held: {hours_held:.1f}h)")
        except Exception as e:
            print(f"[!] Error checking positions: {e}")
    
    def active_position_count(self):
        return sum(1 for p in self.positions.values() if p.in_position)
    
    def check_cooldown(self, coin):
        """[IMPROVEMENT 2] Check if coin is in cooldown after a stop-out."""
        elapsed = time.time() - self.last_stopout_time[coin]
        if elapsed < self.cooldown_seconds:
            remaining = int(self.cooldown_seconds - elapsed)
            print(f"  [{coin}] COOLDOWN: {remaining//60}m {remaining%60}s remaining after stop-out")
            return True
        return False
    
    def check_entry_limit(self, coin):
        """[IMPROVEMENT 3] Check if max entries per time window exceeded."""
        now = time.time()
        # Clean old entries outside the window
        self.entry_timestamps[coin] = [
            t for t in self.entry_timestamps[coin] 
            if now - t < self.entry_window_seconds
        ]
        if len(self.entry_timestamps[coin]) >= self.max_entries_per_window:
            window_hrs = self.entry_window_seconds // 3600
            print(f"  [{coin}] MAX ENTRIES: {self.max_entries_per_window} entries in last {window_hrs}h — locked out")
            return True
        return False
    
    def check_volume_filter(self, candles, coin=""):
        """[IMPROVEMENT 4] Check if current volume is above 20-period average."""
        volumes = [c.get('volume', 0) for c in candles]
        if not volumes or all(v == 0 for v in volumes):
            return True  # If no volume data available, skip the filter
        recent_vols = volumes[-20:] if len(volumes) >= 20 else volumes
        avg_vol = sum(recent_vols) / len(recent_vols)
        current_vol = volumes[-1]
        if avg_vol > 0 and current_vol < avg_vol * 0.5:
            print(f"  [{coin} VOLUME] Current volume {current_vol:.0f} is below 50% of avg ({avg_vol:.0f}) — skipping")
            return False
        return True
    
    def reload_approved_pairs(self):
        """[IMPROVEMENT 7] Regime Transition Handling. Reloads approved pairs mid-run.
        If regime flips, old coins fall off this list. We manage existing trades, but freeze new ones."""
        approved_file = os.path.join(os.path.dirname(__file__), "..", "data", "final_approved_pairs.json")
        if os.path.exists(approved_file):
            try:
                with open(approved_file, 'r') as f:
                    approved = json.load(f)
                    self.approved_for_entry = [p['coin'] for p in approved] if approved else []
                    if approved:
                        for p in approved:
                            self.scan_modes[p['coin']] = p.get('metrics', {}).get('scan_mode', 'standard')
                            if p['coin'] not in self.coins:
                                self.coins.append(p['coin'])
                                self.positions[p['coin']] = CoinPosition(p['coin'])
                                self.last_stopout_time[p['coin']] = 0
                                self.entry_timestamps[p['coin']] = []
                                self.coin_daily_losses[p['coin']] = 0
            except Exception as e:
                print(f"  [!] Failed to reload approved pairs: {e}")
                
    def evaluate_entry(self, coin):
        """Check entry conditions. Returns 'pullback', 'momentum', or None."""
        
        # [v3.2] Per-coin daily loss limit — bench after 2 stops
        if self.coin_daily_losses.get(coin, 0) >= 2:
            print(f"  [{coin}] BENCHED: {self.coin_daily_losses[coin]} losses today — sitting this one out until tomorrow")
            return None

        # [IMPROVEMENT 7] Regime Transition Freeze
        if coin not in self.approved_for_entry:
            return None
            
        # [IMPROVEMENT 2] Cooldown check
        if self.check_cooldown(coin):
            return None
        
        # [IMPROVEMENT 3] Max re-entries check
        if self.check_entry_limit(coin):
            return None
        
        candles = fetch_candles(coin)
        if not candles or len(candles) < 50:
            print(f"  [{coin}] Not enough candle data")
            return None
        
        # Get Regime/Scan Mode
        scan_mode = self.scan_modes.get(coin, "standard")
        if scan_mode == "bear_short":
            # Simple trigger: if price bounces back to EMA21, short it
            prices = [c['close'] for c in candles]
            current_price = prices[-1]
            ema21 = calculate_ema(prices, 21)
            if ema21 and current_price >= (ema21 * 0.99): 
                print(f"  [SIGNAL] SHORT ENTRY for {coin} (Hit EMA21 resistance)")
                return "bear_short"
            return None
        elif scan_mode == "chop_opportunity":
            # Simple trigger: if price is in lower 35% of Bollinger Band channel, long it
            prices = [c['close'] for c in candles]
            current_price = prices[-1]
            bb_u, bb_m, bb_l = calculate_bollinger(prices, 20)
            bb_l_val = bb_l if bb_l else 0.0
            print(f"  [{coin}] Scanning (Chop)... Price: ${current_price:.4f} | BB Lower Support: ${bb_l_val:.4f}")
            if bb_u and bb_l and (bb_u - bb_l) > 0:
                bb_pos = (current_price - bb_l) / (bb_u - bb_l)
                if bb_pos <= 0.35:
                    print(f"  [SIGNAL] CHOP LONG ENTRY for {coin} (Lower channel pos: {bb_pos*100:.0f}%)")
                    return "chop_opportunity"
            return None
            
        # STANDARD / BULL LOGIC
        # [IMPROVEMENT 4] Volume filter (standard entries only — deep value bypasses this)
        if not self.check_volume_filter(candles, coin):
            return None
            
        prices = [c['close'] for c in candles]
        current_price = prices[-1]
        
        ema21 = calculate_ema(prices, 21)
        ema50 = calculate_ema(prices, 50)
        rsi = calculate_rsi(prices, 14)
        bb_upper, bb_mid, bb_lower = calculate_bollinger(prices, 20)
        
        if not all([ema21, ema50, rsi, bb_lower]):
            return None
        
        # Core trend check — [v3.2] HARD GATE: EMA21 must be ABOVE EMA50
        ema_trend_bullish = ema21 > ema50
        uptrend = current_price > ema21 > ema50
        distance_to_mid = abs(current_price - bb_mid) / bb_mid
        price_above_mid = current_price > bb_mid
        
        print(f"\n--- {coin} Analysis ---")
        print(f"  Price:  ${current_price:.4f}")
        print(f"  EMA21:  ${ema21:.4f}  |  EMA50: ${ema50:.4f}")
        print(f"  RSI:    {rsi:.1f}")
        print(f"  BB:     ${bb_lower:.4f} / ${bb_mid:.4f} / ${bb_upper:.4f}")
        print(f"  EMA Trend: {'BULLISH' if ema_trend_bullish else 'BEARISH'}  |  Uptrend: {'YES' if uptrend else 'NO'}  |  {distance_to_mid*100:.1f}% from mid BB")
        
        # [v3.2] HARD GATE: If EMA21 < EMA50, trend is bearish — NO entries allowed
        if not ema_trend_bullish:
            print(f"  [BLOCKED] {coin} — EMA21 < EMA50 (bearish cross). No entries until trend flips.")
            return None
        
        if not uptrend:
            print(f"  [WAIT] {coin} -- price below EMAs. Skipping.")
            return None
        
        # --- Overextension guard (blocks reckless momentum entries) ---
        bb_range = bb_upper - bb_lower if bb_upper and bb_lower else 0
        bb_position = (current_price - bb_lower) / bb_range if bb_range > 0 else 0.5
        lookback_prices = prices[-50:] if len(prices) >= 50 else prices
        lookback_low = min(lookback_prices)
        rally_from_low = ((current_price - lookback_low) / lookback_low * 100) if lookback_low > 0 else 0
        
        is_overextended = (rsi > 72 and bb_position > 0.85) or rally_from_low > 40
        if is_overextended:
            print(f"  [CAUTION] {coin} is overextended (RSI: {rsi:.1f}, BB pos: {bb_position*100:.0f}%, Rally: {rally_from_low:.0f}% from low)")
            print(f"  [WAIT] Only pullback entries allowed on overextended coins.")
            if rsi < 55 and distance_to_mid <= 0.02:
                print(f"  [SIGNAL] PULLBACK entry on extended {coin}! (RSI dipped to {rsi:.1f})")
                return "pullback"
            return None
        
        # [IMPROVEMENT 5] Weekend mode — stricter thresholds
        pullback_rsi_threshold = 45 if self.is_weekend else 55
        momentum_rsi_low = 55
        momentum_rsi_high = 70 if self.is_weekend else 78
        
        # MODE 1: Pullback Entry (safer, wider stop)
        if rsi < pullback_rsi_threshold and distance_to_mid <= 0.02:
            mode_label = "PULLBACK" + (" [WEEKEND]" if self.is_weekend else "")
            print(f"  [SIGNAL] {mode_label} entry for {coin}! (RSI: {rsi:.1f}, {distance_to_mid*100:.1f}% from mid)")
            return "pullback"
        
        # MODE 2: Momentum Entry (tighter stop)
        if momentum_rsi_low <= rsi <= momentum_rsi_high and price_above_mid and distance_to_mid <= 0.05:
            mode_label = "MOMENTUM" + (" [WEEKEND]" if self.is_weekend else "")
            print(f"  [SIGNAL] {mode_label} entry for {coin}! (RSI: {rsi:.1f}, {distance_to_mid*100:.1f}% above mid)")
            return "momentum"
        
        print(f"  [WAIT] {coin} -- RSI {rsi:.1f}, {distance_to_mid*100:.1f}% from mid. No signal.")
        return None
    
    def open_position(self, coin, entry_mode="pullback"):
        """Place a buy order for a specific coin."""
        balance = self.get_account_balance()
        if balance <= 0:
            print(f"[!] No balance available for {coin}")
            return False
            
        current_price = self.get_current_price(coin)
        if current_price <= 0:
            return False
        
        # Select stop loss based on entry mode
        if entry_mode == "deep_value":
            stop_pct = self.stop_loss_deep_value
        elif entry_mode == "momentum":
            stop_pct = self.stop_loss_momentum
        else:
            stop_pct = self.stop_loss_pullback
        
        # Position sizing: ALWAYS 100% all-in (no $100 cap — Joe's decision).
        # We never switch to a 2% risk model. All-in until further notice.
        multiplier = self.size_multipliers.get(coin, 1.0)
        raw_size = (balance * 0.98 * multiplier) / current_price
        risk_amount = raw_size * current_price * stop_pct
        print(f"  [*] ALL-IN MODE: ${balance * 0.98:.2f} USD → {raw_size:.6f} {coin}")
        
        # Round size appropriately based on szDecimals
        sz_dec = self.coin_decimals.get(coin, 0)
        size = round(raw_size, sz_dec)
        if sz_dec == 0:
            size = int(size)
        if size <= 0:
            print(f"[!] Calculated position size too small for {coin} (raw: {raw_size}, decimals: {sz_dec})")
            return False
        
        is_long = (entry_mode != "bear_short")
        
        p = self.positions[coin]
        p.is_long = is_long
        p.stop_price = round(current_price * (1 - stop_pct), 4) if is_long else round(current_price * (1 + stop_pct), 4)
        
        try:
            # Set leverage first (DISABLED for Unified Accounts: explicitly setting leverage forces isolated margin and causes 'Insufficient Margin' errors)
            # self.exchange.update_leverage(self.leverage, coin)
            
            # Add 0.5% slippage
            limit_price = round_to_tick(current_price * 1.005) if is_long else round_to_tick(current_price * 0.995)
            
            print(f"\n[TRADE] Opening {coin} [{entry_mode.upper()}]:")
            print(f"  Size:     {size} ({multiplier}x sizing)")
            print(f"  Price:    ${current_price} (limit: ${limit_price})")
            print(f"  Stop:     ${p.stop_price} ({stop_pct*100}% stop)")
            print(f"  Risk:     ${risk_amount:.2f} ({self.risk_per_trade*100}% of ${balance:.2f})")
            
            # Place order with IOC (immediate-or-cancel)
            order_result = self.exchange.order(
                coin,
                is_long,       # True = Buy/Long, False = Sell/Short
                size,
                limit_price,
                {"limit": {"tif": "Ioc"}}
            )
            
            print(f"  [RAW] Response: {order_result}")
            
            # Check if the order actually filled
            response = order_result.get("response", {}) if isinstance(order_result, dict) else {}
            data = response.get("data", {}) if isinstance(response, dict) else {}
            statuses = data.get("statuses", []) if isinstance(data, dict) else []
            
            # Check if the order actually filled or is resting
            has_fill = any("filled" in str(s).lower() or "resting" in str(s).lower() for s in statuses)
            
            if not has_fill:
                print(f"  [REJECTED] Order was not filled or resting: {statuses if statuses else order_result}")
                return False
            
            p.entry_price = current_price
            p.peak_price = current_price
            p.peak_pnl = 0.0
            p.position_size = size
            p.entry_time = time.time()   # [IMPROVEMENT 6] Track entry time
            p.in_position = True
            
            # [IMPROVEMENT 3] Track entry timestamp
            self.entry_timestamps[coin].append(time.time())
            entries_used = len(self.entry_timestamps[coin])
            print(f"  [FILLED] Position opened successfully! (Entry {entries_used}/{self.max_entries_per_window} in window)")

            # ── NATIVE STOP-LOSS: Place on Hyperliquid's servers immediately ─────────
            # This stop lives on HL's exchange 24/7 regardless of VPS state.
            # Even if this bot crashes or the VPS reboots, Hyperliquid fires the stop.
            stop_price = round_to_tick(current_price * (1 - stop_pct))
            stop_limit  = round_to_tick(stop_price * 0.90)  # 10% below trigger = guarantee fill
            try:
                stop_result = self.exchange.order(
                    coin,
                    not is_long,   # sell to close a long, buy to close a short
                    size,
                    stop_limit,
                    {"trigger": {"triggerPx": stop_price, "isMarket": True, "tpsl": "sl"}},
                    reduce_only=True
                )
                stop_resp     = stop_result.get("response", {}) if isinstance(stop_result, dict) else {}
                stop_data     = stop_resp.get("data", {}) if isinstance(stop_resp, dict) else {}
                stop_statuses = stop_data.get("statuses", []) if isinstance(stop_data, dict) else []
                stop_ok = any(
                    "resting" in str(s).lower() or "success" in str(s).lower()
                    for s in stop_statuses
                )
                if stop_ok:
                    print(f"  [✅ NATIVE STOP] Active on HL at ${stop_price} (-{stop_pct*100:.0f}%)")
                else:
                    print(f"  [⚠️ NATIVE STOP] Uncertain response — verify on HL UI: {stop_statuses}")
            except Exception as se:
                print(f"  [❌ NATIVE STOP] Placement FAILED: {se}. verify_native_stop() will retry.")

            return True
            
        except Exception as e:
            print(f"  [ERROR] Order failed for {coin}: {e}")
            return False
    
    def verify_native_stop(self, coin):
        """Verify a native Hyperliquid trigger stop-loss order exists for this position.
        
        Called every 60s at the start of manage_position.
        If the stop is missing (never placed, VPS restarted, HL cancelled it),
        re-places it immediately using the actual on-chain position size.
        
        Why: The native stop lives on HL's exchange servers, not in this bot.
        Even if this bot crashes and restarts, the stop should already be there.
        This method is the belt-and-suspenders safety net.
        """
        p = self.positions[coin]
        if not p.in_position or not p.entry_price or not p.position_size:
            return  # Nothing to protect
        
        try:
            # Query Hyperliquid for all open orders (frontend_open_orders includes trigger fields)
            open_orders = self.info.frontend_open_orders(self.account_address)
            
            # Look for our stop-loss trigger order for this coin
            stop_found = any(
                order.get("coin") == coin
                and order.get("side") == "A"          # A = Ask = Sell (closing a long)
                and order.get("isTrigger", False)     # Must be a trigger order
                and order.get("reduceOnly", False)    # Must be reduce-only (safety check)
                for order in open_orders
            )
            
            if stop_found:
                print(f"  [{coin}] ✅ Native stop verified active on Hyperliquid")
                return  # All good
            
            # Stop is missing — re-place it
            print(f"  [{coin}] ⚠️ Native stop MISSING! Re-placing now...")
            
            # Get actual on-chain position size (may differ from p.position_size if partially filled)
            actual_size = p.position_size  # fallback
            try:
                user_state = self.info.user_state(self.account_address)
                for pos in user_state.get("assetPositions", []):
                    pd = pos.get("position", {})
                    if pd.get("coin") == coin:
                        on_chain_size = abs(float(pd.get("szi", 0)))
                        if on_chain_size > 0:
                            actual_size = on_chain_size
                        break
            except Exception as sz_err:
                print(f"  [{coin}] Could not fetch on-chain size: {sz_err}. Using cached size.")
            
            stop_price = round_to_tick(p.entry_price * (1 - self.stop_loss_pullback))
            stop_limit = round_to_tick(stop_price * 0.90)
            
            result = self.exchange.order(
                coin,
                not p.is_long,  # sell to close long, buy to close short
                actual_size,
                stop_limit,
                {"trigger": {"triggerPx": stop_price, "isMarket": True, "tpsl": "sl"}},
                reduce_only=True
            )
            resp_statuses = result.get("response", {}).get("data", {}).get("statuses", [])
            if any("resting" in str(s).lower() or "success" in str(s).lower() for s in resp_statuses):
                print(f"  [{coin}] ✅ Native stop RE-PLACED at ${stop_price}")
            else:
                print(f"  [{coin}] ⚠️ Stop re-place response uncertain: {resp_statuses}")
        
        except Exception as e:
            print(f"  [{coin}] ❌ verify_native_stop error: {e}")

    def manage_position(self, coin):
        """Monitor open position — PnL-based trailing stop logic."""
        p = self.positions[coin]
        current_price = self.get_current_price(coin)
        if current_price <= 0:
            return

        # ── FIRST: Verify native HL stop order is active on exchange ──────────────
        # Re-places it automatically if missing (VPS restart, bot crash, HL cancellation).
        self.verify_native_stop(coin)
        
        # Calculate current PnL in dollars
        if p.is_long:
            current_pnl = (current_price - p.entry_price) * p.position_size
        else:
            current_pnl = (p.entry_price - current_price) * p.position_size
        
        # Update peak PnL
        if current_pnl > p.peak_pnl:
            p.peak_pnl = current_pnl
            if p.peak_pnl > 0:
                print(f"  [NEW PEAK] {coin} Peak PnL: ${p.peak_pnl:.2f}")
        
        # PnL trailing stop: only activates once peak PnL clears the noise floor
        # Below the floor, the original 4% stop loss governs the trade
        if p.peak_pnl >= self.min_peak_pnl_for_trail and current_pnl <= (p.peak_pnl * 0.50):
            print(f"\n[PNL TRAIL EXIT] {coin} PnL ${current_pnl:.2f} dropped to 50% of peak ${p.peak_pnl:.2f}")
            print(f"  Profit retained: ${current_pnl:.2f} | Given back: ${p.peak_pnl - current_pnl:.2f}")
            self.close_position(coin)
            self.last_stopout_time[coin] = time.time()
            return
        
        # Time-based & Compounding Exits
        if p.entry_time:
            hours_held = (time.time() - p.entry_time) / 3600
            gain_pct = ((current_price - p.entry_price) / p.entry_price) if p.is_long else ((p.entry_price - current_price) / p.entry_price)
            
            # [OPTION C - COMPOUNDING RULE 1] Milestone Target Exit (+50% profit target)
            if gain_pct >= self.compounding_profit_target_pct:
                print(f"\n[COMPOUND MILESTONE EXIT] {coin} reached +{gain_pct*100:.1f}% gain! Realizing ${current_pnl:.2f} profit to compound into next trade.")
                self.close_position(coin)
                self.last_stopout_time[coin] = time.time()
                return
            
            # [OPTION C - COMPOUNDING RULE 2] 24-Hour Profitable Hold Exit
            if hours_held >= self.compounding_max_hold_hours and gain_pct > 0:
                print(f"\n[24H COMPOUND EXIT] {coin} held {hours_held:.1f}h with +{gain_pct*100:.2f}% gain (${current_pnl:.2f}). Realizing equity to scale next position!")
                self.close_position(coin)
                self.last_stopout_time[coin] = time.time()
                return
            
            # [STALE POSITION EXIT] Held 4h+ without 1.5% gain
            if hours_held >= self.max_hold_hours and gain_pct < self.min_gain_for_trail:
                print(f"\n[TIME EXIT] {coin} held {hours_held:.1f}h with only {gain_pct*100:+.2f}% gain — closing stale position")
                self.close_position(coin)
                self.last_stopout_time[coin] = time.time()
                self.coin_daily_losses[coin] = self.coin_daily_losses.get(coin, 0) + 1
                print(f"  [{coin}] Daily losses: {self.coin_daily_losses[coin]}/2")
                return
        
        # Check stop loss
        stop_hit = (current_price <= p.stop_price) if p.is_long else (current_price >= p.stop_price)
        if stop_hit:
            print(f"\n[EXIT] {coin} Stop hit at ${current_price:.4f} (stop was ${p.stop_price:.4f})")
            self.close_position(coin)
            # [IMPROVEMENT 2] Record stop-out time for cooldown
            self.last_stopout_time[coin] = time.time()
            self.coin_daily_losses[coin] = self.coin_daily_losses.get(coin, 0) + 1
            print(f"  [{coin}] Daily losses: {self.coin_daily_losses[coin]}/2")
            return
        
        # Print P&L with time held
        hours_held = (time.time() - p.entry_time) / 3600 if p.entry_time else 0
        pnl_pct = ((current_price - p.entry_price) / p.entry_price) * 100 if p.is_long else ((p.entry_price - current_price) / p.entry_price) * 100
        print(f"  [{coin}] Price: ${current_price:.4f} | P&L: {pnl_pct:+.2f}% | Stop: ${p.stop_price:.4f} | Held: {hours_held:.1f}h/{self.max_hold_hours}h")
    
    def close_position(self, coin):
        """Close a specific coin's position. Verifies position exists on-chain first."""
        p = self.positions[coin]
        try:
            # SAFETY: Verify position actually exists on exchange before selling
            user_state = self.info.user_state(self.account_address)
            actual_size = 0.0
            for pos in user_state.get("assetPositions", []):
                position = pos.get("position", {})
                if position.get("coin") == coin:
                    actual_size = float(position.get("szi", 0))
                    break
            
            # Verify position exists in the correct direction
            is_valid_dir = (p.is_long and actual_size > 0) or (not p.is_long and actual_size < 0)
            if not is_valid_dir:
                dir_str = "LONG" if p.is_long else "SHORT"
                print(f"  [SAFETY] No {dir_str} position found on-chain for {coin} (actual size: {actual_size}) — skipping close to prevent accidental side position")
                p.in_position = False
                p.entry_price = None
                p.stop_price = None
                p.peak_price = None
                p.position_size = None
                return False
            
            current_price = self.get_current_price(coin)
            close_price = round_to_tick(current_price * 0.995) if p.is_long else round_to_tick(current_price * 1.005)
            close_size = abs(actual_size)
            
            order_result = self.exchange.order(
                coin,
                not p.is_long,  # True if closing a short (buy), False if closing a long (sell)
                close_size,
                close_price,
                {"limit": {"tif": "Ioc"}}
            )
            
            # Check if the close order actually filled
            response = order_result.get("response", {})
            data = response.get("data", {})
            statuses = data.get("statuses", [])
            has_fill = any("filled" in str(s).lower() or "resting" in str(s).lower() for s in statuses)
            
            if not has_fill:
                print(f"  [REJECTED] Close order was not filled: {statuses}")
                return False
            
            pnl = (current_price - p.entry_price) * close_size if p.is_long else (p.entry_price - current_price) * close_size
            pnl_pct = ((current_price - p.entry_price) / p.entry_price) * 100 if p.is_long else ((p.entry_price - current_price) / p.entry_price) * 100
            self.daily_pnl += pnl
            
            print(f"  [CLOSED] {coin} | P&L: ${pnl:.2f} ({pnl_pct:+.2f}%)")
            print(f"  [DAILY]  Total daily P&L: ${self.daily_pnl:.2f}")
            
            # HODL Harvester: send 30% of profits to the HODL bot
            if pnl > 0:
                hodl_amount = pnl * 0.30
                hodl_file = os.path.join(os.path.dirname(__file__), "..", "data", "hodl_deposits.json")
                try:
                    existing = []
                    if os.path.exists(hodl_file):
                        with open(hodl_file, 'r') as f:
                            existing = json.load(f)
                    existing.append({
                        "amount": round(hodl_amount, 2),
                        "source": coin,
                        "pnl": round(pnl, 2),
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
                    with open(hodl_file, 'w') as f:
                        json.dump(existing, f, indent=4)
                    print(f"  [HODL] ${hodl_amount:.2f} (30% of profit) deposited for BTC/SOL accumulation")
                except Exception as e:
                    print(f"  [!] HODL deposit write error: {e}")
            
            # Reset coin state
            p.in_position = False
            p.entry_price = None
            p.stop_price = None
            p.peak_price = None
            p.peak_pnl = 0.0
            p.position_size = None
            
            return True
        except Exception as e:
            print(f"  [ERROR] Close failed for {coin}: {e}")
            return False
    
    def load_daily_kill_state(self):
        try:
            if os.path.exists(self.kill_state_file):
                with open(self.kill_state_file, 'r') as f:
                    state = json.load(f)
                    current_day = str(datetime.datetime.utcnow().date())
                    if state.get("date") == current_day and state.get("kill_switch_triggered"):
                        self.kill_switch_triggered_today = True
                        print(f"[*] Persistent Kill Switch loaded: Halted for today ({current_day})")
        except Exception as e:
            print(f"[!] Error loading daily kill state: {e}")

    def save_daily_kill_state(self, triggered):
        try:
            current_day = str(datetime.datetime.utcnow().date())
            os.makedirs(os.path.dirname(self.kill_state_file), exist_ok=True)
            with open(self.kill_state_file, 'w') as f:
                json.dump({"date": current_day, "kill_switch_triggered": triggered}, f, indent=4)
        except Exception as e:
            print(f"[!] Error saving daily kill state: {e}")

    def check_kill_switch(self):
        """10% daily drawdown = full stop. Only counts BOT-managed P&L, ignoring external positions (moonshots)."""
        if self.kill_switch_triggered_today:
            return True
            
        if self.starting_balance and self.starting_balance > 0:
            # Calculate bot-specific P&L (realized daily + unrealized on bot positions)
            bot_unrealized = 0.0
            for coin, p in self.positions.items():
                if p.in_position:
                    current_price = self.get_current_price(coin)
                    if current_price > 0:
                        unrlzd = (current_price - p.entry_price) * p.position_size if p.is_long else (p.entry_price - current_price) * p.position_size
                        bot_unrealized += unrlzd
            
            # Total bot P&L = realized today + current unrealized
            bot_total_pnl = self.daily_pnl + bot_unrealized
            
            # Drawdown as % of starting balance
            if bot_total_pnl < 0:
                drawdown = abs(bot_total_pnl) / self.starting_balance
                if drawdown >= self.daily_loss_limit:
                    print(f"\n[KILL SWITCH] Bot daily drawdown {drawdown*100:.1f}% exceeds {self.daily_loss_limit*100}% limit")
                    print(f"   Bot P&L: ${bot_total_pnl:.2f} (Realized: ${self.daily_pnl:.2f} + Unrealized: ${bot_unrealized:.2f})")
                    self.kill_switch_triggered_today = True
                    self.save_daily_kill_state(True)
                    # Close all bot-managed positions
                    for coin, p in self.positions.items():
                        if p.in_position:
                            self.close_position(coin)
                    return True
        return False
    
    def run(self, check_interval_seconds=60):
        """Main bot loop — cycles through all coins."""
        print("="*60)
        print(" FLOWSTATE AI TRADING BOT v2 — MAINNET (Multi-Coin)")
        print("="*60)
        
        self.starting_balance = self.get_account_balance()
        if self.starting_balance <= 0:
            print("[!] No balance on mainnet. Please deposit USDC first.")
            return
            
        print(f"[*] Account balance: ${self.starting_balance:.2f}")
        print(f"[*] Monitoring: {', '.join(self.coins)}")
        print(f"[*] Strategy: Dual-Mode (Pullback + Momentum)")
        print(f"[*] Check interval: {check_interval_seconds}s")
        print(f"[*] Press Ctrl+C to stop the bot\n")
        
        # Check for existing positions
        self.check_existing_positions()
        
        try:
            while True:
                # [v3.2] Daily reset check — reset loss counters at midnight UTC
                current_day = datetime.datetime.utcnow().date()
                if not hasattr(self, '_last_reset_day') or self._last_reset_day != current_day:
                    self._last_reset_day = current_day
                    self.daily_pnl = 0.0
                    for coin in self.coins:
                        self.coin_daily_losses[coin] = 0
                    self.is_weekend = datetime.datetime.utcnow().weekday() in (5, 6)
                    self.kill_switch_triggered_today = False
                    self.save_daily_kill_state(False)
                    print(f"\n  [DAILY RESET] New day — losses reset, PNL reset, kill switch cleared, weekend={self.is_weekend}")

                # Reload approved pairs for regime transitions
                self.reload_approved_pairs()
                
                # Kill switch check
                if self.check_kill_switch():
                    print("[*] Bot currently halted by kill switch. Sleep-waiting for next day reset...")
                    time.sleep(check_interval_seconds)
                    continue
                
                # Cycle through each coin
                for coin in self.coins:
                    p = self.positions[coin]
                    
                    if p.in_position:
                        self.manage_position(coin)
                    else:
                        # Only open new positions if under the max
                        if self.active_position_count() < self.max_concurrent:
                            entry_mode = self.evaluate_entry(coin)
                            if entry_mode:
                                self.open_position(coin, entry_mode)
                
                # Summary line
                active = [c for c, p in self.positions.items() if p.in_position]
                if active:
                    print(f"\n  [ACTIVE] Positions: {', '.join(active)} | Daily P&L: ${self.daily_pnl:.2f}")
                
                time.sleep(check_interval_seconds)
                
        except KeyboardInterrupt:
            print("\n[*] Bot stopped by user.")
            for coin, p in self.positions.items():
                if p.in_position:
                    print(f"  [WARNING] Open position in {coin}: Entry ${p.entry_price:.4f} | Size {p.position_size}")


def main():
    private_key = os.environ.get("HL_PRIVATE_KEY")
    account_address = os.environ.get("HL_ACCOUNT_ADDRESS")
    
    if not private_key or not account_address:
        print("="*60)
        print(" FLOWSTATE AI TRADING BOT v2 — SETUP")
        print("="*60)
        print()
        print("Set these environment variables in PowerShell:")
        print()
        print('  $env:HL_PRIVATE_KEY="0xYourPrivateKeyHere"')
        print('  $env:HL_ACCOUNT_ADDRESS="0xYourAccountAddressHere"')
        print()
        print("Then run: python master_trader.py")
        return
    
    # Load approved coins from FA Agent output
    approved_file = os.path.join(os.path.dirname(__file__), "..", "data", "final_approved_pairs.json")
    coins = ["BIO"]  # Default fallback
    size_multipliers = {}  # Per-coin position size multipliers
    
    scan_modes = {}
    if os.path.exists(approved_file):
        with open(approved_file, 'r') as f:
            approved = json.load(f)
            if approved:
                coins = [p['coin'] for p in approved]
                for p in approved:
                    mult = p.get('size_multiplier', 1.0)
                    mode = p.get('metrics', {}).get('scan_mode', 'standard')
                    if mult != 1.0:
                        size_multipliers[p['coin']] = mult
                    scan_modes[p['coin']] = mode
                print(f"[*] Loaded {len(coins)} approved coins from FA Agent: {', '.join(coins)}")
    
    bot = TradingBot(private_key, account_address, coins, size_multipliers, scan_modes)
    bot.approved_for_entry = coins.copy()
    bot.run(check_interval_seconds=60)


if __name__ == "__main__":
    main()
