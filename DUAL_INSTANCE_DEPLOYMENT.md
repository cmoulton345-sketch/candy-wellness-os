# Dual-Instance Deployment Guide
## Local + VPS Setup for Radical Simplicity AI OS

---

## 📋 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Central GitHub Repository                   │
│        https://github.com/joemoulton2022-create/...             │
│                      (Source of Truth)                           │
└─────────────────────────────────────────────────────────────────┘
                    ↓                           ↓
        ┌─────────────────────┐      ┌──────────────────────┐
        │  LOCAL INSTANCE     │      │   VPS INSTANCE       │
        │  (Your PC)          │      │  (Remote Server)     │
        ├─────────────────────┤      ├──────────────────────┤
        │ Windows Desktop     │      │ Linux Server         │
        │ Voice Enabled       │      │ Headless (24/7)      │
        │ Interactive Mode    │      │ Background Daemon    │
        │ .env.local          │      │ .env.vps             │
        │ SAPI TTS            │      │ n8n Webhooks         │
        │ Crypto Local        │      │ Cron Jobs            │
        │ n8n (port 5678)     │      │ PM2 Services         │
        └─────────────────────┘      └──────────────────────┘
        git pull/push              git pull/push
        git add/commit             git add/commit
                │                           │
                └───────────────┬───────────┘
                                ↓
                   Git Auto-Sync (git-sync.md)
                   Every 5-10 mins pull
                   On save: commit + push
```

---

## 🚀 PHASE 1: LOCAL INSTANCE SETUP (Your PC)

### 1a. Clone Repo to Local Directory

```powershell
# Create a local working folder
mkdir c:\Users\Joe\my-ai-os-local
cd c:\Users\Joe\my-ai-os-local

# Clone from your central repo
git clone https://github.com/joemoulton2022-create/My-personal-AI-OS-backup.git .
git branch -a  # Verify you're on 'main'
```

### 1b. Create `.env` for Local Instance

```powershell
# Copy the example and customize
Copy-Item .env.local.example .env

# Edit .env with your local paths
notepad .env
```

**Key settings for LOCAL:**
```
MODE=LOCAL
VOICE_ENABLED=true
OS_ROOT=c:\Users\Joe\my-ai-os-local
N8N_PORT=5678
OPEN_WEBUI_PORT=3000
CRYPTO_PAPER_TRADE=true
TELEGRAM_BOT_ENABLED=false
```

### 1c. Test Startup

```powershell
# Verify n8n is running
npm run start:n8n

# Verify voice listening
python listen.py

# Verify crypto bot
python crypto/orchestrator.py
```

### 1d. Enable Git Auto-Sync on Local

Create a Windows Task Scheduler job to run git-sync every 5 minutes:

```powershell
# Create sync script
$SyncScript = @'
cd c:\Users\Joe\my-ai-os-local
git pull --rebase origin main
'@

$SyncScript | Out-File -Encoding UTF8 "c:\Users\Joe\my-ai-os-local\git-sync.ps1"

# Schedule it every 5 minutes
$Action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File c:\Users\Joe\my-ai-os-local\git-sync.ps1"
$Trigger = New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 365)
$Principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -RunLevel Highest
Register-ScheduledTask -TaskName "AI-OS-Git-Sync" -Action $Action -Trigger $Trigger -Principal $Principal
```

---

## 🌐 PHASE 2: VPS INSTANCE SETUP (Remote Server)

### 2a. SSH into VPS

```bash
ssh root@your_vps_ip_address
```

### 2b. Clone Repo to VPS

```bash
# Create a VPS working folder
mkdir -p /root/my-ai-os-vps
cd /root/my-ai-os-vps

# Clone from your central repo
git clone https://github.com/joemoulton2022-create/My-personal-AI-OS-backup.git .
git branch -a
```

### 2c. Create `.env` for VPS Instance

```bash
# Copy the example and customize
cp .env.vps.example .env

# Edit with your VPS credentials
nano .env
```

**Key settings for VPS:**
```
MODE=VPS
VOICE_ENABLED=false
HEADLESS=true
OS_ROOT=/root/my-ai-os-vps
CRYPTO_API_KEY=your_real_key
CRYPTO_SECRET_KEY=your_real_secret
TELEGRAM_BOT_ENABLED=true
TELEGRAM_BOT_TOKEN=your_telegram_token
PM2_ENABLED=true
```

### 2d. Install Dependencies

```bash
# Install Node.js and npm
curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Python 3
sudo apt install -y python3 python3-pip

# Install PM2 (process manager for 24/7 uptime)
npm install -g pm2

# Install project dependencies
npm install
pip3 install -r requirements.txt
```

### 2e. Start Services with PM2

```bash
# Start n8n daemon
pm2 start "npm run start:n8n" --name "n8n-daemon"

# Start crypto bot daemon
pm2 start "python3 crypto/orchestrator.py" --name "crypto-bot"

# Start webhook listener
pm2 start "python3 listen.py" --name "webhook-listener"

# Save and enable auto-restart on reboot
pm2 save
pm2 startup
```

### 2f. Enable Git Auto-Sync on VPS

```bash
# Create cron job for git sync every 10 minutes
crontab -e

