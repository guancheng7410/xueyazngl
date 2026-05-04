@echo off
echo ========================================
echo   血压守护 - 后端服务启动脚本
echo ========================================
echo.

echo [1/3] 正在安装依赖...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo [错误] 依赖安装失败，请检查Python环境
    pause
    exit /b 1
)

echo.
echo [2/3] 依赖安装完成
echo.

echo [3/3] 正在启动服务...
echo.
echo 服务启动后请访问: http://localhost:5000/api/health
echo 按 Ctrl+C 停止服务
echo.

python run.py

pause
