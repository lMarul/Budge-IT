Write-Host "🚀 Nhost Deployment Script for Budge-IT" -ForegroundColor Green
Write-Host ""

# Check if nhost is available
try {
    $version = npm exec nhost --version 2>$null
    Write-Host "✅ Nhost CLI found: $version" -ForegroundColor Green
} catch {
    Write-Host "❌ Nhost CLI not found. Installing..." -ForegroundColor Red
    npm install -g nhost
}

Write-Host ""
Write-Host "📋 Deployment Steps:" -ForegroundColor Yellow
Write-Host "1. Login to Nhost: npm exec nhost login" -ForegroundColor Cyan
Write-Host "2. Initialize project: npm exec nhost init budge-it" -ForegroundColor Cyan
Write-Host "3. Deploy: npm exec nhost up" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Your website URL will be shown after successful deployment!" -ForegroundColor Green
Write-Host ""

# Ask if user wants to proceed
$response = Read-Host "Do you want to start deployment now? (y/n)"
if ($response -eq "y" -or $response -eq "Y") {
    Write-Host "Starting deployment..." -ForegroundColor Yellow
    npm exec nhost login
} else {
    Write-Host "Run the commands manually when ready." -ForegroundColor Yellow
} 