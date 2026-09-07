import os
import requests, time, json

API_URL = "https://api.hyperliquid.xyz/info"
MACRO_COINS = ["BTC", "SOL"]

def fetch_candles(coin, interval="1d", lookback_days=100):
    end = int(time.time() * 1000)
    start = end - lookback_days * 24 * 3600 * 1000
    r = requests.post(API_URL, json={"type": "candleSnapshot", "req": {"coin": coin, "interval": interval, "startTime": start, "endTime": end}})
    try:
        return [{"high": float(c["h"]), "low": float(c["l"]), "close": float(c["c"])} for c in r.json()]
    except:
        return []

def ema(prices, w):
    if len(prices) < w:
        return None
    m = 2 / (w + 1)
    e = sum(prices[:w]) / w
    for p in prices[w:]:
        e = (p - e) * m + e
    return e

def analyze_trend(coin):
    candles = fetch_candles(coin, interval="1d", lookback_days=250)
    if not candles:
        return "UNKNOWN"
    
    prices = [c["close"] for c in candles]
    current_price = prices[-1]
    
    e21 = ema(prices, 21)
    e50 = ema(prices, 50)
    e200 = ema(prices, 200)
    
    if not e21 or not e50 or not e200:
        return "UNKNOWN"
        
    gap_pct = abs(e21 - e50) / e50 * 100
    
    # Trend Definitions with 200-EMA Hard Gates
    if current_price > e21 > e50 and current_price > e200 and gap_pct > 0.5:
        return "BULL"
    elif current_price < e21 < e50 and current_price < e200 and gap_pct > 0.5:
        return "BEAR"
    else:
        return "CHOP"

def scan_regime():
    print("=" * 60)
    print(" FLOWSTATE AI REGIME SCANNER (The Master Switch)")
    print("=" * 60)
    
    results = {}
    for coin in MACRO_COINS:
        print(f"[*] Analyzing Macro Structure for {coin}...")
        trend = analyze_trend(coin)
        results[coin] = trend
        print(f"  -> {coin} Trend: {trend}")
        time.sleep(1)
        
    print("-" * 60)
    
    # Master Logic
    if results["BTC"] == "BULL" and results["SOL"] == "BULL":
        final_regime = "BULL"
        msg = "The market is trending UP. Activate bull_scanner.py (Pullbacks/Momentum)."
    elif results["BTC"] == "BEAR" and results["SOL"] == "BEAR":
        final_regime = "BEAR"
        msg = "The market is trending DOWN. Activate bear_scanner.py (Shorts) or pause trading."
    else:
        final_regime = "CHOP"
        msg = "The market is SIDEWAYS / MIXED. Activate chop_scanner.py (Ping-Pong / Channels)."
        
    print(f"\n[*] FINAL REGIME DETECTED: {final_regime}")
    print(f"[*] INSTRUCTION: {msg}")
    print("=" * 60)
    
    # Save regime state
    output_file = os.path.join(os.path.dirname(__file__), "..", "data", "market_regime.json")
    with open(output_file, "w") as f:
        json.dump({"regime": final_regime, "btc": results.get("BTC"), "sol": results.get("SOL"), "timestamp": time.time()}, f, indent=4)
        
if __name__ == "__main__":
    scan_regime()
