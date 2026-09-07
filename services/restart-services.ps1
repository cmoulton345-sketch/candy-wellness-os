# Restart the n8n service to pick up the updated config
$ErrorActionPreference = "Continue"
Write-Host "Restarting FlowstateAI-n8n service..."
Restart-Service FlowstateAI-n8n -Force
Start-Sleep -Seconds 10
Write-Host "Restarting FlowstateAI-Tunnel service..."
Restart-Service FlowstateAI-Tunnel -Force
Start-Sleep -Seconds 5
Get-Service FlowstateAI-* | Format-Table Name, Status -AutoSize
