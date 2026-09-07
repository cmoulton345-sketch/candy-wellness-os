# FlowstateAI — SOP Library
### Standard Operating Procedures · Joe Moulton · 2026

> **Purpose:** Every document in this library is a plug-and-play guide. Know nothing. Follow the steps. Get the result.

---

## 📁 Library Structure

### 00 · Business Model
The master document — how we make money, how we scale, how we train new team members.
| File | Description | Status |
|---|---|---|
| [three_tier_scalability_sop.md](00_business_model/three_tier_scalability_sop.md) | 3-Tier business model, infrastructure, deployment SOPs, lockdown, retainer engine, new hire training | ✅ Done |

### 01 · Sales
How we sell — from first contact to signed client.
| File | Description | Status |
|---|---|---|
| [call_to_close_system.md](../work_in_progress/sales_tools/call_to_close_system.md) | Full discovery call script + offer + objection handling + close | ✅ Done |
| [discovery_call_prep.md](01_sales/discovery_call_prep.md) | 15-min pre-call checklist | ✅ Done |
| [proposal_process.md](01_sales/proposal_process.md) | How to send a proposal and follow up | 🔲 To Do |

### 02 · Client Onboarding
What happens after they say yes.
| File | Description | Status |
|---|---|---|
| [onboarding_checklist.md](02_client_onboarding/onboarding_checklist.md) | Full onboarding sequence | ✅ Done |
| [credentials_collection.md](02_client_onboarding/credentials_collection.md) | What access we need + how to get it | 🔲 To Do |

### 03 · Automations
One doc per automation. Setup guides for every workflow we sell.
| File | Automation | n8n Workflow | Status |
|---|---|---|---|
| [appointment_reminder.md](03_automations/appointment_reminder.md) | Appointment Reminder | *(build pending)* | ✅ Done |
| [google_review_request.md](03_automations/google_review_request.md) | Google Review Request | *(build pending)* | ✅ Done |
| [missed_call_textback.md](03_automations/missed_call_textback.md) | Missed Call Text-Back | *(build pending)* | ✅ Done |
| [instant_lead_followup.md](03_automations/instant_lead_followup.md) | Instant Lead Follow-up | *(build pending)* | ✅ Done |
| [noshow_recovery.md](03_automations/noshow_recovery.md) | No-Show Recovery | *(build pending)* | ✅ Done |
| [lapsed_customer_winback.md](03_automations/lapsed_customer_winback.md) | Lapsed Customer Win-Back | *(build pending)* | ✅ Done |

### 04 · Operations
How FlowstateAI itself runs day-to-day.
| File | Description | Status |
|---|---|---|
| [start_n8n.md](04_operations/start_n8n.md) | Start n8n + Cloudflare tunnel | ✅ Done |
| [video_recording_workflow.md](04_operations/video_recording_workflow.md) | Record + upload prospect videos | ✅ Done |
| [r2_file_management.md](04_operations/r2_file_management.md) | Managing R2 storage | 🔲 To Do |

### 05 · Client Library
Industry-specific automation stacks — walk into any meeting ready.
| File | Industry | Status |
|---|---|---|
| [dental.md](05_client_library/dental.md) | Dental Clinics | 🔲 To Do |
| [automotive.md](05_client_library/automotive.md) | Auto Dealerships | 🔲 To Do |
| [trades.md](05_client_library/trades.md) | Trades & Home Services | 🔲 To Do |
| [restaurant.md](05_client_library/restaurant.md) | Restaurants & Hospitality | 🔲 To Do |
| [real_estate.md](05_client_library/real_estate.md) | Real Estate | 🔲 To Do |
| [legal.md](05_client_library/legal.md) | Law Firms | 🔲 To Do |

---

## 🔑 How to Use This Library

**New client just booked?**
→ Start at `01_sales/discovery_call_prep.md`

**Client said yes?**
→ Go to `02_client_onboarding/onboarding_checklist.md`

**Deploying a specific automation?**
→ Find it in `03_automations/` — everything you need is in that one file

**Going to a meeting in a specific industry?**
→ Open the matching file in `05_client_library/`

---

*FlowstateAI Automation — joe@flowstateaiautomation.ai*
