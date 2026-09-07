# SOP: Client Onboarding Checklist
**Category:** Client Onboarding | **Version:** 1.0 | **Last Updated:** March 2026

---

## Overview
Everything that happens from the moment a client pays to the moment their automations are live. Target: **fully onboarded within 7 days of payment.**

---

## Phase 1 — Day 0 (Same Day They Pay)

- [ ] **Send "You're In" email** (Template A from call_to_close_system.md)
- [ ] **Book the onboarding call** — 60 minutes, within 5 days
- [ ] **Create their client folder** in workspace:
  ```
  work_in_progress/clients/[business-name]/
  ├── credentials.md       ← access info (keep private!)
  ├── automations.md       ← what's been built + status
  └── notes.md             ← call notes, preferences
  ```
- [ ] **Add them to the pipeline tracker** (Google Sheet) → status: "Booked"
- [ ] **Send invoice** via Stripe/Wave if not already done

---

## Phase 2 — Before the Onboarding Call

- [ ] Review what package they bought (Starter / Growth / Enterprise)
- [ ] Review which automations they're getting (from call notes)
- [ ] Pre-build their automations in n8n (placeholder versions)
- [ ] Prepare the credentials collection doc — know what you'll need before the call
- [ ] Test that n8n is running and your tunnel is live

**What credentials you'll need (by automation):**

| Automation | What You Need |
|---|---|
| Appointment Reminder | Their booking system login OR Calendly API key |
| Google Review Request | Their Google Business Profile email |
| Missed Call Text-Back | Their business phone number + Twilio/SMS account |
| Instant Lead Follow-up | Their website form webhook OR CRM access |
| No-Show Recovery | Booking system + SMS capability |
| Lapsed Win-Back | Customer email list or CRM access |

---

## Phase 3 — The Onboarding Call (60 Minutes)

**Agenda:**

| Time | Item |
|---|---|
| 0–5 min | Welcome, recap what we're building today |
| 5–15 min | Collect all credentials live on the call |
| 15–45 min | Deploy each automation + test together |
| 45–55 min | Walk them through what "working" looks like |
| 55–60 min | Set 30-day check-in · Ask for a Google review |

**During the call:**
- [ ] Screen share — let them watch you deploy it
- [ ] Test each automation live — trigger it, show the result
- [ ] Walk them through the n8n dashboard (high level only)
- [ ] Confirm their notification email/phone is set correctly

---

## Phase 4 — After the Onboarding Call (Same Day)

- [ ] Send **"Your system is live"** follow-up email (template below)
- [ ] Save all credentials securely in their `credentials.md`
- [ ] Update pipeline tracker → status: "Active Client"
- [ ] Set calendar reminder for 30-day check-in call
- [ ] If they haven't left a Google review — follow up in 48 hours

---

## Post-Onboarding Email Template

**Subject:** Your automations are live — here's what's running

Hi [Name],

Your system is live as of today. Here's a quick summary of what's now running for [Business Name]:

**✅ Automation 1:** [Name] — fires when [trigger]
**✅ Automation 2:** [Name] — fires when [trigger]
**✅ Automation 3:** [Name] — fires when [trigger]

**What to expect:**
- You'll start seeing these in action within the next 24–48 hours as real triggers occur
- If anything looks off or doesn't fire, reply to this email and I'll fix it same day
- We have a 30-day check-in booked for [date] — we'll review results and optimize then

One ask: if you found today's call valuable, a quick Google review goes a long way for a small business like mine. Here's the link: [your Google review link]

Talk soon,
Joe
FlowstateAI Automation
joe@flowstateaiautomation.ai

---

## 30-Day Check-In (Standard Agenda)
- [ ] Review automation activity (how many times each fired)
- [ ] Identify any failures or missed triggers
- [ ] Ask: "What's still happening manually that we could automate?"
- [ ] Upsell opportunity: are they on Starter? Introduce Growth features

---

*FlowstateAI Automation — Client Onboarding SOP*