# Add this line:
*/10 * * * * cd /root/my-ai-os-vps && git pull --rebase origin main >> /var/log/ai-os-sync.log 2>&1
```

---

## 🔄 PHASE 3: SYNC DISCIPLINE

### Local → VPS Sync Workflow

**When you make changes on Local:**

1. **Edit files** in your Local instance (Windows)
2. **Test locally** (voice commands, crypto bot, n8n workflows)
3. **Save/Commit**: `git add -A` → `git commit -m "..."`
4. **Push**: `git push origin main`
5. **VPS auto-pulls** (within 10 minutes via cron)

**Example:**
```powershell
# On Local (Windows)
cd c:\Users\Joe\my-ai-os-local

# Update an agent rule
notepad .agent\rules\jarvis.md

# Save and sync
git add .agent\rules\jarvis.md
git commit -m "feat: update jarvis voice priority routing"
git push origin main

# VPS picks it up automatically in 10 mins
# Check VPS status:
ssh root@your_vps_ip "cd /root/my-ai-os-vps && git log --oneline -5"
```

### Prevent Conflicts

**Local and VPS should NEVER both edit the same file at the same time.**

**Safe Division of Labor:**

| Local Edits | VPS Edits (or Shared) |
|---|---|
| `.agent/rules/` (agent logic) | `.env.vps` (VPS config) |
| `.agent/dispatcher.md` | n8n workflows (versioned) |
| `listen.py` (voice) | `crypto/logs/` |
| `speak.py` (SAPI) | `memory/` (shared journal) |
| | |

**If conflict occurs:**
```bash
# On VPS, manually resolve
cd /root/my-ai-os-vps
git status  # See conflicts
# Edit conflicted files manually
git add <resolved_files>
git commit -m "fix: merge conflict from local"
```

---

## ✅ VERIFICATION CHECKLIST

### Local Instance (Windows)
- [ ] Clone exists at `c:\Users\Joe\my-ai-os-local`
- [ ] `.env` is populated (git-ignored, not in repo)
- [ ] `listen.py` can start without errors
- [ ] `npm run start:n8n` launches Open WebUI
- [ ] Voice command triggers work
- [ ] Task Scheduler job runs git-sync every 5 min
- [ ] `git log` shows recent commits

### VPS Instance (Linux)
- [ ] Clone exists at `/root/my-ai-os-vps`
- [ ] `.env` is populated (git-ignored, not in repo)
- [ ] `pm2 list` shows n8n, crypto-bot, webhook-listener running
- [ ] Cron job added for git sync every 10 min
- [ ] Telegram bot responds to commands
- [ ] `crypto/orchestrator.py` is live trading (or paper)
- [ ] `git log` matches Local (both on same commit)

### Shared
- [ ] `.gitignore` excludes `.env`, `.env.local`, `.env.vps`
- [ ] Central GitHub repo receives both pushes
- [ ] Both instances pull latest changes without conflicts
- [ ] No sensitive keys in committed files

---

## 🛠️ Troubleshooting

### Local instance has uncommitted changes before VPS pull

```powershell
git stash
git pull --rebase origin main
git stash pop  # Re-apply your local work
```

### VPS is out of sync with Local

```bash
# On VPS
cd /root/my-ai-os-vps
git fetch origin
git log origin/main -5  # See what's missing
git pull --rebase origin main
```

### Crypto bot not trading on VPS

```bash
# Check PM2 logs
pm2 logs crypto-bot

# Verify API keys in .env.vps
cat .env | grep CRYPTO
```

### Git auto-sync not running

**Local (Windows):**
```powershell
Get-ScheduledTask -TaskName "AI-OS-Git-Sync" | Select-Object State
# Should show "Running"
```

**VPS (Linux):**
```bash
crontab -l | grep git
tail -f /var/log/ai-os-sync.log
```

---

## 📞 Quick Commands Reference

| Task | Local (Windows) | VPS (Linux) |
|---|---|---|
| **Pull updates** | `git pull origin main` | `git pull origin main` |
| **Save changes** | `git add -A && git commit -m "..."` | (auto via cron) |
| **Push to GitHub** | `git push origin main` | (auto via cron) |
| **Check status** | `git status` | `git status` |
| **View logs** | Crypto: `crypto/logs/` | `pm2 logs` |
| **Restart n8n** | `npm run restart:n8n` | `pm2 restart n8n-daemon` |
| **Stop all** | Ctrl+C or Task Manager | `pm2 stop all` |

---

## 🎯 Next Steps

1. **Set up Local instance** (PHASE 1) — Test everything locally first
2. **Provision VPS** (PHASE 2) — Rent a Linux server ($5-20/month is fine)
3. **Deploy VPS instance** (PHASE 2) — Clone and run
4. **Enable auto-sync** (PHASE 3) — Git push/pull on schedule
5. **Monitor both** — Check logs weekly, ensure sync is working

Once both are running, you have **24/7 operations (VPS) + interactive control (Local)**.

---

## 📧 Support

Questions? Check:
- `.agent/workflows/git-sync.md` — Git workflow details
- `.env.example`, `.env.local.example`, `.env.vps.example` — Config reference
- `README.md` — Project overview
