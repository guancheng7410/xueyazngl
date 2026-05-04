# 血压守护APP - 原生打包指南

## 📱 使用 Capacitor 打包原生APP

### 环境要求

- Node.js >= 16
- npm >= 8
- Android Studio (Android打包)
- Xcode (iOS打包，仅macOS)

### 快速开始

```bash
# 1. 安装依赖
npm install

# 2. 构建web资源
npm run build

# 3. 初始化Android/iOS项目
npx cap add android
npx cap add ios

# 4. 同步代码到原生项目
npx cap sync

# 5. 打开Android Studio进行编译
npm run open:android

# 6. 打开Xcode进行编译
npm run open:ios
```

### 功能特性

- ✅ 全屏沉浸式体验
- ✅ 本地推送通知
- ✅ 离线数据存储
- ✅ 自动同步云端
- ✅ 相机访问（扫码）
- ✅ 文件共享（导出报告）
- ✅ 分享功能

### 目录结构

```
blood-pressure-guardian/
├── www/                    # Web资源目录（构建后）
│   ├── app_pro.html       # 主应用
│   ├── manifest_pro.json  # PWA配置
│   ├── sw_app.js          # Service Worker
│   ├── i18n.js           # 多语言
│   └── assets/           # 静态资源
├── android/               # Android原生项目
├── ios/                   # iOS原生项目
├── capacitor.config.json  # Capacitor配置
└── package.json           # npm配置
```

### 推送通知配置

#### Android

1. 创建Firebase项目
2. 下载`google-services.json`放到`android/app/`
3. 配置推送权限

#### iOS

1. 创建Apple Developer证书
2. 配置Push Notification capability
3. 上传APNs证书到Firebase

### 签名与发布

#### Android APK/AAB

```bash
cd android
./gradlew assembleRelease  # APK
./gradlew bundleRelease    # AAB
```

#### iOS IPA

1. 在Xcode中配置签名证书
2. Product -> Archive
3. Distribute App

### 常见问题

**Q: Android构建失败**
A: 确保Android SDK版本>=33，Gradle版本>=8

**Q: iOS构建失败**
A: 确保Xcode版本>=14，macOS版本>=12

**Q: 推送通知不工作**
A: 检查权限配置和证书是否正确
