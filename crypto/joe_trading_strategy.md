# The FlowstateAI Trading Strategy
**Version 1.0 — Authored by Crypto & Joe Moulton**
**Platform: Hyperliquid | Starting Capital: $100 USDC**

---

## Philosophy

> "Protect capital first. Grow it second. Never gamble — trade with a system."

This strategy is a hybrid of three disciplines:
- **Mean Reversion** — profiting from volatility within a defined range
- **Trend Following** — only trading pairs moving in the right direction
- **Fundamental Filtering** — only trading projects with real substance behind them

Every trade has a thesis, an entry, a target, and a stop — before it is placed.

---

## Capital Structure — Profit Allocation

All profits from the trading bot are split as follows:

| Bucket | Allocation | Purpose |
|--------|-----------|---------|
| **Reinvest (Compound)** | 65% | Grows the bot's trading capital |
| **HODL Harvester** | 30% | BTC/ETH pair trading — Phase 2 |
| **Moonshot Fund** | 5% | One high-conviction speculative play at a time |

The principal trading capital is never touched by moonshots. Only profits fund the moonshot bucket.

---

## Pair Selection — The 4-Filter Screen

A pair must pass ALL 4 filters to qualify for the **Core** bucket:

| Filter | Measurement | Pass Criteria |
|--------|-------------|---------------|
| **Uptrend** | EMA 21 & EMA 50 | Price above both, both pointing up |
| **Volatility** | ATR (14-period) | ATR > 2% of current price |
| **Range Quality** | Bollinger Band Width | BBW > 4% (room to scalp) |
| **Liquidity** | 24h Trading Volume | >$5M on Hyperliquid |

**Trading History Requirement:**
- Core pairs: **6+ months** of trading history minimum
- Moonshot pairs: any age — but position size is capped hard (see Risk Rules)

**Pair Review Cadence:**
- Weekly: check all active pairs still pass filters
- Auto-eject trigger: price closes below EMA 50, OR volume drops below $3M/day
- Expected pair lifespan: 2–4 weeks before rotation is needed

---

## Dual Confirmation System

No trade is placed without both systems agreeing.

### Technical Analysis (TA) Checklist
- [ ] Clear range identified — visible floor and ceiling on chart
- [ ] Price above EMA 21 AND EMA 50
- [ ] RSI between 35–65 (not overextended)
- [ ] Bollinger Band showing active oscillation (not compressed)
- [ ] Volume confirms direction of move

### Fundamental Analysis (FA) Checklist
- [ ] Project has a real, demonstrable use case
- [ ] Active development — recent GitHub activity OR protocol updates
- [ ] TVL or on-chain activity trending flat or up
- [ ] No red flags: anon team without track record, heavily VC-dumped tokenomics, no community
- [ ] Not in a post-hack or regulatory crisis period

### Trade Decision Matrix

| TA | FA | Decision |
|----|----|----------|
| ✅ Green | ✅ Green | **Full position** — core allocation |
| ✅ Green | ⚠️ Mixed | **Half position** — cautious entry |
| ⚠️ Mixed | ✅ Green | **Half position** — wait for TA confirmation |
| ❌ Red | Any | **No trade** — sit on hands |
| Any | ❌ Red | **No trade** — sit on hands |

---

## Entry Logic

**Primary Signal (Mean Reversion):**
- Price touches or approaches the lower Bollinger Band
- RSI reads below 40 (approaching oversold in range context)
- EMA 21/50 still pointing upward (trend intact)

**Confirmation Filter:**
- Volume on the bounce is above 20-period average
- No major news event in next 24 hours that could override technicals

**Entry Type:**
- Limit order at the lower band or nearest support level
- Never chase — if the entry is missed, wait for the next oscillation

---

## Exit Logic

### Initial Stop-Loss (Capital Protection)
- Set immediately at entry — no trade opens without it
- Placement: 3–5% below entry price OR below the nearest structural support level, whichever is tighter
- This stop is **never moved down** — only up as the trade moves in our favor

### Take-Profit Target
- Upper Bollinger Band or nearest resistance level
- Minimum 1.5:1 reward-to-risk ratio required (ideally 2:1+)

### Trailing Stop — The 50% Retracement Rule
Once the price hits the take-profit target:
1. Stop moves to **breakeven** (entry price)
2. If price continues rising, stop trails at **50% of the gain**
3. Trade closes when price reverses and loses 50% of its peak gain

### Compounding Exits — Capital Realization (Option C)
To maximize compounding velocity on Small Accounts (<$100):
1. **50% Compounding Milestone Target**: If unrealized position PnL hits +50% gain, close the position immediately to lock in profit, update account equity balance, and enable the bot to re-enter on the next signal with full compounded buying power.
2. **24-Hour Profitable Hold Exit**: If a position has been open for 24 hours AND is in profit, close the position to release accumulated equity.

**Example:**
```
Entry:          $1.00
Initial Stop:   $0.97
Target:         $1.10  ← stop moves to $1.00 (breakeven)
Price rises to: $1.20  ← stop trails to $1.10
Price rises to: $1.30  ← stop trails to $1.15
Price reverses to $1.15 → CLOSE. Profit locked: $0.15/unit
Compounding exit: If held 24h with profit OR gain hits +50% → CLOSE & compound full equity into next trade!
```

