# FlowstateAI — n8n Workflow Audit
### All Workflows Catalogued · March 2026

> **Purpose:** Know what you have, how it works, what it needs to run for a client, and what tokens expire.

---

## 🗂️ COMPLETE WORKFLOW INVENTORY

| # | File | Name | Type | Status | Client-Ready? |
|---|---|---|---|---|---|
| 1 | `01_intake_webhook.json` | Lead Intake Webhook | Internal tool | ✅ Active | 🟡 Partial |
| 2 | `02_intake_email_sms.json` | FB Lead Ads → Email + SMS | Client deliverable | ✅ Active | 🟡 Need token swap |
| 3 | `04_search_to_social.json` | Auto Facebook Poster (4x Daily) | Internal + client | ✅ Active | 🟡 Need token swap |
| 4 | `05_linkedin_auto_poster.json` | Auto LinkedIn Poster (4x Daily) | Internal + client | ✅ Active | ⚠️ Token expires |
| 5 | `06_cold_outreach.json` | Cold Email Outreach (Daily) | Internal | ✅ Active | 🔴 Internal only |
| 6 | `07_speaking_org_nurture.json` | Speaking Org 90-Day Nurture | Internal | ✅ Active | 🔴 Internal only |
| 7 | `fb_lead_ads_nurture.json` | FB Leads → 10-Day Email Sequence | Client deliverable | ✅ Active | 🟡 Need token swap |
| 8 | `nurture_sequence.json` | Cold Lead 10-Day Nurture | Client deliverable | ✅ Active | 🟢 Most reusable |
| 9 | `n8n_guide_funnel_workflow.json` | Guide/Funnel Workflow | Internal | Unclear | 🔲 Not audited |
| 10 | `weekly_video_workflow.json` | Weekly Video Creator | Internal | Unclear | 🔲 Not audited |
| 11 | `r2-upload-worker/` | R2 Upload Worker | Infrastructure | ✅ Active | N/A |

---

## 📋 WORKFLOW DEEP DIVES

---

### WF-01: Lead Intake Webhook
**File:** `01_intake_webhook.json`
**What it does:** Catches incoming leads from any form or ad (POST webhook) and normalizes the field names into a standard format: `firstName`, `lastName`, `email`, `phone`, `source`.

**Trigger:** HTTP POST to `/incoming-lead`
**Output:** Normalized lead object

**Credentials needed:** None (webhook only)

**To use for a client:**
- Import the workflow into their n8n instance
- Copy the webhook URL → paste into their form or ad
- Connect the output to whatever comes next (email, SMS, CRM, sheet)

**Status:** ✅ Works as-is. Generic and reusable.

---

### WF-02: Facebook Lead Ads → Email + SMS
**File:** `02_intake_email_sms.json`
**What it does:**
1. Handles Facebook's one-time webhook verification (GET request)
2. Receives Facebook Lead Ad notifications (POST)
3. Calls the Facebook Graph API to fetch the actual lead data (name, email, phone)
4. Sends a branded welcome email via Gmail
5. Sends an instant SMS via Twilio

**Trigger:** Facebook webhook (GET for verification + POST for leads)
**Credentials needed:**
- Facebook Graph API access token (hardcoded — needs replacing per client)
- Gmail OAuth credentials
- Twilio Account SID + Auth Token

**⚠️ Token Alert:** The Facebook access token in the workflow (`EAASPs2n9FSU...`) is specific to FlowstateAI. **Must be replaced for each client.**

**To make client-ready:**
1. Replace `access_token` in the "Fetch Lead Details" node with client's token
2. Update email `fromEmail` and content to client's brand
3. Update SMS message to client's brand
4. Update Twilio credentials
5. Give client the webhook URL for their Facebook App

**Time to deploy for a new client: ~30 minutes**

---

### WF-03: Auto Facebook Poster (4x Daily)
**File:** `04_search_to_social.json`
**What it does:**
1. Fires at 10am, 2pm, 6pm, 10pm daily
2. Picks a random topic + CTA from a pre-built list
3. Sends topic to Gemini → writes a branded social post
4. Second Gemini call quality-checks the post (approves or rejects)
5. If rejected → retries up to 3 times, then force-publishes
6. Posts to Facebook Page with a random stock image (Picsum)

**Trigger:** Schedule (4x daily)
**Credentials needed:**
- Gemini API key (hardcoded — `AIzaSy...`)
- Facebook Page ID (hardcoded — `106120138410783`)
- Meta Access Token (hardcoded — `EAF1Aej...`)
- Instagram Account ID (placeholder — not connected)

