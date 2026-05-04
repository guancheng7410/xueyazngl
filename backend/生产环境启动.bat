@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo  BP Guardian - 彻底重启
echo ============================================================
echo.
echo [1] 正在停止所有 Python 进程...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM pythonw.exe 2>nul
taskkill /F /IM python3.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo [2] 正在清理 Python 缓存...
cd /d "%~dp0"
if exist __pycache__ rd /s /q __pycache__
for /d /r %%d in (__pycache__) do rd /s /q "%%d" 2>nul

echo.
echo [3] 正在启动服务器...
echo.
echo ============================================================
echo   服务器地址: http://localhost:5000
echo   首页:       http://localhost:5000/
echo   APP:        http://localhost:5000/app.html
echo   调试:       http://localhost:5000/api/debug
echo ============================================================
echo.
python server.py
pause
