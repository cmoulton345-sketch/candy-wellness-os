# SOP: n8n + Cloudflare Tunnel (Windows Services)
**Category:** Operations | **Version:** 2.0 | **Last Updated:** April 2026

---

## What This Does
n8n and the Cloudflare tunnel now run as **Windows services** that:
- ✅ **Auto-start on boot** — no manual action needed
- ✅ **Auto-restart on crash** — 5-second delay, then back up
- ✅ **Run in the background** — no terminal window to accidentally close
- ✅ **Survive sleep/hibernate** cycles

**Result:** n8n is always live at `http://localhost:5678` and publicly accessible at `https://n8n.flowstateaiautomation.ai`

---

## You Shouldn't Need to Do Anything

The services are set to `Automatic` start. When your computer boots, n8n and the tunnel start automatically. **No manual steps required.**

---

## If Something Goes Wrong

### Check Service Status
```powershell
Get-Service FlowstateAI-*
```

### Restart the Services
Open PowerShell **as Administrator** and run:
```powershell
Restart-Service FlowstateAI-n8n
Restart-Service FlowstateAI-Tunnel
```

### Stop the Services
```powershell
Stop-Service FlowstateAI-n8n
Stop-Service FlowstateAI-Tunnel
```

### View Logs
```powershell
# n8n output
Get-Content "C:\Users\Admin\Agents\radical_simplicity_ai_os_joe-m\services\n8n-stdout.log" -Tail 30

# n8n errors
Get-Content "C:\Users\Admin\Agents\radical_simplicity_ai_os_joe-m\services\n8n-stderr.log" -Tail 30

# Tunnel logs
Get-Content "C:\Users\Admin\Agents\radical_simplicity_ai_os_joe-m\services\tunnel-stderr.log" -Tail 30
```

### Full Reinstall (Nuclear Option)
If services get corrupted, run the installer again as Administrator:
```powershell
Start-Process powershell -Verb RunAs -ArgumentList '-ExecutionPolicy Bypass -File "C:\Users\Admin\Agents\radical_simplicity_ai_os_joe-m\services\setup-all.ps1"'
```

---

## Key Info
| Item | Value |
|---|---|
| Local URL | `http://localhost:5678` |
| Public Webhook URL | `https://n8n.flowstateaiautomation.ai` |
| n8n Service Name | `FlowstateAI-n8n` |
| Tunnel Service Name | `FlowstateAI-Tunnel` |
| Service Scripts | `services/` in workspace root |
| Log Files | `services/n8n-stdout.log`, `services/n8n-stderr.log`, `services/tunnel-*.log` |
| Service Manager | NSSM (Non-Sucking Service Manager) |

---

## Legacy: Manual Startup (No Longer Needed)
The old `start-n8n.ps1` script still works if you ever need to run n8n manually for debugging. Stop the services first, then:
```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\Admin\Agents\radical_simplicity_ai_os_joe-m\start-n8n.ps1"
```

---

*FlowstateAI Automation — Operations SOP*
