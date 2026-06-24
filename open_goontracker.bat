@echo off

cd /d C:\dev\GoonTracker

start "GoonTracker Poller" cmd /k "venv\Scripts\activate.bat && python poller.py"

timeout /t 2 >nul

start "GoonTracker API" cmd /k "venv\Scripts\activate.bat && uvicorn api:app --host 0.0.0.0 --port 8000"

timeout /t 5 >nul

start "" ".\web\index.html"

exit