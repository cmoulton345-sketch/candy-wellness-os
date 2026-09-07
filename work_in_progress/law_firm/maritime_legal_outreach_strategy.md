# Maritime Law Firm Outreach & Socrates Online Freemium Strategy

**Target Market:** Law Firms in New Brunswick, Nova Scotia, and PEI  
**Core Offer:** Firm-wide "AI in Legal Practice" Lunch & Learn / Workshop + Free Socrates Online Access  
**Lead Magnet:** Email-Gated Free Access to Socrates Legal Web Assistant (25 Free Queries/Mo)  
**Authority Lever:** Alignment with Law Society / Barristers' Society Educational Outreach  

---

## 🧭 Executive Summary & Persona Feedback

```
┌────────────────────────────────────────────────────────────────────────┐
│                        THE 3-STEP LEGAL ENGINE                         │
│                                                                        │
│   1. LAW SOCIETY AUTHORITY   ──>   2. FREEMIUM SOCRATES HOOK  ──>  3. FIRM RETAINER  │
│   (Reaching out to Law             (Free access to Socrates        (Lunch & Learn,   │
│    Societies as presenter)          Web via Email OTP)              SOPs, Custom AI) │
└────────────────────────────────────────────────────────────────────────┘
```

### Team Consensus: **10/10 Strategic Genius**

* **Atlas (CMO):** "Law firms are extremely risk-averse. Asking a managing partner to buy software sight-unseen fails. Giving associates and partners a *zero-risk, instant-access trial* of Socrates captures verified corporate emails (`@burkelaw.ca`, `@coxandpalmer.com`, `@stewartmckelvey.com`) and creates internal demand from the ground up."
* **Socrates (Legal Shadow):** "Positioning this alongside Law Society educational outreach establishes FlowstateAI as a trusted Canadian legaltech authority rather than a generic software vendor."
* **Ax (Lead Architect):** "Technically, this is very clean to wire up using our existing Cloudflare Workers stack (`socrates-api` + `socrates-web`). Passwordless Email OTP + Cloudflare D1/KV for credit management gives us instant setup with zero friction."

---

## 📧 Email Pitch Framework for Maritime Law Offices

### **Subject:** Local AI Support for [Firm Name] / Complimentary Socrates Access

**Hi [Partner Name],**

I’m Joe Moulton, founder of FlowstateAI—an AI automation company based right here in New Brunswick. 

I know your inbox is probably flooded with generic software pitches, but I'm reaching out locally because we’re currently partnering with Maritime law firms to help them navigate the messy world of AI adoption securely.

To help your team evaluate practical legal AI without the privacy risks, I want to give the fee-earners at **[Firm Name]** complimentary access to **Socrates Online**—a web assistant we engineered specifically for Canadian case law, statutory analysis, and document drafting.

**How your team can try it out:**
1. Visit **[socrates.flowstateaiautomation.ai](https://socrates.flowstateaiautomation.ai)**
2. Enter your work email (`@[firmdomain].com`) for an instant access pass.
3. Enjoy 25 free research/drafting queries per fee-earner.

*(Zero obligation, no credit card required, and absolutely no exposure or risk to your firm.)*

While your peer firms in the region are starting to streamline their research workflows, I would love to offer **[Firm Name]** a complimentary 30-minute internal Lunch & Learn on practical AI adoption and keeping client data safe.

Do you have 10 minutes next week for a brief introductory call?

Best regards,

**Joe Moulton**  
Founder & CEO | FlowstateAI  
joe@flowstateaiautomation.ai | (506) 607-1791  
[flowstateaiautomation.ai](https://flowstateaiautomation.ai)

***

*Disclaimer: As with any public or cloud-based AI system (and in light of recent jurisprudence regarding AI and attorney-client privilege), we advise that no confidential Client Personally Identifiable Information (PII) or privileged un-redacted fact patterns be entered into the Socrates free-trial environment. Socrates is designed for statutory research, case law analysis, and template drafting using anonymized or redacted inputs.*


## 🛠️ Socrates Online Technical Architecture (Email Gate & Credit Control)

```
   ┌────────────────────┐
   │    User Visits     │
   │  socrates-web UI   │
   └─────────┬──────────┘
             │
             ▼
   ┌────────────────────┐      Generates 6-Digit OTP      ┌────────────────────┐
   │ Enter Work Email   │ ──────────────────────────────> │ Resend API / Mail  │
   └─────────┬──────────┘                                 └─────────┬──────────┘
             │                                                      │
             │ Code Verified                                        │ User Inputs Code
             ▼                                                      ▼
   ┌────────────────────┐      Stores Lead Info & Credit    ┌────────────────────┐
   │ Cloudflare D1 DB   │ <───────────────────────────────> │  Authenticated     │
   │ Track: 25 Uses/Mo  │                                   │  Session Token     │
   └─────────┬──────────┘                                   └────────────────────┘
             │
             │ Credit Balance = 0
             ▼
   ┌────────────────────────────────────────────────────────┐
   │ Upgrade Modal: "Used your 25 monthly queries?           │
   │ Book a 15-min Firm-Wide Demo for Unlimited Access."    │
   └────────────────────────────────────────────────────────┘
```

### 1. Zero-Friction Authentication (Email OTP / Magic Link)
* User enters email on Socrates Web.
* Cloudflare Worker (`socrates-api`) generates a temporary 6-digit OTP via Resend email API.
* User inputs OTP $\rightarrow$ instant session token issued.
* **Result:** Captures full name, email, and law firm domain automatically.

### 2. Credit Management Rules
* **Lifetime Trial Allocation:** 25 Free Lifetime Prompts / Searches per verified email.
* **Domain Recognition:** If 3+ lawyers from the same firm (`@stewartmckelvey.com`) sign up, n8n notifies Joe automatically: *"Hot Lead: 3 partners at Stewart McKelvey are using Socrates!"*
* **Usage Cap Enforcement:** When the 25 lifetime credits reach 0, display a customized CTA modal offering a 15-minute Firm Demo or Unlimited Firm License.

---

## 🎯 Implementation Roadmap

1. **Step 1:** Add Email OTP login modal to `socrates-web` (`work_in_progress/burkelaw/socrates-web`).
2. **Step 2:** Wire up Cloudflare D1 database table in `socrates-api` to track user credits by email.
3. **Step 3:** Deploy updated Socrates Online web app to Cloudflare Pages (`socrates.flowstateaiautomation.ai`).
4. **Step 4:** Build the target Maritime Law Firm contact list (NB, NS, PEI managing partners).
5. **Step 5:** Launch cold outreach email campaign.
