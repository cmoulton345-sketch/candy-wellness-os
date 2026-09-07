# SOP: Instant Lead Follow-Up Automation
**Category:** Automations | **Version:** 1.0 | **Last Updated:** March 2026

---

## What This Automation Does
The moment a new lead submits an inquiry (contact form, Facebook Lead Ad, website form), they receive a personalized response within 60 seconds — 24/7, even at 2am.

**Trigger:** New lead submission (website form, Facebook Lead Ad, or CRM entry)
**Action:** Instant email + SMS to the lead within 60 seconds
**Result:** Lead feels seen immediately; dramatically higher conversion vs. businesses that reply hours later

---

## What to Say on the Sales Call
> "Studies show that the odds of converting a lead drop by 80% if you wait more than 5 minutes to respond. Most small businesses reply hours later — if at all. This automation responds within 60 seconds, every time, while you're sleeping, on a job site, or with another client. It's like having a 24/7 receptionist who never takes a day off."

---

## What You Need from the Client

| Item | Why You Need It | Where to Get It |
|---|---|---|
| Where their leads come in | To connect the trigger | Ask: "When someone contacts you, where does that go?" |
| Lead form access / webhook | To capture the submission | Depends on their system |
| Response message | Personalized to their offer | Draft together |
| SMS capability (Twilio) | To send the text | Twilio account setup |
| CRM or sheet to log leads | Track captured leads | Google Sheets works fine |

---

## Trigger Setup by Lead Source

### Option A: Website Contact Form (Most Common)
**If they use Gravity Forms, Contact Form 7, WPForms (WordPress):**
- Install the n8n or Zapier webhook plugin
- Point the form webhook to the n8n webhook URL

**If they use a custom HTML form:**
- Add `fetch()` POST to n8n webhook URL on form submit
- (We built exactly this in our own free-call landing page)

### Option B: Facebook Lead Ads
- Connect Facebook Lead Ads trigger in n8n
- Auth: Facebook Page access token
- n8n receives lead data automatically on each new submission

### Option C: Calendly Booking (New Booking = New Lead)
- Calendly trigger → `invitee.created` event
- Treat new bookings as leads for immediate follow-up

### Option D: Manual Google Sheet Entry
- Google Sheets trigger → on new row
- Sales rep adds a lead manually → automation fires within 1 minute

---

## n8n Workflow Setup

1. **Trigger:** Webhook (or Facebook Lead Ads / Google Sheets trigger)
2. **Node 2:** Set — extract `first_name`, `email`, `phone`, `business_type`
3. **Node 3 (parallel):** Send Email (Gmail)
   - To: `{{$json.email}}`
   - Subject + body: use email template below
4. **Node 4 (parallel):** Send SMS (Twilio)
   - To: `{{$json.phone}}`
   - Body: use SMS template below
5. **Node 5:** Google Sheets → Append Row (log lead to pipeline sheet)
6. **Node 6 (optional):** Send internal notification to Joe's phone — "New lead: [Name] from [Business]"
7. Save and **Activate**

---

## Message Templates

### Instant SMS (fires within 60 seconds)
```
Hey [First Name]! This is Joe from FlowstateAI — thanks for reaching out. 
I'll be in touch shortly to set up your free automation call. 
In the meantime, is there a best time to reach you? — Joe
```

*(Personalize to the client's business — this is the template for FlowstateAI itself)*

### Client Version — Appointment-Based Business
```
Hi [First Name]! Thanks for reaching out to [Business Name]. 
We received your message and will be in touch shortly. 
Want to book a time now? [booking link] — [Business Name]
```

### Client Version — Trades / Service Business
```
Thanks for contacting [Business Name], [First Name]! 
We got your request and will call you back within the hour. 
For urgent needs, call us directly: [phone]. — [Owner Name]
```

### Instant Email
**Subject:** Got your message, [First Name] — here's what happens next

```
Hi [First Name],

Thanks for reaching out to [Business Name]! We received your message 
and someone will be in touch with you shortly.

While you wait, here's what to expect:
- We'll contact you within [X hours / same business day]
- [Any relevant info, pricing, booking link, etc.]

If you need to reach us right away: [phone number]

Talk soon,
[Owner Name]
[Business Name]
[Website]
```

---

## Internal Notification Setup (For Joe / The Client)
Add a node to notify the business owner when a new lead comes in:

**SMS to owner:**
```
🔥 New Lead: [First Name] from [Business or City]
Email: [email] | Phone: [phone]
Source: [form/Facebook/Calendly]
```

This way the owner knows a lead has been auto-responded to, and can follow up personally if needed.

---

## How to Test It
1. Submit a test form or lead entry
2. Confirm n8n execution fires within 60 seconds
3. Check SMS received at test number
4. Check email received at test address
5. Verify lead logged in Google Sheet

---

## What "Working" Looks Like
- Every new lead gets an instant response, every time
- Lead feels attended to immediately — no awkward silence
- Owner gets a notification so they can follow up personally
- All leads are logged in one place

---

## Common Issues

| Problem | Fix |
|---|---|
| Webhook not receiving data | Check the form is POSTing to the right n8n URL |
| Email going to spam | Warm up the sending address; check SPF/DKIM |
| SMS not sending | Check Twilio credentials + phone number format (must be E.164: +15061234567) |
| Duplicate notifications | Add a dedup check on email field |

---

## Upgrade Path
> "This handles the first touch. Want to add a 10-day nurture sequence after this? If they don't book in 3 days, they get a follow-up. If still nothing in 7 days, another one. Most clients see 20–30% more bookings just from the follow-up sequence alone."

---

*FlowstateAI Automation — Automations SOP*
