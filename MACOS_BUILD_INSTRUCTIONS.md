# macOS APK构建完整指南

## 🔧 前置步骤

### 1. 安装JDK 17

```bash
brew install openjdk@17
```

### 2. 设置JDK系统识别

python-for-android需要通过`/usr/libexec/java_home`检测JDK，需要创建符号链接：

```bash
# 运行设置脚本（需要sudo权限）
./setup_jdk.sh

# 或手动执行：
sudo ln -sfn /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk
```

### 3. 验证JDK检测

```bash
/usr/libexec/java_home -V
```

应该能看到openjdk-17。

## 🚀 开始构建

### 方法1：使用自动化脚本（推荐）

```bash
./build_apk_macos.sh
```

### 方法2：手动构建

```bash
source venv/bin/activate
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
export P4A_ALLOW_PREREQUISITES=1
export ANDROID_ACCEPT_SDK_LICENSE=1
yes | buildozer android debug
```

## 📊 监控构建

```bash
# 实时查看日志
tail -f build.log

# 检查构建状态
./check_build_status.sh
```

## ⚠️ 已知问题

### 问题1：JDK检测失败

**症状**：`[ERROR]: Prerequisite JDK is not met`

**解决**：
1. 确保已运行 `./setup_jdk.sh`
2. 验证：`/usr/libexec/java_home -V` 应该显示JDK 17
3. 如果仍失败，尝试：
   ```bash
   export JAVA_HOME=$(/usr/libexec/java_home -v 17)
   export PATH="$JAVA_HOME/bin:$PATH"
   ```

### 问题2：证书验证错误

**症状**：`curl: (77) error setting certificate verify locations`

**解决**：
```bash
# 检查并备份证书文件
if [ -f ~/Downloads/cacert.pem ]; then
    mv ~/Downloads/cacert.pem ~/Downloads/cacert.pem.bak
fi

# 清除证书环境变量
unset CURL_CA_BUNDLE
unset SSL_CERT_FILE
```

### 问题3：AAB支持要求

**症状**：`This buildozer version requires a python-for-android version with AAB support`

**解决**：
- 已在 `buildozer.spec` 中设置 `android.debug_artifact = apk`
- 如果仍出现，可能需要更新buildozer或python-for-android

## ✅ 构建成功标志

构建完成后，会在 `bin/` 目录下生成APK文件：
```
bin/scoreapp-0.1-arm64-v8a_armeabi-v7a-debug.apk
```

## 📱 安装到设备

```bash
# 通过ADB安装
adb install bin/scoreapp-0.1-*-debug.apk

# 或直接传输到设备后手动安装
```

## 🆘 需要帮助？

如果遇到其他问题：
1. 查看完整日志：`tail -100 build.log`
2. 清理重建：`buildozer android clean && ./build_apk_macos.sh`
3. 考虑使用GitHub Actions自动构建（更稳定）

