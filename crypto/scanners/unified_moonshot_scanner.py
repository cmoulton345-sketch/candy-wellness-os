import json
import os
import re
import time
import requests
import math
from datetime import datetime, timezone

# ============================================================
#  FLOWSTATE AI — UNIFIED MOONSHOT SCANNER
#  Consolidates New Listings and Social Narrative Scanners
#  to optimize API usage, reduce rate limits, and output to
#  a single, unified candidates file for the FA Agent.
# ============================================================

HYPERLIQUID_API    = "https://api.hyperliquid.xyz/info"
COINGECKO_SEARCH   = "https://api.coingecko.com/api/v3/search"
COINGECKO_TRENDING = "https://api.coingecko.com/api/v3/search/trending"
COINGECKO_COIN      = "https://api.coingecko.com/api/v3/coins/{id}"
REDDIT_NEW          = "https://www.reddit.com/r/CryptoMoonShots/new.json?limit=100"
REDDIT_HOT          = "https://www.reddit.com/r/CryptoMoonShots/hot.json?limit=50"
REDDIT_HEADERS      = {"User-Agent": "FlowstateAI/1.0 (unified-moonshot-scanner)"}

# --- Base Settings ---
MIN_VOLUME_24H      = 250_000  # $250K minimum daily volume to check any coin

# --- Route A: New Listing Engine Parameters ---
MAX_AGE_NEW_LISTING = 30       # Days on HL to qualify as fresh listing
MAX_DUMP_PCT        = 0.90     # Skip if price dropped >90% from launch high
MAX_PRICE_NEW       = 2.00     # Max price for a new listing candidate
MIN_SCORE_NEW       = 25       # Minimum score for Route A

# --- Route B: Social Narrative Engine Parameters ---
MAX_AGE_NARRATIVE   = 60      # Max listing age on HL to qualify
MAX_PRICE_NARRATIVE = 1.00     # Price must be under $1.00 to qualify
MIN_MC              = 100_000  # $100K minimum market cap
MAX_MC              = 10_000_000 # $10M max market cap (underdeveloped gem)
MAX_RSI_ENTRY       = 68       # RSI above this is overheated
MAX_EMA_EXTENSION   = 0.22     # 22% above EMA21 max
MIN_SCORE_NARRATIVE = 35       # Minimum score for Route B


# =============================================================
# DATA FETCHING PIPELINE
# =============================================================

def fetch_reddit_mentions():
    """Scan Reddit r/CryptoMoonShots for ticker mentions in the last 24h."""
    print("[*] Scanning Reddit r/CryptoMoonShots...")
    ticker_pattern = re.compile(r'\b\$?([A-Z]{2,8})\b')
    skip = {
        "I", "A", "CEO", "ICO", "AMA", "NFT", "DeFi", "DAO", "ATH", "ATL",
        "USD", "USDT", "USDC", "BTC", "ETH", "SOL", "BNB", "TRX", "FUD",
        "FOMO", "KYC", "DEX", "CEX", "API", "GPU", "AI", "ML", "GPT",
        "IMO", "TBH", "LFG", "GG", "OP", "UP", "DD", "FOR", "NOT", "NEW",
        "ALL", "ARE", "THE", "BUT", "TOP", "HOW", "WHY", "GET", "OUT",
        "HAS", "ITS", "AND", "CAN", "NOW", "RUN", "SEE", "DID", "USE"
    }
    mentions = {}
    now = time.time()
    for url in [REDDIT_HOT, REDDIT_NEW]:
        try:
            r = requests.get(url, headers=REDDIT_HEADERS, timeout=10)
            posts = r.json().get("data", {}).get("children", [])
            for post in posts:
                p = post.get("data", {})
                if now - p.get("created_utc", 0) > 86400:
                    continue
                text = f"{p.get('title', '')} {p.get('selftext', '')}".upper()
                for ticker in ticker_pattern.findall(text):
                    if ticker not in skip and len(ticker) >= 2:
                        mentions[ticker] = mentions.get(ticker, 0) + 1
            time.sleep(1)
        except Exception as e:
            print(f"    [!] Reddit error: {e}")
    
    # Filter for signals (2+ mentions)
    qualified = {k: v for k, v in mentions.items() if v >= 2}
    print(f"    Found {len(qualified)} symbols with 2+ Reddit mentions (Total raw mentions: {len(mentions)})")
    return mentions, qualified


