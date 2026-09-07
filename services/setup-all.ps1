$ErrorActionPreference = "Continue"
$nssm = "C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\NSSM.NSSM_Microsoft.Winget.Source_8wekyb3d8bbwe\nssm-2.24-101-g897c7ad\win64\nssm.exe"
$servicesDir = "C:\Users\Admin\Agents\radical_simplicity_ai_os_joe-m\services"
$cloudflared = "C:\Users\Admin\tools\cloudflared\cloudflared.exe"
$tunnelConfig = "C:\Users\Admin\tools\cloudflared\tunnel-config.yml"

# Kill any running n8n/cloudflared
Stop-Process -Name "node" -Force -ErrorAction SilentlyContinue
Stop-Process -Name "cloudflared" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# ── Remove old services (clean slate) ──
& $nssm stop FlowstateAI-n8n 2>$null
& $nssm remove FlowstateAI-n8n confirm 2>$null
& $nssm stop FlowstateAI-Tunnel 2>$null
& $nssm remove FlowstateAI-Tunnel confirm 2>$null
Start-Sleep -Seconds 2

# ── Install n8n service ──
& $nssm install FlowstateAI-n8n "$servicesDir\n8n-service.cmd"
& $nssm set FlowstateAI-n8n DisplayName "FlowstateAI n8n Automation Engine"
& $nssm set FlowstateAI-n8n Description "n8n automation engine - auto-starts on boot"
& $nssm set FlowstateAI-n8n Start SERVICE_AUTO_START
& $nssm set FlowstateAI-n8n AppStdout "$servicesDir\n8n-stdout.log"
& $nssm set FlowstateAI-n8n AppStderr "$servicesDir\n8n-stderr.log"
& $nssm set FlowstateAI-n8n AppRotateFiles 1
& $nssm set FlowstateAI-n8n AppRotateBytes 5242880
& $nssm set FlowstateAI-n8n AppRestartDelay 5000

# ── Install tunnel service ──
& $nssm install FlowstateAI-Tunnel "$cloudflared"
& $nssm set FlowstateAI-Tunnel AppParameters "tunnel --config `"$tunnelConfig`" run flowstateai-n8n"
& $nssm set FlowstateAI-Tunnel DisplayName "FlowstateAI Cloudflare Tunnel"
& $nssm set FlowstateAI-Tunnel Description "Cloudflare tunnel for webhooks"
& $nssm set FlowstateAI-Tunnel Start SERVICE_AUTO_START
& $nssm set FlowstateAI-Tunnel DependOnService FlowstateAI-n8n
& $nssm set FlowstateAI-Tunnel AppStdout "$servicesDir\tunnel-stdout.log"
& $nssm set FlowstateAI-Tunnel AppStderr "$servicesDir\tunnel-stderr.log"
& $nssm set FlowstateAI-Tunnel AppRotateFiles 1
& $nssm set FlowstateAI-Tunnel AppRotateBytes 5242880
& $nssm set FlowstateAI-Tunnel AppRestartDelay 3000

# ── Start services ──
& $nssm start FlowstateAI-n8n
Start-Sleep -Seconds 8
& $nssm start FlowstateAI-Tunnel

# ── Report ──
Start-Sleep -Seconds 3
Get-Service FlowstateAI-* | Format-Table Name, Status, StartType -AutoSize
