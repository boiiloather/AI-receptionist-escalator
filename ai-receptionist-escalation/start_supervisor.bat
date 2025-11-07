@echo off
echo ========================================
echo   Supervisor UI - Quick Start
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [2/2] Starting Supervisor Web UI...
echo.
echo Supervisor Dashboard will open at:
echo   http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python run_supervisor.py

pause





