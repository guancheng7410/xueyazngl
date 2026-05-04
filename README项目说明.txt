========================================
血压守护APP - D:\APP 目录说明
========================================

【当前文件清单】

1. 血压守护APP下载安装操作手册.html
   - 完整的图文安装教程
   - 包含3种安装方式的详细步骤
   - 双击即可在浏览器中查看

2. 血压守护APK构建指南.txt
   - APK构建的详细步骤
   - 包含环境要求和配置方法

3. README_安装说明.txt（本文件）
   - 快速入门指南

【如何获取APK？】

当前电脑缺少Android开发环境（Java JDK + Android SDK），
需要安装后才能构建APK。

推荐方案（按简单到复杂）：

方案一：HBuilderX云打包（最简单，5分钟）
----------------------------------------
1. 下载 HBuilderX（12MB）
   https://www.dcloud.io/hbuilderx.html

2. 解压后运行 HBuilderX.exe

3. 文件 -> 导入 -> 从本地目录导入
   选择：E:\开发需要\blood-pressure-guardian\www

4. 右键项目 -> 发行 -> 原生App-云打包

5. 选择Android，点击"打包"

6. 等待3-5分钟，APK自动下载

7. 将APK复制到此目录：D:\APP\血压守护.apk


方案二：安装完整开发环境（30分钟）
----------------------------------------
步骤1：安装Java JDK
   下载：https://adoptium.net/
   选择 JDK 17，下载.exe安装文件
   运行安装程序，一路"下一步"

步骤2：安装Android Studio
   下载：https://developer.android.com/studio
   运行安装程序
   首次启动会自动下载Android SDK（约2GB）

步骤3：构建APK
   打开命令行，依次执行：
   
   cd E:\开发需要\blood-pressure-guardian
   自动构建APK.bat
   
   或在Android Studio中：
   npx cap open android
   Build -> Build APK


方案三：使用PWA方式（无需APK，3分钟）
----------------------------------------
1. 双击运行：E:\开发需要\blood-pressure-guardian\安装到手机.bat

2. 在手机浏览器访问显示的网址

3. 点击"添加到主屏幕"

4. 完成！像APP一样使用


【自动化脚本说明】

E:\开发需要\blood-pressure-guardian\目录下有：

1. 检查环境.bat
   - 检查是否已安装所有必要环境
   - 运行后显示环境状态

2. 自动构建APK.bat
   - 自动检查环境
   - 自动安装依赖
   - 自动构建APK
   - 自动复制到D:\APP


【操作手册】

双击打开：血压守护APP下载安装操作手册.html

包含完整图文教程，建议打印或保存PDF备用。


【技术支持】

如遇问题，请查看：
- 操作手册第十章：常见问题解答
- APK构建指南.txt

========================================
血压守护 版本2.0.0
========================================
