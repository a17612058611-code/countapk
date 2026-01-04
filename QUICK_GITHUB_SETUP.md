# 快速设置GitHub Actions

## 一键设置步骤

### 1. 初始化Git仓库（如果还没有）

```bash
git init
git add .
git commit -m "Initial commit: 每日分数记录Android应用"
```

### 2. 在GitHub创建仓库

1. 访问 https://github.com/new
2. 创建新仓库（例如：countapk）
3. **不要**初始化README、.gitignore或license

### 3. 推送代码

```bash
git remote add origin https://github.com/你的用户名/countapk.git
git branch -M main
git push -u origin main
```

### 4. 触发构建

1. 打开 https://github.com/你的用户名/countapk/actions
2. 点击 "Build Android APK"
3. 点击 "Run workflow" → "Run workflow"

### 5. 等待构建完成（30-60分钟）

### 6. 下载APK

在Actions页面底部，点击 "scoreapp-apk" 下载

## 完成！

现在每次推送代码都会自动构建APK 🎉