def fetch_coingecko_trending():
    """Get current CoinGecko trending coin symbols."""
    print("[*] Fetching CoinGecko Trending...")
    try:
        r = requests.get(COINGECKO_TRENDING, timeout=10)
        coins = r.json().get("coins", [])
        trending = []
        trending_symbols = set()
        for item in coins:
            coin = item.get("item", {})
            sym = coin.get("symbol", "").upper()
            trending.append({
                "symbol": sym,
                "name": coin.get("name", ""),
                "id": coin.get("id", ""),
                "rank": coin.get("score", 99),
            })
            trending_symbols.add(sym)
        print(f"    Found {len(trending)} trending coins on CoinGecko")
        return trending, trending_symbols
    except Exception as e:
        print(f"    [!] CoinGecko trending failed: {e}")
        return [], set()


def fetch_hl_universe():
    """Fetch all active coins on Hyperliquid with mark price and 24h volume."""
    print("[*] Fetching Hyperliquid universe...")
    try:
        r = requests.post(HYPERLIQUID_API, json={"type": "metaAndAssetCtxs"}, timeout=10)
        data = r.json()
        universe = data[0]["universe"]
        contexts = data[1]
        coins = {}
        for i, asset in enumerate(universe):
            name = asset["name"].upper()
            ctx = contexts[i]
            price = float(ctx.get("markPx", 0))
            volume = float(ctx.get("dayNtlVlm", 0))
            oi = float(ctx.get("openInterest", 0))
            if price > 0:
                coins[name] = {"price": price, "volume_24h": volume, "open_interest": oi}
        print(f"    {len(coins)} total tradeable coins, {sum(1 for c in coins.values() if c['volume_24h'] >= MIN_VOLUME_24H)} with >${MIN_VOLUME_24H/1e3:.0f}K+ daily volume")
        return coins
    except Exception as e:
        print(f"    [!] HL fetch failed: {e}")
        return {}


def get_listing_age(coin):
    """Estimate listing age on HL by counting daily candles over the last 1 year."""
    try:
        end = int(time.time() * 1000)
        start = end - (365 * 24 * 3600 * 1000)
        r = requests.post(HYPERLIQUID_API, json={
            "type": "candleSnapshot",
            "req": {"coin": coin, "interval": "1d", "startTime": start, "endTime": end}
        }, timeout=10)
        candles = r.json()
        if not candles:
            return None, []
        return len(candles), candles
    except Exception:
        return None, []


def fetch_candles_1h(coin, hours=120):
    """Fetch 1h candles for TA indicators (RSI + EMA)."""
    end = int(time.time() * 1000)
    start = end - (hours * 3600 * 1000)
    try:
        r = requests.post(HYPERLIQUID_API, json={
            "type": "candleSnapshot",
            "req": {"coin": coin, "interval": "1h", "startTime": start, "endTime": end}
        }, timeout=10)
        candles = r.json()
        if not candles:
            return None
        return [{"close": float(c["c"]), "high": float(c["h"]), "low": float(c["l"]), "volume": float(c["v"])} for c in candles]
    except Exception:
        return None


# =============================================================
# COINGECKO RESOLVERS
# =============================================================

def find_coingecko_id(symbol):
    """Search CoinGecko for a coin ID by symbol."""
    try:
        r = requests.get(COINGECKO_SEARCH, params={"query": symbol}, timeout=10)
        results = r.json().get("coins", [])
        for coin in results[:5]:
            if coin.get("symbol", "").upper() == symbol.upper():
                return coin.get("id", ""), coin.get("name", "")
        return None, None
    except Exception:
        return None, None


