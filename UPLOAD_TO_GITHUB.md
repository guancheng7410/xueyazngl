# 📦 血压守护项目 - GitHub上传完整指南

## ⚠️ GitHub Token已失效

您之前提供的Token已失效或被删除。

---

## 🔑 第一步：创建新的Personal Access Token

1. **访问**: https://github.com/settings/tokens
2. **点击**: "Generate new token" → "Generate new token (classic)"
3. **设置**:
   - Note: 血压守护项目
   - Expiration: 7 days (或根据需要)
   - 勾选: `repo` (完整仓库权限)
4. **生成并复制**新Token (格式: `ghp_xxxxxxxxxxxxx`)

---

## 🚀 第二步：在本地电脑上传代码

### 方法1: 使用Git命令

```bash
# 1. 确保项目文件在本地
cd /path/to/blood-pressure-guardian

# 2. 初始化Git（如果还没有）
git init

# 3. 添加远程仓库
git remote add origin https://github.com/guancheng7410/xueyazngl.git

# 4. 添加所有文件
git add .

# 5. 提交
git commit -m "血压守护项目完整版本 v2.0.0"

# 6. 使用新Token推送（替换YOUR_NEW_TOKEN）
git push https://guancheng7410:YOUR_NEW_TOKEN@github.com/guancheng7410/xueyazngl.git main
```

### 方法2: 使用GitHub Desktop（最简单）

1. 下载: https://desktop.github.com/
2. 登录GitHub账号
3. File → Add Local Repository → 选择项目目录
4. Publish repository → 推送到 `guancheng7410/xueyazngl`

---

## 📋 项目状态

- ✅ 所有代码已准备好
- ✅ BUG已修复（4个）
- ✅ 测试已通过（35/35）
- ✅ 敏感信息已清理
- ✅ .gitignore已更新
- ⏳ 等待新Token后上传

---

## 💡 提示

1. **创建新Token** 是必须的步骤
2. 推荐使用 **GitHub Desktop** 最简单
3. Token创建后请立即使用，避免过期
