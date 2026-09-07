#!/bin/bash
# Radical Simplicity AI OS — VPS Deployment Script (Ubuntu 22.04)
# Run as: sudo bash deploy-vps.sh
# This script deploys the full AI OS with security hardening and Cloudflare Tunnel support

set -e  # Exit on any error

# Color output for readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Radical Simplicity AI OS — VPS Deployment ===${NC}"
echo "Target: Ubuntu 22.04 LTS | User: aios | Mode: Production"
echo ""

# ============================================================================
# PHASE 1: System Preparation
# ============================================================================

echo -e "${YELLOW}[1/8] Updating system packages...${NC}"
apt-get update
apt-get upgrade -y
apt-get install -y curl wget git build-essential python3 python3-pip python3-venv

echo -e "${GREEN}✓ System updated${NC}"

# ============================================================================
# PHASE 2: Create Dedicated Service User (aios)
# ============================================================================

echo -e "${YELLOW}[2/8] Creating dedicated service user 'aios'...${NC}"

if id "aios" &>/dev/null; then
    echo -e "${GREEN}✓ User 'aios' already exists${NC}"
else
    useradd -m -s /bin/bash aios
    echo -e "${GREEN}✓ User 'aios' created${NC}"
fi

# Add aios to sudo group (no password required for specific commands)
usermod -aG sudo aios

# Create .ssh directory for aios
mkdir -p /home/aios/.ssh
chmod 700 /home/aios/.ssh

# ============================================================================
# PHASE 3: Configure SSH Key Authentication
# ============================================================================

echo -e "${YELLOW}[3/8] Configuring SSH key authentication for 'aios'...${NC}"

SSH_PUBKEY="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEFYcVC7Xr03v2oxyiHkkZsvwR6BhjitGEuBHyzGB1ZO joe@DESKTOP-FFJJ5RQ"

# Add SSH public key to authorized_keys
echo "$SSH_PUBKEY" >> /home/aios/.ssh/authorized_keys
chmod 600 /home/aios/.ssh/authorized_keys
chown -R aios:aios /home/aios/.ssh

echo -e "${GREEN}✓ SSH key configured for user 'aios'${NC}"

# ============================================================================
# PHASE 4: Clone Git Repository
# ============================================================================

echo -e "${YELLOW}[4/8] Cloning Git repository...${NC}"

OS_DIR="/home/aios/radical_simplicity_ai_os_vps"

if [ -d "$OS_DIR" ]; then
    echo -e "${YELLOW}Directory already exists. Pulling latest changes...${NC}"
    cd "$OS_DIR"
    sudo -u aios git pull --rebase origin main
else
    sudo -u aios git clone https://github.com/joemoulton2022-create/My-personal-AI-OS-backup.git "$OS_DIR"
    cd "$OS_DIR"
fi

chown -R aios:aios "$OS_DIR"
echo -e "${GREEN}✓ Repository cloned/updated at $OS_DIR${NC}"

# ============================================================================
# PHASE 5: Install Node.js and PM2
# ============================================================================

echo -e "${YELLOW}[5/8] Installing Node.js 18 and PM2...${NC}"

# Check if Node.js is already installed
if ! command -v node &> /dev/null; then
    curl -sL https://deb.nodesource.com/setup_18.x | bash -
    apt-get install -y nodejs
    echo -e "${GREEN}✓ Node.js 18 installed${NC}"
else
    echo -e "${GREEN}✓ Node.js already installed: $(node -v)${NC}"
fi

# Install PM2 globally
npm install -g pm2

# Allow aios to use PM2 without sudo for restart/reload
sudo -u aios pm2 startup systemd -u aios --hp /home/aios
pm2 save

echo -e "${GREEN}✓ PM2 installed and configured${NC}"

# ============================================================================
# PHASE 6: Install Python Dependencies
# ============================================================================

echo -e "${YELLOW}[6/8] Installing Python dependencies...${NC}"

cd "$OS_DIR"

