@echo off
echo Starting Nhost deployment...
echo.

REM Check if nhost is available
npm exec nhost --version >nul 2>&1
if errorlevel 1 (
    echo Error: Nhost CLI not found. Installing...
    npm install -g nhost
)

echo Nhost CLI version:
npm exec nhost --version

echo.
echo To deploy your app:
echo 1. npm exec nhost login
echo 2. npm exec nhost init budge-it
echo 3. npm exec nhost up
echo.
echo Your website will be available at the URL shown after deployment.
pause 