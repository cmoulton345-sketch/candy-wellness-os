$ErrorActionPreference = "Stop"

$nssm = "C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\NSSM.NSSM_Microsoft.Winget.Source_8wekyb3d8bbwe\nssm-2.24-101-g897c7ad\win64\nssm.exe"
$servicesDir = "C:\Users\Admin\Agents\radical_simplicity_ai_os_joe-m\services"

Write-Host "============================================"
Write-Host "  FlowstateAI Service Installer"
Write-Host "============================================"
Write-Host ""

# ── Service 1: n8n ──────────────────────────────────
Write-Host "[1/2] Installing n8n service..."

# Remove existing service if present
& $nssm stop FlowstateAI-n8n 2>$null
& $nssm remove FlowstateAI-n8n confirm 2>$null

& $nssm install FlowstateAI-n8n "$servicesDir\n8n-service.cmd"
& $nssm set FlowstateAI-n8n DisplayName "FlowstateAI n8n Automation Engine"
& $nssm set FlowstateAI-n8n Description "FlowstateAI n8n automation engine - auto-starts on boot, restarts on crash"
& $nssm set FlowstateAI-n8n Start SERVICE_AUTO_START
& $nssm set FlowstateAI-n8n AppStdout "$servicesDir\n8n-stdout.log"
& $nssm set FlowstateAI-n8n AppStderr "$servicesDir\n8n-stderr.log"
& $nssm set FlowstateAI-n8n AppRotateFiles 1
& $nssm set FlowstateAI-n8n AppRotateBytes 5242880
& $nssm set FlowstateAI-n8n AppRestartDelay 5000

Write-Host "[OK] n8n service installed" -ForegroundColor Green
Write-Host ""

# ── Service 2: Cloudflare Tunnel ────────────────────
Write-Host "[2/2] Installing Cloudflare Tunnel service..."

$cloudflared = "C:\Users\Admin\tools\cloudflared\cloudflared.exe"
$tunnelConfig = "C:\Users\Admin\tools\cloudflared\tunnel-config.yml"

# Remove existing service if present
& $nssm stop FlowstateAI-Tunnel 2>$null
& $nssm remove FlowstateAI-Tunnel confirm 2>$null

& $nssm install FlowstateAI-Tunnel "$cloudflared"
& $nssm set FlowstateAI-Tunnel AppParameters "tunnel --config `"$tunnelConfig`" run flowstateai-n8n"
& $nssm set FlowstateAI-Tunnel DisplayName "FlowstateAI Cloudflare Tunnel"
& $nssm set FlowstateAI-Tunnel Description "Cloudflare tunnel for n8n webhooks - routes n8n.flowstateaiautomation.ai to localhost:5678"
& $nssm set FlowstateAI-Tunnel Start SERVICE_AUTO_START
& $nssm set FlowstateAI-Tunnel DependOnService FlowstateAI-n8n
& $nssm set FlowstateAI-Tunnel AppStdout "$servicesDir\tunnel-stdout.log"
& $nssm set FlowstateAI-Tunnel AppStderr "$servicesDir\tunnel-stderr.log"
& $nssm set FlowstateAI-Tunnel AppRotateFiles 1
& $nssm set FlowstateAI-Tunnel AppRotateBytes 5242880
& $nssm set FlowstateAI-Tunnel AppRestartDelay 3000

Write-Host "[OK] Cloudflare Tunnel service installed" -ForegroundColor Green
Write-Host ""

# ── Start both services ─────────────────────────────
Write-Host "Starting services..."
& $nssm start FlowstateAI-n8n
Start-Sleep -Seconds 5
& $nssm start FlowstateAI-Tunnel

Write-Host ""
Write-Host "============================================"
Write-Host "  DONE! Both services are running."
Write-Host "  n8n: http://localhost:5678"
Write-Host "  Tunnel: https://n8n.flowstateaiautomation.ai"
Write-Host "============================================"
Write-Host ""
Write-Host "Services will now:"
Write-Host "  - Auto-start on boot"
Write-Host "  - Auto-restart on crash (5s delay)"
Write-Host "  - Log to $servicesDir"
Write-Host ""
Write-Host "To check status:  Get-Service FlowstateAI-*"
Write-Host "To stop:          nssm stop FlowstateAI-n8n"
Write-Host "To restart:       nssm restart FlowstateAI-n8n"
