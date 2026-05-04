@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================================
echo   BP Guardian - 一键启动
echo ============================================================
echo.
echo [1] 停止所有旧服务器...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM pythonw.exe 2>nul
timeout /t 2 /nobreak >nul

echo [2] 清理缓存...
if exist __pycache__ rd /s /q __pycache__
for /d /r %%d in (__pycache__) do rd /s /q "%%d" 2>nul

echo [3] 启动新服务器...
echo.
echo ============================================================
python standalone_server.py
pause
