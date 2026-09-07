"""
UNIVERSAL HODL FIXER
Reads actual on-chain state and rebalances to exactly $250 BTC + $250 ETH.
No assumptions about current state.
"""
import os
import math
import json
import time
import eth_account
from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants

TARGET_PER_LEG = 250  # $250 per coin

def round_to_tick(price):
    if price <= 0: return price
    sig_figs = 5
    magnitude = math.floor(math.log10(abs(price)))
    factor = 10 ** (sig_figs - 1 - magnitude)
    return round(price * factor) / factor

private_key = os.environ.get("HL_PRIVATE_KEY")
account_address = os.environ.get("HL_ACCOUNT_ADDRESS")

wallet = eth_account.Account.from_key(private_key)
info = Info(constants.MAINNET_API_URL, skip_ws=True)
exchange = Exchange(wallet, constants.MAINNET_API_URL, account_address=account_address)

# ---- STEP 1: Read actual on-chain state ----
print("=" * 50)
print(" UNIVERSAL HODL FIXER")
print("=" * 50)

user_state = info.user_state(account_address)
all_mids = info.all_mids()
btc_price = float(all_mids.get("BTC", 0))
eth_price = float(all_mids.get("ETH", 0))

btc_size = 0.0
eth_size = 0.0

for pos in user_state.get("assetPositions", []):
    p = pos.get("position", {})
    coin = p.get("coin")
    size = float(p.get("szi", 0))
    entry = float(p.get("entryPx", 0))
    if coin == "BTC":
        btc_size = size
    elif coin == "ETH":
        eth_size = size
    if size != 0:
        value = abs(size) * float(all_mids.get(coin, 0))
        direction = "LONG" if size > 0 else "SHORT"
        print(f"  {coin}: {size} ({direction}) @ ${entry:.2f} = ${value:.2f}")

print(f"\nBTC: ${btc_price:.2f} | ETH: ${eth_price:.2f}")
print(f"\nCurrent: BTC={btc_size}, ETH={eth_size}")

btc_value = btc_size * btc_price if btc_size > 0 else 0
eth_value = eth_size * eth_price if eth_size > 0 else 0
print(f"BTC value: ${btc_value:.2f} | ETH value: ${eth_value:.2f}")
print(f"Target:    ${TARGET_PER_LEG:.2f} each")

# ---- STEP 2: Close ALL positions first (clean slate) ----
print(f"\n--- STEP 1: Close all positions ---")

if btc_size != 0:
    is_buy = btc_size < 0  # If short, buy to close
    close_size = abs(btc_size)
    slippage = 1.005 if is_buy else 0.995
    limit = round_to_tick(btc_price * slippage)
    print(f"  Closing BTC: {'BUY' if is_buy else 'SELL'} {close_size} @ ${limit:.2f}")
    result = exchange.order("BTC", is_buy, close_size, limit, {"limit": {"tif": "Ioc"}})
    statuses = result.get("response", {}).get("data", {}).get("statuses", [])
    filled = any(isinstance(s, dict) and "filled" in s for s in statuses)
    print(f"  {'FILLED' if filled else 'FAILED'}: {statuses}")
else:
    print(f"  BTC: no position to close")

if eth_size != 0:
    is_buy = eth_size < 0
    close_size = abs(eth_size)
    slippage = 1.005 if is_buy else 0.995
    limit = round_to_tick(eth_price * slippage)
    print(f"  Closing ETH: {'BUY' if is_buy else 'SELL'} {close_size} @ ${limit:.2f}")
    result = exchange.order("ETH", is_buy, close_size, limit, {"limit": {"tif": "Ioc"}})
    statuses = result.get("response", {}).get("data", {}).get("statuses", [])
    filled = any(isinstance(s, dict) and "filled" in s for s in statuses)
    print(f"  {'FILLED' if filled else 'FAILED'}: {statuses}")
else:
    print(f"  ETH: no position to close")

