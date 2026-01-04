# 构建APK说明

## 当前构建状态

构建过程正在进行中。首次构建需要：
1. 下载Android SDK和NDK（约2-3GB）
2. 安装系统依赖（automake等）
3. 编译Python和Kivy
4. 打包APK

**预计时间：30-60分钟**（取决于网络速度）

## 检查构建状态

运行以下命令查看构建进度：

```bash
./check_build_status.sh
```

或者查看实时日志：

```bash
tail -f build.log
```

## 常见问题解决

### 1. JDK问题

如果遇到JDK相关错误，确保已安装JDK：

```bash
# macOS
brew install openjdk@11

# 设置JAVA_HOME
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
```

### 2. 系统依赖

macOS上可能需要安装以下依赖：

```bash
brew install autoconf automake libtool pkg-config
brew install libffi openssl
```

### 3. 构建失败

如果构建失败，可以：

1. 清理构建缓存：
```bash
buildozer android clean
```

2. 重新构建：
```bash
./build_apk.sh
```

## 构建完成后

APK文件将位于 `bin/` 目录下，文件名类似：
- `scoreapp-0.1-arm64-v8a_armeabi-v7a-debug.apk`

可以将此APK文件安装到Android设备上进行测试。

