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

def calculate_bollinger(prices, window=20, num_std=2):
    if len(prices) < window: return None, None, None
    recent = prices[-window:]
    mean = sum(recent) / window
    variance = sum((p - mean) ** 2 for p in recent) / window
    std_dev = math.sqrt(variance)
    upper = mean + (num_std * std_dev)
    lower = mean - (num_std * std_dev)
    return upper, mean, lower

def calculate_bb_width(prices, window=20, num_std=2):
    if len(prices) < window: return None
    recent = prices[-window:]
    mean = sum(recent) / window
    variance = sum((p - mean) ** 2 for p in recent) / window
    std_dev = math.sqrt(variance)
    if mean == 0: return 0
    return ((2 * num_std * std_dev) / mean) * 100

def analyze_pair_chop(candles, current_price):
    if len(candles) < 50: return False, "Not enough data"
    
    prices = [c['close'] for c in candles]
    ema21 = calculate_ema(prices, 21)
    ema50 = calculate_ema(prices, 50)
    bb_width = calculate_bb_width(prices, 20)
    
    if not all([ema21, ema50, bb_width]): return False, "Calc error"
        
    # CHOP CRITERIA 1: EMAs must be flat/tight. Gap < 1.0%
    ema_gap_pct = (abs(ema21 - ema50) / ema50) * 100
    if ema_gap_pct > 1.5:
        return False, f"Gap too wide ({ema_gap_pct:.2f}% > 1.5%) - Not in chop"
        
    # CHOP CRITERIA 2: Range must exist but not be wild (BBW between 3% and 10%)
    if bb_width < 3.0:
        return False, f"Range too tight (BBW {bb_width:.2f}% < 3%)"
    if bb_width > 12.0:
        return False, f"Range too wild (BBW {bb_width:.2f}% > 12%)"
        
    # CHOP CRITERIA 3: Price should be in the lower half of the channel to buy the bounce
    bb_upper, bb_mid, bb_lower = calculate_bollinger(prices, 20)
    bb_position = 0
    if bb_upper and bb_lower and (bb_upper - bb_lower) > 0:
        bb_position = (current_price - bb_lower) / (bb_upper - bb_lower)
        
    if bb_position > 0.40:
        return False, f"Price too high in channel (Pos: {bb_position*100:.0f}% > 40%)"
    
    return True, {
        "EMA_21": round(ema21, 4),
        "EMA_50": round(ema50, 4),
        "EMA_Gap_Pct": round(ema_gap_pct, 2),
        "BBW_Pct": round(bb_width, 2),
        "BB_Position": round(bb_position, 2),
        "scan_mode": "chop_opportunity"
    }

def main():
    print("="*60)
    print(" HYPERLIQUID CHOP SCANNER (Opportunity Mode)")
    print("="*60)
    
    liquid_pairs = fetch_markets_and_filter_liquidity()
    qualified_pairs = []
    
    print("\n[*] Running channel analysis on liquid pairs...")
    
    for pair in liquid_pairs:
        coin, price = pair['coin'], pair['price']
        try:
            candles = fetch_candles(coin)
            if not candles: continue
            passed, metrics = analyze_pair_chop(candles, price)
            
            if passed:
                qualified_pairs.append({"coin": coin, "price": price, "volume_24h": pair['volume'], "metrics": metrics})
                print(f"  [OPPORTUNITY] {coin} -> Vol: ${pair['volume']/1e6:.1f}M | BB Pos: {metrics['BB_Position']*100:.0f}% | EMA Gap: {metrics['EMA_Gap_Pct']}% | BBW: {metrics['BBW_Pct']}%")
            else:
                pass
        except Exception as e:
            print(f"  [ERROR] {coin}: {str(e)}")
        time.sleep(0.1)
        
    print("="*60)
    print(f" SCAN COMPLETE. Found {len(qualified_pairs)} Ping-Pong opportunities.")
    print("="*60)
    
    output_file = os.path.join(os.path.dirname(__file__), "..", "data", "qualified_pairs.json")
    with open(output_file, 'w') as f:
        json.dump(qualified_pairs, f, indent=4)
    print(f"[*] Saved qualified pairs to {output_file}")

if __name__ == "__main__":
    main()
