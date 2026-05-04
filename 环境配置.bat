@echo off
chcp 65001 >nul
cls
echo.
echo ================================================
echo    血压守护 APK 构建 - 环境检查
echo ================================================
echo.

set HAS_ERROR=0

:: 检查Node.js
echo [检查] Node.js...
node --version >nul 2>&1
if %errorlevel% equ 0 (
    echo   [OK] Node.js 已安装
    node --version
) else (
    echo   [失败] 未安装Node.js
    echo   下载：https://nodejs.org/
    set HAS_ERROR=1
)
echo.

:: 检查Java
echo [检查] Java JDK...
java -version >nul 2>&1
if %errorlevel% equ 0 (
    echo   [OK] Java 已安装
    java -version
) else (
    echo   [失败] 未安装Java JDK
    echo   下载：https://adoptium.net/
    set HAS_ERROR=1
)
echo.

:: 检查Android SDK
echo [检查] Android SDK...
if defined ANDROID_HOME (
    echo   [OK] ANDROID_HOME 已设置: %ANDROID_HOME%
) else (
    echo   [警告] ANDROID_HOME 未设置
    echo   请安装Android Studio或设置环境变量
    set HAS_ERROR=1
)
echo.

:: 检查npm依赖
echo [检查] npm依赖...
if exist "node_modules\@capacitor\core" (
    echo   [OK] Capacitor 已安装
) else (
    echo   [提示] 需要先运行 npm install
    echo   安装命令：npm install
)
echo.

:: 检查Android平台
echo [检查] Android平台...
if exist "android" (
    echo   [OK] Android平台已添加
) else (
    echo   [提示] Android平台未添加
    echo   添加命令：npx cap add android
)
echo.

echo ================================================
if %HAS_ERROR% equ 0 (
    echo [结果] 环境检查通过！可以构建APK
    echo.
    echo 下一步：运行 自动构建APK.bat
) else (
    echo [结果] 发现环境问题，需要先安装缺失组件
    echo.
    echo 请按以下顺序安装：
    echo   1. Node.js (https://nodejs.org/)
    echo   2. Java JDK (https://adoptium.net/)
    echo   3. Android Studio (https://developer.android.com/studio)
)
echo ================================================
echo.
pause
