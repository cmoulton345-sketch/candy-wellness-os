# FlowstateAI OS — Daily Briefing v2 Setup Guide

## Architecture Overview

```
GitHub (Private Repo)          n8n (VPS - Docker)           Telegram
┌──────────────────┐          ┌──────────────────┐         ┌──────────┐
│ client_pipeline  │◄─── GET ─┤ CRON Triggers    │         │          │
│ current_state    │◄─── GET ─┤ Fetch 3 Files    │──POST──►│ Joe's    │
│ MASTER_TODO      │◄─── GET ─┤ Compose Briefing │         │ Phone    │
└──────────────────┘          └──────────────────┘         └──────────┘
    (Your OS files              (Runs 24/7 on VPS,           (Chat ID:
     synced via git)             no PC needed)              8877601731)
```

**Key difference from v1:** n8n pulls your OS files directly from GitHub via API. 
Your PC can be off. Antigravity can be closed. It just works.

---

## Setup Steps

### Step 1: Create a GitHub Personal Access Token (PAT)

1. Go to: https://github.com/settings/tokens?type=beta
2. Click **"Generate new token"** (Fine-grained)
3. Settings:
   - **Token name:** `n8n-os-briefing`
   - **Expiration:** 90 days (or custom)
   - **Repository access:** Select **"Only select repositories"** → pick `My-personal-AI-OS-backup`
   - **Permissions → Repository permissions → Contents:** Read-only
4. Click **Generate token**
5. **COPY THE TOKEN** — you'll only see it once!

### Step 2: Add Credentials in n8n

1. Open n8n: https://n8n.flowstateaiautomation.ai
2. Go to **Settings → Credentials → Add Credential**
3. Search for **"Header Auth"**
4. Set:
   - **Name:** `GitHub PAT`
   - **Header Name:** `Authorization`
   - **Header Value:** `Bearer ghp_YOUR_TOKEN_HERE`
5. Save

### Step 3: Set Telegram Bot Token as Environment Variable

On your VPS, add to the n8n Docker container:

```bash
# SSH into VPS
ssh root@your-vps-ip

# Stop n8n container
docker stop $(docker ps -q --filter ancestor=n8nio/n8n)

# Restart with the env variable
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -e TELEGRAM_BOT_TOKEN=7969096831:AAG1VbgL1xgGUGz55UX6P4MZyUFqYnbxYyE \
  -e WEBHOOK_URL=https://n8n.flowstateaiautomation.ai/ \
  -e N8N_HOST=n8n.flowstateaiautomation.ai \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n
```

### Step 4: Import the Workflow

1. In n8n, click **"Add workflow"**
2. Click the **"..."** menu → **"Import from file"**
3. Upload: `daily_3x_os_briefing_automation.json`
4. In each "Fetch" node, update the credential dropdown to select your **"GitHub PAT"** credential
5. **Activate** the workflow (toggle ON)

### Step 5: Test

Click "Execute Workflow" manually to verify:
- All 3 GitHub fetches return your OS file contents
- The briefing composes correctly
- Telegram message arrives on your phone

---

## CRON Schedule (UTC → Atlantic)

| Briefing | Atlantic Time | UTC (CRON) | Purpose |
|----------|--------------|------------|---------|
| Morning Prime | 7:00 AM ADT | `0 11 * * *` | Physical prime + pipeline review |
| Midday Momentum | 12:30 PM ADT | `30 16 * * *` | Energy reset + ONE Thing audit |
| Evening Transition | 6:00 PM ADT | `0 22 * * *` | Shutdown + recovery protocol |

> **Note:** When ADT ends (Nov → AST, UTC-4), update CRONs by +1 hour.

---

## Security Notes

- Bot token is stored as a VPS environment variable, NOT in committed code
- GitHub PAT is scoped to read-only on a single private repo
- PAT expires in 90 days — set a calendar reminder to rotate
