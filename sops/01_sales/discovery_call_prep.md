# SOP: Discovery Call Prep
**Category:** Sales | **Version:** 1.0 | **Last Updated:** March 2026

---

## What This Is
A 15-minute pre-call checklist. Do this before every discovery call without exception. Being prepared is your competitive advantage — most consultants show up cold.

---

## The 15-Minute Pre-Call Checklist

### Step 1 — Review Their Booking (2 min)
- [ ] What automation did they pick on the booking form?
- [ ] What's their business name?
- [ ] Any notes they left in the form?

### Step 2 — Research Their Business (5 min)
Open a browser and do this quickly:
- [ ] Google their business name — visit their website
- [ ] Check their Google reviews — how many? What's their average? Any patterns in the feedback?
- [ ] Visit their Facebook page — are they active? What kind of content?
- [ ] Note: **How busy do they look?** Established or struggling?
- [ ] Note: **One genuine observation** you can mention on the call (shows you prepared)

### Step 3 — Pre-Build Their Automation (5 min)
Build a basic version of what they asked for in n8n — ready to demo.

| They Picked | What to Pre-Build |
|---|---|
| Appointment Reminder | Workflow with Calendly trigger + 24hr/2hr wait + email/SMS send |
| Google Review Request | Workflow with schedule/completion trigger + review link SMS |
| Missed Call Text-Back | Workflow with webhook trigger + Twilio SMS response |
| Instant Lead Follow-up | Workflow with webhook trigger + instant email + SMS |
| No-Show Recovery | Workflow with Sheets trigger + 30min wait + rebook SMS |
| Lapsed Win-Back | Workflow with daily schedule + 90-day filter + re-engagement SMS |

Use placeholder credentials for now — you'll connect the real ones during onboarding.

### Step 4 — Open Your Tools (2 min)
Before the call starts, have these open:
- [ ] n8n (localhost:5678) — workflow ready to demo
- [ ] Your Call Notes doc (blank, name filled in)
- [ ] The Call-to-Close System doc (quick reference)
- [ ] Calendly — in case they want to book a follow-up on the spot
- [ ] Stripe/Wave — ready to send invoice if they say yes

### Step 5 — Set Yourself Up (1 min)
- [ ] Camera on — clean background or blurred
- [ ] Microphone tested — no echo
- [ ] Notifications off (phone + computer)
- [ ] Glass of water nearby
- [ ] Have the quick reference card visible (bottom of call_to_close_system.md)

---

## What to Know About Them Going In

After your 5-minute research, answer these quickly:

**What kind of business is it?**
*(Service-based, appointment-based, product-based, trade)*

**How established are they?**
*(New startup, growing SME, established but flat)*

**What's their biggest likely pain point?**
*(Based on industry — e.g., dental = no-shows + reviews; trades = missed calls + scheduling)*

**What package are they probably going to fit?**
*(Starter, Growth, or Enterprise — make a mental bet before the call)*

---

## The One Question to Answer Before You Dial

> *"If this call goes perfectly, what does this client's business look like in 90 days, and how did FlowstateAI get them there?"*

Have that picture in your head. It will come through in how you speak.

---

## Post-Call (Do Immediately After)
- [ ] Send Template A or B (from call_to_close_system.md) within 30 minutes
- [ ] Update the pipeline tracker
- [ ] Set follow-up reminder if needed
- [ ] Write 3 bullet notes while it's fresh: what they cared about, what they were unsure of, what the hook was

---

*FlowstateAI Automation — Sales SOP*
