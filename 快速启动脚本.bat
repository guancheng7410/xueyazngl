@echo off
chcp 65001 >nul
cls
echo.
echo ================================================
echo    血压守护 - 手机访问服务器
echo ================================================
echo.
echo 正在启动服务器...
echo.

cd /d "%~dp0www"

echo [方法1] 使用Python启动...
python -m http.server 8082 --bind 0.0.0.0

if %errorlevel% neq 0 (
    echo.
    echo Python启动失败，尝试使用Node.js...
    echo.
    npx -y http-server -p 8082 --address 0.0.0.0
)

pause
