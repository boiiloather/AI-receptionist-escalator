@echo off
echo ========================================
echo   AI Receptionist Agent - Quick Start
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [2/3] Starting LiveKit Agent...
echo.
echo IMPORTANT: Keep this window open!
echo The agent must stay running to handle calls.
echo.
echo ========================================
echo.

python run_agent.py dev

pause





