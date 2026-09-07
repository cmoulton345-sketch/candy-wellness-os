import json
import os
import math
import time
import requests

# ============================================================
#  FLOWSTATE AI MOONSHOT SCANNER v2
#  Finds high-momentum coins on Hyperliquid using MAINNET data
#  Filters for real liquidity, overextension, and momentum
# ============================================================

# MAINNET API for real market data (scanning only — no trades placed)
API_URL = "https://api.hyperliquid.xyz/info"

# --- Scanner Thresholds ---
MIN_VOLUME_USD = 1_000_000      # $1M minimum daily volume — must be able to exit
MAX_VOLUME_USD = 50_000_000     # $50M cap — above this is blue-chip territory, not moonshot
MIN_VOLUME_SURGE = 2.0          # Recent volume must be 2x+ vs average
MIN_SCORE = 50                  # Minimum score to qualify

# --- Overextension Thresholds ---
MAX_RSI = 78                    # RSI above this = too hot for entry
MAX_RALLY_FROM_LOW_PCT = 60     # Moonshots can rally more, but 60%+ = late
MAX_DISTANCE_FROM_EMA50 = 0.25  # 25% above EMA50 = overextended (wider than core)


def fetch_markets_and_volumes():
    """Get all markets with 24h volume from Hyperliquid mainnet."""
    try:
        payload = {"type": "metaAndAssetCtxs"}
        response = requests.post(API_URL, json=payload, timeout=10)
        data = response.json()
        
        universe = data[0]["universe"]
        contexts = data[1]
        
        markets = []
        for i, asset in enumerate(universe):
            coin = asset["name"]
            ctx = contexts[i]
            day_volume = float(ctx.get("dayNtlVlm", 0))
            mark_price = float(ctx.get("markPx", 0))
            
            if mark_price > 0:
                markets.append({
                    "coin": coin,
                    "price": mark_price,
                    "volume_24h": day_volume,
                    "maxLeverage": asset.get("maxLeverage", 0)
                })
        
        return markets
    except Exception as e:
        print(f"[!] Error fetching markets: {e}")
        return []


def fetch_candles(coin, interval="1h", lookback_hours=168):
    """Fetch 7 days of hourly candles for analysis."""
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
            "open": float(c["o"]),
            "high": float(c["h"]),
            "low": float(c["l"]),
            "close": float(c["c"]),
            "volume": float(c["v"])
        } for c in candles]
    except Exception as e:
        print(f"  [!] Candle fetch error for {coin}: {e}")
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
        change = prices[i] - prices[i-1]
        gains.append(max(change, 0))
        losses.append(abs(min(change, 0)))
    avg_gain = sum(gains[:window]) / window
    avg_loss = sum(losses[:window]) / window
    for i in range(window, len(gains)):
        avg_gain = (avg_gain * (window - 1) + gains[i]) / window
        avg_loss = (avg_loss * (window - 1) + losses[i]) / window
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def calculate_atr(candles, window=14):
    if len(candles) < window + 1:
        return None
    trs = []
    for i in range(1, len(candles)):
        high = candles[i]["high"]
        low = candles[i]["low"]
        prev_close = candles[i - 1]["close"]
        tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
        trs.append(tr)
    if len(trs) < window:
        return None
    return sum(trs[-window:]) / window


def check_overextension(prices, current_price, ema50):
    """Check if coin is overextended — returns (is_overextended, reasons)."""
    reasons = []
    
    rsi = calculate_rsi(prices, 14)
    if rsi and rsi > MAX_RSI:
        reasons.append(f"RSI {rsi:.1f} > {MAX_RSI}")
    
    lookback_low = min(prices[-50:]) if len(prices) >= 50 else min(prices)
    if lookback_low > 0:
        rally_pct = ((current_price - lookback_low) / lookback_low) * 100
        if rally_pct > MAX_RALLY_FROM_LOW_PCT:
            reasons.append(f"Rally {rally_pct:.0f}% from low")
    
    if ema50 and ema50 > 0:
        distance = (current_price - ema50) / ema50
        if distance > MAX_DISTANCE_FROM_EMA50:
            reasons.append(f"{distance*100:.1f}% above EMA50")
    
    return len(reasons) >= 2, reasons, rsi