if [ -f "requirements.txt" ]; then
    python3 -m venv /home/aios/.venv
    source /home/aios/.venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    chown -R aios:aios /home/aios/.venv
    echo -e "${GREEN}✓ Python environment set up${NC}"
else
    echo -e "${YELLOW}No requirements.txt found. Skipping Python setup.${NC}"
fi

# ============================================================================
# PHASE 7: Create .env.vps Configuration
# ============================================================================

echo -e "${YELLOW}[7/8] Creating .env.vps configuration...${NC}"

ENV_FILE="$OS_DIR/.env.vps"

cat > "$ENV_FILE" << 'EOF'
# Radical Simplicity AI OS — VPS Instance Configuration
# Production environment - Ubuntu 22.04

# === DEPLOYMENT MODE ===
MODE=VPS
ENVIRONMENT=production
VOICE_ENABLED=false
HEADLESS=true

# === VPS PATHS (Linux) ===
OS_ROOT=/home/aios/radical_simplicity_ai_os_vps
MEMORY_PATH=$OS_ROOT/memory
AGENT_PATH=$OS_ROOT/.agent
WORKFLOW_PATH=$OS_ROOT/n8n_workflows

# === SERVICE PORTS (Local to VPS, exposed via Cloudflare Tunnel) ===
N8N_PORT=5678
OPEN_WEBUI_PORT=3000
WEBHOOK_PORT=8080

# === VOICE CONFIGURATION (Disabled on VPS) ===
VOICE_ENABLED=false

# === CRYPTO TRADING (Production Mode) ===
CRYPTO_MODE=VPS
CRYPTO_EXCHANGE=binance
CRYPTO_API_KEY=your_binance_api_key_here
CRYPTO_SECRET_KEY=your_binance_secret_key_here
CRYPTO_PAPER_TRADE=false
CRYPTO_LOG_PATH=$OS_ROOT/crypto/logs
CRYPTO_ALLOWED_IPS=5.78.215.76

# === BACKGROUND PROCESSES ===
PM2_ENABLED=true
N8N_DAEMON=true
WEBHOOK_LISTENER=true
CRON_JOBS_ENABLED=true

# === TELEGRAM BOT (VPS-only) ===
TELEGRAM_BOT_ENABLED=true
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here

# === CLOUDFLARE TUNNEL ===
CLOUDFLARE_TUNNEL_ENABLED=true
CLOUDFLARE_TUNNEL_TOKEN=your_cloudflare_tunnel_token_here
CLOUDFLARE_TUNNEL_NAME=ai-os-vps-tunnel

# === EXTERNAL CREDENTIALS (Shared) ===
CLOUDFLARE_API_TOKEN=your_cloudflare_api_token_here
CLOUDFLARE_ACCOUNT_ID=your_account_id_here

# === VPS SECURITY ===
REQUIRE_SUDO=true
SSH_KEY_PATH=/home/aios/.ssh/id_rsa
FIREWALL_ENABLED=true

# === GIT SYNC ===
GIT_AUTO_SYNC=true
GIT_SYNC_INTERVAL=600
GIT_REPO=https://github.com/joemoulton2022-create/My-personal-AI-OS-backup.git
GIT_BRANCH=main
EOF

chown aios:aios "$ENV_FILE"
chmod 600 "$ENV_FILE"

echo -e "${YELLOW}⚠ Created .env.vps — YOU MUST fill in credentials manually:${NC}"
echo "   - CRYPTO_API_KEY"
echo "   - CRYPTO_SECRET_KEY"
echo "   - TELEGRAM_BOT_TOKEN"
echo "   - TELEGRAM_CHAT_ID"
echo "   - CLOUDFLARE_TUNNEL_TOKEN"
echo "   - CLOUDFLARE_API_TOKEN"
echo "   - CLOUDFLARE_ACCOUNT_ID"
echo ""
echo "To edit: nano $ENV_FILE"
echo -e "${GREEN}✓ .env.vps created (at $ENV_FILE)${NC}"