def fetch_market_cap(coingecko_id):
    """Fetch circulating market cap + genesis date from CoinGecko by coin ID."""
    try:
        url = COINGECKO_COIN.format(id=coingecko_id)
        r = requests.get(url, timeout=10, params={"localization": "false", "tickers": "false", "community_data": "false", "developer_data": "false"})
        data = r.json()
        mdata = data.get("market_data", {})
        mc = mdata.get("market_cap", {}).get("usd", None)
        fdv = mdata.get("fully_diluted_valuation", {}).get("usd", None)
        genesis_date = data.get("genesis_date", None)
        return mc, fdv, genesis_date
    except Exception:
        return None, None, None


# =============================================================
# CALCULATIONS
# =============================================================

def calculate_ema(prices, window):
    if len(prices) < window: return None
    mult = 2 / (window + 1)
    ema = sum(prices[:window]) / window
    for p in prices[window:]:
        ema = (p - ema) * mult + ema
    return ema


def calculate_rsi(prices, window=14):
    if len(prices) < window + 1: return None
    gains, losses = [], []
    for i in range(1, len(prices)):
        chg = prices[i] - prices[i - 1]
        gains.append(max(chg, 0))
        losses.append(abs(min(chg, 0)))
    ag = sum(gains[:window]) / window
    al = sum(losses[:window]) / window
    for i in range(window, len(gains)):
        ag = (ag * (window - 1) + gains[i]) / window
        al = (al * (window - 1) + losses[i]) / window
    if al == 0: return 100
    return 100 - (100 / (1 + ag / al))


# =============================================================
# ROUTE A: NEW LISTING ENGINE
# =============================================================

def check_volume_momentum(candles):
    """Compare recent volume (last 7 days) vs launch volume (first 7 days)."""
    if not candles or len(candles) < 7:
        return 0.0, "insufficient data"
    volumes = [float(c.get("v", 0)) * float(c.get("c", 0)) for c in candles]  # vol in USD
    early_vol = sum(volumes[:7]) / 7 if len(volumes) >= 7 else 0
    recent_vol = sum(volumes[-7:]) / 7
    if early_vol == 0:
        return 0.0, "no early volume data"
    ratio = recent_vol / early_vol
    if ratio >= 2.0:
        label = f"Volume 2x+ vs launch ({ratio:.1f}x) — momentum BUILDING"
    elif ratio >= 1.0:
        label = f"Volume holding vs launch ({ratio:.1f}x) — stable"
    elif ratio >= 0.5:
        label = f"Volume declining vs launch ({ratio:.1f}x) — cooling off"
    else:
        label = f"Volume collapsed vs launch ({ratio:.1f}x) — fading"
    return ratio, label


def check_price_health(candles, current_price):
    """Check drawdown from launch peak. Returns (healthy, launch_price, drawdown_pct, label)."""
    if not candles:
        return True, current_price, 0, "no history"
    launch_price = float(candles[0].get("o", current_price))
    all_highs = [float(c.get("h", 0)) for c in candles]
    peak = max(all_highs) if all_highs else current_price
    drawdown = (peak - current_price) / peak if peak > 0 else 0
    change_from_launch = (current_price - launch_price) / launch_price * 100 if launch_price > 0 else 0
    
    if drawdown > MAX_DUMP_PCT:
        return False, launch_price, drawdown, f"DOWN {drawdown*100:.0f}% from peak — possible rug"
    elif drawdown > 0.70:
        label = f"Down {drawdown*100:.0f}% from peak, launch: ${launch_price:.6f}"
    elif change_from_launch > 0:
        label = f"Up {change_from_launch:.0f}% from launch ${launch_price:.6f}"
    else:
        label = f"Down {abs(change_from_launch):.0f}% from launch ${launch_price:.6f}"
    return True, launch_price, drawdown, label


