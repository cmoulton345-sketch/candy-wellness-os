$processes = Get-CimInstance Win32_Process | Where-Object {
    $_.CommandLine -like "*voice_system.py*" -or $_.CommandLine -like "*speak.py*" -or $_.CommandLine -like "*listen.py*"
}
foreach ($p in $processes) {
    Write-Host "Killing process ID: $($p.ProcessId) - $($p.CommandLine)"
    Stop-Process -Id $p.ProcessId -Force
}
