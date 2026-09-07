from hyperliquid.info import Info
from hyperliquid.utils import constants

import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
address = os.environ.get("HL_ACCOUNT_ADDRESS")
info = Info(constants.MAINNET_API_URL, skip_ws=True)

print("--- Perps Account State ---")
user_state = info.user_state(address)
margin = user_state.get("marginSummary", {})
print("accountValue:    " + str(margin.get("accountValue")))
print("totalMarginUsed: " + str(margin.get("totalMarginUsed")))
print("withdrawable:    " + str(margin.get("withdrawable")))

print()
print("--- Spot Balance ---")
spot = info.spot_user_state(address)
for b in spot.get("balances", []):
    print("  " + b["coin"] + ": " + str(b["total"]))

print()
print("--- Open Positions ---")
for pos in user_state.get("assetPositions", []):
    p = pos.get("position", {})
    if float(p.get("szi", 0)) != 0:
        print("  " + p["coin"] + ": size=" + p["szi"] + " entryPx=" + p["entryPx"])