def analyze_moonshot(coin, candles, volume_24h):
    """
    Moonshot scoring v2 — looks for early-stage breakout coins
    with REAL volume and momentum, filtered for overextension.
    """
    if not candles or len(candles) < 50:
        return None
    
    prices = [c["close"] for c in candles]
    current_price = prices[-1]
    
    # --- Volume Analysis ---
    volumes = [c["volume"] for c in candles]
    if len(volumes) < 48:
        return None
    
    recent_24h_vol = sum(volumes[-24:])
    avg_daily_vol = sum(volumes) / (len(volumes) / 24)
    
    if avg_daily_vol == 0:
        return None
    
    volume_surge = recent_24h_vol / avg_daily_vol
    
    # --- Trend Analysis ---
    ema21 = calculate_ema(prices, 21)
    ema50 = calculate_ema(prices, 50)
    
    if not ema21 or not ema50 or ema50 == 0:
        return None
    
    uptrend = ema21 > ema50
    momentum_pct = ((current_price - ema50) / ema50) * 100
    
    # --- RSI ---
    rsi = calculate_rsi(prices, 14)
    
    # --- Volatility ---
    atr = calculate_atr(candles)
    if not atr or current_price == 0:
        return None
    atr_pct = (atr / current_price) * 100
    
    # --- Overextension Check ---
    is_overextended, ext_reasons, _ = check_overextension(prices, current_price, ema50)
    if is_overextended:
        return {"coin": coin, "rejected": True, "reason": f"OVEREXTENDED: {' | '.join(ext_reasons)}"}
    
    # --- Moonshot Score (0-100) ---
    score = 0
    reasons = []
    
    # Volume surge (max 25 pts)
    if volume_surge >= 3.0:
        score += 25
        reasons.append(f"Volume SURGE {volume_surge:.1f}x")
    elif volume_surge >= 2.0:
        score += 15
        reasons.append(f"Volume growing {volume_surge:.1f}x")
    elif volume_surge >= 1.5:
        score += 5
        reasons.append(f"Volume uptick {volume_surge:.1f}x")
    
    # Uptrend (max 25 pts)
    if uptrend and momentum_pct > 15:
        score += 25
        reasons.append(f"Strong uptrend +{momentum_pct:.0f}% above EMA50")
    elif uptrend and momentum_pct > 5:
        score += 15
        reasons.append(f"Uptrend +{momentum_pct:.0f}% above EMA50")
    elif uptrend:
        score += 10
        reasons.append(f"Early uptrend forming")
    
    # Volatility (max 25 pts)
    if atr_pct > 6:
        score += 25
        reasons.append(f"Extreme volatility ATR {atr_pct:.1f}%")
    elif atr_pct > 4:
        score += 20
        reasons.append(f"High volatility ATR {atr_pct:.1f}%")
    elif atr_pct > 3:
        score += 10
        reasons.append(f"Good volatility ATR {atr_pct:.1f}%")
    
    # Price momentum — recent acceleration (max 25 pts)
    if len(prices) >= 72:
        price_3d_ago = prices[-72]
        price_change_3d = ((current_price - price_3d_ago) / price_3d_ago) * 100
        
        if price_change_3d > 30:
            score += 25
            reasons.append(f"3-day move +{price_change_3d:.0f}%")
        elif price_change_3d > 15:
            score += 20
            reasons.append(f"3-day move +{price_change_3d:.0f}%")
        elif price_change_3d > 5:
            score += 10
            reasons.append(f"3-day move +{price_change_3d:.0f}%")
    
    return {
        "coin": coin,
        "price": current_price,
        "score": score,
        "volume_24h": volume_24h,
        "volume_surge": volume_surge,
        "momentum_pct": momentum_pct,
        "atr_pct": atr_pct,
        "rsi": rsi,
        "uptrend": uptrend,
        "reasons": reasons,
        "rejected": False
    }


