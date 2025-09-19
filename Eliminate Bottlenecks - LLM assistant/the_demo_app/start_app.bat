@echo off
echo Starting TechAdvance Solutions...
echo.
echo This will launch PowerShell to run the setup script.
echo Press any key to continue or Ctrl+C to cancel.
pause >nul

powershell -ExecutionPolicy Bypass -File "start_app.ps1"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error occurred. Press any key to exit.
    pause >nul
)

