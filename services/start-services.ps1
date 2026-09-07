$ErrorActionPreference = "Stop"
$nssm = "C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\NSSM.NSSM_Microsoft.Winget.Source_8wekyb3d8bbwe\nssm-2.24-101-g897c7ad\win64\nssm.exe"

# Check if tunnel service exists, install if not
$tunnelSvc = Get-Service FlowstateAI-Tunnel -ErrorAction SilentlyContinue
if (-not $tunnelSvc) {
    Write-Host "Tunnel service missing — installing now..."
    $cloudflared = "C:\Users\Admin\tools\cloudflared\cloudflared.exe"
    $tunnelConfig = "C:\Users\Admin\tools\cloudflared\tunnel-config.yml"
    $servicesDir = "C:\Users\Admin\Agents\radical_simplicity_ai_os_joe-m\services"

    & $nssm install FlowstateAI-Tunnel "$cloudflared"
    & $nssm set FlowstateAI-Tunnel AppParameters "tunnel --config `"$tunnelConfig`" run flowstateai-n8n"
    & $nssm set FlowstateAI-Tunnel DisplayName "FlowstateAI Cloudflare Tunnel"
    & $nssm set FlowstateAI-Tunnel Description "Cloudflare tunnel for n8n webhooks"
    & $nssm set FlowstateAI-Tunnel Start SERVICE_AUTO_START
    & $nssm set FlowstateAI-Tunnel DependOnService FlowstateAI-n8n
    & $nssm set FlowstateAI-Tunnel AppStdout "$servicesDir\tunnel-stdout.log"
    & $nssm set FlowstateAI-Tunnel AppStderr "$servicesDir\tunnel-stderr.log"
    & $nssm set FlowstateAI-Tunnel AppRotateFiles 1
    & $nssm set FlowstateAI-Tunnel AppRotateBytes 5242880
    & $nssm set FlowstateAI-Tunnel AppRestartDelay 3000
    Write-Host "[OK] Tunnel service installed"
}

Write-Host "Starting FlowstateAI-n8n..."
& $nssm start FlowstateAI-n8n
Start-Sleep -Seconds 8
Write-Host "Starting FlowstateAI-Tunnel..."
& $nssm start FlowstateAI-Tunnel
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "Service Status:"
Get-Service FlowstateAI-* | Format-Table Name, Status, StartType -AutoSize

Write-Host ""
Write-Host "Press any key to close..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
