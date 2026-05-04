# 血压守护 APK 安装指南

## 方式一：PWA 安装（推荐，无需APK）

### 在手机上安装
1. 将 `www` 文件夹部署到任意 HTTP 服务器
2. 在手机浏览器中打开网址
3. 点击浏览器菜单中的"添加到主屏幕"
4. 即可像原生APP一样使用

### 在电脑上测试
1. 双击 `启动本地服务器.bat`
2. 浏览器自动打开应用

## 方式二：构建 Android APK

### 环境要求
- Node.js 14+ (https://nodejs.org/)
- Java JDK 11+ (https://adoptium.net/)
- Android SDK (通过Android Studio安装)

### 构建步骤

#### 方法A：使用构建脚本（推荐）
1. 双击运行 `BUILD_APK.bat`
2. 按照提示完成构建
3. APK 将自动复制到 `D:\APP\血压守护.apk`

#### 方法B：手动构建
```bash
# 1. 安装依赖
npm install

# 2. 添加 Android 平台
npx cap add android

# 3. 同步项目
npx cap sync android

# 4. 打开 Android Studio
npx cap open android

# 5. 在 Android Studio 中：
#    Build -> Build Bundle/APK -> Build APK

# 6. APK 位置：
# android/app/build/outputs/apk/debug/app-debug.apk
```

### 安装到手机
1. 将 APK 复制到手机
2. 允许安装未知来源应用
3. 点击 APK 文件进行安装

## 方式三：使用 HBuilderX 打包（最简单）

1. 下载 HBuilderX：https://www.dcloud.io/hbuilderx.html
2. 导入 `www` 文件夹
3. 发行 -> 原生App-云打包
4. 选择 Android
5. 等待云端打包完成
6. 下载 APK 并安装

## 功能说明

### 已实现功能
- ✅ 药物管理与服药提醒
- ✅ 血压记录与趋势图表
- ✅ 家庭成员协同管理
- ✅ 本地数据存储
- ✅ 离线使用支持
- ✅ 数据导出功能

### 数据存储
- 所有数据存储在浏览器 localStorage
- 可通过"导出数据"功能备份
- 支持导入备份数据

## 常见问题

Q: 为什么构建APK失败？
A: 请确保已安装 Java JDK 和 Android SDK

Q: 数据会丢失吗？
A: 只要不清除浏览器数据，数据不会丢失

Q: 可以多设备同步吗？
A: 当前为单机版，暂不支持云端同步

## 技术支持
如有问题，请查看项目文档或联系开发者。