# ---- STEP 3: Wait and verify clean state ----
time.sleep(2)
print(f"\n--- STEP 2: Verify clean slate ---")
user_state = info.user_state(account_address)
remaining = []
for pos in user_state.get("assetPositions", []):
    p = pos.get("position", {})
    size = float(p.get("szi", 0))
    if size != 0:
        remaining.append(f"{p.get('coin')}: {size}")

if remaining:
    print(f"  WARNING: Still have positions: {remaining}")
    print(f"  Close these manually on the UI before continuing!")
    exit(1)
else:
    print(f"  All positions closed. Clean slate.")

# ---- STEP 4: Open fresh $250 BTC + $250 ETH ----
time.sleep(1)
all_mids = info.all_mids()
btc_price = float(all_mids.get("BTC", 0))
eth_price = float(all_mids.get("ETH", 0))

btc_buy_size = round(TARGET_PER_LEG / btc_price, 5)
eth_buy_size = round(TARGET_PER_LEG / eth_price, 3)

print(f"\n--- STEP 3: Open fresh HODL positions ---")
print(f"  BTC: {btc_buy_size} @ ${btc_price:.2f} (${TARGET_PER_LEG})")
print(f"  ETH: {eth_buy_size} @ ${eth_price:.2f} (${TARGET_PER_LEG})")

# Set leverage
exchange.update_leverage(1, "BTC")
exchange.update_leverage(1, "ETH")

# Buy BTC
btc_limit = round_to_tick(btc_price * 1.005)
btc_result = exchange.order("BTC", True, btc_buy_size, btc_limit, {"limit": {"tif": "Ioc"}})
btc_statuses = btc_result.get("response", {}).get("data", {}).get("statuses", [])
btc_filled = any(isinstance(s, dict) and "filled" in s for s in btc_statuses)
print(f"  BTC: {'FILLED' if btc_filled else 'FAILED'} — {btc_statuses}")

# Buy ETH
eth_limit = round_to_tick(eth_price * 1.005)
eth_result = exchange.order("ETH", True, eth_buy_size, eth_limit, {"limit": {"tif": "Ioc"}})
eth_statuses = eth_result.get("response", {}).get("data", {}).get("statuses", [])
eth_filled = any(isinstance(s, dict) and "filled" in s for s in eth_statuses)
print(f"  ETH: {'FILLED' if eth_filled else 'FAILED'} — {eth_statuses}")

# ---- STEP 5: Verify and update state ----
time.sleep(1)
print(f"\n--- FINAL STATE ---")
user_state = info.user_state(account_address)
all_mids = info.all_mids()

btc_final = 0.0
eth_final = 0.0
btc_entry = 0.0
eth_entry = 0.0

for pos in user_state.get("assetPositions", []):
    p = pos.get("position", {})
    coin = p.get("coin")
    size = float(p.get("szi", 0))
    entry = float(p.get("entryPx", 0))
    if size != 0:
        value = abs(size) * float(all_mids.get(coin, 0))
        print(f"  {coin}: {size} @ ${entry:.2f} = ${value:.2f}")
        if coin == "BTC" and size > 0:
            btc_final = size
            btc_entry = entry
        elif coin == "ETH" and size > 0:
            eth_final = size
            eth_entry = entry

# Update state file
state_file = os.path.join(os.path.dirname(__file__), "..", "data", "hodl_state.json")
state = {
    "btc_size": btc_final,
    "eth_size": eth_final,
    "btc_entry": btc_entry,
    "eth_entry": eth_entry,
    "total_invested": 500,
    "target_btc_pct": 0.5,
    "rebalance_count": 0,
    "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
}
with open(state_file, 'w') as f:
    json.dump(state, f, indent=4)

# Remove lockfile
lock = os.path.join(os.path.dirname(__file__), "hodl_bot.lock")
if os.path.exists(lock):
    os.remove(lock)

print(f"\n[DONE] State file updated. Ready to restart HODL bot.")
