import json
import os
import math
import time
import requests
import eth_account
from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants

# ============================================================
#  FLOWSTATE AI HODL BOT — BTC/SOL Accumulation + Rebalancing
#
#  Strategy:
#  1. Always LONG both BTC and SOL (you hold them)
#  2. Monitor BTC/SOL ratio for rebalancing signals
#  3. Rebalance allocation when ratio signals opportunity
#  4. Absorb 30% of core bot profits as new deposits
#  5. Stack grows over time: appreciation + rebalancing + deposits
#
#  This bot runs INDEPENDENTLY from the core altcoin bot.
# ============================================================

API_URL = "https://api.hyperliquid.xyz/info"

# --- Configuration ---
INITIAL_LEG_USD = 250        # $250 per coin at start ($500 total)
LEVERAGE = 1                 # No leverage — true HODL
CHECK_INTERVAL = 300         # 5 minutes
DEFAULT_ALLOCATION = 0.60    # 60/40 BTC/SOL baseline
REBALANCE_DRIFT = 0.10       # Rebalance when allocation drifts >10% from target
DAILY_LOSS_LIMIT = 0.10      # 10% kill switch (HODL bot P&L only)
DEPOSITS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "hodl_deposits.json")
STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "hodl_state.json")
LOCKFILE = os.path.join(os.path.dirname(__file__), "hodl_bot.lock")


# ============================================================
#  UTILITY FUNCTIONS
# ============================================================

def round_to_tick(price):
    """Round price to 5 significant figures (Hyperliquid tick convention)."""
    if price <= 0:
        return price
    sig_figs = 5
    magnitude = math.floor(math.log10(abs(price)))
    factor = 10 ** (sig_figs - 1 - magnitude)
    return round(price * factor) / factor


def fetch_candles(coin, interval="1h", lookback_hours=168):
    """Fetch 7 days of hourly candles."""
    end_time = int(time.time() * 1000)
    start_time = end_time - (lookback_hours * 3600 * 1000)
    payload = {
        "type": "candleSnapshot",
        "req": {"coin": coin, "interval": interval, "startTime": start_time, "endTime": end_time}
    }
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        candles = response.json()
        if not candles:
            return None
        return [{
            "timestamp": int(c["t"]),
            "close": float(c["c"]),
        } for c in candles]
    except Exception as e:
        print(f"  [!] Candle error for {coin}: {e}")
        return None


def calculate_ema(prices, window):
    if len(prices) < window:
        return None
    multiplier = 2 / (window + 1)
    ema = sum(prices[:window]) / window
    for price in prices[window:]:
        ema = (price - ema) * multiplier + ema
    return ema


def calculate_rsi(prices, window=14):
    if len(prices) < window + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i-1]
        gains.append(max(diff, 0))
        losses.append(max(-diff, 0))
    avg_gain = sum(gains[-window:]) / window
    avg_loss = sum(losses[-window:]) / window
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def build_ratio_series(btc_candles, sol_candles):
    """Build BTC/SOL ratio from aligned candle timestamps."""
    btc_by_time = {c["timestamp"]: c["close"] for c in btc_candles}
    sol_by_time = {c["timestamp"]: c["close"] for c in sol_candles}
    common = sorted(set(btc_by_time.keys()) & set(sol_by_time.keys()))
    ratios = []
    for t in common:
        if sol_by_time[t] > 0:
            ratios.append(btc_by_time[t] / sol_by_time[t])
    return ratios


# ============================================================
#  HODL BOT CLASS
# ============================================================

