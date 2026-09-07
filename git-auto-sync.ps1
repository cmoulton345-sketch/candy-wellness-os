Set-Location "c:\Users\Admin\Agents\radical_simplicity_ai_os_v2"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
try {
    git pull --rebase origin master 2>&1 | Out-File -Append "c:\Users\Admin\Agents\radical_simplicity_ai_os_v2\git-sync.log"
    Add-Content "c:\Users\Admin\Agents\radical_simplicity_ai_os_v2\git-sync.log" "$timestamp - sync complete"
} catch {
    Add-Content "c:\Users\Admin\Agents\radical_simplicity_ai_os_v2\git-sync.log" "$timestamp - ERROR: $_"
}
