# Decisions Log

Key decisions made across sessions. Referenced when context is needed on WHY something was done a certain way.

---

## Website & Conversion

| Date | Decision | Context |
|------|----------|---------|
| 2026-03-31 | Beta page will be a separate URL, NOT overwrite production | De-risk the redesign — production stays live while beta is reviewed |
| 2026-03-31 | CTA buttons should open Calendly modal, not scroll to bottom | Audit finding: scrolling kills momentum for hot leads |
| 2026-03-31 | Dynamic scarcity ("X of 4 Sprint slots remaining") goes above pricing, not in footer | Cardone + Brunsen: if it's real, make it visible |
| 2026-03-31 | Replace anonymous testimonials with real, named ones | All four audit lenses agreed: anonymous social proof is worse than none |
| 2026-03-31 | Joe Moulton bio section → Epiphany Bridge format | Graziosi + Ziglar: story beats credentials |
| 2026-03-30 | Free-call landing page uses automation picker (6 options) | Let prospects self-select which automation interests them — qualifies before call |
| 2026-03-30 | Form submits to n8n webhook, then redirects to Calendly | Capture lead data first, then route to booking |

## Infrastructure & Tools

| Date | Decision | Context |
|------|----------|---------|
| 2026-03-31 | Memory system lives in `memory/` at workspace root | Centralized, version-controlled, always available to agent |
| 2026-08-28 | Warden Live System Debugging Protocol (INC-001/INC-002) | Priority-0 gate intercepting all debug tasks; mandatory 4-item evidence gate, no-speculation lock, 2-theory termination limit, commit gate |
| 2026-03-30 | `redeploy.ps1` for Cloudflare Pages deploys | One-command deploys, no manual dashboard clicking |
| 2026-03-16 | Cloudflare tunnel for n8n webhooks | Exposes local n8n to internet for Facebook Lead Ads triggers |
| 2026-03-16 | Industry decks use HTML (not PDF) | Easier to iterate, can deploy as web pages, print to PDF when needed |

## Business Strategy

| Date | Decision | Context |
|------|----------|---------|
| 2026-03-27 | Target professional associations for speaking outreach | Higher leverage than individual cold outreach — one talk = many leads |
| 2026-03-27 | Build industry-specific assets before outreach | Need credibility collateral before approaching associations |
| 2026-03-10 | Partnership with Stephen — proceed cautiously | Psyche analysis flagged complementary strengths but need clear role boundaries |
| 2026-06-18 | Pivot outreach to "Live 7-Day Free Trial" offer | Offer pre-built automation running for 7 days free to eliminate all prospect risk and friction |


---
