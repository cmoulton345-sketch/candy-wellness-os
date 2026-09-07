# SOP: Missed Call Text-Back Automation
**Category:** Automations | **Version:** 1.0 | **Last Updated:** March 2026

---

## What This Automation Does
When a customer calls the business and no one answers, they instantly receive a personalized text message. Captures leads that would otherwise just call a competitor next.

**Trigger:** Missed incoming call on business phone
**Action:** Instant SMS reply (within 60 seconds)
**Result:** Leads are held until someone can call back; conversion from missed calls increases dramatically

---

## What to Say on the Sales Call
> "Every missed call is a potential customer who just called your competitor next. With this automation, the moment someone calls and you can't answer, they get a text back within 60 seconds: 'Hey, sorry we missed you — we're with another client. What can we help you with?' You stay in the conversation instead of losing them. Most business owners are shocked at how many leads this recovers."

---

## What You Need from the Client

| Item | Why You Need It | Where to Get It |
|---|---|---|
| Business phone number | The number to monitor for missed calls | Ask them |
| Phone system type | Determines the setup approach | Ask: "Are you on a cell phone or a business phone system?" |
| Twilio account (or set up new) | To send the text-back | Create at twilio.com |
| Callback message text | Personalized to their brand | Draft together |

---

## Setup Approach by Phone Type

### Option A: Cell Phone (Most Common for Small Businesses)
**How it works:** Forward unanswered calls to a Twilio number. Twilio detects the missed call and fires the n8n webhook.

1. Set up a Twilio phone number (local area code, ~$1/month)
2. In phone settings: enable **"Forward to Twilio number when unanswered after 20 seconds"**
3. In Twilio: configure the number to send a webhook to n8n on missed call
4. n8n receives the webhook → sends SMS back to the caller

### Option B: VoIP / Business Phone System (RingCentral, Grasshopper, etc.)
Most VoIP systems have built-in missed call webhooks or Zapier integrations.
1. Find the missed call webhook setting in their VoIP dashboard
2. Point it to the n8n webhook URL
3. n8n receives → sends SMS

### Option C: Google Voice
Google Voice doesn't have native webhooks — use the sheet approach:
1. Enable missed call email notifications in Google Voice settings
2. n8n Gmail trigger → detect missed call email → parse caller number → send SMS via Twilio

---

## n8n Workflow Setup (Twilio Approach)

1. **Trigger:** Webhook → POST (copy URL, paste into Twilio missed call webhook field)
2. **Node 2:** IF → check `CallStatus = no-answer` OR `CallStatus = busy`
3. **Node 3:** Twilio → Send SMS
   - To: `{{$json.From}}` (the caller's number)
   - From: Twilio business number
   - Body: Text-back message (template below)
4. Save and **Activate**

---

## Message Templates

### Immediate Text-Back (Default)
```
Hey [First Name if known, otherwise omit], sorry we missed your call! 
We're with a client right now but we'll call you back shortly. 
In the meantime, what can we help you with? — [Business Name]
```

### Appointment-Oriented Business
```
Hi! Sorry we missed you at [Business Name]. We'd love to help — 
reply here or book online anytime: [booking link]. 
We'll also call you back as soon as we're free!
```

### Service/Trades Business
```
Thanks for calling [Business Name]! We missed you — we're on a job site right now. 
Text us what you need and we'll get back to you ASAP. — [Owner Name]
```

---

## Twilio Setup (If Client Doesn't Have an Account)

1. Go to **twilio.com** → Create account (free trial gives ~$15 credit)
2. Get a local phone number (~$1.15/month after trial)
3. Go to: Phone Numbers → Manage → Active Numbers → click the number
4. Under **"A Call Comes In"** → set to Webhook → paste n8n webhook URL
5. Copy: Account SID + Auth Token → paste into n8n Twilio credentials

---

## How to Test It
1. Call the business number from a different phone and don't answer
2. Wait 20–30 seconds
3. Confirm a text-back arrives on the calling phone
4. Check n8n execution log shows the workflow fired

---

## What "Working" Looks Like
- Every unanswered call triggers an instant text within 60 seconds
- Business owner receives no missed-call leads silently — every caller is captured
- Replies to the text-back come in as SMS conversations via Twilio

---

## Common Issues

| Problem | Fix |
|---|---|
| Text not sending | Check Twilio account balance + credentials in n8n |
| Wrong number receiving the text | Verify `$json.From` is the caller's number in the webhook payload |
| Webhook not triggering | Confirm Twilio number's missed call webhook URL matches n8n |
| Call forwarding not set up | Walk through phone settings together on the onboarding call |

---

## Upgrade Path
> "Now that we're capturing missed calls, want to add a follow-up sequence? If they don't respond to the first text in 24 hours, it sends a second one automatically."

---

*FlowstateAI Automation — Automations SOP*
