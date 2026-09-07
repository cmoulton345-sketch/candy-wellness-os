# FlowstateAI Crypto Trading System — Standard Operating Procedures

**Version 1.0 — May 4, 2026**
**System Architect: Crypto (AI) | Operator: Joe Moulton**
**Platform: Hyperliquid Mainnet → Mainnet**

---

## 1. Strategy Overview

> "Protect capital first. Grow it second. Never gamble — trade with a system."

The FlowstateAI trading system runs **three independent bots** on a single Hyperliquid account. Each bot has its own strategy, its own risk management, and its own kill switch. They do not interfere with each other.

### Profit Allocation Rule (65 / 30 / 5)

| Bucket | Allocation | Destination |
|--------|-----------|-------------|
| **Reinvest** | 65% | Stays in core bot trading capital |
| **HODL Harvester** | 30% | Auto-deposited to BTC/ETH accumulation |
| **Moonshot Fund** | 5% | One high-conviction speculative play |

---

## 2. The Three Bots

### Bot 1: Core Trading Bot (`trading_bot.py`)

**Purpose:** Active momentum/pullback trading on qualified altcoin pairs.

| Parameter | Value |
|-----------|-------|
| Strategy | Mean reversion + momentum breakout |
| Pairs | Scanned daily via `pair_scanner.py` |
| FA Requirement | 5/5 conviction score from `fa_agent.py` |
| Leverage | 3x maximum |
| Stop Loss | 3% (momentum) / 4% (pullback) |
| Trailing Stop | 50% retracement of peak gain |
| Kill Switch | 10% daily drawdown → bot halts |
| Check Interval | 60 seconds |

**How it works:**
1. Pair scanner filters Hyperliquid for coins with >$5M volume, >2% ATR, >4% BBW
2. FA Agent scores each qualified pair (0-5) on fundamentals
3. Only 5/5 pairs are approved for trading
4. Bot monitors approved pairs and enters on pullback (lower BB + RSI <40) or momentum (EMA crossover)
5. Trailing stop locks in gains; kill switch prevents catastrophic loss
6. On profitable close, 30% of profit is written to `hodl_deposits.json` for the HODL bot

**Key Files:**
- `pair_scanner.py` — Scans all Hyperliquid pairs, outputs `qualified_pairs.json`
- `fa_agent.py` — AI fundamental analysis, outputs to `final_approved_pairs.json`
- `trading_bot.py` — The active trading engine
- `final_approved_pairs.json` — Only pairs listed here are traded

---

### Bot 2: HODL Accumulation Bot (`hodl_bot.py`)

**Purpose:** Long-term BTC/ETH accumulation with dynamic ratio-based rebalancing.

| Parameter | Value |
|-----------|-------|
| Strategy | Always LONG both BTC and ETH; rebalance based on ratio |
| Starting Allocation | $250 BTC + $250 ETH |
| Leverage | 1x (no leverage) |
| Default Split | 50/50 BTC/ETH |
| Rebalance Threshold | 10% drift from target allocation |
| Kill Switch | 10% portfolio drawdown → bot halts |
| Check Interval | 5 minutes |

**How it works:**
1. Buys and holds both BTC and ETH (always LONG, never sells to zero)
2. Every 5 minutes, analyzes the BTC/ETH ratio using EMA and RSI
3. If BTC is outperforming → shifts allocation to 60/40 or 70/30 BTC-heavy
4. If ETH is outperforming → shifts to 40/60 or 30/70 ETH-heavy
5. If neutral → maintains current allocation
6. Picks up 30% profit deposits from the core bot and buys more BTC/ETH
7. Over time, the stack grows from: price appreciation + rebalancing gains + new deposits

**Rebalancing Signals:**

| Condition | Target |
|-----------|--------|
| Ratio > EMA21 > EMA50, RSI > 55 | 60/40 BTC/ETH |
| Ratio > EMA21, RSI > 70 | 70/30 BTC/ETH |
| Ratio < EMA21 < EMA50, RSI < 45 | 40/60 BTC/ETH |
| Ratio < EMA21, RSI < 30 | 30/70 BTC/ETH |
| No strong signal | Maintain current |

**Key Files:**
- `hodl_bot.py` — The accumulation engine
- `hodl_state.json` — Crash recovery state (positions, invested, rebalance count)
- `hodl_deposits.json` — Pending deposits from core bot profits
- `hodl_bot.lock` — Prevents duplicate instances
- `fix_hodl_positions.py` — Emergency position fixer (close all → reopen 50/50)

---

### Bot 3: Moonshot Pipeline (`moonshot_scanner.py` + `moonshot_launcher.py`)

**Purpose:** One high-conviction speculative play at a time, funded by 5% of profits.

| Parameter | Value |
|-----------|-------|
| Strategy | Manual conviction-based, AI-assisted scanning |
| Max Concurrent | 1 moonshot at a time |
| Max Position | 5% of total portfolio |
| Stop Loss | -40% hard stop OR thesis breaks |
| Exit Target | 10x minimum |
| Frequency | Weekly scan, manual approval required |

