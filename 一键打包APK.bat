@echo off
chcp 65001 >nul
cls
echo.
echo ================================================
echo    血压守护 APK 自动安装与构建工具
echo ================================================
echo.
echo 本脚本将自动完成以下步骤：
echo   1. 检查并安装必要环境
echo   2. 下载并配置Android SDK
echo   3. 构建APK
echo   4. 复制到D:\APP目录
echo.
echo ================================================
echo.
pause

:: 设置变量
set PROJECT_DIR=E:\开发需要\blood-pressure-guardian
set APP_DIR=D:\APP
set SDK_DIR=%LOCALAPPDATA%\Android\Sdk
set BUILD_TOOLS_VERSION=33.0.0
set PLATFORM_VERSION=33

:: 创建D:\APP目录
if not exist "%APP_DIR%" (
    echo [1/8] 创建D:\APP目录...
    mkdir "%APP_DIR%"
)

:: 检查Node.js
echo.
echo [2/8] 检查Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] 未安装Node.js
    echo.
    echo 请先安装Node.js：
    echo 1. 访问 https://nodejs.org/
    echo 2. 下载LTS版本
    echo 3. 运行安装程序
    echo 4. 重新运行本脚本
    echo.
    pause
    exit /b 1
) else (
    echo [OK] Node.js 已安装
    node --version
)

:: 检查npm
echo.
echo [3/8] 检查npm...
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] npm未找到
    pause
    exit /b 1
) else (
    echo [OK] npm 已安装
    npm --version
)

:: 安装项目依赖
echo.
echo [4/8] 安装项目依赖...
cd /d "%PROJECT_DIR%"
call npm install
if %errorlevel% neq 0 (
    echo [!] npm install 失败
    pause
    exit /b 1
)
echo [OK] 依赖安装完成

:: 检查Java
echo.
echo [5/8] 检查Java环境...
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [!] 未安装Java JDK
    echo.
    echo ================================================
    echo 需要安装Java JDK才能构建APK
    echo ================================================
    echo.
    echo 请选择安装方式：
    echo.
    echo 1. 自动下载并打开JDK安装页面（推荐JDK 17）
    echo 2. 我已安装Java，继续构建
    echo 3. 退出
    echo.
    set /p JDK_CHOICE=请输入选项(1-3): 
    
    if "%JDK_CHOICE%"=="1" (
        echo 正在打开JDK下载页面...
        start https://adoptium.net/temurin/releases/?version=17
        echo.
        echo 请在打开的页面中下载JDK 17
        echo 安装完成后，重新运行本脚本
        echo.
        pause
        exit /b 0
    ) else if "%JDK_CHOICE%"=="2" (
        echo 继续构建...
    ) else (
        exit /b 0
    )
) else (
    echo [OK] Java 已安装
    java -version
)

:: 检查Android SDK
echo.
echo [6/8] 检查Android SDK...
if exist "%SDK_DIR%\platforms\android-%PLATFORM_VERSION%" (
    echo [OK] Android SDK 已安装
) else (
    echo.
    echo [!] Android SDK 未安装或版本不匹配
    echo.
    echo ================================================
    echo 需要安装Android SDK
    echo ================================================
    echo.
    echo 推荐安装方式：
    echo.
    echo 方式一：安装Android Studio（推荐）
    echo   1. 访问 https://developer.android.com/studio
    echo   2. 下载并安装Android Studio
    echo   3. 首次启动会自动安装SDK
    echo.
    echo 方式二：仅安装Command Line Tools
    echo   1. 访问 https://developer.android.com/studio#command-line-tools-only
    echo   2. 下载Command Line Tools
    echo   3. 解压到 %LOCALAPPDATA%\Android
    echo.
    echo 是否现在打开Android Studio下载页面？
    set /p AS_CHOICE=(y/n): 
    
    if /i "%AS_CHOICE%"=="y" (
        start https://developer.android.com/studio
        echo.
        echo 已打开下载页面
        echo 安装完成后，重新运行本脚本
        echo.
        pause
        exit /b 0
    )
)

:: 添加Android平台
echo.
echo [7/8] 配置Capacitor Android平台...
cd /d "%PROJECT_DIR%"

if exist "android" (
    echo [提示] Android平台已存在，将重新同步
    call npx cap sync android
) else (
    echo 添加Android平台...
    call npx cap add android
    if %errorlevel% neq 0 (
        echo.
        echo [!] 添加Android平台失败
        echo 请检查错误信息并修复后重试
        pause
        exit /b 1
    )
    echo [OK] Android平台添加成功
    call npx cap sync android
)

if %errorlevel% neq 0 (
    echo [!] 同步失败
    pause
    exit /b 1
)

echo [OK] 项目同步完成

:: 构建APK
echo.
echo [8/8] 构建APK...
echo.

if exist "android\gradlew.bat" (
    echo 使用Gradle构建APK...
    cd android
    
    echo 正在构建Debug版本APK...
    echo 这可能需要几分钟时间，请耐心等待...
    echo.
    
    call gradlew.bat assembleDebug
    
    if %errorlevel% equ 0 (
        echo.
        echo ================================================
        echo [成功] APK构建完成！
        echo ================================================
        echo.
        
        :: 查找APK文件
        if exist "app\build\outputs\apk\debug\app-debug.apk" (
            echo 正在复制APK到D:\APP...
            mkdir "%APP_DIR%" 2>nul
            copy "app\build\outputs\apk\debug\app-debug.apk" "%APP_DIR%\血压守护.apk"
            
            echo.
            echo ================================================
            echo [成功] APK已保存到：
            echo   %APP_DIR%\血压守护.apk
            echo ================================================
            echo.
            echo 您可以：
            echo   1. 将APK发送到手机进行安装
            echo   2. 通过微信/QQ发送APK到手机
            echo   3. 使用数据线复制到手机
            echo.
        ) else (
            echo [!] APK文件未找到
            echo 请检查构建日志
        )
    ) else (
        echo.
        echo ================================================
        echo [失败] APK构建失败
        echo ================================================
        echo.
        echo 常见原因：
        echo   1. Android SDK未正确安装
        echo   2. Gradle同步失败
        echo   3. 缺少必要的构建工具
        echo.
        echo 解决方案：
        echo   1. 打开Android Studio检查SDK安装
        echo   2. 在Android Studio中打开此项目
        echo   3. 等待Gradle同步完成后重新构建
        echo.
        echo 或者在Android Studio中手动构建：
        echo   Build ^> Build Bundle/APK ^> Build APK
        echo.
    )
    cd ..
) else (
    echo.
    echo [!] 未找到Gradle包装器
    echo.
    echo 请使用以下方式构建：
    echo.
    echo 1. 打开Android Studio
    echo    npx cap open android
    echo.
    echo 2. 在Android Studio中构建APK
    echo    Build ^> Build Bundle/APK ^> Build APK
    echo.
)

echo.
echo ================================================
echo 构建流程完成
echo ================================================
echo.
echo 如需查看详细说明，请打开：
echo   %APP_DIR%\血压守护APP下载安装操作手册.html
echo.
pause
