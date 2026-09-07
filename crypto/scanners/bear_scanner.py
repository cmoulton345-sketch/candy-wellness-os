import requests
import time
import json
import os
import math

API_URL = "https://api.hyperliquid.xyz/info"

def fetch_markets_and_filter_liquidity(min_volume_usd=5_000_000):
    print(f"[*] Fetching all active markets from Hyperliquid...")
    payload = {"type": "metaAndAssetCtxs"}
    response = requests.post(API_URL, json=payload)
    data = response.json()
    
    universe = data[0]["universe"]
    contexts = data[1]
    
    liquid_pairs = []
    for i, asset in enumerate(universe):
        coin = asset["name"]
        ctx = contexts[i]
        day_volume = float(ctx.get("dayNtlVlm", 0))
        mark_price = float(ctx.get("markPx", 0))
        
        if day_volume >= min_volume_usd:
            liquid_pairs.append({"coin": coin, "volume": day_volume, "price": mark_price})
            
    print(f"[+] Found {len(liquid_pairs)} pairs with > ${min_volume_usd:,.0f} 24h volume.")
    return liquid_pairs

def fetch_candles(coin, interval="1h", lookback_hours=100):
    end_time = int(time.time() * 1000)
    start_time = end_time - (lookback_hours * 3600 * 1000)
    payload = {"type": "candleSnapshot", "req": {"coin": coin, "interval": interval, "startTime": start_time, "endTime": end_time}}
    
    response = requests.post(API_URL, json=payload)
    candles = response.json()
    if not candles: return None
        
    formatted = []
    for c in candles:
        formatted.append({
            'high': float(c['h']),
            'low': float(c['l']),
            'close': float(c['c'])
        })
    return formatted

def calculate_ema(prices, window):
    if len(prices) < window: return None
    multiplier = 2 / (window + 1)
    ema = sum(prices[:window]) / window
    for price in prices[window:]:
        ema = (price - ema) * multiplier + ema
    return ema

def calculate_atr(candles, window=14):
    if len(candles) < window + 1: return None
    true_ranges = []
    for i in range(1, len(candles)):
        h, l, pc = candles[i]['high'], candles[i]['low'], candles[i-1]['close']
        true_ranges.append(max(h - l, abs(h - pc), abs(l - pc)))
    
    atr = sum(true_ranges[:window]) / window
    for tr in true_ranges[window:]:
        atr = (atr * (window - 1) + tr) / window
    return atr

def analyze_pair_bear(candles, current_price):
    if len(candles) < 50: return False, "Not enough data"
    
    prices = [c['close'] for c in candles]
    ema21 = calculate_ema(prices, 21)
    ema50 = calculate_ema(prices, 50)
    atr14 = calculate_atr(candles, 14)
    
    if not all([ema21, ema50, atr14]): return False, "Calc error"
        
    # BEAR CRITERIA 1: Downtrend confirmed
    if not (current_price < ema21 < ema50):
        return False, "Failed Downtrend"
        
    # BEAR CRITERIA 2: Strong separation (don't short a fakeout)
    ema_gap_pct = ((ema50 - ema21) / ema50) * 100
    if ema_gap_pct < 1.0:
        return False, f"Downtrend too weak (Gap {ema_gap_pct:.2f}% < 1.0%)"
        
    # BEAR CRITERIA 3: Volatility check (needs to be moving)
    atr_pct = (atr14 / current_price) * 100
    if atr_pct < 2.0:
        return False, f"Too slow to short (ATR {atr_pct:.2f}% < 2%)"
    
    # BEAR CRITERIA 4: Proximity to EMA 21 (we want to short the pullback, not the bottom)
    distance_from_ema21 = ((ema21 - current_price) / current_price) * 100
    if distance_from_ema21 > 5.0:
        return False, f"Too overextended downwards to short (Dist {distance_from_ema21:.1f}%)"
    
    return True, {
        "EMA_21": round(ema21, 4),
        "EMA_50": round(ema50, 4),
        "EMA_Gap_Pct": round(ema_gap_pct, 2),
        "ATR_Pct": round(atr_pct, 2),
        "Dist_EMA21_Pct": round(distance_from_ema21, 2),
        "scan_mode": "bear_short"
    }

def main():
    print("="*60)
    print(" HYPERLIQUID BEAR SCANNER (Short Selling Mode)")
    print("="*60)
    
    liquid_pairs = fetch_markets_and_filter_liquidity()
    qualified_pairs = []
    
    print("\n[*] Running technical analysis for short targets...")
    
    for pair in liquid_pairs:
        coin, price = pair['coin'], pair['price']
        try:
            candles = fetch_candles(coin)
            if not candles: continue
            passed, metrics = analyze_pair_bear(candles, price)
            
            if passed:
                qualified_pairs.append({"coin": coin, "price": price, "volume_24h": pair['volume'], "metrics": metrics})
                print(f"  [SHORT TARGET] {coin} -> Vol: ${pair['volume']/1e6:.1f}M | EMA Gap: {metrics['EMA_Gap_Pct']}% | Dist to EMA21: {metrics['Dist_EMA21_Pct']}%")
            else:
                pass
        except Exception as e:
            print(f"  [ERROR] {coin}: {str(e)}")
        time.sleep(0.1)
        
    print("="*60)
    print(f" SCAN COMPLETE. Found {len(qualified_pairs)} short selling targets.")
    print("="*60)
    
    output_file = os.path.join(os.path.dirname(__file__), "..", "data", "qualified_pairs.json")
    with open(output_file, 'w') as f:
        json.dump(qualified_pairs, f, indent=4)
    print(f"[*] Saved qualified pairs to {output_file}")

if __name__ == "__main__":
    main()
