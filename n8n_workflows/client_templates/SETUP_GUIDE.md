# Setup Guide: 10-Day Lead Nurture Client Template
**File:** `10_day_nurture_template.json`
**Deploy time:** ~2 hours (mostly email content writing)

---

## Overview

This is a 5-email, 10-day automated nurture sequence that:
1. Delivers a lead magnet or welcome resource (Day 0)
2. Highlights a key insight to build trust (Day 2)
3. Makes a direct offer — booking a call or consultation (Day 4)
4. Shares social proof / what others are experiencing (Day 7)
5. Sends a final "breakup" email that leaves the door open (Day 10)

**Works for:** Any service business with a lead magnet and a booking link.

---

## Step 1: Import the Workflow into n8n

1. Open n8n (`http://localhost:5678`)
2. Click **"Workflows"** → **"Import from File"**
3. Select `10_day_nurture_template.json`
4. Rename the workflow to: `[Client Name] — 10-Day Nurture`
5. **DO NOT activate yet**

---

## Step 2: Fill in the Setup Variables Node

Open the **"Setup Client Variables"** node. Replace every `REPLACE_...` value:

| Variable | Replace With | Example |
|---|---|---|
| `senderFirstName` | Client's first name | `Sarah` |
| `senderFullName` | Full name | `Sarah Brennan` |
| `senderTitle` | Title + company | `Owner, Coastal Dental` |
| `companyName` | Business name | `Coastal Dental` |
| `bookingUrl` | Their Calendly / booking link | `https://calendly.com/coastal-dental/consult` |
| `logoUrl` | Public URL to their logo image | Upload to R2 → copy URL |
| `photoUrl` | Public URL to their headshot | Upload to R2 → copy URL |
| `siteUrl` | Their website | `https://coastaldental.ca` |
| `leadMagnetUrl` | URL of the thing they're giving away | Link to PDF, page, video, etc. |
| `leadMagnetTitle` | Name of the lead magnet | `"The New Patient Welcome Guide"` |
| `offerName` | What the free call/consult is called | `"Free New Patient Consultation"` |
| `replyToEmail` | The email for replies | `sarah@coastaldental.ca` |

---

## Step 3: Set Up Gmail Credentials

1. In n8n → **Settings → Credentials → New**
2. Add **Gmail OAuth2** credentials
3. Authenticate with the **client's Gmail or Google Workspace account**
4. Name the credential clearly: `Gmail — [Client Name]`
5. In each email Send node, select this new credential

> ⚠️ **Never use Joe's Gmail account for client emails.** Each client must have their own sending credential.

---

## Step 4: Upload Client Assets to R2

**Logo:**
1. Get their logo file (PNG, transparent background preferred)
2. Go to Cloudflare R2 → `flowstatesocialimages` → Upload
3. Path: `clients/[client-name]/logo.png`
4. Copy the public URL → paste into `logoUrl`

**Headshot:**
1. Get a professional photo of the client/owner (ideally already on their website)
2. Upload to R2: `clients/[client-name]/headshot.jpg`
3. Copy URL → paste into `photoUrl`

---

## Step 5: Write the Email Content

Open each **"Build Email"** code node and find the `EDIT:` comments. Replace all placeholder text with real content for the client.

### Day 0 — Welcome + Delivery
- Confirm what the lead magnet is
- Write a warm, brief welcome
- Make the download button obvious

### Day 2 — Key Insight
- Pick the most important thing from their lead magnet
- Or share a tip/insight they can act on immediately
- No hard pitch — just deliver value

### Day 3 — Direct Offer
- Name the offer clearly
- Describe what happens on the call (length, what they'll get)
- Keep it low-pressure

### Day 7 — Social Proof
- Use a real result or testimonial if available
- Or describe a pattern: "Most [industry] businesses I work with find that..."
- Re-pitch the offer briefly

### Day 10 — Breakup
- Acknowledge they've been in touch
- Say you don't want to keep emailing if it's not the right time
- One last CTA
- End warmly — "I'm rooting for you"

---

## Step 6: Choose the Lead Source Trigger

The default trigger is an n8n form (manual entry). For most clients, replace it:

| Their Lead Source | Use This Trigger |
|---|---|
| Calendly booking | Calendly Trigger → `invitee.created` |
| Website contact form | Webhook (POST) — update form to POST to n8n URL |
| Facebook Lead Ads | See `02_intake_email_sms.json` for FB handling |
| Manual entry (Joe adds leads) | Keep the form trigger as-is |
| Google Sheet | Google Sheets Trigger → on row added |

**After changing the trigger**, update the **"Capture Lead Data"** node to map the correct field names from the new trigger output.

---

## Step 7: Test Before Going Live

1. Using the form trigger (or manual execution), submit a test lead with your own email
2. Confirm Day 0 email arrives and looks correct
3. Check branding: logo, headshot, sender name all correct
4. Temporarily set Wait nodes to **1 minute** to test the full sequence quickly
5. Once confirmed → reset Wait nodes to real durations (2 days, 2 days, 3 days, 3 days)
6. **Activate the workflow**

---

## Step 8: Document in Client Folder

Create a file in `work_in_progress/clients/[client-name]/automations.md`:

```markdown
# [Client Name] — Active Automations

## 10-Day Lead Nurture
- Workflow: [Client Name] — 10-Day Nurture
- Status: ✅ Active
- Lead source: [form/webhook/FB ads]
- Sending from: [their email]
- Booking link: [their Calendly]
- Lead magnet: [name + URL]
- Activated: [date]
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Emails not sending | Check Gmail credential is authorized and selected in all Send nodes |
| Logo/headshot not showing | Confirm R2 URLs are public and accessible (try in browser) |
| Leads not triggering | Check trigger is active and connected to correct lead source |
| Wait nodes seem to not fire | n8n must be running 24/7 — make sure start-n8n.ps1 is running |
| Day 7 says "your business" instead of their industry | Check "Capture Lead Data" node — `serviceInterest` field mapping |

---

## What to Charge for This

| Package | Includes | Price |
|---|---|---|
| Starter add-on | Template + 5 emails written | $297 one-time setup + monthly retainer |
| Growth Package | This + instant lead follow-up + appointment reminder | Included in $997/month |
| Enterprise | Fully custom sequence, 10+ emails, industry-specific | Custom |

---

*FlowstateAI Automation — Client Template Setup Guide*
