# FlowstateAI — n8n Credentials Cheat Sheet

> This doc tells you exactly what credentials to gather and where to paste each one in n8n.
> Once all credentials are added, the full intake workflow will be live.

---

## ✅ Instagram System User Token (Permanent — Never Expires)

| Field | Value |
|-------|-------|
| **System User** | FlowstateAi Automation |
| **Token** | `EAF1AejZCO7fEBRHMyD64GUYUdhz0iJ2ntC8cPvf49Jah9uMtWwDh18o2VZAFOjagu4Q1BQqaCjJidWADrzh5tEgPyoIup9qAK53ZBNzcaZBfzPu7h2941M6UuzFkKRJc1bK2Bxp4HuaWDoOcioH4g6A1EPxFXi8XWiAjOwKF7RZAZBxPs7SnkY8kd8cqCxswZDZD` |
| **Type** | System User (never expires) |
| **Generated** | 2026-03-20 |
| **Instagram Account** | @joe_flowstateai_automation |

---

## How to Add Credentials in n8n
1. Open n8n in your browser (`http://localhost:5678`)
2. Go to the top right menu → **Credentials**
3. Click **+ Add Credential**
4. Search for the credential type listed below and follow the steps

---

## Credential 1: Email (Gmail or SMTP)

**Used by:** `Send Welcome Email` node in `02_intake_email_sms` workflow

### Option A — Gmail (Easiest)
1. In n8n Credentials, search for **Gmail OAuth2**
2. Click **Connect with Google**
3. Log in with the Gmail account you want to send emails FROM
4. Authorize n8n to send on your behalf
5. Name the credential `FlowstateAI Gmail`
6. Go back to the `Send Welcome Email` node and select this credential

> **Important:** Update the `Reply-To` email in the Send Email node from `your-email@yourdomain.com` to your actual email address.

### Option B — SMTP (Any email host)
| Field | Value |
|-------|-------|
| Host | Your email provider's SMTP server (e.g. `smtp.gmail.com`) |
| Port | `587` (TLS) or `465` (SSL) |
| User | Your full email address |
| Password | Your email password or App Password |
| SSL/TLS | Enabled |

---

## Credential 2: Twilio (SMS)

**Used by:** `Send SMS (Twilio)` node in `02_intake_email_sms` workflow

### Sign Up Steps
1. Go to **[twilio.com](https://twilio.com)** → Sign Up Free
2. Verify your email and phone number
3. Get a free Twilio phone number (used as your "From" sender)
4. Go to your **Console Dashboard** and copy:
   - **Account SID**
   - **Auth Token**

### Add to n8n
1. In n8n Credentials, search for **Twilio**
2. Paste your Account SID and Auth Token
3. Name it `FlowstateAI Twilio`
4. In the `Send SMS (Twilio)` node, set:
   - **From:** Your Twilio phone number (e.g. `+15145551234`)
   - **Credential:** FlowstateAI Twilio

### Twilio Cost Reference
| Action | Cost (USD) |
|--------|------------|
| Phone number (monthly) | ~$1.15/mo |
| Outbound SMS | ~$0.0079/message |
| 100 leads/month | ~$0.79 in SMS fees |

---

## Workflow Activation Checklist

- [ ] Import `02_intake_email_sms.json` into n8n
- [ ] Add Gmail or SMTP credential → connect to `Send Welcome Email` node
- [ ] Update Reply-To email in `Send Welcome Email` node
- [ ] Sign up for Twilio → add credential → connect to `Send SMS (Twilio)` node
- [ ] Set your Twilio "From" phone number in the SMS node
- [ ] Toggle workflow to **Active** (top right toggle in the workflow editor)
- [ ] Copy the **Production Webhook URL** from the Webhook node
- [ ] Paste Production URL into Facebook Webhooks → Verify and Save

---

## What the Improved Workflow Now Does
1. **Webhook catches lead data** from Facebook or any form
2. **Immediately replies 200 OK** so Facebook doesn't retry or error
3. **Normalizes data** — handles any field naming convention
4. **Guards before sending** — only fires email if email exists, only fires SMS if phone exists
5. **Sends personalized HTML email** with FlowstateAI branding
6. **Sends compliant SMS** with STOP opt-out message (required by law)
