Get-Content C:\Users\Admin\Agents\radical_simplicity_ai_os_joe-m\.env | ForEach-Object { if ($_ -match '^([^#]\w+)=(.+)$') { [Environment]::SetEnvironmentVariable($matches[1], $matches[2]) } }
npx wrangler pages deploy . --project-name flowstate-automation --branch main
