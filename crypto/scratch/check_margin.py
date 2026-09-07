import os
import json
from hyperliquid.info import Info
from hyperliquid.utils import constants

def check_account():
    address = os.environ.get("HL_ACCOUNT_ADDRESS")
    if not address:
        print("No HL_ACCOUNT_ADDRESS found in env.")
        return
        
    info = Info(constants.MAINNET_API_URL, skip_ws=True)
    
    print(f"Checking account: {address}")
    
    try:
        user_state = info.user_state(address)
        margin_summary = user_state.get("marginSummary", {})
        print("\n--- Margin Summary ---")
        print(json.dumps(margin_summary, indent=2))
        
        positions = user_state.get("assetPositions", [])
        print(f"\n--- Open Positions: {len(positions)} ---")
        for pos in positions:
            print(json.dumps(pos, indent=2))
            
        open_orders = info.open_orders(address)
        print(f"\n--- Open Orders: {len(open_orders)} ---")
        for order in open_orders:
            print(json.dumps(order, indent=2))
            
        print("\n--- Asset Positions (Leverage State) ---")
        for pos in positions:
            if pos.get("position", {}).get("coin") == "LIT":
                print(json.dumps(pos, indent=2))
                
        # Also let's try to fetch meta to see if there's a specific requirement for LIT
        meta = info.meta()
        for asset in meta.get("universe", []):
            if asset.get("name") == "LIT":
                print(f"\n--- LIT Asset Info ---")
                print(json.dumps(asset, indent=2))
                
        print("\n--- Spot State ---")
        spot_state = info.spot_user_state(address)
        print(json.dumps(spot_state, indent=2))
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_account()
