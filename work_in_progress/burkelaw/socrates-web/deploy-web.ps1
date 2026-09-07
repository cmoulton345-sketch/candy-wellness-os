$ErrorActionPreference = "Stop"

# Load environment variables from the workspace .env file
Get-Content C:\Users\Admin\Agents\radical_simplicity_ai_os_joe-m\.env | ForEach-Object { 
    if ($_ -match '^([^#]\w+)=(.+)$') { 
        [Environment]::SetEnvironmentVariable($matches[1], $matches[2]) 
    } 
}

# Ensure we are in the frontend directory
Set-Location C:\Users\Admin\Agents\radical_simplicity_ai_os_joe-m\work_in_progress\burkelaw\socrates-web

Write-Host "Creating Cloudflare Pages project..."
# We ignore errors here in case the project already exists
npx wrangler pages project create socrates-legal-shadow --production-branch main

Write-Host "Deploying Socrates Web Application..."
npx wrangler pages deploy dist --project-name socrates-legal-shadow
