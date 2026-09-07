$ErrorActionPreference = "Stop"

# Load environment variables from the workspace .env file
Get-Content C:\Users\Admin\Agents\radical_simplicity_ai_os_v2\.env | ForEach-Object { 
    if ($_ -match '^([^#]\w+)=(.+)$') { 
        [Environment]::SetEnvironmentVariable($matches[1], $matches[2]) 
    } 
}

Set-Location C:\Users\Admin\Agents\radical_simplicity_ai_os_v2\work_in_progress\burkelaw\socrates-api

# The API KEY has to be passed via stdin to `wrangler secret put`
Write-Host "Setting GEMINI_API_KEY secret..."
$env:GEMINI_API_KEY | npx wrangler secret put GEMINI_API_KEY

Write-Host "Deploying Socrates API Worker..."
npx wrangler deploy
