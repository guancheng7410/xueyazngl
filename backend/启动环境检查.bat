@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ================================================
echo   Blood Pressure Guardian Server
echo ================================================
echo.
echo   Web:   http://localhost:5000
echo   APP:   http://localhost:5000/app.html
echo   API:   http://localhost:5000/api/health
echo   Debug: http://localhost:5000/api/debug
echo.
echo   Press Ctrl+C to stop
echo ================================================
echo.
python server.py
pause