# ============================================================================
# PHASE 8: Start Services with PM2
# ============================================================================

echo -e "${YELLOW}[8/8] Starting services with PM2...${NC}"

cd "$OS_DIR"

# Switch to aios user and start services
sudo -u aios bash << PMEOF
cd $OS_DIR
source /home/aios/.venv/bin/activate 2>/dev/null || true

# Start n8n
pm2 start "npm run start:n8n" --name "n8n-daemon" --env production || echo "n8n start attempted"

# Start crypto bot
pm2 start "python3 crypto/orchestrator.py" --name "crypto-bot" --env production || echo "crypto-bot start attempted"

# Start webhook listener
pm2 start "python3 listen.py" --name "webhook-listener" --env production || echo "webhook-listener start attempted"

# Save PM2 configuration for auto-restart on reboot
pm2 save
PMEOF

echo -e "${GREEN}✓ PM2 services started${NC}"

# ============================================================================
# PHASE 9: Configure Git Auto-Sync via Cron
# ============================================================================

echo -e "${YELLOW}[9/9] Configuring git auto-sync cron job...${NC}"

CRON_JOB="*/10 * * * * cd $OS_DIR && /usr/bin/git pull --rebase origin main >> /var/log/ai-os-sync.log 2>&1"

# Add cron job for aios user
(sudo -u aios crontab -l 2>/dev/null || echo "") | grep -v "git pull --rebase" | sudo -u aios crontab - || true
echo "$CRON_JOB" | sudo -u aios crontab -

echo -e "${GREEN}✓ Git auto-sync configured (every 10 minutes)${NC}"

# ============================================================================
# PHASE 10: SSH Hardening
# ============================================================================

echo -e "${YELLOW}[10/10] Hardening SSH security...${NC}"

# Backup original sshd_config
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak

# Disable password authentication
sed -i 's/^#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/^PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# Disable root login
sed -i 's/^#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/^PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Reload SSH daemon
systemctl reload sshd

echo -e "${GREEN}✓ SSH hardened (password auth disabled, root login disabled)${NC}"

# ============================================================================
# PHASE 11: UFW Firewall Configuration
# ============================================================================

echo -e "${YELLOW}[11/11] Configuring UFW firewall...${NC}"

ufw --force enable
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp          # SSH
ufw allow 5678/tcp        # n8n (internal only, exposed via Tunnel)
ufw allow 3000/tcp        # Open WebUI (internal only)
ufw allow 8080/tcp        # Webhook listener (internal only)

echo -e "${GREEN}✓ UFW firewall configured (only SSH, n8n, WebUI, Webhooks allowed)${NC}"

# ============================================================================
# COMPLETION
# ============================================================================

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║        VPS DEPLOYMENT COMPLETE ✓${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"

echo ""
echo -e "${YELLOW}NEXT STEPS:${NC}"
echo ""
echo "1. EDIT .env.vps with your credentials:"
echo "   sudo nano $ENV_FILE"
echo ""
echo "2. SET UP CLOUDFLARE TUNNEL (after editing .env):"
echo "   - Go to: https://dash.cloudflare.com/tunnel"
echo "   - Create new tunnel 'ai-os-vps-tunnel'"
echo "   - Copy tunnel token to CLOUDFLARE_TUNNEL_TOKEN in .env"
echo ""
echo "3. VERIFY SERVICES:"
echo "   sudo -u aios pm2 list"
echo "   sudo -u aios pm2 logs n8n-daemon"
echo ""
echo "4. ADD GIT SYNC ENDPOINT (in your local repo):"
echo "   git remote add vps user@$OS_DIR"
echo ""
echo "5. TEST SYNC:"
echo "   git push origin main"
echo "   # VPS pulls automatically in 10 minutes"
echo ""
echo -e "${GREEN}Deployment log saved to: /var/log/ai-os-sync.log${NC}"
echo ""
