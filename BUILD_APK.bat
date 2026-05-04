@echo off
chcp 65001 >nul
echo ======================================
echo 血压守护 APK 构建脚本
echo ======================================
echo.

echo [1/5] 检查环境...
echo.

REM 检查Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Node.js，请先安装 Node.js
    echo 下载地址: https://nodejs.org/
    pause
    exit /b 1
) else (
    echo [OK] Node.js 已安装
    node --version
)

REM 检查Java
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] 未找到 Java，Android构建需要JDK 11或更高版本
    echo 请下载并安装JDK: https://adoptium.net/
    echo.
    set /p CONTINUE="是否继续?(y/n): "
    if /i not "%CONTINUE%"=="y" exit /b 1
) else (
    echo [OK] Java 已安装
    java -version
)

echo.
echo [2/5] 安装依赖...
echo.
call npm install
if %errorlevel% neq 0 (
    echo [错误] npm install 失败
    pause
    exit /b 1
)
echo [OK] 依赖安装完成

echo.
echo [3/5] 添加Android平台...
echo.
REM 检查是否已有android目录
if exist android (
    echo [提示] Android平台已存在，跳过添加
) else (
    call npx cap add android
    if %errorlevel% neq 0 (
        echo [错误] 添加Android平台失败
        echo 请确保已安装Android Studio和Android SDK
        pause
        exit /b 1
    )
    echo [OK] Android平台添加成功
)

echo.
echo [4/5] 同步项目...
echo.
call npx cap sync android
if %errorlevel% neq 0 (
    echo [错误] 同步项目失败
    pause
    exit /b 1
)
echo [OK] 项目同步完成

echo.
echo [5/5] 构建APK...
echo.

REM 检查是否安装了Android Studio的命令行工具
if exist "%ANDROID_HOME%\cmdline-tools" (
    echo 使用Android SDK构建...
    cd android
    call gradlew.bat assembleDebug
    if %errorlevel% neq 0 (
        echo [错误] APK构建失败
        echo 请检查Android SDK配置
        cd ..
        pause
        exit /b 1
    )
    
    REM 复制APK到D:\APP
    if exist "app\build\outputs\apk\debug\app-debug.apk" (
        mkdir D:\APP 2>nul
        copy "app\build\outputs\apk\debug\app-debug.apk" "D:\APP\血压守护.apk"
        echo.
        echo ======================================
        echo [成功] APK构建完成！
        echo 文件位置: D:\APP\血压守护.apk
        echo ======================================
    ) else (
        echo [错误] APK文件未找到
    )
    cd ..
) else (
    echo.
    echo [提示] 未检测到AndroidSDK，将打开Android Studio进行构建
    echo 请在Android Studio中点击 Build -> Build Bundle/APK -> Build APK
    echo.
    call npx cap open android
    echo.
    echo ======================================
    echo Android Studio已打开
    echo 请在Android Studio中完成构建后，手动复制APK到D:\APP
    echo ======================================
)

echo.
pause