def score_new_listing(age_days, vol_ratio, drawdown, reddit_mentions, on_cg, cg_trending, current_price):
    score = 0
    reasons = []
    
    # Age score (max 30 pts)
    if age_days <= 14:
        score += 30
        reasons.append(f"Listed {age_days}d ago — prime discovery window")
    elif age_days <= 30:
        score += 22
        reasons.append(f"Listed {age_days}d ago — under 1 month")
    elif age_days <= 45:
        score += 14
        reasons.append(f"Listed {age_days}d ago — early listing stage")
    else:
        score += 6
        reasons.append(f"Listed {age_days}d ago — under 2 months")
        
    # Vol momentum (max 25 pts)
    if vol_ratio >= 2.0:
        score += 25
        reasons.append(f"Volume 2x+ vs launch ({vol_ratio:.1f}x)")
    elif vol_ratio >= 1.0:
        score += 15
        reasons.append(f"Volume stable vs launch ({vol_ratio:.1f}x)")
    elif vol_ratio >= 0.5:
        score += 5
        reasons.append(f"Volume cooling ({vol_ratio:.1f}x)")
        
    # Price health (max 15 pts)
    if drawdown < 0.30:
        score += 15
        reasons.append("Price holding strong (<30% from peak)")
    elif drawdown < 0.50:
        score += 10
        reasons.append(f"Price pullback moderate ({drawdown*100:.0f}% from peak)")
    elif drawdown < 0.70:
        score += 4
        reasons.append(f"Price pullback deep ({drawdown*100:.0f}% from peak)")
        
    # Reddit mentions (max 15 pts)
    if reddit_mentions >= 5:
        score += 15
        reasons.append(f"Reddit VIRAL — {reddit_mentions} mentions in 24h")
    elif reddit_mentions >= 2:
        score += 10
        reasons.append(f"Reddit BUZZ — {reddit_mentions} mentions in 24h")
    elif reddit_mentions == 1:
        score += 5
        reasons.append("Reddit — early mention detected")
        
    # CoinGecko indexed (max 10 pts)
    if cg_trending:
        score += 10
        reasons.append("CoinGecko TRENDING — high traffic")
    elif on_cg:
        score += 5
        reasons.append("CoinGecko indexed — visibility growing")
        
    # Price unit bonus (max 5 pts)
    if current_price < 0.001:
        score += 5
        reasons.append("Sub-$0.001 price — high unit multiplier potential")
    elif current_price < 0.01:
        score += 3
        reasons.append("Sub-cent price")
        
    return score, reasons


# =============================================================
# ROUTE B: SOCIAL NARRATIVE ENGINE
# =============================================================

def score_ta_entry(coin, current_price):
    candles = fetch_candles_1h(coin)
    if not candles or len(candles) < 30:
        return 20, None, None, ["Insufficient candle data — neutral TA"]
    prices = [c["close"] for c in candles]
    volumes = [c["volume"] for c in candles]
    rsi = calculate_rsi(prices, 14)
    ema21 = calculate_ema(prices, 21)
    
    score = 0
    reasons = []
    
    # RSI (0-20 pts)
    if rsi:
        if rsi < 35:
            score += 20
            reasons.append(f"RSI {rsi:.0f} — oversold pullback")
        elif rsi < 45:
            score += 16
            reasons.append(f"RSI {rsi:.0f} — cool entry window")
        elif rsi < 55:
            score += 12
            reasons.append(f"RSI {rsi:.0f} — neutral")
        elif rsi < 65:
            score += 6
            reasons.append(f"RSI {rsi:.0f} — warm, wait for cooling")
            
    # Proximity to EMA21 (0-20 pts)
    if ema21 and ema21 > 0:
        dist = (current_price - ema21) / ema21
        if dist <= 0.05:
            score += 20
            reasons.append("Price within 5% of EMA21 — breakout/pullback support")
        elif dist <= 0.10:
            score += 15
            reasons.append(f"Price {dist*100:.1f}% above EMA21 — good buy zone")
        elif dist <= 0.20:
            score += 8
            reasons.append(f"Price {dist*100:.1f}% above EMA21 — slightly extended")
            
    return score, rsi, ema21, reasons


def compute_mc_score(market_cap):
    if market_cap is None: return 5, "MC unknown"
    if market_cap < 1_000_000:
        return 20, f"MC ${market_cap/1e6:.2f}M — micro cap"
    elif market_cap < 3_000_000:
        return 17, f"MC ${market_cap/1e6:.1f}M — prime early stage"
    elif market_cap < 6_000_000:
        return 13, f"MC ${market_cap/1e6:.1f}M — solid low cap"
    elif market_cap < 10_000_000:
        return 8,  f"MC ${market_cap/1e6:.1f}M — moderate moonshot cap"
    return 0, f"MC ${market_cap/1e6:.1f}M — too large for moonshot"


