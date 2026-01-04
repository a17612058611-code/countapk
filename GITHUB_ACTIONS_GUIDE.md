# GitHub Actions 自动构建 APK 指南

## 🚀 快速开始

### 步骤1：将项目推送到GitHub

如果还没有GitHub仓库，先创建一个：

```bash
# 初始化git仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: 每日分数记录应用"

# 在GitHub上创建新仓库，然后：
git remote add origin https://github.com/a17612058611-code/countapk.git
git branch -M main
git push -u origin main
```

### 步骤2：触发构建

有两种方式触发构建：

#### 方式1：手动触发（推荐首次使用）

1. 打开GitHub仓库页面：https://github.com/a17612058611-code/countapk
2. 点击 **Actions** 标签页
3. 在左侧选择 **Build Android APK**
4. 点击 **Run workflow** 按钮
5. 选择分支（通常是 `main`）
6. 点击绿色的 **Run workflow** 按钮

#### 方式2：自动触发

当你推送代码到 `main` 或 `master` 分支时，会自动触发构建。

### 步骤3：查看构建进度

1. 在 **Actions** 标签页中，点击正在运行的workflow
2. 点击 **build** job查看详细日志
3. 构建通常需要 **30-60分钟**

### 步骤4：下载APK

构建完成后：

1. 在workflow页面，滚动到底部
2. 在 **Artifacts** 部分，点击 **scoreapp-apk**
3. 下载ZIP文件
4. 解压后即可获得APK文件

## 📋 构建配置说明

### 触发条件

- **手动触发**：随时可以在Actions页面手动运行
- **自动触发**：当以下文件更改时自动构建：
  - `*.py` - Python源代码
  - `*.spec` - Buildozer配置
  - `requirements.txt` - 依赖列表
  - `.github/workflows/build_apk.yml` - 工作流配置

### 构建环境

- **操作系统**：Ubuntu Latest
- **Python版本**：3.10
- **JDK版本**：11
- **超时时间**：120分钟

### 输出文件

- APK文件位于 `bin/` 目录
- 构建成功后自动上传到Artifacts
- Artifacts保留30天

## 🔧 故障排除

### 构建失败

1. **查看日志**：在Actions页面点击失败的workflow，查看详细错误
2. **常见问题**：
   - 依赖下载失败：网络问题，重试即可
   - 编译错误：检查代码是否有语法错误
   - 超时：构建时间超过120分钟，可能需要优化配置

### 重新构建

如果构建失败，可以：
1. 修复问题后推送新代码（自动触发）
2. 或手动点击 **Run workflow** 重新运行

## 📱 安装APK到设备

### 方法1：通过ADB

```bash
# 连接Android设备
adb devices

# 安装APK
adb install scoreapp-0.1-*-debug.apk
```

### 方法2：直接安装

1. 将APK文件传输到Android设备
2. 在设备上打开文件管理器
3. 点击APK文件进行安装
4. 如果提示"未知来源"，需要在设置中允许安装

## ✅ 优势

使用GitHub Actions构建的优势：

1. **无需本地配置**：不需要在本地安装Android SDK/NDK
2. **自动化**：代码推送后自动构建
3. **稳定环境**：Linux环境，避免macOS的各种问题
4. **免费**：GitHub Actions对公开仓库免费
5. **可追溯**：所有构建历史都有记录

## 📝 注意事项

1. **首次构建较慢**：需要下载Android SDK/NDK（约2-3GB），可能需要30-60分钟
2. **后续构建较快**：如果只修改了代码，通常10-20分钟
3. **Artifacts保留**：构建产物保留30天，记得及时下载
4. **私有仓库**：私有仓库有使用限制，但通常足够使用

## 🎯 下一步

1. 将代码推送到GitHub
2. 在Actions页面手动触发构建
3. 等待构建完成
4. 下载APK文件
5. 安装到Android设备测试

祝你构建顺利！🎉

