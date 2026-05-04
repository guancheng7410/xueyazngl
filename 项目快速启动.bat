@echo off
chcp 65001 >nul
cls
echo.
echo ================================================
echo          血压守护 - 手机端安装程序
echo ================================================
echo.
echo 本程序将帮助您在手机上安装血压守护应用
echo.
echo [方式一] 使用PWA安装（推荐）
echo   - 无需APK文件
echo   - 像原生APP一样使用
echo   - 支持离线使用
echo.
echo [方式二] 构建Android APK
echo   - 需要Android开发环境
echo   - 适合发布到应用商店
echo.
echo ================================================
echo.

:menu
echo 请选择安装方式：
echo.
echo 1. 启动本地服务器（在浏览器中使用）
echo 2. 查看手机安装指南
echo 3. 构建Android APK（需要开发环境）
echo 4. 退出
echo.
set /p CHOICE=请输入选项(1-4): 

if "%CHOICE%"=="1" goto start_server
if "%CHOICE%"=="2" goto show_guide
if "%CHOICE%"=="3" goto build_apk
if "%CHOICE%"=="4" goto exit
goto menu

:start_server
echo.
echo [正在启动服务器...]
echo.
echo 服务器启动后，请在手机浏览器中访问：
echo http://您的电脑IP:8082
echo.
echo 例如：http://192.168.1.100:8082
echo.
echo 提示：查看本机IP请在命令行运行 ipconfig
echo.
echo 按 Ctrl+C 可停止服务器
echo.
echo ================================================
echo.
cd /d "%~dp0"
python -m http.server 8082
goto exit

:show_guide
echo.
echo ================================================
echo           手机安装指南
echo ================================================
echo.
echo 【iPhone 安装步骤】
echo.
echo 1. 确保手机和电脑在同一WiFi网络
echo.
echo 2. 在手机 Safari 浏览器中打开：
echo    http://您的电脑IP:8082
echo.
echo 3. 点击底部"分享"按钮
echo.
echo 4. 向下滚动，点击"添加到主屏幕"
echo.
echo 5. 点击"添加"
echo.
echo 6. 现在可以在主屏幕找到"血压守护"图标
echo.
echo ================================================
echo.
echo 【Android 安装步骤】
echo.
echo 1. 确保手机和电脑在同一WiFi网络
echo.
echo 2. 在手机 Chrome 浏览器中打开：
echo    http://您的电脑IP:8082
echo.
echo 3. 点击右上角菜单（三个点）
echo.
echo 4. 点击"添加到主屏幕"
echo.
echo 5. 点击"添加"
echo.
echo 6. 现在可以在主屏幕找到"血压守护"图标
echo.
echo ================================================
echo.
echo 提示：安装后可以离线使用，无需联网
echo.
pause
goto menu

:build_apk
echo.
echo ================================================
echo        构建 Android APK
echo ================================================
echo.
echo 构建APK需要以下环境：
echo.
echo [必需]
echo   - Node.js 14+ 
echo   - Java JDK 11+
echo   - Android SDK
echo.
echo [安装步骤]
echo.
echo 1. 安装 Node.js
echo    下载：https://nodejs.org/
echo.
echo 2. 安装 Java JDK
echo    下载：https://adoptium.net/
echo.
echo 3. 安装 Android Studio
echo    下载：https://developer.android.com/studio
echo.
echo 4. 在 Android Studio 中安装 Android SDK
echo.
echo 5. 运行本目录下的 BUILD_APK.bat
echo.
echo 或者使用云端打包服务：
echo   - HBuilderX：https://www.dcloud.io/
echo   - 导入 www 文件夹
echo   - 发行 -> 原生App-云打包
echo.
echo ================================================
echo.
pause
goto menu

:exit
echo.
echo 感谢使用血压守护！
echo.
timeout /t 2 >nul
exit
