@echo off
echo ========================================
echo    Vercel Deployment Script
echo ========================================
echo.

echo Checking if Vercel CLI is installed...
vercel --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Vercel CLI not found. Installing...
    npm install -g vercel
    if %errorlevel% neq 0 (
        echo Failed to install Vercel CLI. Please install manually:
        echo npm install -g vercel
        pause
        exit /b 1
    )
)

echo.
echo Deploying to Vercel...
echo.
vercel

echo.
echo Deployment complete!
echo Check the URL above for your live application.
echo.
pause 