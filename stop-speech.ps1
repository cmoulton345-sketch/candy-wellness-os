# Instant Speech Silencer Script
$stopFlag = Join-Path -Path $PSScriptRoot -ChildPath "stop.flag"
"1" | Out-File -FilePath $stopFlag -Encoding ascii -Force
Write-Host "⏹️ Speech silenced via stop.flag!" -ForegroundColor Yellow
