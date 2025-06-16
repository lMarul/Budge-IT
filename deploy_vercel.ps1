# Vercel Deployment Script for PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    Vercel Deployment Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Vercel CLI is installed
Write-Host "Checking if Vercel CLI is installed..." -ForegroundColor Yellow
try {
    $vercelVersion = vercel --version 2>$null
    Write-Host "✅ Vercel CLI found: $vercelVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Vercel CLI not found. Installing..." -ForegroundColor Red
    try {
        npm install -g vercel
        Write-Host "✅ Vercel CLI installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to install Vercel CLI. Please install manually:" -ForegroundColor Red
        Write-Host "npm install -g vercel" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "Deploying to Vercel..." -ForegroundColor Yellow
Write-Host ""

# Deploy to Vercel
vercel

Write-Host ""
Write-Host "Deployment complete!" -ForegroundColor Green
Write-Host "Check the URL above for your live application." -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to exit" 