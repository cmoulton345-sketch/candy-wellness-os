# SOP: Crypto Trading System

> **Status:** SHELVED — No active funds. Will resume when FlowstateAI reaches success.
> **Last Updated:** 2026-07-06

---

## Overview

An automated crypto trading system running on the remote VPS (Linux server at `/root/ax-os/`).

## Platform
- **Exchange:** Hyperliquid
- **Main Wallet:** `0x55F38791f921EB3635a406BdB34cDCFd2d1BB032`
- **API Wallet:** `0x25911Ffb2F49517dC6f4A80418463d84fdb9b89d`

## Components

| Component | File | Status |
|-----------|------|--------|
| Master Trader | `/root/ax-os/crypto/bots/master_trader.py` | Active (no funds) |
| HODL Bot | `/root/ax-os/crypto/bots/hodl_bot.py` | Disabled |
| Moonshot Launcher | `/root/ax-os/crypto/bots/moonshot_launcher.py` | Active (no funds) |
| Orchestrator | `/root/ax-os/crypto/orchestrator.py` | Active |
| Scanners | `/root/ax-os/crypto/scanners/` | Active |
| FA Agents | `/root/ax-os/crypto/agents/` | Active |

## Systemd Services
- `flowstate-trader.service` (master_trader.py) — running
- `flowstate-orchestrator.service` (orchestrator.py) — running
- `flowstate-hodl.service` — disabled

## Strategy Parameters
- Risk per trade: 2%
- Max leverage: 3x
- Stop loss: 4%
- Trailing stop activation: 1.5%
- Trailing stop trail: 50%
- Daily kill switch: 10% drawdown

## Known Bugs
- SKIP button not working — system trades skipped coins
- Human approval must gate ALL trades, not just alerts

## How to Check Status
```bash
systemctl status flowstate-trader
journalctl -u flowstate-trader -n 50 --no-pager
cat /root/ax-os/crypto/data/orchestrator_state.json
```

## Reactivation Checklist
- [ ] Fund the Hyperliquid wallet
- [ ] Fix the SKIP button bug
- [ ] Implement human approval gate for all trades
- [ ] Re-enable HODL bot
- [ ] Monitor for 48 hours before leaving unattended