**⚠️ Token Alert:** Meta Access Token expires. Check expiry date. Must be refreshed.

**To make client-ready:**
1. Create a client version with their topic list (industry-specific topics)
2. Replace `facebook_page_id` with client's Page ID
3. Replace `meta_access_token` with client's token
4. Update CTA list to their brand/offer
5. Optionally remove Picsum and replace with their own images from R2

**Time to deploy for a new client: ~45 minutes (mostly topic customization)**

**Sellable as:** Social Media Automation package — "AI writes and posts to your Facebook 4x a day, automatically."

---

### WF-04: Auto LinkedIn Poster (4x Daily)
**File:** `05_linkedin_auto_poster.json`
**What it does:** Identical architecture to the Facebook poster but:
- Posts to LinkedIn personal profile (not a page)
- Uses LinkedIn's UGC API
- LinkedIn-optimized post format (professional tone, 3-5 paragraphs, minimal emojis)

**Trigger:** Schedule (4x daily)
**Credentials needed:**
- Gemini API key
- LinkedIn Access Token
- LinkedIn Author URN (`urn:li:person:awTZOzacNq`)

**⚠️ CRITICAL Token Alert:**
> LinkedIn OAuth tokens expire in ~60 days from issue date.
> Current token was issued around March 5, 2026.
> **EXPIRES APPROXIMATELY: May 4, 2026**
> Must be refreshed via OAuth flow before then.

**To make client-ready:**
- LinkedIn posting requires personal profile OAuth — each person has their own token
- Client needs to authorize their own LinkedIn API app
- Feasibility: medium complexity (requires client to have a LinkedIn API app or use yours)
- **More practical for personal brand clients than businesses**

**Time to deploy for a new client: ~90 minutes (mostly OAuth setup)**

---

### WF-05: Cold Email Outreach (Daily)
**File:** `06_cold_outreach.json`
**What it does:**
1. Runs every day at 9am
2. Reads "Flowstate Scrapped Leads" tab from Google Sheet
3. Picks up to 10 uncontacted leads per industry (Real Estate, Medical, Automotive)
4. Builds a custom HTML email per industry with Joe's branding
5. Sends via Gmail
6. Marks each lead as "Contacted - YYYY-MM-DD" in the sheet

**Trigger:** Schedule (9am daily)
**Google Sheet ID:** `1ggsYpkeK8JponX61hJYC_pC3NgVXHZoCeVYQ1HuiPCA`
**Tab:** `Flowstate Scrapped Leads`

**Credentials needed:**
- Google Sheets OAuth
- Gmail OAuth

**⚠️ This is an internal FlowstateAI workflow.** The email content, branding, and CTA are all built for Joe's business. Not directly client-deployable in its current form.

**Could be sold as:** "Automated cold outreach system" — but requires significant customization of email content, industry list, and branding per client.

---

### WF-06: Speaking Org 90-Day Nurture Sequence
**File:** `07_speaking_org_nurture.json`
**What it does:**
1. Runs every day at 9am
2. Reads "Speaking Org Leads" tab from same Google Sheet
3. Checks each lead's `Sequence Start Date` and calculates days elapsed
4. Sends a different email at days: 7, 14, 21, 28, 45, 60, 90
5. Skips leads marked: Responded, Booked, Declined, Complete
6. Updates "Last Follow-up Sent" and date in the sheet

**7 email touchpoints — all fully written:**
- Day 7: Follow-up on the speaking opportunity
- Day 14: Stats your members might find useful
- Day 21: Atlantic Canada has a window right now
- Day 28: Lighter-lift format options
- Day 45: Something specifically for your members (custom one-pager offer)
- Day 60: Checking in — AI and your members
- Day 90: Final email — leaving the door open

**⚠️ Internal workflow.** Content is specific to Joe's speaking pitch.

**Could be sold as:** "Long-term relationship nurture sequence" for B2B sales. The architecture (7-touch, day-based, sheet-driven, skip logic) is highly reusable.

---

### WF-07: Facebook Lead Ads → 10-Day Email Nurture
**File:** `fb_lead_ads_nurture.json`
**What it does:**
1. Polls Google Sheet every 5 minutes for new leads
2. Filters for leads from "blueprint" Facebook Lead Ad form with a valid email
3. Sends 5 emails over 10 days: Day 0, 2, 4, 7, 10
4. Each email is a different angle: deliver the freebie → bottleneck → audit → local proof → final close
5. CTA throughout: book a free Systems Audit call

