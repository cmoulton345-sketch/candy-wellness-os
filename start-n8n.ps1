$ErrorActionPreference = "Stop"

Write-Host "Starting FlowstateAI n8n + Permanent Tunnel..."
Write-Host "n8n will be available at: http://localhost:5678"
Write-Host "Webhook URL (permanent): https://n8n.flowstateaiautomation.ai"
Write-Host "Press Ctrl+C to stop."
Write-Host ""

# Ensure Node.js path is loaded
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Allow crypto and other built-in Node.js modules in n8n Code nodes
$env:NODE_FUNCTION_ALLOW_BUILTIN = "crypto,fs,path"

# WEBHOOK_URL commented out — Google Sheets trigger uses polling (no webhooks needed)
# Re-enable only if using webhook-based triggers that require the public tunnel URL
# $env:WEBHOOK_URL = "https://n8n.flowstateaiautomation.ai/"

# Start Cloudflare quick tunnel in background
$cloudflared = "C:\Program Files (x86)\cloudflared\cloudflared.exe"
$logFile = "$env:TEMP\cloudflare_n8n.log"
Remove-Item $logFile -ErrorAction SilentlyContinue

Start-Process -NoNewWindow -FilePath $cloudflared -ArgumentList "tunnel", "--url", "http://localhost:5678", "--protocol", "http2" -RedirectStandardError $logFile

Write-Host "Starting Cloudflare quick tunnel..."
Start-Sleep -Seconds 5
if (Test-Path $logFile) {
    $tunnelUrl = Select-String -Path $logFile -Pattern "https://.*\.trycloudflare\.com" | Select-Object -First 1
    if ($tunnelUrl) {
        $cleanUrl = $tunnelUrl.Matches.Value
        Write-Host "Cloudflare tunnel started -> $cleanUrl"
    } else {
        Write-Host "Cloudflare tunnel is starting. Check logs at: $logFile"
    }
}
Write-Host ""

# Start n8n (foreground - keeps the window open)
n8n.cmd
