# FlowstateAI — 3-Tier Scalability SOP

**Purpose:** The definitive business model, deployment playbook, and new-employee training manual for scaling FlowstateAI's 3-tier offering across multiple businesses.

**Audience:** FlowstateAI team members (current and future hires). This document contains proprietary methodology — do not share externally.

**Last Updated:** July 2026

---

## Table of Contents

1. [The 3-Tier Model](#1-the-3-tier-model)
2. [Infrastructure Architecture](#2-infrastructure-architecture)
3. [Tier 1: Automations Deployment](#3-tier-1-automations-deployment)
4. [Tier 2: Specialized AI Deployment](#4-tier-2-specialized-ai-deployment)
5. [Tier 3: Domination (Full OS) Deployment](#5-tier-3-domination-full-os-deployment)
6. [Lockdown & IP Protection](#6-lockdown--ip-protection)
7. [The Retainer Engine](#7-the-retainer-engine)
8. [New Employee Onboarding](#8-new-employee-onboarding)
9. [Credential & Token Management](#9-credential--token-management)

---

## 1. The 3-Tier Model

FlowstateAI sells AI-powered business transformation in three tiers. Each tier builds on the one below it.

### Tier Overview

| | Tier 1: Automations | Tier 2: Specialized AI | Tier 3: Domination (Full OS) |
|---|---|---|---|
| **What they get** | N8N workflow automations (missed call textback, review requests, nurture sequences, social posting) | Custom AI persona(s) built for their business (e.g., a legal AI, a sales AI, an EHS AI) | Full AI Operating System — personas, axioms, workflows, dispatcher, content system |
| **Who uses it** | Business admin (1 person) | Multiple team members (each gets own login) | 1-2 senior leaders |
| **Account model** | One admin account, managed by FlowstateAI | Each user gets own username + paid AI account (Gemini/Claude) | Dedicated accounts, dedicated workspace |
| **IP exposure** | Zero — they see results, not code | Minimal — they interact with the AI, don't see prompts | Controlled — OS runs locally but source is protected |
| **Retainer driver** | New automations, maintenance, token refresh | New personas, capability upgrades, usage monitoring | New personas, axioms, workflows, integrations |
| **Typical client** | Local businesses (dental, trades, restaurants) | Mid-market companies with specific domain needs | Growth companies wanting full AI transformation |

### Client Fit Criteria

**Tier 1 fits when:** The client has manual, repetitive processes that lose them money (missed calls, no-show appointments, zero follow-up). They want results, not technology.

**Tier 2 fits when:** The client has domain experts who need AI amplification — a law firm that wants instant legal research, a safety team that needs compliance AI, a sales team that needs pitch generation. Multiple users will interact with the AI.

**Tier 3 fits when:** The client's leadership wants to fundamentally change how their business operates. They want an AI co-pilot embedded in their workflow — not a tool, a system.

---

## 2. Infrastructure Architecture

### 2.1 N8N Architecture (Tier 1 + Tier 2)

**Current state:** Single self-hosted n8n instance (Docker on VPS, accessed via Cloudflare Tunnel).

**Scaled state:** Instance-per-client model.

```
VPS-1 (Primary — FlowstateAI Internal)
├── n8n-flowstate/          ← Internal workflows (cold outreach, lead gen)
├── n8n-client-alpha/       ← Client Alpha's isolated instance
├── n8n-client-beta/        ← Client Beta's isolated instance
└── docker-compose.yml      ← Manages all containers

VPS-2 (Overflow — when VPS-1 hits capacity)
├── n8n-client-gamma/
├── n8n-client-delta/
└── docker-compose.yml
```

**Why instance-per-client:**
- Credential isolation — one client's Facebook token leak doesn't expose others
- Failure isolation — one crashing workflow doesn't take down everyone
- Clean billing — each instance's execution count maps to one client
- Industry standard for automation agencies

**Capacity planning:**
- Each n8n container uses ~200-400MB RAM idle
- A 4GB VPS comfortably runs 5-8 client instances
- A 8GB VPS handles 10-15 instances
- **Decision point:** At 8+ clients, purchase a second VPS ($20-40/mo)

**Per-client instance setup:**

```yaml
# docker-compose.yml — add a new service block per client
n8n-clientname:
  image: n8nio/n8n
  container_name: n8n-clientname
  environment:
    - N8N_HOST=clientname-n8n.flowstateai.com
    - N8N_PORT=5678
    - N8N_PROTOCOL=https
    - GENERIC_TIMEZONE=America/Halifax
  volumes:
    - ./n8n-clientname-data:/home/node/.n8n
  ports:
    - "5679:5678"  # Increment port per client
  restart: unless-stopped
```

Each client gets a Cloudflare Tunnel subdomain: `clientname-n8n.flowstateai.com`

### 2.2 AI Account Architecture (Tier 2 + Tier 3)

**Principle:** Each client's AI usage is tied to their own paid account. FlowstateAI builds the system; the client's account pays for the tokens.

| Tier | AI Account Model | Who Pays |
|---|---|---|
| Tier 1 | FlowstateAI's Gemini key (used in n8n for content generation) | FlowstateAI absorbs — baked into retainer |
| Tier 2 | Client gets their own Gemini/Claude paid account | Client pays directly. FlowstateAI sets it up. If usage is light, cost absorbed into retainer. Heavy usage = additional charge discussed during intake. |
| Tier 3 | Client provides their own API keys stored in their `.env` | Client pays directly. "Their tokens, our architecture." |

**Per-client setup for Tier 2:**

1. Create a Google Cloud project for the client (or have them create one)
2. Enable the Gemini API
3. Generate a restricted API key scoped to Gemini only
4. Store the key in the client's n8n instance credentials
5. If using Claude: create a separate Anthropic account/workspace for the client
6. Document the key in the client's credential tracker

**Per-client setup for Tier 3:**

1. Client creates their own Gemini/Claude account (or FlowstateAI creates it under their billing)
2. API key goes into their OS workspace `.env` file
3. `.env` is NEVER synced via `/push-os-updates` — it stays client-specific
4. Usage monitoring: check Google Cloud Console monthly during retainer check-ins

### 2.3 GitHub & Code Management Architecture

**Principle:** Clients use the OS but never see the source. The "secret sauce" (personas, axioms, dispatcher logic, workflows) stays proprietary.

**Architecture:**

```
GitHub Organization: FlowstateAI-Clients (private)
├── radical_simplicity_ai_os_master     ← Source of truth (Joe's workspace)
├── radical_simplicity_ai_os_alpha      ← Client Alpha's OS (FlowstateAI access only)
├── radical_simplicity_ai_os_beta       ← Client Beta's OS (FlowstateAI access only)
└── ...
```

**Critical rule:** Clients do NOT get GitHub access to their OS repo. FlowstateAI owns and operates all repos. The client interacts with their OS through the AI interface only.

**Why no client GitHub access:**
- The `.agent/rules/` directory contains our proprietary prompt engineering — the entire value of the business
- Markdown persona files cannot be encrypted or compiled — if someone can read the filesystem, they can read the prompts
- Contractual protection (NDA) is a backup, not a primary defense
- The OS is the product. Exposing it is like giving away the franchise manual.

**How clients get their work synced:**
- The `work_in_progress/` directory is where all client deliverables live
- FlowstateAI can set up a *separate* client-owned repo that syncs ONLY `work_in_progress/` — giving them version history of their output without exposing the OS internals
- Alternatively: deliverables are exported and shared via cloud storage, email, or the MCP Fileclerk system (future)

**Update flow:**

```
Joe improves a persona/workflow/axiom in master workspace
    ↓
Runs /push-os-updates from master workspace
    ↓
Script reads deployments.yaml → pushes to all client OS directories
    ↓
Changes propagate to all clients automatically
    ↓
Client's .env and work_in_progress/ are NEVER touched
```

---

## 3. Tier 1: Automations Deployment

### 3.1 Pre-Deployment (During Sales)

Refer to: `sops/01_sales/discovery_call_prep.md` and `work_in_progress/sales_tools/call_to_close_system.md`

During the discovery call, identify which automations fit the client's business. Use the automation catalog in `sops/03_automations/` to match pain points to solutions.

### 3.2 Deployment Steps

**Time estimate:** 2-4 hours total (including onboarding call)

1. **Create client n8n instance** (15 min)
   - Add new service block to VPS docker-compose.yml
   - Assign unique port and subdomain
   - Start container: `docker compose up -d n8n-clientname`
   - Set up Cloudflare Tunnel route for the subdomain
   - Create admin credentials for the client's instance

2. **Deploy automations** (30-90 min depending on count)
   - Import workflow templates from `n8n_workflows/client_templates/`
   - Swap all placeholder credentials with client's real tokens
   - Refer to `sops/n8n_workflow_audit.md` for per-workflow credential requirements
   - Test each workflow end-to-end

3. **Run onboarding call** (60 min)
   - Follow `sops/02_client_onboarding/onboarding_checklist.md`
   - Screen share, deploy live, test together
   - Set 30-day check-in

4. **Post-deployment**
   - Send "system is live" email
   - Add client to pipeline tracker
   - Add client to `deployments.yaml` for n8n monitoring
   - Schedule token refresh reminders (Facebook, LinkedIn, etc.)

### 3.3 Ongoing Management

- Monthly: Check workflow execution logs for failures
- Monthly: Verify token/credential expiry dates
- Quarterly: 30-day check-in → upsell conversation
- As needed: Deploy new automations (billable)

---

## 4. Tier 2: Specialized AI Deployment

### 4.1 Pre-Deployment (Intake & Discovery)

This tier requires a deeper discovery process than Tier 1. You're building a custom AI, not deploying templates.

**Intake process:**

1. **Domain interview** (60-90 min) — Use the Collect persona to extract:
   - What does the expert do daily?
   - What decisions do they make repeatedly?
   - What references/documents/frameworks do they use?
   - Who are the users? How many? What roles?
   - What does "good output" look like? Get examples.

2. **Scope definition** — Define:
   - How many personas to build (usually 1-3)
   - What data/documents to ingest as reference material
   - Which AI model fits (Gemini for speed/cost, Claude for depth/nuance)
   - User count → determines account structure

3. **API account setup decision** — During intake, determine:
   - Expected usage volume (light = absorbed, heavy = additional charge)
   - Whether client creates their own Google Cloud project or FlowstateAI manages it
   - Budget threshold for usage alerts

### 4.2 Deployment Steps

**Time estimate:** 1-3 days depending on complexity

1. **Create the AI account** (30 min)
   - Set up Google Cloud project or Anthropic workspace for client
   - Generate restricted API key
   - Set billing alerts at agreed thresholds
   - Document in client credential tracker

2. **Build the persona(s)** (2-8 hours)
   - Use the existing persona template: `.agent/references/rule_template.md`
   - Write the persona rule file based on intake data
   - Include: identity, session behavior, domain expertise, output format, boundaries
   - Test extensively before delivery

3. **Deploy the persona** — Two deployment options:

   **Option A: Embedded in n8n (chatbot/API)**
   - Create an n8n workflow with AI Agent node
   - Load persona prompt as system message
   - Expose via webhook or chat widget
   - Each user authenticates via the n8n form or a frontend auth layer

   **Option B: Deployed as an OS workspace (for power users)**
   - Run `/deploy-os -TargetName "clientname"`
   - Strip all personas except the ones built for this client
   - Inject client API key into `.env`
   - Each user gets their own workspace copy with their own credentials

4. **User provisioning** (per user, 15 min each)
   - Create username/password for n8n access (Option A) or workspace credentials (Option B)
   - Generate individual API keys if needed (one per user for usage tracking)
   - Send welcome email with access instructions

5. **Training session** (30-60 min)
   - Walk users through how to interact with their AI
   - Show example prompts and expected outputs
   - Set expectations on what the AI can/cannot do

### 4.3 Ongoing Management

- Monthly: Review API usage per client (Google Cloud Console / Anthropic dashboard)
- Monthly: Check if usage exceeds absorbed threshold → invoice if needed
- As needed: Build additional personas (billable retainer work)
- Quarterly: Performance review — is the AI producing good output? Refine prompts if not.

---

## 5. Tier 3: Domination (Full OS) Deployment

### 5.1 Pre-Deployment

This is the premium offering. The client gets a full AI Operating System — the same architecture FlowstateAI runs internally, customized for their business.

**Intake process** (more extensive than Tier 2):

1. **Business deep-dive** (2-3 hours across multiple sessions)
   - Business model, revenue streams, team structure
   - Current pain points, manual processes, decision bottlenecks
   - Brand voice, values, communication style
   - Domain-specific knowledge that needs to be encoded

2. **OS design session** (60 min)
   - Which personas does this business need?
   - What axioms govern their output quality?
   - What workflows automate their processes?
   - Who are the 1-2 users and what are their roles?

3. **Account setup**
   - Client creates their own Gemini + Claude accounts
   - API keys provided to FlowstateAI for `.env` configuration
   - GitHub: FlowstateAI creates a private repo — client gets NO access

### 5.2 Deployment Steps

**Time estimate:** 1-2 weeks for full customization

1. **Clone the OS** (5 min)
   ```powershell
   .\deploy-os.ps1 -TargetName "clientname"
   ```

2. **Customize mission.md** (1-2 hours)
   - Rewrite primary directives for client's business
   - Define goals, agent fleet composition, chain of custody
   - Remove FlowstateAI-specific content

3. **Customize personas** (4-16 hours depending on count)
   - Remove personas the client doesn't need (prune from `.agent/rules/`)
   - Build custom personas based on intake data
   - Update `.agent/router.yaml` to reflect the client's persona fleet
   - Update `.agent/dispatcher.md` routing table

4. **Customize axioms** (2-4 hours)
   - Keep core OS axioms (OS.0-OS.6) — these are universal quality controls
   - Add client-specific domain axioms in `content-system/axioms/`
   - Remove FlowstateAI-specific axioms

5. **Configure environment** (30 min)
   - Inject client's API keys into `.env`
   - Set up Cloudflare project if client needs web deployment
   - Configure any client-specific integrations

6. **Register the deployment** (5 min)
   - Add to `deployments.yaml` for future update syncing
   - Create private GitHub repo in FlowstateAI-Clients org
   - Push initial commit

7. **Lockdown** (30 min) — See Section 6

8. **Training & handoff** (2-3 hours)
   - Walk the 1-2 users through their OS
   - Show persona activation, workflow execution
   - Set expectations: "To add new capabilities, contact FlowstateAI"

### 5.3 Ongoing Management

- `/push-os-updates` pushes core improvements to all Tier 3 clients automatically
- Client requests for new personas/axioms/workflows = billable retainer work
- Monthly: API usage review
- Quarterly: OS health check — are they using it? What's working? What needs tuning?

---

## 6. Lockdown & IP Protection

### 6.1 The Problem

The AI OS's value IS the prompt engineering — the persona rules, axioms, dispatcher logic, and workflow definitions. These are plain markdown files. If a client can read the filesystem, they can read (and copy) everything.

### 6.2 The Solution: Layered Defense

**Layer 1: Access Architecture (Primary Defense)**

- Clients NEVER get GitHub access to their OS repo
- The OS repo lives in FlowstateAI's private GitHub org
- Only FlowstateAI team members can clone, read, or modify the source
- Client interaction is exclusively through the AI interface (VS Code + Antigravity or web chat)

**Layer 2: Workspace Separation**

```
Client's OS directory (on their machine or FlowstateAI-managed machine):
├── .agent/           ← EXISTS locally (AI needs it) but client shouldn't browse it
├── .gemini/          ← EXISTS locally but client shouldn't browse it
├── .vscode/
│   └── settings.json ← Configured to HIDE .agent/ and .gemini/ from file explorer
├── work_in_progress/ ← This is what the client sees and uses
└── ...
```

VS Code `settings.json` to hide protected directories:
```json
{
  "files.exclude": {
    ".agent": true,
    ".gemini": true,
    "content-system": true,
    ".env": true,
    ".git": true,
    "*.ps1": true,
    "*.py": true
  }
}
```

> **Important:** This is friction, not security. A technical client could unhide these. That's what Layer 3 is for.

**Layer 3: Contractual Protection (Legal Backstop)**

Every Tier 2 and Tier 3 client signs:
- **NDA** covering all AI OS internals (persona definitions, axioms, dispatcher logic)
- **License agreement** stating: the OS is licensed, not sold. Client has usage rights only. Reverse-engineering, copying, or distributing the prompt architecture is prohibited.
- **IP assignment clause**: any personas, axioms, or workflows built by FlowstateAI remain FlowstateAI IP, licensed to the client for the duration of the retainer

**Layer 4: Future Architecture (Roadmap)**

The long-term solution is the **MCP Fileclerk server-side architecture** from `mission.md`:
- Persona prompts live on FlowstateAI's server, not the client's machine
- Client's AI connects to FlowstateAI's MCP server to retrieve instructions
- "Their tokens, our data" — client pays for AI compute, FlowstateAI owns the intelligence layer
- This makes IP theft technically impossible, not just contractually prohibited

### 6.3 Client GitHub Sync (Work Output Only)

If a client wants version history of their work:
1. Create a SEPARATE repo in the client's own GitHub account
2. This repo syncs ONLY `work_in_progress/` contents
3. Add a `.gitignore` at the workspace root that excludes everything except `work_in_progress/`
4. The client sees their deliverables, notes, and project files — never the OS internals

```gitignore
# Client-facing .gitignore — sync work output only
*
!work_in_progress/
!work_in_progress/**
!.gitignore
```

---

## 7. The Retainer Engine

### 7.1 Why the Locked OS Creates Recurring Revenue

The OS is deliberately designed so that the client **cannot** add or modify capabilities themselves. This is not a limitation — it's the business model.

```
Client uses OS daily → discovers new needs
    ↓
"I wish the AI could also do X" / "Can we add a persona for Y?"
    ↓
Client contacts FlowstateAI → scoping call (15 min)
    ↓
FlowstateAI builds the new persona/axiom/workflow
    ↓
Pushes update via /push-os-updates
    ↓
Client gets more value → more dependent on the OS → retainer justified
    ↓
Repeat
```

### 7.2 Billable Activities by Tier

| Activity | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| New automation workflow | ✅ Billable | ✅ Billable | ✅ Billable |
| New AI persona | N/A | ✅ Billable | ✅ Billable |
| New axiom/rule set | N/A | N/A | ✅ Billable |
| New workflow integration | ✅ Billable | ✅ Billable | ✅ Billable |
| Persona tuning/refinement | N/A | ✅ Included in retainer (minor) | ✅ Included in retainer (minor) |
| Token/credential refresh | ✅ Included | ✅ Included | ✅ Included |
| OS core updates | N/A | N/A | ✅ Included (via /push-os-updates) |
| Custom training sessions | ✅ Billable | ✅ Billable | ✅ Billable |

### 7.3 Upsell Paths

- **Tier 1 → Tier 2:** "Your automations are saving you 10 hours/week. What if your team had an AI that could also handle [domain task]?"
- **Tier 2 → Tier 3:** "Your AI persona is working great. What if your entire business ran on a system like this?"
- **Within Tier 3:** Every new persona, axiom, or integration is an expansion opportunity

---

## 8. New Employee Onboarding

### 8.1 Required Reading (In Order)

| # | Document | What It Teaches |
|---|----------|-----------------|
| 1 | This document (you're reading it) | The business model and how everything fits together |
| 2 | `mission.md` | The OS philosophy, agent fleet, and long-term vision |
| 3 | `.agent/rules/core_axioms.md` | The quality standards every output must meet |
| 4 | `sops/README.md` | The full SOP library index |
| 5 | `sops/n8n_workflow_audit.md` | Every automation we have, what it does, what it needs |
| 6 | `.agent/workflows/deploy-os.md` | How to deploy a new OS instance |
| 7 | `.agent/workflows/push-os-updates.md` | How to push updates to all clients |

### 8.2 Shadowing Checklist

Before deploying solo, a new team member must shadow (observe, then execute with supervision):

- [ ] Deploy a Tier 1 automation for a live client
- [ ] Build a test persona using `rule_template.md`
- [ ] Run `/deploy-os` to create a test workspace
- [ ] Run `/push-os-updates` to sync changes
- [ ] Complete a client onboarding call
- [ ] Handle a credential rotation (Facebook token, LinkedIn token)

### 8.3 Tools You Need Access To

| Tool | Purpose | Access Level |
|---|---|---|
| VS Code + Gemini/Antigravity | Building and operating the OS | Full |
| VPS (SSH access) | Managing n8n instances | Full |
| Cloudflare Dashboard | DNS, Tunnels, Pages | Full |
| GitHub (FlowstateAI-Clients org) | Code management | Admin |
| Google Cloud Console | API keys, billing monitoring | Admin |
| Anthropic Dashboard | Claude API keys, usage | Admin |
| Client Pipeline Tracker (Google Sheet) | Client status, billing | Edit |

---

## 9. Credential & Token Management

### 9.1 Per-Client Credential Tracker

Every client gets a `credentials.md` file in their workspace (`work_in_progress/clients/[name]/credentials.md` or a secure vault). Track:

```markdown
# Client: [Name]
## API Keys
- Gemini API Key: [stored in .env as GEMINI_API_KEY]
- Claude API Key: [stored in .env as ANTHROPIC_API_KEY]
- Created: [date]
- Billing: [client's Google Cloud project / Anthropic workspace]

## N8N Instance
- URL: https://clientname-n8n.flowstateai.com
- Admin user: [username]
- Port: [assigned port on VPS]

## Social Tokens (if Tier 1)
- Facebook Page Token: expires [date] — refresh via Meta Business Suite
- LinkedIn Token: expires [date] — refresh via OAuth flow
- Gmail OAuth: rolling — re-auth if revoked

## Refresh Schedule
- [ ] Monthly: Check API usage vs. threshold
- [ ] Quarterly: Rotate any expiring tokens
- [ ] Annually: Review billing structure
```

### 9.2 Critical Deadlines

| Item | Deadline | Impact |
|---|---|---|
| Google API Key migration (Standard → Auth keys) | **September 2026** | All standard API keys stop working. Migrate to service-account-bound Auth keys before this date. |
| LinkedIn OAuth tokens | Every 60 days | Auto-posting stops if not refreshed |
| Facebook/Meta tokens | Varies | Check Meta Business Suite monthly |

### 9.3 🚨 API Key Migration Task (Standard → Auth Keys)

**Deadline: September 2026 — Standard Gemini API keys stop working.**

**What to migrate:**
- [ ] FlowstateAI internal n8n workflows (Facebook poster, LinkedIn poster — `AIzaSy...` keys)
- [ ] FlowstateAI `.env` (master OS workspace)
- [ ] Crypton trading bot (VPS)
- [ ] Every deployed client `.env` that uses a Standard Gemini key
- [ ] Any future deployments — use Auth keys from day one

**Migration steps per key:**
1. Google Cloud Console → Select project
2. Create Service Account (e.g., `clientname-gemini@project.iam.gserviceaccount.com`)
3. Grant `Vertex AI User` role
4. Generate Auth key for the Service Account
5. Replace old `AIzaSy...` key with new Auth key in `.env` / n8n credentials
6. Test all workflows that use the key
7. Delete the old Standard key

**Weekly Reminder Schedule:**

| Week | Date | Action |
|---|---|---|
| Week 1 | **August 1, 2026** | Start migration. Migrate FlowstateAI internal keys first (n8n + master OS + Crypton). |
| Week 2 | August 8, 2026 | Verify internal migration is stable. Begin migrating client deployments. |
| Week 3 | August 15, 2026 | Continue client migrations. Test all migrated workflows. |
| Week 4 | August 22, 2026 | Complete all remaining client migrations. Final testing. |
| Week 5 | **August 29, 2026** | **Final check.** Audit every deployment — confirm zero Standard keys remain. Delete all old keys. |
| Deadline | **September 2026** | Standard keys stop working. If you followed this schedule, you're safe. |

> ⚠️ **Set these as calendar reminders NOW.** This SOP cannot send you notifications — add each date above to Google Calendar or your phone with the action item as the description.

---

### 9.4 Security Rules

1. **Never commit API keys to GitHub.** All keys live in `.env` files which are `.gitignore`d.
2. **Never share credentials via email or chat.** Use a secure vault or encrypted document.
3. **One key per client, per service.** Never reuse keys across clients.
4. **Revoke immediately** when a client churns — remove their API keys, shut down their n8n instance, archive their workspace.

---

## Appendix A: Quick Reference Commands

```powershell
# Deploy new OS instance for a client
.\deploy-os.ps1 -TargetName "clientname"

# Deploy with a specific project included
.\deploy-os.ps1 -TargetName "clientname" -IncludeWip "projectname"

# Push OS updates to ALL clients
.\push-os-updates.ps1

# Push OS update to ONE client
.\push-os-updates.ps1 -TargetName "clientname"

# Dry run (see what would sync)
.\push-os-updates.ps1 -DryRun

# Start n8n + Cloudflare tunnel
.\start-n8n.ps1
```

## Appendix B: File Map — What's Protected vs. Open

| Path | Status | Notes |
|---|---|---|
| `.agent/rules/` | 🔒 PROTECTED | Persona definitions — the core IP |
| `.agent/workflows/` | 🔒 PROTECTED | Operational workflows |
| `.agent/dispatcher.md` | 🔒 PROTECTED | Routing logic |
| `.agent/router.yaml` | 🔒 PROTECTED | Persona-to-model mapping |
| `.gemini/` | 🔒 PROTECTED | System prompt config |
| `content-system/axioms/` | 🔒 PROTECTED | Quality control rules |
| `mission.md` | 🔒 PROTECTED | OS identity |
| `.env` | 🔑 CLIENT-SPECIFIC | Their API keys — never synced |
| `work_in_progress/` | ✅ OPEN | Client's actual work — the only thing they interact with |

---

*FlowstateAI — 3-Tier Scalability SOP*
*Confidential — Internal Use Only*