**How it works:**
1. `moonshot_scanner.py` (technical momentum) or `unified_moonshot_scanner.py` (social narrative & new listings) scans for candidates
2. `moonshot_fa_agent.py` scores candidates on fundamentals
3. Joe manually approves or rejects
4. `moonshot_launcher.py` opens the position
5. Position rides until 10x or thesis breaks

**Current Rule:** No more than 1 new moonshot per week. If one is active, wait.

---

## 3. Daily Operations Workflow

### Morning Checklist (Every Trading Day)

```
□ Step 1: Check Hyperliquid portfolio for any unexpected positions
□ Step 2: Verify HODL bot is running (check terminal for heartbeat)
□ Step 3: Run pair scanner
          Command: python pair_scanner.py
□ Step 4: Review qualified pairs
□ Step 5: Run FA Agent on qualified pairs
          Command: python fa_agent.py
□ Step 6: If 5/5 pair found → update final_approved_pairs.json
□ Step 7: Launch core bot
          Command: python trading_bot.py
□ Step 8: If no 5/5 pair → sit on hands. No trading today.
```

### End of Day Checklist

```
□ Step 1: Check core bot P&L
□ Step 2: Check HODL bot portfolio status
□ Step 3: Check for any unexpected positions or shorts
□ Step 4: Git sync all changes
          Command: git add -A && git commit -m "day X results" && git push
□ Step 5: If core bot is done for the day, Ctrl+C to stop it
          (HODL bot runs 24/7 — do NOT stop it)
```

---

## 4. Weekly Operations

### Every Monday

```
□ Run moonshot scanner (if no active moonshot)
□ Review HODL bot rebalance history
□ Review weekly P&L across all bots
□ Check if current moonshot thesis still holds
□ Review and update qualified pairs list
```

---

## 5. Safety Protocols

### Kill Switch Isolation

Each bot has its own kill switch. They are completely independent:

| Bot | Kill Switch Trigger | What Happens |
|-----|-------------------|--------------|
| Core Bot | 10% daily P&L drawdown | Bot halts, positions closed |
| HODL Bot | 10% portfolio drawdown | Bot halts, positions stay open |
| Moonshot | -40% per position | Position closed |

**Critical:** The core bot's kill switch only tracks its own P&L. It ignores HODL positions and moonshots. The HODL bot's kill switch only tracks BTC/ETH value. They cannot trigger each other.

### Anti-Short Protection

The core bot has on-chain verification before every sell:
- Checks actual position size on Hyperliquid before executing
- If no long position exists, the sell is **blocked** (prevents accidental shorts)
- If a short position is detected, it logs a WARNING and does NOT manage it

### Lockfile Protection

The HODL bot creates `hodl_bot.lock` when it starts. If a second instance tries to start, it sees the lockfile and **refuses to run**. This prevents duplicate bots from executing conflicting trades.

### Ghost Process Prevention

After stopping any bot, always verify no orphaned Python processes remain:

```powershell
Get-Process python -ErrorAction SilentlyContinue
```

If any appear, kill them:

```powershell
Stop-Process -Name python -Force
```

---

## 6. Emergency Procedures

### If positions are wrong (doubled, missing, or incorrect allocation):

1. **Stop ALL bots** (Ctrl+C every terminal)
2. **Kill ALL Python processes:**
   ```powershell
   Stop-Process -Name python -Force
   ```
3. **Run the universal fixer:**
   ```powershell
   python fix_hodl_positions.py
   ```
   This closes everything and reopens fresh $250 BTC + $250 ETH.

4. **Restart the HODL bot:**
   ```powershell
   python hodl_bot.py
   ```
5. **Verify** it says "Existing positions confirmed on-chain"

### If an accidental short position appears:

1. Go to https://app.hyperliquid.xyz/trade/[COIN]
2. Click "Close" on the short position
3. Or use the "Market" close button on the Portfolio page

### If the bot crashes:

The HODL bot saves state to `hodl_state.json` on every rebalance and on graceful shutdown. Simply restart it — it will restore from state and verify on-chain.

---

## 7. Environment Setup

### Required Environment Variables

```powershell
$env:HL_PRIVATE_KEY="your_private_key_here"
$env:HL_ACCOUNT_ADDRESS="your_account_address_here"
$env:GEMINI_API_KEY="your_gemini_key_here"  # For FA Agent only
```

### Required Python Packages

```
pip install hyperliquid-python-sdk requests eth_account google-genai
```

---

## 8. File Map

