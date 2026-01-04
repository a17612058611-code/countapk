# macOS APK构建修复说明

## ✅ 已修复的问题

1. **JDK检测问题** - ✅ 已解决
   - 在 `buildozer.spec` 中设置了 `android.java_home`
   - 使用 `/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home`
   - JDK现在可以被正确检测到

2. **证书问题** - ✅ 已处理
   - 检查并处理了证书文件问题
   - 设置了环境变量避免证书验证错误

## 🚀 使用方法

### 方法1：使用修复后的脚本（推荐）

```bash
./build_apk_macos.sh
```

这个脚本会自动：
- 设置正确的JAVA_HOME
- 处理证书问题
- 清理旧构建
- 开始新的构建

### 方法2：手动构建

```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 设置环境变量
export JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
export PATH="$JAVA_HOME/bin:$PATH"
export P4A_ALLOW_PREREQUISITES=1
export ANDROID_ACCEPT_SDK_LICENSE=1

# 3. 开始构建
yes | buildozer android debug
```

## 📊 监控构建进度

```bash
# 查看实时日志
tail -f build.log

# 或使用状态检查脚本
./check_build_status.sh
```

## ⏱️ 预计时间

- 首次构建：30-60分钟
- 后续构建：10-20分钟（如果只修改了代码）

## 📦 构建完成后

APK文件将位于 `bin/` 目录：
- `scoreapp-0.1-arm64-v8a_armeabi-v7a-debug.apk`

## 🔧 如果遇到问题

1. **JDK问题**：
   ```bash
   brew install openjdk@17
   ```

2. **查看详细错误**：
   ```bash
   tail -100 build.log
   ```

3. **清理重建**：
   ```bash
   buildozer android clean
   ./build_apk_macos.sh
   ```

## ✅ 当前状态

构建正在进行中！JDK已被正确检测，所有依赖都已满足。

