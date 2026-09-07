# Memory Manifest — System Health Tracker

> **Purpose:** Master index of all memory files. Checked at session start to detect staleness.
> **Last Full Audit:** 2026-07-06
> **Next Scheduled Audit:** 2026-10-06 (90 days)

---

## Tier 1 — Active Memory (Always Loaded)

| File | Purpose | Last Updated | Last Verified | Threshold | Status |
|------|---------|:------------:|:-------------:|:---------:|:------:|
| `active/identity.md` | Who Joe is, who the company is | 2026-07-06 | 2026-07-06 | 90 days | ✅ Fresh |
| `active/current_state.md` | What's happening right now | 2026-07-06 | 2026-07-06 | 14 days | ✅ Fresh |
| `active/session_memory.md` | Last session context | 2026-07-06 | 2026-07-06 | 7 days | ✅ Fresh |

## Tier 2 — Long-Term Memory (Loaded on Demand)

| File | Purpose | Last Updated | Last Verified | Threshold | Status |
|------|---------|:------------:|:-------------:|:---------:|:------:|
| `long_term/session_log.md` | Chronological session history | 2026-07-06 | 2026-07-06 | 30 days | ✅ Fresh |
| `long_term/decisions.md` | Key decisions & rationale | 2026-07-06 | 2026-07-06 | 30 days | ✅ Fresh |
| `long_term/preferences.md` | Working style & standards | 2026-07-06 | 2026-07-06 | 90 days | ✅ Fresh |
| `long_term/joe_profile.md` | Joe's voice, story, beliefs | 2026-07-06 | 2026-07-06 | 90 days | ✅ Fresh |
| `long_term/psyche/joe_sessions.md` | Joe's Psyche journal (PRIVATE) | 2026-07-06 | 2026-07-06 | N/A | ✅ Fresh |
| `long_term/psyche/candy_sessions.md` | Candy's Psyche journal (PRIVATE) | 2026-07-06 | 2026-07-06 | N/A | ✅ Fresh |
| `long_term/psyche/candy_context.md` | Candy background primer (PRIVATE) | 2026-07-06 | 2026-07-06 | N/A | ✅ Fresh |
| `long_term/psyche/shared_patterns.md` | Cross-patterns (PSYCHE-ONLY) | 2026-07-06 | 2026-07-06 | N/A | ✅ Fresh |

## Reference & SOPs (Not Memory — Searchable on Demand)

| File | Purpose | Location |
|------|---------|----------|
| Trading System SOP | Crypto trading details (shelved) | `sops/crypto_trading_system.md` |
| Client Pipeline | Active leads & outreach status | `work_in_progress/flowstateautomation/client_pipeline.md` |
| WCB Report | LNG inspection reference | `knowledge/wcb_LNG_report.md` |
| Toronto Targets | Toronto outreach organizations | `knowledge/toronto_outreach_targets.md` |
| Wealth Ideas | Strategic wealth generation plays | `knowledge/wealth_generation_ideas.md` |
| Vancouver Materials | Pitch, contacts, templates | `knowledge/vancouver_*` |

---

## Staleness Rules

1. **Tier 1 files:** If `Last Updated` exceeds threshold, agent flags at session start:
   *"⚠️ `current_state.md` hasn't been updated in X days. Want me to refresh it?"*

2. **Tier 2 files:** Checked only when loaded. If stale, agent notes it but doesn't block work.

3. **Quarterly Audit:** Every 90 days from `Last Full Audit`, the system prompts:
   *"It's been 90 days since the last full memory audit. Want me to run a verification pass?"*

## Privacy Rules

- `psyche/joe_sessions.md` — Psyche reads when Joe is the user. Never surfaced to Candy.
- `psyche/candy_sessions.md` — Psyche reads when Candy is the user. Never surfaced to Joe.
- `psyche/candy_context.md` — Psyche-only. Candy does not know this file exists.
- `psyche/shared_patterns.md` — Psyche-only. Neither Joe nor Candy sees raw cross-references.
