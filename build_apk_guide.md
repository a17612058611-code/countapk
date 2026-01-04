# APK打包指南

## 当前状态

APK打包正在进行中。首次打包需要较长时间（30-60分钟），因为需要：
1. 下载Android SDK和NDK（约2-3GB）
2. 编译Python和Kivy
3. 打包APK

## 检查构建进度

```bash
# 查看实时日志
tail -f build.log

# 或使用状态检查脚本
./check_build_status.sh
```

## 构建完成后

APK文件将位于 `bin/` 目录下，文件名类似：
- `scoreapp-0.1-arm64-v8a_armeabi-v7a-debug.apk`

## 常见问题

### 1. 构建失败

如果构建失败，可以：

```bash
# 清理构建缓存
buildozer android clean

# 重新构建
buildozer android debug
```

### 2. JDK问题

如果遇到JDK相关错误：

```bash
# macOS上安装JDK
brew install openjdk@11

# 设置JAVA_HOME
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
```

### 3. 在macOS上构建

macOS上构建Android APK可能会有一些问题，建议：
- 使用Linux系统（WSL2或虚拟机）
- 或使用云构建服务

## 安装APK到设备

```bash
# 通过ADB安装
adb install bin/scoreapp-0.1-*-debug.apk

# 或直接传输到设备后安装
```

