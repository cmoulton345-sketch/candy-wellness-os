import json
import os

def rank_pairs():
    print("=" * 60)
    print(" FLOWSTATE AI — PAIR RANKER")
    print("=" * 60)

    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    data_path = os.path.join(data_dir, "qualified_pairs.json")
    approved_path = os.path.join(data_dir, "fa_approved_pairs.json")

    with open(data_path) as f:
        qualified = {p['coin']: p for p in json.load(f)}

    with open(approved_path) as f:
        approved = [p['coin'] for p in json.load(f)]

    scores = []
    for coin in approved:
        if coin not in qualified:
            continue
        p = qualified[coin]
        m = p.get('metrics', {})

        bbw     = float(m.get('BBW_Pct', 0))
        vol     = float(p.get('volume_24h', 0)) / 1_000_000
        bb_pos  = float(m.get('BB_Position', 0.5)) * 100  # convert 0.23 → 23
        ema_gap = float(m.get('EMA_Gap_Pct', 5))

        # Score each factor 0-100
        bbw_score  = min(bbw / 10 * 100, 100)            # wider = better
        vol_score  = min(vol / 50 * 100, 100)             # more = better
        bb_score   = max(0, 100 - (bb_pos * 2))           # lower pos = better
        ema_score  = max(0, 100 - (ema_gap / 2 * 100))    # tighter = better

        final = (bbw_score * 0.35) + (vol_score * 0.25) + \
                (bb_score  * 0.25) + (ema_score * 0.15)

        scores.append({
            'coin':    coin,
            'score':   round(final, 1),
            'bbw':     bbw,
            'volume':  round(vol, 1),
            'bb_pos':  round(bb_pos, 1),
            'ema_gap': ema_gap
        })

    scores.sort(key=lambda x: x['score'], reverse=True)

    print(f"\n{'Rank':<6}{'Pair':<10}{'Score':<10}{'BBW%':<10}{'Vol($M)':<12}{'BB Pos%':<10}{'EMA Gap%'}")
    print("-" * 65)
    for i, s in enumerate(scores, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
        print(f"{medal} {i:<4}{s['coin']:<10}{s['score']:<10}{s['bbw']:<10}{s['volume']:<12}{s['bb_pos']:<10}{s['ema_gap']}")

    print("=" * 65)
    top3 = [s['coin'] for s in scores[:3]]
    print(f"\n✅ Top 3 picks: {', '.join(top3)}")
    print("⚠️  Max 3 positions. Risk 2% per trade. 3x leverage max.")

    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    ranked_path = os.path.join(data_dir, "ranked_pairs.json")
    with open(ranked_path, 'w') as f:
        json.dump(scores, f, indent=2)
    print(f"[*] Rankings saved to ranked_pairs.json")

if __name__ == "__main__":
    rank_pairs()
