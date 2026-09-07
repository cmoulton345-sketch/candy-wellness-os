# Switch Git Remote to Private Backup Repository
# Run this script from PowerShell inside the radical_simplicity_ai_os_joe-m folder

Write-Host "Removing old remotes..."
git remote remove origin 2>$null
git remote remove external 2>$null

Write-Host "Adding new private backup remote..."
git remote add origin https://github.com/joemoulton2022-create/My-personal-AI-OS-backup.git

Write-Host "Pulling latest from new remote..."
git pull origin master --allow-unrelated-histories

Write-Host ""
Write-Host "Done! Verifying..."
git remote -v
Write-Host ""
Write-Host "Your home computer is now syncing to the private backup repo."