**Email sequence:**
- Day 0: Blueprint delivery
- Day 2: "Did you see this on Page 4?" (Bottleneck Matrix)
- Day 4: "Let's look under the hood" (audit pitch)
- Day 7: "What businesses near you are doing differently" (local proof)
- Day 10: "Closing the loop" (final breakup email)

**Credentials needed:**
- Google Sheets OAuth (reads "FlowstateAI Leads" sheet, "Leads" tab)
- Gmail OAuth

**⚠️ Content is FlowstateAI-specific.** References "the Blueprint", Joe's photo, FlowstateAI branding.

**To make client-ready:** Huge effort — all email content, branding, CTA, and lead source would need to change per client. This is a premium deliverable in your Enterprise package.

**Sellable as:** "Custom 10-day lead nurture sequence" — charge accordingly.

---

### WF-08: Cold Lead 10-Day Nurture (Most Reusable)
**File:** `nurture_sequence.json`
**What it does:** Nearly identical to WF-07 but:
- Triggered by an **n8n form** (not Google Sheet polling)
- Allows manual entry of a lead (First Name, Email, Industry) to start the sequence
- Industry-aware: Day 7 email references their specific industry
- Otherwise same 5-email, 10-day structure

**This is your most client-deployable template** because:
- Lead source is flexible (the form can be replaced with any trigger)
- Industry field makes it semi-personalized out of the box
- No dependency on a specific Google Sheet

**To make client-ready:**
1. Replace all FlowstateAI branding (logo URL, Joe's photo URL, site URL)
2. Update Calendly URL → client's booking link
3. Rewrite email body content for client's offer/industry
4. Replace Gmail credentials with client's email
5. Change the form trigger → connect to their lead source

**Time to fully customize for a client: 2–3 hours (email content rewrite is the bulk)**

---

## ⚠️ CREDENTIAL & TOKEN STATUS

| Credential | Current Owner | Expiry | Action Required |
|---|---|---|---|
| Facebook Graph API Token (`EAASPs2n9...`) | FlowstateAI | Unknown — check Meta dashboard | Replace for every client |
| Meta Page Token (`EAF1Aej...`) | FlowstateAI | Unknown | Check Meta → refresh |
| LinkedIn Access Token | Joe's personal account | **~May 4, 2026** | Refresh before expiry |
| Gemini API Key (`AIzaSyCaU...`) | FlowstateAI | No expiry | Keep — replace for clients |
| Gmail OAuth | Joe (joemoulton2022@gmail.com) | Rolling | Replace for each client |
| Google Sheets OAuth | Joe | Rolling | Replace for each client |
| Twilio | FlowstateAI | No expiry | Use client's account per deployment |

---

## 🎯 CLIENT DEPLOYMENT PRIORITY

### 🟢 Easiest to Deploy (< 1 hour)
1. **WF-01: Lead Intake Webhook** — generic, just swap the destination
2. **Appointment Reminder** — build fresh from SOP, simple n8n flow
3. **Google Review Request** — build fresh from SOP

### 🟡 Medium Effort (1–3 hours)
4. **WF-02: FB Lead Ads → Email + SMS** — swap tokens + email content
5. **WF-03: Auto Facebook Poster** — swap tokens + topic list
6. **WF-08: Cold Lead Nurture** — rewrite email content

### 🔴 Heavy Lift (3+ hours — Enterprise tier)
7. **WF-07: FB Leads → 10-Day Nurture** — full rewrite
8. **WF-04: LinkedIn Auto Poster** — OAuth complexity
9. **WF-06: 90-Day Speaking Nurture** — complete content rewrite

---

## 📌 NEXT STEPS

### Immediate (This Week)
- [ ] Check LinkedIn token expiry — renew if within 30 days
- [ ] Check Meta access token expiry in Meta Business Suite
- [ ] Create "client template" versions of WF-02 and WF-08 with placeholder variables

### When First Client Onboards
- [ ] Create `n8n_workflows/client_templates/` folder
- [ ] Build WF-02-CLIENT-TEMPLATE.json (all credentials = placeholders)
- [ ] Build WF-08-CLIENT-TEMPLATE.json (all branding = placeholders)

### Ongoing
- [ ] Document each new workflow here as it's built
- [ ] Update token status table monthly

---

*FlowstateAI Automation — n8n Workflow Audit*
*Last updated: March 2026*
