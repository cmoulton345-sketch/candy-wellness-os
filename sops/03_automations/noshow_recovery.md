# SOP: No-Show Recovery Automation
**Category:** Automations | **Version:** 1.0 | **Last Updated:** March 2026

---

## What This Automation Does
When a customer misses an appointment without cancelling, they automatically receive a message within 30–60 minutes offering to rebook. Recovers revenue that would otherwise just disappear.

**Trigger:** Appointment marked as no-show / not checked in by appointment time
**Action:** Wait 30 minutes → Send SMS + email trying to rebook
**Result:** 20–40% of no-shows rebook within 24 hours when followed up automatically

---

## What to Say on the Sales Call
> "No-shows are pure lost revenue. Someone booked a slot, you held it, they didn't show — and most businesses just move on. This automation sends them a message 30 minutes after their missed appointment: 'Hey, we missed you today — life happens! Want to grab another time?' We typically see 20–40% of no-shows rebook when you follow up this fast. It's money you were already going to lose, recovered automatically."

---

## What You Need from the Client

| Item | Why You Need It | Where to Get It |
|---|---|---|
| Booking system with no-show status | To detect the missed appointment | Most systems have this |
| Customer phone + email | To send the rebook message | Comes from booking system |
| Rebooking link | So they can book a new slot instantly | Calendly / Acuity link |
| Warm re-engagement message | To not sound robotic | Draft together |

---

## Setup Approach by Booking System

### Calendly
Calendly does **not** have a built-in no-show status.
**Workaround:** 
1. Create a Google Sheet where salon/clinic staff marks no-shows manually
2. Google Sheets trigger in n8n → on row marked "no-show" → send follow-up
3. OR: Schedule trigger fires at appointment time → check if invitee confirmed → if no confirmation, send message

### Acuity Scheduling
Acuity has appointment status webhooks.
1. Acuity webhook → `appointment.noshow` event → n8n trigger
2. Wait 30 min → Send SMS + Email

### Jane App (Medical/Dental)
Jane has no native webhook for no-shows.
**Workaround:** Staff marks no-show in Jane → updates a Google Sheet → n8n triggers

### Square Appointments / Mindbody
Both have APIs with appointment status.
1. Schedule trigger every 15 minutes → poll for appointments that started more than 30 min ago with no check-in
2. Send follow-up to those customers

---

## n8n Workflow Setup (Google Sheet Approach — Most Universal)

1. **Trigger:** Google Sheets Trigger → On Row Changed (when status column changes to "no-show")
2. **Node 2:** Wait 30 minutes
3. **Node 3 — Parallel:**
   - Send SMS (Twilio): rebook message
   - Send Email (Gmail): rebook message
4. **Node 4:** Update Sheet → mark "recovery sent = TRUE" (prevents duplicate messages)
5. Save and **Activate**

---

## Message Templates

### SMS (30 minutes after no-show)
```
Hey [First Name]! We missed you at your [Time] appointment today at [Business Name]. 
No worries — life happens! Would you like to grab another time? 
Book here anytime: [booking link] 
Or just reply to this message and we'll sort it out. 😊
```

### Email
**Subject:** We missed you today, [First Name]

```
Hi [First Name],

We noticed you weren't able to make your [Time] appointment with us today — 
no worries at all, life gets busy!

We'd love to get you rescheduled at a time that works better for you.

👉 Book a new time here: [booking link]

Or if you'd prefer, just reply to this email and we'll find something that works.

We look forward to seeing you soon!

[Owner Name]
[Business Name]
[Phone]
```

### 24-Hour Follow-Up (If No Response)
```
Hi [First Name], just following up from yesterday — 
we'd still love to get you in at [Business Name]. 
Here's the link to grab a spot: [booking link] 
Have a great day! — [Business Name]
```

---

## Staff No-Show Sheet Setup

Create a Google Sheet with these columns:

| Customer Name | Phone | Email | Appointment Date | Appointment Time | Status | Recovery Sent |
|---|---|---|---|---|---|---|
| | | | | | no-show | FALSE |

Staff marks **Status = no-show** → automation triggers → marks **Recovery Sent = TRUE**

---

## How to Test It
1. Enter a test row in the sheet with status = "no-show"
2. Confirm n8n trigger fires
3. Verify SMS and email arrive at test number/address
4. Confirm "Recovery Sent" column updates to TRUE

---

## What "Working" Looks Like
- No-show messages fire automatically within 30 minutes of missed appointment
- 20–40% of those customers rebook within 24 hours
- Staff no longer has to manually chase no-shows
- Revenue that was lost is visibly recovered over 30–60 days

---

## Common Issues

| Problem | Fix |
|---|---|
| No-show status not triggering | Confirm Google Sheet trigger is watching the right column |
| Duplicate messages sent | Check "Recovery Sent" flag is being set correctly |
| Low rebook rate | Test different message tones — warmer = better; add booking link |
| Sheet not updating | Check n8n has edit permissions on the Google Sheet |

---

## Upgrade Path
> "The next level is combining this with the Lapsed Customer Win-Back. If they don't rebook in 30 days, they automatically go into a win-back sequence. Fully passive revenue recovery."

---

*FlowstateAI Automation — Automations SOP*
