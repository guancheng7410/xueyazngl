@echo off
chcp 65001 >nul
title 血压守护APP服务器
echo ========================================
echo   血压守护 APP 服务器
echo ========================================
echo.
echo 正在启动服务器...
echo.
echo 访问地址:
echo   APP端: http://localhost:8081/app_mobile.html
echo   测试端: http://localhost:8081/test_app_mobile.html
echo   测试报告: http://localhost:8081/test_app_verify.py
echo.
echo 按 Ctrl+C 停止服务器
echo.
cd /d "%~dp0"
python -m http.server 8081
pause
