# SOP: Google Review Request Automation
**Category:** Automations | **Version:** 1.0 | **Last Updated:** March 2026

---

## What This Automation Does
Automatically sends a review request to a customer after every completed appointment or sale. Builds Google reviews on autopilot without the business owner ever having to ask manually.

**Trigger:** Appointment marked complete / sale recorded
**Action:** Wait 2 hours → Send personalized review request via email or SMS
**Result:** Consistent stream of new Google reviews; typically 3–5x more reviews within 60 days

---

## What to Say on the Sales Call
> "Most businesses get reviews from maybe 5% of their happy customers — because they forget to ask, or it feels awkward. This automation sends a personalized request 2 hours after every appointment, when the experience is still fresh. We've seen businesses go from 12 reviews to 80+ in 90 days. It's the single easiest way to build your reputation without doing anything different."

---

## What You Need from the Client

| Item | Why You Need It | Where to Get It |
|---|---|---|
| Booking system / POS access | To detect when an appointment is complete | Onboarding call |
| Customer email or phone | To send the request | Comes from booking system |
| Google Business Profile URL | The review link customers click | Google Maps → their listing → "Write a review" |
| Business name + warm tone | For message personalization | Ask them |

**How to get their Google Review link:**
1. Go to Google Maps → search their business
2. Click "Write a review"
3. Copy the URL from the browser
4. Shorten it with bit.ly for SMS use

---

## n8n Workflow Setup

### Standard Flow
1. **Trigger:** Booking system (Calendly / Acuity / Sheets) → appointment status = "completed"
   OR Google Calendar event end time passes
2. **Node 2:** Wait 2 hours (`PT2H`)
3. **Node 3:** Send SMS (Twilio) OR Email (Gmail)
   - Content: Review request message (template below)
4. Save and **Activate**

### Alternative: Daily Batch (Simpler for Manual Systems)
1. **Trigger:** Schedule Trigger → Every day at 6:00 PM
2. **Node 2:** Google Sheets → Get rows where date = today AND reviewed = FALSE
3. **Node 3:** Loop → Send SMS/email to each row
4. **Node 4:** Update Sheet → mark reviewed = TRUE
5. Save and **Activate**

---

## Message Templates

### SMS Version
```
Hi [First Name]! It was great seeing you at [Business Name] today. 
If you have 60 seconds, we'd love a Google review — it makes a huge 
difference for a local business: [review link]
Thank you! — [Business Name]
```

### Email Version
**Subject:** How did we do today, [First Name]?

```
Hi [First Name],

Thank you for coming in today — it was a pleasure having you at [Business Name]!

We'd really appreciate it if you could take 60 seconds to share your experience on Google. 
Reviews from customers like you make a big difference for a small local business.

👉 Leave a review here: [Google Review Link]

It only takes a minute and means the world to us.

Thank you,
[Owner Name]
[Business Name]
```

---

## How to Get the Google Review Direct Link
1. Go to **Google Maps** and search the business
2. Click on their listing
3. Click **"Write a review"** button
4. Copy the full URL (looks like: `https://g.page/r/XXXXX/review`)
5. Use this link in the automation

---

## How to Test It
1. Mark a test appointment as complete (or add a test row to the sheet)
2. Confirm n8n workflow fires
3. Check that the message arrives at your test number/email
4. Verify the review link works (opens Google review form)

---

## What "Working" Looks Like
- Review requests fire automatically after every appointment
- Client sees a gradual increase in Google reviews over 30–60 days
- Review count is visibly growing on their Google Business Profile
- Owner gets more word-of-mouth referrals from improved star rating

---

## Common Issues

| Problem | Fix |
|---|---|
| Appointment "complete" not triggering | Check if booking system has a status webhook; may need manual/sheet approach |
| SMS link too long | Use bit.ly to shorten the Google review URL |
| Low review conversion rate | Test the message tone — make it warmer and more personal |
| Customer getting multiple requests | Add a "reviewed" flag in the sheet to prevent duplicates |

---

## Upgrade Path
Natural next step: **"Want to also auto-respond to new reviews with a thank-you? That's an advanced add-on."**

---

*FlowstateAI Automation — Automations SOP*
