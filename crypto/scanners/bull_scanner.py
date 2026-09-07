import requests
import time
import json
import os
import math

API_URL = "https://api.hyperliquid.xyz/info"

# --- Overextension Thresholds ---
MAX_RSI = 75                    # RSI above this = overbought
MAX_RALLY_FROM_LOW_PCT = 40     # If price rallied >40% from lookback low, too late
MAX_DISTANCE_FROM_EMA50 = 0.15  # If price is >15% above EMA50, overextended
MAX_BB_POSITION = 0.90          # If price is >90% of the way from lower to upper BB, too hot

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
            
    print(f"[+] Found {len(liquid_pairs)} pairs with > ${min_volume_usd:,.0f} 24h volume out of {len(universe)} total pairs.")
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

def calculate_bb_width(prices, window=20, num_std=2):
    if len(prices) < window: return None
    recent = prices[-window:]
    mean = sum(recent) / window
    variance = sum((p - mean) ** 2 for p in recent) / window
    std_dev = math.sqrt(variance)
    return ((2 * num_std * std_dev) / mean) * 100

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

def check_overextension(prices, current_price, ema50):
    """Check if a coin is overextended. Returns (is_overextended, reasons_list)."""
    reasons = []
    
    # 1. RSI overbought check
    rsi = calculate_rsi(prices, 14)
    if rsi and rsi > MAX_RSI:
        reasons.append(f"RSI {rsi:.1f} > {MAX_RSI}")
    
    # 2. Rally from recent low check
    lookback_low = min(prices[-50:]) if len(prices) >= 50 else min(prices)
    if lookback_low > 0:
        rally_pct = ((current_price - lookback_low) / lookback_low) * 100
        if rally_pct > MAX_RALLY_FROM_LOW_PCT:
            reasons.append(f"Rally {rally_pct:.0f}% from low ${lookback_low:.4f}")
    
    # 3. Distance from EMA50 check
    if ema50 and ema50 > 0:
        distance = (current_price - ema50) / ema50
        if distance > MAX_DISTANCE_FROM_EMA50:
            reasons.append(f"{distance*100:.1f}% above EMA50")
    
    # 4. Bollinger Band position check
    bb_upper, bb_mid, bb_lower = calculate_bollinger(prices, 20)
    if bb_upper and bb_lower and (bb_upper - bb_lower) > 0:
        bb_position = (current_price - bb_lower) / (bb_upper - bb_lower)
        if bb_position > MAX_BB_POSITION:
            reasons.append(f"BB position {bb_position*100:.0f}% (near upper band)")
    
    return len(reasons) >= 2, reasons, rsi  # Need 2+ flags to reject


def analyze_pair(candles, current_price):
    if len(candles) < 50: return False, "Not enough data"
    
    prices = [c['close'] for c in candles]
    ema21 = calculate_ema(prices, 21)
    ema50 = calculate_ema(prices, 50)
    bb_width = calculate_bb_width(prices, 20)
    atr14 = calculate_atr(candles, 14)
    
    if not all([ema21, ema50, bb_width, atr14]): return False, "Calc error"
        
    if not (current_price > ema21 > ema50):
        return False, "Failed Uptrend"
    
    # [v3.2] EMA separation check — reject fragile crosses
    ema_gap_pct = ((ema21 - ema50) / ema50) * 100
    if ema_gap_pct < 0.5:
        return False, f"Failed EMA Strength (gap {ema_gap_pct:.2f}% < 0.5% — fragile cross)"
        
    atr_pct = (atr14 / current_price) * 100
    if atr_pct < 2.0:
        return False, f"Failed Volatility (ATR {atr_pct:.2f}% < 2%)"
        
    if bb_width < 4.0:
        return False, f"Failed Range Quality (BBW {bb_width:.2f}% < 4%)"
    
    # --- OVEREXTENSION CHECK ---
    is_overextended, ext_reasons, rsi = check_overextension(prices, current_price, ema50)
    if is_overextended:
        return False, f"OVEREXTENDED: {' | '.join(ext_reasons)}"
    
    # Calculate rally from low for reporting
    lookback_low = min(prices[-50:]) if len(prices) >= 50 else min(prices)
    rally_pct = ((current_price - lookback_low) / lookback_low) * 100 if lookback_low > 0 else 0
    ema50_dist = ((current_price - ema50) / ema50) * 100 if ema50 > 0 else 0
    
    return True, {
        "EMA_21": round(ema21, 4),
        "EMA_50": round(ema50, 4),
        "EMA_Gap_Pct": round(ema_gap_pct, 2),
        "ATR_Pct": round(atr_pct, 2),
        "BBW_Pct": round(bb_width, 2),
        "RSI": round(rsi, 1) if rsi else None,
        "Rally_Pct": round(rally_pct, 1),
        "EMA50_Dist_Pct": round(ema50_dist, 1),
        "scan_mode": "standard"
    }