```
crypto/
├── pair_scanner.py          # Scans for qualified trading pairs
├── fa_agent.py              # AI fundamental analysis (5-point scoring)
├── trading_bot.py           # Core momentum/pullback trading bot
├── hodl_bot.py              # BTC/ETH accumulation + rebalancing bot
├── moonshot_scanner.py      # Low-cap moonshot scanner (technical)
├── unified_moonshot_scanner.py # Narrative & New Listing scanner (combined)
├── moonshot_fa_agent.py     # Moonshot fundamental scoring
├── moonshot_launcher.py     # Opens moonshot positions
├── fix_hodl_positions.py    # Emergency position fixer
├── qualified_pairs.json     # Output of pair scanner
├── final_approved_pairs.json # FA-approved pairs (core bot reads this)
├── hodl_state.json          # HODL bot crash recovery state
├── hodl_deposits.json       # Pending profit deposits for HODL bot
├── hodl_bot.lock            # Prevents duplicate HODL instances
├── moonshot_approved.json   # Approved moonshot candidates
├── moonshot_candidates.json # Raw moonshot scan results
└── joe_trading_strategy.md  # Full strategy document
```

---

## Appendix A: Manual Setup Guide (Step-by-Step)

> Use this guide if AI is unavailable and you need to set up or modify the bots manually.

### A.1 — Connecting to Hyperliquid Mainnet

1. Open your browser and go to: `https://app.hyperliquid.xyz`
2. Click **"Connect"** in the top right corner
3. Choose **MetaMask** as your wallet
4. Approve the connection in MetaMask
5. You should see your account address and balance in the top right

### A.2 — Claiming Mainnet USDC

1. Go to: `https://app.hyperliquid.xyz/drip`
2. Click **"Claim 1000 USDC"**
3. Wait 10 seconds for the transaction to confirm
4. Your balance should now show $1000 USDC

### A.3 — Manually Opening a Position

1. Navigate to: `https://app.hyperliquid.xyz/trade/BTC`
2. On the right side, you'll see the **Order Panel**
3. Select **"Buy"** (green) for a long position
4. Set **Order Type** to "Market" for immediate fill
5. Set **Size** — enter the USD amount (e.g., $250)
6. Set **Leverage** — click the leverage selector and choose **1x**
7. Click **"Buy / Long"** to execute
8. The position will appear in the **Positions** tab at the bottom

### A.4 — Manually Closing a Position

1. Go to: `https://app.hyperliquid.xyz/portfolio`
2. Find the position you want to close in the **Positions** tab
3. Click **"Market"** next to the position (this closes at market price)
4. Confirm the close
5. The position disappears from the list

### A.5 — Checking Your Portfolio

1. Go to: `https://app.hyperliquid.xyz/portfolio`
2. The **Positions** tab shows all open positions with:
   - Coin, Size, Entry Price, Mark Price, P&L, Margin
3. The top section shows Total Equity and overall P&L

### A.6 — Starting the Core Bot Manually

1. Open a **new PowerShell terminal**
2. Set environment variables:
   ```powershell
   $env:HL_PRIVATE_KEY="your_key"
   $env:HL_ACCOUNT_ADDRESS="your_address"
   ```
3. Run the pair scanner:
   ```powershell
   python c:\Users\Admin\Agents\radical_simplicity_ai_os_v2\work_in_progress\crypto\pair_scanner.py
   ```
4. Check `qualified_pairs.json` for results
5. Run the FA agent:
   ```powershell
   $env:GEMINI_API_KEY="your_gemini_key"
   python c:\Users\Admin\Agents\radical_simplicity_ai_os_v2\work_in_progress\crypto\fa_agent.py
   ```
6. If a pair scores 5/5, edit `final_approved_pairs.json`:
   ```json
   [{"coin": "PENDLE", "fa_score": 5}]
   ```
7. Launch the bot:
   ```powershell
   python c:\Users\Admin\Agents\radical_simplicity_ai_os_v2\work_in_progress\crypto\trading_bot.py
   ```
8. The bot will print entry/exit signals. Press **Ctrl+C** to stop.

### A.7 — Starting the HODL Bot Manually

1. Open a **separate PowerShell terminal** (not the same as the core bot)
2. Set environment variables:
   ```powershell
   $env:HL_PRIVATE_KEY="your_key"
   $env:HL_ACCOUNT_ADDRESS="your_address"
   ```
3. Launch:
   ```powershell
   python c:\Users\Admin\Agents\radical_simplicity_ai_os_v2\work_in_progress\crypto\hodl_bot.py
   ```
4. If this is the first run, it will buy $250 BTC + $250 ETH automatically
5. If resuming, it will say "Existing positions confirmed on-chain"
6. Leave this terminal running 24/7
7. Press **Ctrl+C** to stop (positions stay open on exchange)

### A.8 — Fixing Messed Up Positions

1. **Stop ALL bots** — Ctrl+C every terminal
2. **Kill orphan processes:**
   ```powershell
   Stop-Process -Name python -Force
   ```
3. **Run the fixer:**
   ```powershell
   $env:HL_PRIVATE_KEY="your_key"
   $env:HL_ACCOUNT_ADDRESS="your_address"
   python c:\Users\Admin\Agents\radical_simplicity_ai_os_v2\work_in_progress\crypto\fix_hodl_positions.py
   ```
4. This will close everything and reopen clean $250/$250 positions
5. Restart the HODL bot

---

*SOP authored by Crypto (AI Trading Architect) in collaboration with Joe Moulton.*
*Last updated: May 4, 2026*
