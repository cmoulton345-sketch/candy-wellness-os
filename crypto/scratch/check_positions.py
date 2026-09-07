import os, json, eth_account
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".env")
load_dotenv(env_path if os.path.exists(env_path) else None)

from hyperliquid.info import Info
from hyperliquid.utils import constants

pk = os.environ.get("HL_PRIVATE_KEY", "").strip().strip("'\"")
addr = os.environ.get("HL_ACCOUNT_ADDRESS", "").strip().strip("'\"")

if pk:
    try:
        addr = eth_account.Account.from_key(pk).address
    except Exception as e:
        print("PK parse error:", e)

print(f"Checking wallet: {addr}")
info = Info(constants.MAINNET_API_URL, skip_ws=True)

try:
    user_state = info.user_state(addr)
    margin = user_state.get("marginSummary", {})
    print(f"Account Value: ${float(margin.get('accountValue', 0)):.2f}")
    
    positions = user_state.get("assetPositions", [])
    open_positions = []
    for pos_item in positions:
        pos = pos_item.get("position", {})
        szi = float(pos.get("szi", 0))
        if szi != 0:
            open_positions.append({
                "coin": pos.get("coin"),
                "size": szi,
                "entry_price": float(pos.get("entryPx", 0)),
                "position_value": float(pos.get("positionValue", 0)),
                "unrealized_pnl": float(pos.get("unrealizedPnl", 0))
            })
            
    if open_positions:
        print(f"\nFound {len(open_positions)} active position(s):")
        for p in open_positions:
            print(f" - Coin: {p['coin']} | Size: {p['size']} | Entry: ${p['entry_price']:.4f} | Value: ${p['position_value']:.2f} | Unr PnL: ${p['unrealized_pnl']:.2f}")
    else:
        print("\nNo open positions currently active on Hyperliquid.")
except Exception as e:
    print("API Error:", e)