def compute_price_score(price):
    if price < 0.00001: return 20, f"Price ${price:.8f} — ultra cheap"
    elif price < 0.0001: return 18, f"Price ${price:.7f} — sub-millicent"
    elif price < 0.001: return 15, f"Price ${price:.6f} — sub-cent"
    elif price < 0.01: return 12, f"Price ${price:.5f} — cheap"
    elif price < 0.10: return 7,  f"Price ${price:.4f} — low price"
    elif price < 1.00: return 3,  f"Price ${price:.3f} — moderate"
    return 0, f"Price ${price:.2f} — over $1.00"


def compute_age_score(genesis_date):
    if not genesis_date: return 0, None
    try:
        listed = datetime.strptime(genesis_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        days_old = (datetime.now(timezone.utc) - listed).days
        if days_old < 90: return 10, f"CG listed {days_old}d ago — fresh launch"
        elif days_old < 180: return 7, f"CG listed {days_old}d ago — early listing"
        elif days_old < 365: return 3, f"CG listed {days_old}d ago — under 1 year"
    except Exception:
        pass
    return 0, None


def compute_hl_age_score(days_on_hl):
    if days_on_hl is None: return 5, "HL age unknown"
    if days_on_hl <= 30: return 15, f"On HL {days_on_hl}d — first month discovery"
    elif days_on_hl <= 60: return 12, f"On HL {days_on_hl}d — very fresh"
    elif days_on_hl <= 90: return 9, f"On HL {days_on_hl}d — fresh window"
    elif days_on_hl <= 180: return 5, f"On HL {days_on_hl}d — under 6 months"
    elif days_on_hl <= 270: return 2, f"On HL {days_on_hl}d — established"
    return 0, f"On HL {days_on_hl}d — old listing"


# =============================================================
# MAIN UNIFIED PIPELINE
# =============================================================

def main():
    print("=" * 60)
    print(" FLOWSTATE AI — UNIFIED MOONSHOT SCANNER (SIS + NEW LISTING)")
    print("=" * 60)
    print()

    # Step 1: Global Social Data Fetching (Run once to save API requests)
    reddit_raw, reddit_signals = fetch_reddit_mentions()
    cg_trending_list, cg_trending_symbols = fetch_coingecko_trending()
    
    # Step 2: Fetch Hyperliquid Active Markets
    hl_universe = fetch_hl_universe()
    if not hl_universe:
        print("[!] Could not fetch data from Hyperliquid. Exiting.")
        return
        
    print()
    print("-" * 60)
    print(f"[*] Analyzing HL markets (Scanning {len(hl_universe)} active assets)...")
    print("-" * 60)

    results = []
    
    # Build list of candidates to scan
    # Filter by 24h volume to ensure minimum tradeability
    liquid_hl_coins = {k: v for k, v in hl_universe.items() if v["volume_24h"] >= MIN_VOLUME_24H}
    
    # We will fetch candle snapshots for these liquid coins to verify age
    print(f"[*] Checking listing age for {len(liquid_hl_coins)} liquid coins...")
    print("    (This takes ~1 min due to sequential API checks with 0.25s rate limits)")
    print()
    
    count = 0
    for coin, data in liquid_hl_coins.items():
        count += 1
        current_price = data["price"]
        volume_24h = data["volume_24h"]
        
        # 1. Fetch HL listing age
        days_on_hl, candles = get_listing_age(coin)
        time.sleep(0.25)  # Cooldown to protect Hyperliquid info API
        
        if days_on_hl is None:
            continue
            
        is_fresh_listing = days_on_hl <= MAX_AGE_NEW_LISTING
        is_narrative_candidate = (
            days_on_hl <= MAX_AGE_NARRATIVE and 
            current_price < MAX_PRICE_NARRATIVE
        )
        
        # Check if we should process Route A (New Listing)
        passed_route_a = False
        route_a_data = {}
        if is_fresh_listing and current_price <= MAX_PRICE_NEW:
            # Run Route A check
            healthy, launch_price, drawdown, health_label = check_price_health(candles, current_price)
            if healthy:
                vol_ratio, vol_label = check_volume_momentum(candles)
                reddit_count = reddit_raw.get(coin, 0)
                on_cg = (coin in cg_trending_symbols) or (reddit_count > 0) # basic CG flag
                in_trending = coin in cg_trending_symbols
                
                score, reasons = score_new_listing(
                    days_on_hl, vol_ratio, drawdown,
                    reddit_count, on_cg, in_trending, current_price
                )
                
                if score >= MIN_SCORE_NEW:
                    passed_route_a = True
                    route_a_data = {
                        "coin": coin,
                        "name": coin,
                        "type": "new_listing",
                        "price": current_price,
                        "score": score,
                        "volume_24h": round(volume_24h, 2),
                        "market_cap": None,
                        "days_on_hl": days_on_hl,
                        "launch_price": round(launch_price, 8),
                        "drawdown_pct": round(drawdown * 100, 1),
                        "vol_momentum": round(vol_ratio, 2),
                        "reddit_mentions": reddit_count,
                        "on_coingecko": on_cg,
                        "cg_trending": in_trending,
                        "rsi": None,
                        "ema21": None,
                        "sources": ["Hyperliquid New Listing"] + (["Reddit r/CryptoMoonShots"] if reddit_count >= 2 else []) + (["CoinGecko Trending"] if in_trending else []),
                        "reasons": reasons,
                        # FA Compatibility
                        "volume_surge": round(vol_ratio, 2),
                        "momentum_pct": round((1 - drawdown) * 100, 2),
                        "atr_pct": 0
                    }

        # Check if we should process Route B (Social Narrative)
        passed_route_b = False
        route_b_data = {}
        # Social Narrative requires active buzz to trigger CoinGecko search (to avoid query spam)
        has_buzz = (coin in cg_trending_symbols) or (coin in reddit_signals)
        
        if is_narrative_candidate and has_buzz:
            # Resolve CoinGecko ID
            cg_id, cg_name = find_coingecko_id(coin)
            time.sleep(0.3)
            
            if cg_id:
                # Fetch market cap & genesis date
                market_cap, fdv, genesis_date = fetch_market_cap(cg_id)
                time.sleep(1.0) # Rate limit protect
                
                # Check MC hard gates
                if market_cap and (MIN_MC <= market_cap <= MAX_MC):
                    # Score TA
                    ta_pts, rsi, ema21, ta_reasons = score_ta_entry(coin, current_price)
                    
                    # Check TA hard gates
                    passed_ta_gates = True
                    if rsi and rsi > MAX_RSI_ENTRY:
                        passed_ta_gates = False
                    if ema21 and ema21 > 0:
                        ext = (current_price - ema21) / ema21
                        if ext > MAX_EMA_EXTENSION:
                            passed_ta_gates = False
                            
                    if passed_ta_gates:
                        # Build Score
                        score = 0
                        reasons = []
                        
                        # CG trending score
                        if coin in cg_trending_symbols:
                            rank = next((item["rank"] for item in cg_trending_list if item["symbol"] == coin), 5)
                            pts = max(5, 20 - (rank * 2))
                            score += pts
                            reasons.append(f"CoinGecko Trending (rank #{rank+1})")
                            
                        # Reddit score
                        reddit_count = reddit_raw.get(coin, 0)
                        red_pts, red_reason = compute_reddit_score(reddit_count)
                        score += red_pts
                        if red_reason: reasons.append(red_reason)
                        
                        # Market Cap score
                        mc_pts, mc_reason = compute_mc_score(market_cap)
                        score += mc_pts
                        reasons.append(mc_reason)
                        
                        # Price score
                        price_pts, price_reason = compute_price_score(current_price)
                        score += price_pts
                        reasons.append(price_reason)
                        
                        # CG Genesis Age score
                        age_pts, age_reason = compute_age_score(genesis_date)
                        score += age_pts
                        if age_reason: reasons.append(age_reason)
                        
                        # HL Age score
                        hl_pts, hl_reason = compute_hl_age_score(days_on_hl)
                        score += hl_pts
                        if hl_reason: reasons.append(hl_reason)
                        
                        # TA score
                        score += ta_pts
                        reasons.extend(ta_reasons)
                        
                        if score >= MIN_SCORE_NARRATIVE:
                            passed_route_b = True
                            route_b_data = {
                                "coin": coin,
                                "name": cg_name or coin,
                                "type": "social_narrative",
                                "price": current_price,
                                "score": score,
                                "volume_24h": round(volume_24h, 2),
                                "market_cap": round(market_cap, 2),
                                "days_on_hl": days_on_hl,
                                "launch_price": None,
                                "drawdown_pct": None,
                                "vol_momentum": 1.0,
                                "reddit_mentions": reddit_count,
                                "on_coingecko": True,
                                "cg_trending": coin in cg_trending_symbols,
                                "rsi": round(rsi, 1) if rsi else None,
                                "ema21": round(ema21, 6) if ema21 else None,
                                "sources": (["CoinGecko Trending"] if coin in cg_trending_symbols else []) + (["Reddit r/CryptoMoonShots"] if reddit_count >= 2 else []),
                                "reasons": reasons,
                                # FA Compatibility
                                "volume_surge": 1.0,
                                "momentum_pct": round(((current_price - ema21) / ema21) * 100, 2) if ema21 else 0,
                                "atr_pct": 0
                            }

        # Add to results if either route passed
        # If a coin passes both routes, prefer the Route B (Social Narrative) data as it contains MC & TA details
        if passed_route_b:
            print(f"  [HIT] {coin:>6} — Social Narrative Opportunity! | Score: {route_b_data['score']}/100 | MC: ${route_b_data['market_cap']/1e6:.1f}M | RSI: {route_b_data['rsi']}")
            results.append(route_b_data)
        elif passed_route_a:
            print(f"  [HIT] {coin:>6} — Fresh Listing Opportunity!    | Score: {route_a_data['score']}/100 | Age: {route_a_data['days_on_hl']} days")
            results.append(route_a_data)

    print()
    print("=" * 60)
    print(f" UNIFIED SCAN COMPLETE — FOUND {len(results)} CANDIDATES")
    print("=" * 60)

    # Sort results by score descending
    results.sort(key=lambda x: x["score"], reverse=True)

    if results:
        print()
        print("=" * 60)
        print(" TOP MOONSHOT CANDIDATES (Ranked by Score)")
        print("=" * 60)
        for i, c in enumerate(results[:10], 1):
            type_lbl = "NEW LISTING" if c["type"] == "new_listing" else "NARRATIVE MOVER"
            mc_str = f"${c['market_cap']/1e6:.1f}M MC" if c["market_cap"] else "MC N/A"
            age_str = f"HL Age: {c['days_on_hl']}d"
            rsi_str = f" | RSI: {c['rsi']}" if c["rsi"] else ""
            
            print(f"\n  #{i}  {c['coin']} [{type_lbl}]")
            print(f"      Price:    ${c['price']:.8f} | {age_str}{rsi_str}")
            print(f"      Score:    {c['score']}/100 | {mc_str} | Volume 24h: ${c['volume_24h']/1e6:.2f}M")
            print(f"      Sources:  {', '.join(c['sources'])}")
            print(f"      Signals:  {' | '.join(c['reasons'][:3])}")

        # Save to moonshot_candidates.json
        output_file = os.path.join(os.path.dirname(__file__), "..", "data", "moonshot_candidates.json")
        with open(output_file, "w") as f:
            json.dump(results[:10], f, indent=4)
        print(f"\n[*] Saved top {min(10, len(results))} candidates to {output_file}")
        print("[*] Next: Run 'python crypto/agents/moonshot_fa_agent.py' to run Google Gemini FA checks")
    else:
        print("\n[-] No candidates qualified under either scanning engine today.")
        print("    Market is quiet. Try again tomorrow or after high-volatility shifts.")

if __name__ == "__main__":
    main()
