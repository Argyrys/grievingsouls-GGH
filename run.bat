@echo off
title Veritas Vision
cd /d "%~dp0"

echo.
echo   VERITAS VISION
echo   Dashboard : http://127.0.0.1:8000/
echo   Mock pages: http://127.0.0.1:8000/mocks/
echo   Stop      : close this window
echo.

start "Veritas Vision Server" cmd /k "cd /d %~dp0 && py -m uvicorn backend.main:app --host 127.0.0.1 --port 8000"
timeout /t 4 /nobreak >nul
start "" http://127.0.0.1:8000/
echo   Server window opened. Browser should be loading now.
pause
