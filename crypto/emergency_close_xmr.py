"""
EMERGENCY XMR CLOSE SCRIPT
Closes any open XMR position on Hyperliquid immediately. Zero external dependencies.
"""
import os
import math
import sys
import eth_account

# Manually load environment variables from .env_trading or .env files
possible_env_paths = [
    "/root/.env_trading",
    os.path.join(os.path.dirname(__file__), "..", ".env_trading"),
    os.path.join(os.path.dirname(__file__), "..", ".env"),
    os.path.join(os.path.dirname(__file__), ".env")
]

for env_path in possible_env_paths:
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    parts = line.strip().split("=", 1)
                    if len(parts) == 2:
                        k, v = parts[0].strip(), parts[1].strip().strip("'\"")
                        if k and not os.environ.get(k):
                            os.environ[k] = v

from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants

def round_to_tick(price):
    if price <= 0: return price
    sig_figs = 5
    magnitude = math.floor(math.log10(abs(price)))
    factor = 10 ** (sig_figs - 1 - magnitude)
    return round(price * factor) / factor

raw_key = os.environ.get("HL_PRIVATE_KEY", "").strip().strip("'\"")
if raw_key.startswith("0x"):
    raw_key = raw_key[2:]
HL_KEY = "0x" + "".join(c for c in raw_key if c in "0123456789abcdefABCDEF")
HL_ADDRESS = os.environ.get("HL_ACCOUNT_ADDRESS", "").strip().strip("'\"")

if not HL_KEY or not HL_ADDRESS or len(HL_KEY) < 64:
    print(f"[!] Missing or invalid HL credentials in env (Key len: {len(HL_KEY)}, Address: {HL_ADDRESS})")
    sys.exit(1)

account = eth_account.Account.from_key(HL_KEY)
info = Info(constants.MAINNET_API_URL, skip_ws=True)
exchange = Exchange(account, constants.MAINNET_API_URL, account_address=HL_ADDRESS)

print("=" * 60)
print(" 🚨 EMERGENCY CLOSE POSITION CHECK: XMR")
print("=" * 60)

user_state = info.user_state(HL_ADDRESS)
all_mids = info.all_mids()
xmr_price = float(all_mids.get("XMR", 0))

print(f"Current XMR Price: ${xmr_price}")

xmr_pos = None
for pos in user_state.get("assetPositions", []):
    p = pos.get("position", {})
    if p.get("coin") == "XMR":
        xmr_pos = p
        break

if not xmr_pos or float(xmr_pos.get("szi", 0)) == 0:
    print("✅ No open XMR position found on Hyperliquid! Account is clean.")
    sys.exit(0)

szi = float(xmr_pos.get("szi", 0))
entry_px = float(xmr_pos.get("entryPx", 0))
is_long = szi > 0
close_size = abs(szi)

print(f"⚠️ FOUND ACTIVE POSITION: {'LONG' if is_long else 'SHORT'} {close_size} XMR @ ${entry_px}")

# Place IOC close order with 1% slippage
limit_price = round_to_tick(xmr_price * 0.99) if is_long else round_to_tick(xmr_price * 1.01)
print(f"Executing MARKET CLOSE for {close_size} XMR @ limit ${limit_price}...")

result = exchange.order(
    "XMR",
    not is_long, # Sell if Long, Buy if Short
    close_size,
    limit_price,
    {"limit": {"tif": "Ioc"}},
    reduce_only=True
)

print(f"Close Result: {result}")
print("🎉 Emergency close execution finished.")
