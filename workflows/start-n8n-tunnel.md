---
description: Start the Cloudflare Tunnel for n8n webhooks
---
// turbo-all

# Start n8n Tunnel Workflow

> **Who runs this?** The AI. Triggered via `/start-n8n-tunnel` or when user asks to expose n8n to public webhooks.

## 1. Check for Running Processes
Stop any existing cloudflared tunnels to prevent port conflicts:

```powershell
Step 1: Stop existing cloudflared
$ Stop-Process -Name cloudflared -Force -ErrorAction SilentlyContinue
```

## 2. Start Cloudflare Quick Tunnel
Run the Cloudflare tunnel binary pointing to the local n8n port (5678):

```powershell
Step 2: Start tunnel
$ C:\Users\Admin\tools\cloudflared\cloudflared.exe tunnel --url http://localhost:5678 > C:\Users\Admin\tools\cloudflared\tunnel.log 2>&1
```

## 3. Retrieve Production URL
Wait a few seconds for the tunnel to establish, then extract the URL from the log file:

```powershell
Step 3: Get URL
$ Start-Sleep -Seconds 5; Select-String -Path C:\Users\Admin\tools\cloudflared\tunnel.log -Pattern "https://.*\.trycloudflare\.com"
```

## 4. Report to User
Provide the generated `trycloudflare.com` URL to the user so they can update their webhook configurations.