class HodlBot:
    def __init__(self):
        private_key = os.environ.get("HL_PRIVATE_KEY")
        account_address = os.environ.get("HL_ACCOUNT_ADDRESS")
        
        if not private_key or not account_address:
            raise ValueError("Set HL_PRIVATE_KEY and HL_ACCOUNT_ADDRESS")
        
        self.account_address = account_address
        self.wallet = eth_account.Account.from_key(private_key)
        self.info = Info(constants.MAINNET_API_URL, skip_ws=True)
        self.exchange = Exchange(self.wallet, constants.MAINNET_API_URL, account_address=account_address)
        
        # Position tracking
        self.btc_size = 0.0
        self.sol_size = 0.0
        self.btc_entry = 0.0
        self.sol_entry = 0.0
        self.total_invested = 0.0
        self.target_btc_pct = DEFAULT_ALLOCATION  # Dynamic — shifts with ratio signals
        self.daily_pnl = 0.0
        self.starting_balance = None
        self.rebalance_count = 0
        
        print(f"[HODL] BTC/SOL Accumulation Bot initialized on MAINNET")
        print(f"[HODL] Starting allocation: 60% BTC + 40% SOL")
        print(f"[HODL] Leverage: {LEVERAGE}x | Check: {CHECK_INTERVAL // 60}min")
    
    def get_prices(self):
        """Get current BTC and SOL prices."""
        try:
            all_mids = self.info.all_mids()
            return float(all_mids.get("BTC", 0)), float(all_mids.get("SOL", 0))
        except Exception as e:
            print(f"  [!] Price error: {e}")
            return 0, 0
    
    def get_account_balance(self):
        """Get total equity."""
        try:
            total = 0.0
            user_state = self.info.user_state(self.account_address)
            total += float(user_state.get("marginSummary", {}).get("accountValue", 0))
            spot_state = self.info.spot_user_state(self.account_address)
            for b in spot_state.get("balances", []):
                if b.get("coin") == "USDC":
                    total += float(b.get("total", 0))
            return total if total > 0 else 0.0
        except:
            return -1
    
    def get_on_chain_positions(self):
        """Get actual BTC and SOL position sizes from exchange."""
        try:
            user_state = self.info.user_state(self.account_address)
            btc = {"size": 0.0, "entry": 0.0, "upnl": 0.0}
            sol = {"size": 0.0, "entry": 0.0, "upnl": 0.0}
            
            for pos in user_state.get("assetPositions", []):
                p = pos.get("position", {})
                coin = p.get("coin")
                size = float(p.get("szi", 0))
                entry = float(p.get("entryPx", 0))
                upnl = float(p.get("unrealizedPnl", 0))
                
                if coin == "BTC":
                    btc = {"size": size, "entry": entry, "upnl": upnl}
                elif coin == "SOL":
                    sol = {"size": size, "entry": entry, "upnl": upnl}
            
            return btc, sol
        except Exception as e:
            print(f"  [!] Position check error: {e}")
            return None, None
    
    def analyze_ratio(self):
        """Analyze BTC/SOL ratio and return target BTC allocation (0.0 to 1.0)."""
        btc_candles = fetch_candles("BTC")
        sol_candles = fetch_candles("SOL")
        
        if not btc_candles or not sol_candles:
            return DEFAULT_ALLOCATION
        
        ratios = build_ratio_series(btc_candles, sol_candles)
        if len(ratios) < 50:
            return DEFAULT_ALLOCATION
        
        current_ratio = ratios[-1]
        ema21 = calculate_ema(ratios, 21)
        ema50 = calculate_ema(ratios, 50)
        rsi = calculate_rsi(ratios, 14)
        
        if not all([ema21, ema50, rsi]):
            return DEFAULT_ALLOCATION
        
        print(f"\n  - BTC/SOL Ratio Analysis ---")
        print(f"  Ratio:  {current_ratio:.4f}")
        print(f"  EMA21:  {ema21:.4f}  |  EMA50: {ema50:.4f}")
        print(f"  RSI:    {rsi:.1f}")
        
        # Determine target allocation based on ratio signals
        target = DEFAULT_ALLOCATION  # 60/40 baseline
        
        # BTC relatively strong (ratio rising) -> favor BTC
        if current_ratio > ema21 > ema50 and rsi > 55:
            target = 0.70  # 70% BTC / 30% SOL
            print(f"  [SIGNAL] BTC strong — target 70/30 BTC/SOL")
        
        # BTC extremely strong -> cap at 75%
        elif current_ratio > ema21 and rsi > 70:
            target = 0.75  # 75% BTC / 25% SOL
            print(f"  [SIGNAL] BTC dominant — target 75/25 BTC/SOL")
        
        # SOL relatively strong (ratio falling) -> favor SOL
        elif current_ratio < ema21 < ema50 and rsi < 45:
            target = 0.50  # 50% BTC / 50% SOL
            print(f"  [SIGNAL] SOL strong — target 50/50 BTC/SOL")
        
        # SOL extremely strong
        elif current_ratio < ema21 and rsi < 30:
            target = 0.40  # 40% BTC / 60% SOL
            print(f"  [SIGNAL] SOL dominant — target 40/60 BTC/SOL")
        
        else:
            print(f"  [NEUTRAL] No strong signal — maintaining {int(self.target_btc_pct*100)}/{int((1-self.target_btc_pct)*100)}")
            target = self.target_btc_pct  # Keep current target
        
        return target
    
    def initial_buy(self):
        """Buy initial BTC and SOL positions."""
        btc_price, sol_price = self.get_prices()
        if btc_price <= 0 or sol_price <= 0:
            print("[!] Cannot get prices for initial buy")
            return False
        
        btc_usd = INITIAL_LEG_USD * 2 * DEFAULT_ALLOCATION
        sol_usd = INITIAL_LEG_USD * 2 * (1 - DEFAULT_ALLOCATION)
        btc_size = round(btc_usd / btc_price, 5)
        sol_size = round(sol_usd / sol_price, 2)
        
        print(f"\n[HODL] Initial Buy:")
        print(f"  BTC: {btc_size} @ ${btc_price:.2f} (${btc_usd:.0f})")
        print(f"  SOL: {sol_size} @ ${sol_price:.2f} (${sol_usd:.0f})")
        
        try:
            self.exchange.update_leverage(LEVERAGE, "BTC")
            self.exchange.update_leverage(LEVERAGE, "SOL")
            
            # Buy BTC
            btc_limit = round_to_tick(btc_price * 1.005)
            btc_result = self.exchange.order(
                "BTC", True, btc_size, btc_limit,
                {"limit": {"tif": "Ioc"}}
            )
            btc_statuses = btc_result.get("response", {}).get("data", {}).get("statuses", [])
            btc_filled = any(isinstance(s, dict) and "filled" in s for s in btc_statuses)
            
            if not btc_filled:
                print(f"  [!] BTC buy failed: {btc_statuses}")
                return False
            print(f"  [FILLED] BTC: {btc_size} @ ${btc_price:.2f}")
            
            # Buy SOL
            sol_limit = round_to_tick(sol_price * 1.005)
            sol_result = self.exchange.order(
                "SOL", True, sol_size, sol_limit,
                {"limit": {"tif": "Ioc"}}
            )
            sol_statuses = sol_result.get("response", {}).get("data", {}).get("statuses", [])
            sol_filled = any(isinstance(s, dict) and "filled" in s for s in sol_statuses)
            
            if not sol_filled:
                print(f"  [!] SOL buy failed: {sol_statuses}")
                self.exchange.order(
                    "BTC", False, btc_size,
                    round_to_tick(btc_price * 0.995),
                    {"limit": {"tif": "Ioc"}}
                )
                return False
            print(f"  [FILLED] SOL: {sol_size} @ ${sol_price:.2f}")
            
            self.btc_size = btc_size
            self.sol_size = sol_size
            self.btc_entry = btc_price
            self.sol_entry = sol_price
            self.total_invested = btc_usd + sol_usd
            
            self.save_state()
            
            print(f"\n  [HODL] Initial positions established!")
            print(f"  Total invested: ${self.total_invested:.2f}")
            return True
            
        except Exception as e:
            print(f"  [ERROR] Initial buy failed: {e}")
            return False
    
    def rebalance(self, target_btc_pct):
        """Rebalance BTC/ETH allocation toward target."""
        btc_price, sol_price = self.get_prices()
        if btc_price <= 0 or sol_price <= 0:
            return
        
        # Current values
        btc_value = self.btc_size * btc_price
        sol_value = self.sol_size * sol_price
        total_value = btc_value + sol_value
        
        if total_value <= 0:
            return
        
        current_btc_pct = btc_value / total_value
        drift = abs(current_btc_pct - target_btc_pct)
        
        # Only rebalance if drift exceeds threshold
        if drift < REBALANCE_DRIFT:
            return
        
        # Calculate target values
        target_btc_value = total_value * target_btc_pct
        target_sol_value = total_value * (1 - target_btc_pct)
        
        btc_delta_usd = target_btc_value - btc_value
        sol_delta_usd = target_sol_value - sol_value
        
        print(f"\n  [REBALANCE] Drift: {current_btc_pct*100:.0f}/{(1-current_btc_pct)*100:.0f} → Target: {target_btc_pct*100:.0f}/{(1-target_btc_pct)*100:.0f}")
        
        try:
            # If BTC needs more → buy BTC, sell ETH
            if btc_delta_usd > 0:
                btc_buy_size = round(abs(btc_delta_usd) / btc_price, 5)
                sol_sell_size = round(abs(sol_delta_usd) / sol_price, 2)
                
                if sol_sell_size > 0 and sol_sell_size <= self.sol_size:
                    _, sol_onchain = self.get_on_chain_positions()
                    if sol_onchain and sol_onchain["size"] > 0:
                        sell_size = min(sol_sell_size, sol_onchain["size"])
                        
                        self.exchange.order(
                            "SOL", False, sell_size,
                            round_to_tick(sol_price * 0.995),
                            {"limit": {"tif": "Ioc"}}
                        )
                        self.sol_size -= sell_size
                        print(f"  [SOLD] {sell_size} SOL @ ${sol_price:.2f}")
                    
                    # Buy more BTC
                    if btc_buy_size > 0:
                        self.exchange.order(
                            "BTC", True, btc_buy_size,
                            round_to_tick(btc_price * 1.005),
                            {"limit": {"tif": "Ioc"}}
                        )
                        self.btc_size += btc_buy_size
                        print(f"  [BOUGHT] {btc_buy_size} BTC @ ${btc_price:.2f}")
            
            # If ETH needs more → buy ETH, sell BTC
            else:
                sol_buy_size = round(abs(sol_delta_usd) / sol_price, 2)
                btc_sell_size = round(abs(btc_delta_usd) / btc_price, 5)
                
                if btc_sell_size > 0 and btc_sell_size <= self.btc_size:
                    btc_onchain, _ = self.get_on_chain_positions()
                    if btc_onchain and btc_onchain["size"] > 0:
                        sell_size = min(btc_sell_size, btc_onchain["size"])
                        
                        self.exchange.order(
                            "BTC", False, sell_size,
                            round_to_tick(btc_price * 0.995),
                            {"limit": {"tif": "Ioc"}}
                        )
                        self.btc_size -= sell_size
                        print(f"  [SOLD] {sell_size} BTC @ ${btc_price:.2f}")
                    
                    if sol_buy_size > 0:
                        self.exchange.order(
                            "SOL", True, sol_buy_size,
                            round_to_tick(sol_price * 1.005),
                            {"limit": {"tif": "Ioc"}}
                        )
                        self.sol_size += sol_buy_size
                        print(f"  [BOUGHT] {sol_buy_size} SOL @ ${sol_price:.2f}")
            
            self.rebalance_count += 1
            self.target_btc_pct = target_btc_pct
            self.save_state()
            print(f"  [REBALANCED] #{self.rebalance_count} — Now {target_btc_pct*100:.0f}/{(1-target_btc_pct)*100:.0f} BTC/SOL")
            
        except Exception as e:
            print(f"  [ERROR] Rebalance failed: {e}")
    
    def check_deposits(self):
        """Check for new profit deposits from the core bot."""
        if not os.path.exists(DEPOSITS_FILE):
            return
        
        try:
            with open(DEPOSITS_FILE, 'r') as f:
                deposits = json.load(f)
            
            if not deposits:
                return
            
            total_deposit = sum(d.get("amount", 0) for d in deposits)
            if total_deposit <= 0:
                return
            
            btc_price, sol_price = self.get_prices()
            if btc_price <= 0 or sol_price <= 0:
                return
            
            # Split deposit according to current target allocation
            btc_alloc = total_deposit * self.target_btc_pct
            sol_alloc = total_deposit * (1 - self.target_btc_pct)
            
            btc_buy = round(btc_alloc / btc_price, 5)
            sol_buy = round(sol_alloc / sol_price, 2)
            
            print(f"\n  [DEPOSIT] ${total_deposit:.2f} from core bot profits!")
            print(f"  Buying: {btc_buy} BTC (${btc_alloc:.2f}) + {sol_buy} SOL (${sol_alloc:.2f})")
            
            if btc_buy > 0:
                self.exchange.order(
                    "BTC", True, btc_buy,
                    round_to_tick(btc_price * 1.005),
                    {"limit": {"tif": "Ioc"}}
                )
                self.btc_size += btc_buy
            
            if sol_buy > 0:
                self.exchange.order(
                    "SOL", True, sol_buy,
                    round_to_tick(sol_price * 1.005),
                    {"limit": {"tif": "Ioc"}}
                )
                self.sol_size += sol_buy
            
            self.total_invested += total_deposit
            
            # Clear deposits file
            with open(DEPOSITS_FILE, 'w') as f:
                json.dump([], f)
            
            self.save_state()
            print(f"  [DEPOSIT] Complete. Total invested: ${self.total_invested:.2f}")
            
        except Exception as e:
            print(f"  [!] Deposit check error: {e}")
    
    def display_status(self):
        """Display current HODL portfolio status."""
        btc_price, sol_price = self.get_prices()
        if btc_price <= 0 or sol_price <= 0:
            return
        
        btc_value = self.btc_size * btc_price
        sol_value = self.sol_size * sol_price
        total_value = btc_value + sol_value
        total_pnl = total_value - self.total_invested
        pnl_pct = (total_pnl / self.total_invested * 100) if self.total_invested > 0 else 0
        
        btc_pct = (btc_value / total_value * 100) if total_value > 0 else 0
        sol_pct = (sol_value / total_value * 100) if total_value > 0 else 0
        
        ratio = btc_price / sol_price if sol_price > 0 else 0
        
        print(f"\n  [HODL PORTFOLIO]")
        print(f"  BTC: {self.btc_size:.5f} (${btc_value:.2f}) — {btc_pct:.0f}%")
        print(f"  SOL: {self.sol_size:.2f}   (${sol_value:.2f}) — {sol_pct:.0f}%")
        print(f"  Total Value:    ${total_value:.2f}")
        print(f"  Total Invested: ${self.total_invested:.2f}")
        print(f"  P&L:            ${total_pnl:+.2f} ({pnl_pct:+.1f}%)")
        print(f"  BTC/SOL Ratio:  {ratio:.4f}")
        print(f"  Target:         {self.target_btc_pct*100:.0f}/{(1-self.target_btc_pct)*100:.0f} BTC/SOL")
        print(f"  Rebalances:     {self.rebalance_count}")
    
    def save_state(self):
        state = {
            "btc_size": self.btc_size,
            "sol_size": self.sol_size,
            "btc_entry": self.btc_entry,
            "sol_entry": self.sol_entry,
            "total_invested": self.total_invested,
            "target_btc_pct": self.target_btc_pct,
            "rebalance_count": self.rebalance_count,
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=4)
    
    def load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, 'r') as f:
                    state = json.load(f)
                self.btc_size = state.get("btc_size", 0.0)
                self.sol_size = state.get("sol_size", 0.0)
                self.btc_entry = state.get("btc_entry", 0.0)
                self.sol_entry = state.get("sol_entry", 0.0)
                self.total_invested = state.get("total_invested", 0.0)
                self.target_btc_pct = state.get("target_btc_pct", DEFAULT_ALLOCATION)
                self.rebalance_count = state.get("rebalance_count", 0)
                print(f"[HODL] Restored state from {state.get('last_updated', 'unknown')}")
                return True
            except:
                pass
        return False
    
    def check_kill_switch(self):
        """Kill switch on HODL bot's own portfolio value."""
        btc_price, sol_price = self.get_prices()
        if btc_price <= 0 or sol_price <= 0:
            return False
        
        total_value = (self.btc_size * btc_price) + (self.sol_size * sol_price)
        if self.total_invested > 0:
            drawdown = (self.total_invested - total_value) / self.total_invested
            if drawdown >= DAILY_LOSS_LIMIT:
                print(f"\n[HODL KILL SWITCH] Portfolio down {drawdown*100:.1f}%")
                print(f"   Invested: ${self.total_invested:.2f} | Current: ${total_value:.2f}")
                return True
        return False
    
    def run(self):
        """Main HODL bot loop."""
        # Lockfile — prevent duplicate instances
        if os.path.exists(LOCKFILE):
            print("[!] HODL bot is already running (lockfile exists).")
            print(f"    If this is wrong, delete: {LOCKFILE}")
            return
        
        try:
            with open(LOCKFILE, 'w') as f:
                f.write(str(os.getpid()))
        except:
            pass
        
        print("\n" + "=" * 60)
        print(" FLOWSTATE AI HODL BOT — BTC/SOL Accumulator (MAINNET)")
        print("=" * 60)
        
        self.starting_balance = self.get_account_balance()
        if self.starting_balance <= 0:
            print("[!] No balance available.")
            self._cleanup_lock()
            return
        
        print(f"[HODL] Account balance: ${self.starting_balance:.2f}")
        
        # Try to restore previous state
        restored = self.load_state()
        
        if restored and self.btc_size > 0 and self.sol_size > 0:
            # Verify on-chain positions match
            btc_oc, sol_oc = self.get_on_chain_positions()
            if btc_oc and sol_oc and btc_oc["size"] > 0 and sol_oc["size"] > 0:
                print(f"[HODL] Existing positions confirmed on-chain")
                self.display_status()
            else:
                print(f"[HODL] State file exists but positions not found on-chain. Starting fresh.")
                restored = False
        
        if not restored or self.btc_size == 0:
            print(f"\n[HODL] No existing positions. Opening initial HODL...")
            if not self.initial_buy():
                print("[!] Initial buy failed. Exiting.")
                return
        
        print(f"\n[HODL] Check interval: {CHECK_INTERVAL // 60} minutes")
        print(f"[HODL] Press Ctrl+C to stop\n")
        
        try:
            while True:
                # Kill switch
                if self.check_kill_switch():
                    print("[HODL] Kill switch triggered. Positions remain open — review manually.")
                    break
                
                # Analyze ratio and get target allocation
                target = self.analyze_ratio()
                
                # Rebalance if needed
                self.rebalance(target)
                
                # Check for new deposits from core bot
                self.check_deposits()
                
                # Display status
                self.display_status()
                
                time.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            print(f"\n[HODL] Bot stopped by user.")
            self.display_status()
            self.save_state()
            print(f"[HODL] State saved. Positions remain open on exchange.")
            print(f"[HODL] Restart the bot to resume management.")
        finally:
            self._cleanup_lock()
    
    def _cleanup_lock(self):
        """Remove lockfile on exit."""
        try:
            if os.path.exists(LOCKFILE):
                os.remove(LOCKFILE)
        except:
            pass


if __name__ == "__main__":
    bot = HodlBot()
    bot.run()