def main():
    print("=" * 60)
    print(" FLOWSTATE AI MOONSHOT SCANNER v2")
    print(" Real volume data from Hyperliquid MAINNET")
    print("=" * 60)
    
    # Get all markets with real volume
    markets = fetch_markets_and_volumes()
    print(f"[*] Fetched {len(markets)} markets from mainnet\n")
    
    # Filter: moonshot range — $1M to $50M daily volume
    moonshot_range = [m for m in markets if MIN_VOLUME_USD <= m["volume_24h"] <= MAX_VOLUME_USD]
    blue_chips = [m for m in markets if m["volume_24h"] > MAX_VOLUME_USD]
    dust = [m for m in markets if m["volume_24h"] < MIN_VOLUME_USD]
    
    print(f"[*] Volume breakdown:")
    print(f"    Blue chips (>${MAX_VOLUME_USD/1e6:.0f}M): {len(blue_chips)} — too big for moonshots")
    print(f"    Moonshot range (${MIN_VOLUME_USD/1e6:.0f}M-${MAX_VOLUME_USD/1e6:.0f}M): {len(moonshot_range)} — scanning these")
    print(f"    Dust (<${MIN_VOLUME_USD/1e6:.0f}M): {len(dust)} — illiquid, skipping")
    
    # Skip stablecoins and wrapped assets
    skip_coins = {"USDC", "USDT", "DAI", "WBTC", "WETH", "stETH", "BTC", "ETH"}
    
    candidates = []
    overextended = []
    
    print(f"\n[*] Analyzing {len(moonshot_range)} coins...\n")
    
    for market in moonshot_range:
        coin = market["coin"]
        
        if coin in skip_coins:
            continue
        
        candles = fetch_candles(coin)
        if not candles:
            continue
        
        result = analyze_moonshot(coin, candles, market["volume_24h"])
        if not result:
            continue
        
        if result.get("rejected"):
            overextended.append(result)
            print(f"  [SKIP] {coin:>8} | {result['reason']}")
            continue
        
        if result["score"] >= MIN_SCORE and result["uptrend"]:
            candidates.append(result)
            print(f"  [HIT]  {coin:>8} | Score: {result['score']:>3} | Vol: ${result['volume_24h']/1e6:.1f}M | Surge: {result['volume_surge']:.1f}x | RSI: {result['rsi']:.0f} | +{result['momentum_pct']:.0f}%")
        
        time.sleep(0.1)
    
    # Sort by score
    candidates.sort(key=lambda x: x["score"], reverse=True)
    
    print(f"\n{'=' * 60}")
    print(f" SCAN COMPLETE")
    print(f" {len(candidates)} moonshot candidates | {len(overextended)} overextended (skipped)")
    print(f"{'=' * 60}")
    
    if candidates:
        print(f"\n{'='*60}")
        print(f" TOP MOONSHOT CANDIDATES (Ranked by Score)")
        print(f"{'='*60}")
        
        for i, c in enumerate(candidates[:10], 1):
            print(f"\n  #{i}  {c['coin']}")
            print(f"      Price:    ${c['price']:.6f}")
            print(f"      Score:    {c['score']}/100")
            print(f"      Volume:   ${c['volume_24h']/1e6:.1f}M (24h) | Surge: {c['volume_surge']:.1f}x")
            print(f"      Momentum: +{c['momentum_pct']:.1f}% above EMA50")
            print(f"      RSI:      {c['rsi']:.1f}")
            print(f"      ATR:      {c['atr_pct']:.1f}%")
            print(f"      Signals:  {', '.join(c['reasons'])}")
        
        # Save top candidates
        output_file = os.path.join(os.path.dirname(__file__), "..", "data", "moonshot_candidates.json")
        save_data = [{
            "coin": c["coin"],
            "price": c["price"],
            "score": c["score"],
            "volume_24h": round(c["volume_24h"], 2),
            "volume_surge": round(c["volume_surge"], 2),
            "momentum_pct": round(c["momentum_pct"], 2),
            "atr_pct": round(c["atr_pct"], 2),
            "rsi": round(c["rsi"], 1) if c["rsi"] else None,
            "reasons": c["reasons"]
        } for c in candidates[:10]]
        
        with open(output_file, "w") as f:
            json.dump(save_data, f, indent=4)
        print(f"\n[*] Saved top candidates to {output_file}")
        print(f"[*] Next step: python moonshot_fa_agent.py")
    else:
        print("\n[-] No moonshot candidates found. Market may be quiet — check back later.")


if __name__ == "__main__":
    main()
