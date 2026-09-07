# SOP: Appointment Reminder Automation
**Category:** Automations | **Version:** 1.0 | **Last Updated:** March 2026

---

## What This Automation Does
Automatically sends a reminder (email and/or SMS) to a client's customers before their upcoming appointment. Reduces no-shows without anyone having to remember to do it.

**Trigger:** New appointment booked
**Actions:** Send reminder 24 hours before → Send reminder 2 hours before
**Result:** Typically 30–60% reduction in no-shows

---

## What to Say on the Sales Call
> "Every missed appointment is lost revenue you can never get back. This automation fires automatically the moment a booking is made — 24 hours before and again 2 hours before. Most of my clients see no-shows drop by half within the first month. We set it up once and it runs forever."

---

## What You Need from the Client

| Item | Why You Need It | Where to Get It |
|---|---|---|
| Booking system name | To connect the trigger | Ask them on the call |
| Booking system login/API | To read new appointments | Ask on onboarding call |
| SMS number (Twilio) | To send text reminders | Set up Twilio account or use theirs |
| "From" email address | For email reminders | Their business email |
| Reminder message text | Personalized to their brand | Draft together on the call |

**Supported booking systems:** Calendly, Acuity, Jane App, Square Appointments, Google Calendar, Mindbody, manual Google Sheet entry

---

## n8n Workflow Setup

### If Using Calendly (Most Common)
1. Open n8n → New Workflow
2. **Trigger:** Calendly Trigger → Event: `invitee.created`
3. **Node 2:** Wait — set to `{{$json.event.start_time}} - 24 hours`
4. **Node 3:** Send Email (Gmail) OR SMS (Twilio)
   - To: `{{$json.invitee.email}}` / `{{$json.invitee.text_reminder_number}}`
   - Message: use template below
5. **Node 4:** Wait — set to `{{$json.event.start_time}} - 2 hours`
6. **Node 5:** Send Email/SMS (same as Node 3, different message text)
7. Save and **Activate**

### If Using Google Calendar
1. **Trigger:** Google Calendar Trigger → Watch: new events
2. Same flow from Node 2 onwards

### If Using Manual Entry (Google Sheets)
1. **Trigger:** Google Sheets Trigger → On Row Added
2. Read: appointment date/time + customer phone/email from row
3. Same Wait → SMS/Email flow

---

## Message Templates

### 24-Hour Reminder (SMS)
```
Hi [Customer First Name]! Just a reminder that your appointment with [Business Name] 
is tomorrow at [Time]. Reply CONFIRM to confirm or call us at [Phone] to reschedule. 
See you then! 😊
```

### 2-Hour Reminder (SMS)
```
[Customer First Name], your [Business Name] appointment is in 2 hours at [Time]. 
We're looking forward to seeing you! [Address if applicable]
```

### 24-Hour Reminder (Email)
**Subject:** Your appointment is tomorrow — [Business Name]

```
Hi [First Name],

Just a quick reminder that you have an appointment with us tomorrow:

📅 Date: [Date]
🕐 Time: [Time]
📍 Location: [Address or "virtual"]

Need to reschedule? No problem — just reply to this email or call us at [Phone].

See you tomorrow!

[Business Name]
```

---

## How to Test It
1. Make a test booking in their booking system
2. Check n8n executions — confirm the workflow fired
3. Confirm the SMS/email was received at your own number/email
4. Verify the timing is correct (you can manually trigger with a test time)

---

## What "Working" Looks Like
- Every new booking auto-triggers the workflow in n8n
- Client sees execution logs in n8n showing confirmations sent
- Customer receives reminder at the right time with the right info
- No-show rate begins declining within 2–4 weeks

---

## Common Issues

| Problem | Fix |
|---|---|
| Calendly trigger not firing | Check webhook is activated in Calendly settings |
| SMS not sending | Verify Twilio credentials + account balance |
| Wrong time on reminders | Confirm timezone is set correctly in n8n settings |
| Email going to spam | Set up SPF/DKIM for their sending domain |

---

## Upgrade Path
Once this is running, natural upsell: **"Want to also auto-text them if they miss? That's the No-Show Recovery automation."**

---

*FlowstateAI Automation — Automations SOP*