---

## Risk Management Rules

These are non-negotiable. They override any signal, any conviction, any opportunity.

| Rule | Parameter |
|------|-----------|
| **Max risk per trade** | 2% of total capital per trade |
| **Max daily loss** | 10% of total capital — bot pauses automatically |
| **Max total drawdown** | 25% — full stop, manual review required before resuming |
| **Leverage** | 3x maximum (beginners). Never more. |
| **Moonshot position size** | Max 5% of total capital per play — hard limit |
| **Moonshot stop-loss** | Hard -40% per moonshot position — no exceptions |
| **Concurrent positions** | Max 3 open at once on $100 account |
| **Correlation** | No more than 2 positions in the same sector simultaneously |
| **Kill switch** | Any single position loses 5% of total capital → close it regardless |

### The 3 Ways Traders Blow Up (We Avoid All 3)
1. **Over-leveraging** — solved by 3x max
2. **No stop-loss** — solved by mandatory stops on every position
3. **Revenge trading** — solved by the 10% daily kill switch (bot stops, human reviews)

---

## HODL Harvesting Protocol

Trading profits build a permanent long-term asset stack.

**Trigger:** When trading account grows 10% above its starting value at any point

**Action:**
- Sweep 30% of the gain to the HODL wallet
- Split the sweep: **60% BTC / 40% ETH**
- HODL stack is never touched for trading losses — it is permanent accumulation

**Example:**
```
Start: $100
Account grows to: $110 (10% gain = $10)
Sweep: 30% of $10 = $3 → HODL wallet ($1.80 BTC + $1.20 ETH)
Trading account continues at: $107
Next trigger: when account hits $117.70 (10% above $107)
```

Over time this builds a growing BTC/ETH stack funded entirely by active trading profits.

---

## Moonshot Protocol

**Funded by:** 5% of trading profits only — never principal.

**Rules — Non-Negotiable:**

| Rule | Parameter |
|------|-----------|
| **Max concurrent** | 1 moonshot at a time — ONE bullet, ONE shot |
| **Max position size** | 5% of total portfolio — hard cap |
| **Stop loss** | None — binary bet. Moon or zero. |
| **Exit target** | 10x minimum, or ride until thesis breaks |
| **Approach** | Manual, conviction-based — NOT automated |

**What Qualifies:**
- New narrative with momentum (AI agents, DeSci, RWA, etc.)
- Low market cap — under $50M, ideally under $20M
- Fresh listing — hit Hyperliquid or major CEX in last 30 days
- Community signal — CT is talking but it hasn't pumped yet

**What Disqualifies:**
- Anonymous team with no track record
- No working product at all
- Already pumped 500%+ (you missed it)
- Meme coin with zero utility

**Exit philosophy:** Moonshots either hit 10x+ or go to zero. There is no "holding and hoping" in between. One at a time. Full focus.

---

## Bot Architecture Summary

```
Pair Scanner (Python)
  → Pulls Hyperliquid API data
  → Applies 4-filter screen
  → Outputs qualified pair shortlist weekly

Trading Bot (Python)
  → Monitors active pairs on 1H timeframe
  → Entry: limit order at lower BB + RSI < 40
  → Stop-loss: placed immediately at -3 to -5%
  → Trailing stop: activates after TP, trails at 50% of gain
  → Daily drawdown monitor: pauses bot at -10%
  → All trades logged: timestamp, entry, exit, P&L, reason

Monitoring
  → Telegram alerts on: trade open, trade close, daily P&L summary, drawdown warning
  → Weekly review report: win rate, average R:R, best/worst pairs

HODL Trigger
  → Auto-detects 10% account growth milestone
  → Alerts Joe to manually sweep 30% to HODL wallet
```

---

## Pre-Trade Checklist

Run this before every trade — bot or manual:

- [ ] Pair passes all 4 scanner filters
- [ ] TA checklist complete — at least 3 of 5 green
- [ ] FA checklist complete — at least 3 of 5 green
- [ ] Position size calculated — risking ≤2% of capital
- [ ] Stop-loss level defined and placed
- [ ] Take-profit target defined (minimum 1.5:1 R:R)
- [ ] Trailing stop logic set
- [ ] Leverage at 3x or below
- [ ] Daily loss not already at 8%+ (approaching kill switch)
- [ ] No major market events (FOMC, CPI, major protocol news) in next 4 hours

---

## Phases to Go Live

| Phase | Action | Status |
|-------|--------|--------|
| 1 | Connect MetaMask to Hyperliquid | ✅ Complete |
| 2 | Small mainnet deposit ($10-20) | ✅ Complete |
| 3 | Claim 1000 mock USDC on testnet | ✅ Complete |
| 4 | Build and run pair scanner | ✅ Complete |
| 5 | Build trading bot | ✅ Complete |
| 6 | Paper trade on testnet (2 weeks minimum) | ⬜ Pending |
| 7 | Go live with $100 real capital | ⬜ Pending |
| 8 | First HODL harvest milestone | ⬜ Pending |

---

*Strategy authored by Crypto (AI Trading Architect) in collaboration with Joe Moulton.*
*Last updated: April 28, 2026*
*Next review: After 2 weeks of testnet trading data*
