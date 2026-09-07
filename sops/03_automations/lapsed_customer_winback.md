# SOP: Lapsed Customer Win-Back Automation
**Category:** Automations | **Version:** 1.0 | **Last Updated:** March 2026

---

## What This Automation Does
Identifies customers who haven't returned in 90 days and automatically sends them a personalized re-engagement message. Turns a dormant customer list into active revenue without any manual effort.

**Trigger:** Customer's last visit/purchase was 90 days ago (checked daily)
**Action:** Send personalized re-engagement email + SMS
**Result:** Typically 10–25% of lapsed customers rebook when contacted; pure recovered revenue from an asset the business already has

---

## What to Say on the Sales Call
> "You already have customers — people who liked you enough to pay you before. But if you're not staying in touch, they'll just start going somewhere else out of convenience. This automation watches your customer list every day. The moment someone hasn't been back in 90 days, it sends them a personal note — not a generic newsletter — something that sounds like it came from you. Most businesses that run this bring back 10–25% of their lapsed customers within the first 60 days. That's revenue you already earned once, earned again."

---

## What You Need from the Client

| Item | Why You Need It | Where to Get It |
|---|---|---|
| Customer list with last visit date | Core data for the trigger | Their CRM, POS, or booking system |
| Customer email + phone | To reach them | Same source |
| 90-day threshold (can adjust) | When to trigger the message | Confirm with client — some prefer 60 days |
| Re-engagement offer (optional) | Something to bring them back | Discuss: discount, free add-on, priority booking |
| Warm message in their voice | Feels personal, not automated | Draft together on the call |

---

## Setup Approach

### Option A: Google Sheets Customer List (Universal — Works for Everyone)
The simplest and most reliable approach. Works for any business that can export their customers.

**Sheet columns:**
| Customer Name | First Name | Email | Phone | Last Visit Date | Win-Back Sent | Win-Back Date |
|---|---|---|---|---|---|---|

**Workflow:**
1. **Trigger:** Schedule → Every day at 9:00 AM
2. **Node 2:** Google Sheets → Get all rows
3. **Node 3:** Filter → where `Last Visit Date` is more than 90 days ago AND `Win-Back Sent` = FALSE
4. **Node 4:** Loop → for each matching customer:
   - Send Email (Gmail)
   - Send SMS (Twilio)
   - Update Sheet: mark `Win-Back Sent = TRUE`, `Win-Back Date = today`
5. Save and **Activate**

### Option B: Square POS / Mindbody API
For businesses using a supported POS that has customer history via API:
1. Schedule trigger daily → Pull customer list with last purchase date
2. Same filter + send logic

### Option C: Acuity / Calendly
Export clients with their last appointment date → import to Google Sheet → use Option A

---

## Message Templates

### SMS Version
```
Hey [First Name]! It's been a while since we've seen you at [Business Name] 
and we miss having you in. [Optional: We're running a special this month — 
[offer].] Would love to have you back — book anytime here: [booking link]
Hope you're doing well! — [Owner Name]
```

### Email Version
**Subject:** Hey [First Name], it's been a while 👋

```
Hi [First Name],

I noticed it's been a few months since we last saw you at [Business Name], 
and I just wanted to check in.

We've really enjoyed having you as a customer and wanted to reach out personally 
— not just send a generic newsletter!

[Optional paragraph: mention something seasonal, a new service, or a personal note]

[Optional: "As a thank-you for being a loyal customer, we'd love to offer you 
[discount / priority booking / free add-on] on your next visit."]

If you're ready to book, you can grab a time here anytime: [booking link]

Or just reply to this email and I'll personally get you set up.

Hope to see you soon,

[Owner Name]
[Business Name]
[Phone]
```

---

## Offer Ideas (To Include or Not — Client's Choice)
- "Book this month and get 15% off" (simple, works for most businesses)
- "We'll add a complimentary [add-on service] to your next visit"
- "Priority booking — you pick the time before we open it publicly"
- No offer — just the personal note (often works just as well)

---

## How Often to Send
- **Day 90:** First win-back message (warm, personal)
- **Day 120 (optional):** Second attempt if no response — slightly different angle
- **Day 180:** Final attempt — longer absence, more urgent tone
- After 3 attempts with no response → remove from win-back sequence, archive

---

## How to Test It
1. Add a test row to the sheet with a Last Visit Date more than 90 days ago
2. Manually trigger the workflow (or wait for scheduled run)
3. Confirm email + SMS fire to test addresses
4. Verify the "Win-Back Sent" column updates to TRUE

---

## What "Working" Looks Like
- Daily batch runs silently every morning
- Lapsed customers receive a personal-feeling message right at 90 days
- Business owner sees inbound bookings from customers they hadn't heard from in months
- Over 60 days: visible uptick in returning customers; measurable revenue from dormant list

---

## Common Issues

| Problem | Fix |
|---|---|
| All customers triggering at once on Day 1 | Add `Win-Back Sent = FALSE` filter; process in batches of 10/day if needed |
| Dates not calculating correctly | Make sure dates are in consistent format in the sheet (YYYY-MM-DD) |
| Messages feeling spammy | Reduce the offer language; keep it conversational and personal |
| Low re-engagement rate | Test subject lines; "Hey [First Name], it's been a while" outperforms promo subjects |

---

## Upgrade Path
> "This is the last automation in the retention stack. Once you've got all six running, you've got a complete customer lifecycle — from new inquiry to loyal returning client — all automated. That's the Growth System."

---

*FlowstateAI Automation — Automations SOP*
