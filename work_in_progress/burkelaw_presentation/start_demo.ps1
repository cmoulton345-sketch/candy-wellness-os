# Start the Burke Law Presentation Environment

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Initializing Flowstate AI Demo OS      " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Start Socrates Web App
Write-Host "[1/5] Booting Socrates Web App..." -ForegroundColor Yellow
$socratesPath = "$PSScriptRoot\..\burkelaw\socrates-web"
Start-Process powershell -ArgumentList "-WindowStyle Minimized -Command cd '$socratesPath'; python -m http.server 3000"
Start-Sleep -Seconds 3

# 2. Start Socrates API Proxy
Write-Host "[2/5] Booting Socrates API Proxy..." -ForegroundColor Yellow
$apiPath = "$PSScriptRoot\..\burkelaw\socrates-api"
Start-Process powershell -ArgumentList "-WindowStyle Minimized -Command cd '$apiPath'; python server.py"
Start-Sleep -Seconds 2

# 3. Start Presentation Server
Write-Host "[3/5] Booting Presentation Server..." -ForegroundColor Yellow
$presentationPath = "$PSScriptRoot"
Start-Process powershell -ArgumentList "-WindowStyle Minimized -Command cd '$presentationPath'; python -m http.server 8080"
Start-Sleep -Seconds 1

# 4. Start Burke Law Website Server
Write-Host "[4/5] Booting Burke Law Website..." -ForegroundColor Yellow
$burkeSitePath = "$PSScriptRoot\..\burkelaw"
Start-Process powershell -ArgumentList "-WindowStyle Minimized -Command cd '$burkeSitePath'; python -m http.server 8090"
Start-Sleep -Seconds 4

# 5. Open all browser tabs
Write-Host "[5/5] Opening Browser..." -ForegroundColor Yellow
Start-Process "http://localhost:8080"
Start-Sleep -Seconds 1
Start-Process "http://localhost:3000"
Start-Sleep -Seconds 1
Start-Process "http://localhost:8090"
Start-Sleep -Seconds 1
Start-Process "http://localhost:5678"

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "  All Systems GO!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host "  Presentation:    http://localhost:8080" -ForegroundColor Green
Write-Host "  Socrates:        http://localhost:3000" -ForegroundColor Green
Write-Host "  API Proxy:       http://localhost:8787" -ForegroundColor Green
Write-Host "  Burke Law Site:  http://localhost:8090" -ForegroundColor Green
Write-Host "  n8n Workspace:   http://localhost:5678" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Start-Sleep -Seconds 5