def analyze_pair_deep_value(candles, current_price):
    """Second-chance analysis for oversold coins.
    Catches deep dips on coins with intact underlying trends.
    Bypasses the uptrend requirement — only needs RSI < 25 + EMA50 slope rising."""
    if len(candles) < 55: return False, "Not enough data for deep value"
    
    prices = [c['close'] for c in candles]
    ema21 = calculate_ema(prices, 21)
    ema50 = calculate_ema(prices, 50)
    ema50_prev = calculate_ema(prices[:-5], 50)
    atr14 = calculate_atr(candles, 14)
    rsi = calculate_rsi(prices, 14)
    bb_width = calculate_bb_width(prices, 20)
    
    if not all([ema21, ema50, ema50_prev, atr14, rsi]): return False, "Calc error"
    
    # Gate 1: RSI must be deeply oversold
    if rsi >= 25:
        return False, f"RSI {rsi:.1f} not oversold enough (need < 25)"
    
    # Gate 2: EMA50 slope must be rising (trend is alive, just dipping)
    if ema50 <= ema50_prev:
        return False, f"EMA50 slope DOWN ({ema50_prev:.4f} -> {ema50:.4f}) — trend may be dying"
    
    # Gate 3: Still needs minimum volatility to be tradeable
    atr_pct = (atr14 / current_price) * 100
    if atr_pct < 2.0:
        return False, f"ATR too low ({atr_pct:.2f}%)"
    
    bb_upper, bb_mid, bb_lower = calculate_bollinger(prices, 20)
    bb_position = 0
    if bb_upper and bb_lower and (bb_upper - bb_lower) > 0:
        bb_position = (current_price - bb_lower) / (bb_upper - bb_lower) * 100
    
    ema50_dist = ((current_price - ema50) / ema50) * 100 if ema50 > 0 else 0
    
    return True, {
        "EMA_21": round(ema21, 4),
        "EMA_50": round(ema50, 4),
        "EMA50_Prev": round(ema50_prev, 4),
        "ATR_Pct": round(atr_pct, 2),
        "BBW_Pct": round(bb_width, 2) if bb_width else None,
        "RSI": round(rsi, 1),
        "BB_Position": round(bb_position, 1),
        "EMA50_Dist_Pct": round(ema50_dist, 1),
        "scan_mode": "deep_value"
    }

def main():
    print("="*60)
    print(" HYPERLIQUID PAIR SCANNER (Phase 4)")
    print("="*60)
    
    liquid_pairs = fetch_markets_and_filter_liquidity()
    qualified_pairs = []
    
    print("\n[*] Running technical analysis on liquid pairs...")
    
    standard_count = 0
    deep_value_count = 0
    
    for pair in liquid_pairs:
        coin, price = pair['coin'], pair['price']
        try:
            candles = fetch_candles(coin)
            if not candles: continue
            passed, metrics = analyze_pair(candles, price)
            
            if passed:
                qualified_pairs.append({"coin": coin, "price": price, "volume_24h": pair['volume'], "metrics": metrics})
                standard_count += 1
                print(f"  [PASS] {coin} -> Vol: ${pair['volume']/1e6:.1f}M | EMA Gap: {metrics['EMA_Gap_Pct']}% | ATR: {metrics['ATR_Pct']}% | BBW: {metrics['BBW_Pct']}% | RSI: {metrics.get('RSI', '?')} | Rally: {metrics.get('Rally_Pct', '?')}%")
            else:
                # Second chance: Deep Value scan for oversold coins
                dv_passed, dv_metrics = analyze_pair_deep_value(candles, price)
                if dv_passed:
                    qualified_pairs.append({"coin": coin, "price": price, "volume_24h": pair['volume'], "metrics": dv_metrics})
                    deep_value_count += 1
                    print(f"  [DEEP VALUE] {coin} -> Vol: ${pair['volume']/1e6:.1f}M | RSI: {dv_metrics['RSI']} | ATR: {dv_metrics['ATR_Pct']}% | BB Pos: {dv_metrics['BB_Position']}% | EMA50 Slope: RISING")
                elif isinstance(metrics, str) and "OVEREXTENDED" in metrics:
                    print(f"  [SKIP] {coin} -> {metrics}")
        except Exception as e:
            print(f"  [ERROR] {coin}: {str(e)}")
        time.sleep(0.1)
        
    print("="*60)
    print(f" SCAN COMPLETE. Found {len(qualified_pairs)} qualified pairs ({standard_count} standard + {deep_value_count} deep value) out of {len(liquid_pairs)}.")
    print("="*60)
    
    output_file = os.path.join(os.path.dirname(__file__), "..", "data", "qualified_pairs.json")
    with open(output_file, 'w') as f:
        json.dump(qualified_pairs, f, indent=4)
    print(f"[*] Saved qualified pairs to {output_file}")

if __name__ == "__main__":
    main()
