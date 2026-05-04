@echo off
chcp 65001 >nul
echo ==================================================
echo    血压守护项目 - 一键推送到GitHub
echo ==================================================
echo.

echo 请确认以下步骤：
echo   1. 您已创建新的GitHub Personal Access Token
echo   2. 您已将Token复制到剪贴板
echo.

set /p token="请粘贴您的新GitHub Token: "
echo.

echo 正在配置远程仓库...
git remote set-url origin https://guancheng7410:%token%@github.com/guancheng7410/xueyazngl.git

echo.
echo 正在推送代码...
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo ==================================================
    echo    ✅ 推送成功！
    echo ==================================================
    echo.
    echo 查看仓库: https://github.com/guancheng7410/xueyazngl
    echo.
) else (
    echo.
    echo ==================================================
    echo    ❌ 推送失败！
    echo ==================================================
    echo.
    echo 请检查：
    echo   1. Token是否正确
    echo   2. Token是否有 repo 权限
    echo   3. 网络连接是否正常
    echo.
)

pause
