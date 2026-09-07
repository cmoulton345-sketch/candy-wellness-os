# stop_speak.ps1
# Create stop signal to immediately interrupt ongoing speech in speak.py

$stopFlag = Join-Path $PSScriptRoot "stop.flag"
New-Item -Path $stopFlag -ItemType File -Force | Out-Null
$stopSpeech = Join-Path $PSScriptRoot "stop_speech.txt"
New-Item -Path $stopSpeech -ItemType File -Force | Out-Null
Write-Host "Sent stop signal to voice assistant."
