Get-Content "C:\Users\Admin\Agents\radical_simplicity_ai_os_joe-m\.env" | ForEach-Object {
    if ($_ -match '^([^#]\w+)=(.+)$') {
        [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2])
    }
}
npx wrangler pages deploy "C:\Users\Admin\Agents\radical_simplicity_ai_os_joe-m\work_in_progress\flowstateautomation" --project-name flowstate-automation --branch main
