# 开发文档

本文档包含开发环境配置、构建说明、故障排除等开发相关的所有信息。

## 目录

- [构建APK](#构建apk)
- [macOS构建指南](#macos构建指南)
- [Android兼容性修复](#android兼容性修复)
- [字体问题修复](#字体问题修复)
- [故障排除](#故障排除)
- [GitHub Actions](#github-actions)


# Readme Build

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
./tools/check_build_status.sh
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
./tools/build_apk.sh
```

## 构建完成后

APK文件将位于 `bin/` 目录下，文件名类似：
- `scoreapp-0.1-arm64-v8a_armeabi-v7a-debug.apk`

可以将此APK文件安装到Android设备上进行测试。
---

# Macos Build Instructions

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
./tools/setup_jdk.sh

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
./tools/build_apk_macos.sh
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
./tools/check_build_status.sh
```

## ⚠️ 已知问题

### 问题1：JDK检测失败

**症状**：`[ERROR]: Prerequisite JDK is not met`

**解决**：
1. 确保已运行 `./tools/setup_jdk.sh`
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
2. 清理重建：`buildozer android clean && ./tools/build_apk_macos.sh`
3. 考虑使用GitHub Actions自动构建（更稳定）
---

# Macos Build Fixed

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
./tools/build_apk_macos.sh
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
./tools/check_build_status.sh
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
   ./tools/build_apk_macos.sh
   ```

## ✅ 当前状态

构建正在进行中！JDK已被正确检测，所有依赖都已满足。
---

# Android Fix

# Android 兼容性修复说明

## 修复内容

### 1. 中文字体显示问题 ✅

**问题**：在Android上中文显示为"XXXX"

**解决方案**：
- 检测Android平台，使用系统默认字体（Android系统字体通常支持中文）
- 在Android上不强制设置`font_name`，让Kivy使用系统默认字体
- Android系统通常包含DroidSansFallback或NotoSansCJK字体，这些字体支持中文

**技术实现**：
```python
# 检测Android平台
is_android = os.path.exists('/system/build.prop') or 'ANDROID_ARGUMENT' in os.environ

# 在Android上不设置font_name，使用系统默认字体
if CHINESE_FONT and not is_android:
    label.font_name = CHINESE_FONT
```

### 2. 布局优化 ✅

**问题**：布局在手机上显示不佳，元素太大或太小

**解决方案**：
- 根据平台自动调整布局参数（padding、spacing、字体大小）
- 添加ScrollView支持滚动，适应小屏幕
- 优化控件高度和字体大小

**Android布局参数**：
- `padding`: 10（桌面：20）
- `spacing`: 8（桌面：15）
- `title_font_size`: 20（桌面：24）
- `normal_font_size`: 14（桌面：18）
- `label_height`: 35（桌面：40）
- `input_height`: 45（桌面：50）
- `button_height`: 45（桌面：50）

**主要改进**：
1. 主布局使用ScrollView包装，支持滚动
2. 所有控件高度和字体大小根据平台自适应
3. 弹窗大小在Android上更大（0.95 vs 0.8）
4. 历史记录弹窗在Android上占满屏幕（0.9高度）

## 测试建议

1. **本地测试**（桌面）：
   ```bash
   ./tools/run_app.sh
   ```
   应该正常显示，布局较大

2. **Android测试**：
   - 重新打包APK
   - 安装到Android设备
   - 检查：
     - ✅ 中文是否正常显示（不再是XXXX）
     - ✅ 布局是否适合手机屏幕
     - ✅ 是否可以滚动查看所有内容
     - ✅ 输入框和按钮大小是否合适

## 技术细节

### Android字体检测
```python
is_android = os.path.exists('/system/build.prop') or 'ANDROID_ARGUMENT' in os.environ
```

### ScrollView实现
```python
# 主布局容器
root = BoxLayout(orientation='vertical')
scroll = ScrollView(size_hint=(1, 1))
scroll.add_widget(main_layout)
root.add_widget(scroll)
```

### 自适应布局
所有布局参数都根据`is_android`标志动态调整，确保在不同平台上都有良好的显示效果。

## 下一步

1. 重新构建APK：
   ```bash
   # 通过GitHub Actions构建
   git add .
   git commit -m "修复Android中文字体和布局问题"
   git push
   ```

2. 测试APK：
   - 下载构建好的APK
   - 安装到Android设备
   - 验证修复效果

## 注意事项

- Android系统字体支持中文，不需要额外打包字体文件
- 如果某些Android设备仍然显示乱码，可能需要考虑打包字体文件
- 布局参数可以根据实际测试结果进一步微调
---

# Android Font Fix

# Android 字体显示问题最终解决方案

## 问题

在Android设备上，即使打包了字体文件，中文仍然无法显示。

## 根本原因

1. **字体文件可能没有正确打包到APK**
2. **Android上访问assets目录的路径问题**
3. **Kivy在Android上需要使用资源系统访问assets**

## 解决方案

### 1. 确保字体文件被打包

检查 `buildozer.spec` 文件，确保包含：
```ini
source.include_exts = py,png,jpg,kv,atlas,json,ttf,otf
source.include_patterns = assets/fonts/*
```

### 2. 字体文件放置位置

字体文件必须放在 `assets/fonts/` 目录：
```
assets/
  fonts/
    SourceHanSansCN-Regular.otf  (或其他中文字体)
```

### 3. 代码改进

代码已经更新，现在：
- 使用 `resource_find` 在Android上查找字体资源
- 使用 `resource_add_path` 添加资源路径
- 自动回退到系统字体（如果可用）

### 4. 如果仍然无法显示

#### 选项A：下载并添加字体文件（推荐）

1. **下载思源黑体**：
   ```bash
   # 访问 https://github.com/adobe-fonts/source-han-sans/releases
   # 下载 SourceHanSansCN.zip
   # 解压后找到 SourceHanSansCN-Regular.otf
   ```

2. **放置字体文件**：
   ```bash
   mkdir -p assets/fonts
   cp SourceHanSansCN-Regular.otf assets/fonts/
   ```

3. **提交并构建**：
   ```bash
   git add assets/fonts/
   git commit -m "添加中文字体文件"
   git push
   ```

#### 选项B：使用英文版本

如果无法添加字体文件，应用会自动切换到英文版本，确保可用性。

## 验证步骤

1. **检查字体文件是否存在**：
   ```bash
   ls -la assets/fonts/
   ```

2. **检查buildozer.spec配置**：
   ```bash
   grep -A 2 "source.include" buildozer.spec
   ```

3. **构建APK并测试**：
   - 通过GitHub Actions构建
   - 安装到Android设备
   - 查看日志输出（使用logcat或adb logcat）

4. **查看应用日志**：
   ```bash
   adb logcat | grep -i font
   ```
   应该看到：
   ```
   中文字体已注册: assets/fonts/...
   Kivy默认字体已设置为: ChineseFont
   ```

## 调试技巧

1. **检查APK内容**：
   ```bash
   # 解压APK
   unzip app.apk -d apk_content
   # 检查assets目录
   ls -la apk_content/assets/
   ```

2. **运行时检查**：
   应用启动时会打印字体注册信息，检查日志确认字体是否成功加载。

3. **如果字体未加载**：
   - 应用会自动使用英文界面
   - 所有文本都会显示为英文，确保应用可用

## 常见问题

### Q: 字体文件太大怎么办？
A: 可以使用字体子集工具，只包含常用汉字，减小文件大小到2-5MB。

### Q: 构建后字体仍然不显示？
A: 
1. 确认字体文件在 `assets/fonts/` 目录
2. 确认 `buildozer.spec` 配置正确
3. 检查构建日志，确认字体文件被打包
4. 查看运行时日志，确认字体是否成功注册

### Q: 可以只使用英文版本吗？
A: 可以。如果没有字体文件或字体加载失败，应用会自动使用英文版本。

## 最终建议

1. **优先添加字体文件**：下载思源黑体或Noto Sans CJK，放到 `assets/fonts/` 目录
2. **确保配置正确**：检查 `buildozer.spec` 中的字体文件包含配置
3. **如果无法添加字体**：应用会自动使用英文版本，功能完全可用
---

# Font Fix

# 中文字体显示问题修复说明

## 问题描述

应用界面中的中文文字显示为 "XXXX" 或乱码，这是因为 Kivy 默认字体不支持中文字符。

## 解决方案

已为应用添加了中文字体支持：

1. **自动检测系统字体**：根据操作系统自动选择合适的中文字体
   - macOS: PingFang SC（苹方）
   - Windows: Microsoft YaHei（微软雅黑）
   - Linux/Android: Noto Sans CJK SC

2. **统一字体配置**：所有文本组件（Label、Button、TextInput、Popup）都使用中文字体

3. **兼容性处理**：如果系统字体不可用，会回退到默认字体

## 测试方法

运行应用查看中文是否正常显示：

```bash
./tools/run_app.sh
```

如果中文仍然显示为 "XXXX"，请检查：

1. **确认虚拟环境已激活**
   ```bash
   source venv/bin/activate
   ```

2. **检查字体是否识别**
   ```bash
   python -c "from main import CHINESE_FONT; print('字体:', CHINESE_FONT)"
   ```

3. **重新运行应用**
   ```bash
   python main.py
   ```

## Android APK 字体支持

在 Android 上，应用会自动使用系统默认的中文字体（通常是 Noto Sans CJK SC 或 Droid Sans Fallback）。如果 Android 设备上没有中文字体，可能需要：

1. 在 `buildozer.spec` 中添加字体文件
2. 或使用包含中文字体的字体文件

## 技术细节

- 使用 `font_name` 属性为每个文本组件指定字体
- 通过 `platform.system()` 检测操作系统
- 使用 `Config.set()` 设置 Kivy 默认字体（可选）
---

# Chinese Font Setup

# Android 中文字体设置指南

## 问题说明

在Android设备上，Kivy应用可能无法正确显示中文，因为系统默认字体可能不支持中文字符。解决方案是打包一个支持中文的字体文件到APK中。

## 解决方案

### 方法1：使用思源黑体（推荐）

1. **下载思源黑体**
   - 访问：https://github.com/adobe-fonts/source-han-sans/releases
   - 下载 `SourceHanSansCN.zip`（简体中文版本）
   - 解压后找到 `SourceHanSansCN-Regular.otf` 或 `.ttf` 文件

2. **放置字体文件**
   ```bash
   # 创建字体目录
   mkdir -p assets/fonts
   
   # 将字体文件复制到 assets/fonts/ 目录
   cp SourceHanSansCN-Regular.otf assets/fonts/
   ```

3. **重新构建APK**
   - 字体文件会自动包含在APK中
   - 运行构建命令或通过GitHub Actions构建

### 方法2：使用Noto Sans CJK

1. **下载Noto Sans CJK**
   - 访问：https://www.google.com/get/noto/
   - 搜索 "Noto Sans CJK SC"
   - 下载并解压

2. **放置字体文件**
   ```bash
   mkdir -p assets/fonts
   cp NotoSansCJK-Regular.ttf assets/fonts/
   ```

### 方法3：使用其他中文字体

任何支持中文的 `.ttf` 或 `.otf` 字体文件都可以使用：

1. 将字体文件放到 `assets/fonts/` 目录
2. 确保文件名匹配代码中查找的字体名称，或修改 `main.py` 中的字体路径

## 代码说明

应用会自动查找以下字体文件（按优先级）：
- `assets/fonts/SourceHanSansCN-Regular.otf`
- `assets/fonts/SourceHanSansCN-Regular.ttf`
- `assets/fonts/NotoSansCJK-Regular.ttf`
- `assets/fonts/NotoSansCJK-Regular.otf`
- `assets/fonts/DroidSansFallback.ttf`

如果找到字体文件，会自动注册并在所有文本组件中使用。

## 验证字体是否生效

1. **检查字体文件是否存在**
   ```bash
   ls -la assets/fonts/
   ```

2. **运行应用测试**
   ```bash
   ./tools/run_app.sh
   ```
   查看控制台输出，应该看到：
   ```
   中文字体已注册: assets/fonts/SourceHanSansCN-Regular.otf
   Kivy默认字体已设置为: ChineseFont
   ```

3. **构建APK并测试**
   - 通过GitHub Actions构建APK
   - 安装到Android设备
   - 检查中文是否正常显示

## 常见问题

### Q: 字体文件太大怎么办？
A: 可以使用字体子集工具，只包含需要的字符，减小文件大小。

### Q: 构建后字体仍然不显示？
A: 检查：
1. 字体文件是否在 `assets/fonts/` 目录
2. `buildozer.spec` 中是否包含 `source.include_exts = py,png,jpg,kv,atlas,json,ttf,otf`
3. 构建日志中是否有字体相关的错误

### Q: 可以使用系统字体吗？
A: 理论上可以，但不同Android设备的系统字体不同，有些可能不支持中文。打包字体文件是最可靠的方法。

## 快速开始

1. **下载字体**（选择一个）：
   ```bash
   # 使用wget下载思源黑体（需要手动解压）
   wget https://github.com/adobe-fonts/source-han-sans/releases/download/2.004R/SourceHanSansCN.zip
   unzip SourceHanSansCN.zip
   ```

2. **复制字体文件**：
   ```bash
   mkdir -p assets/fonts
   # 找到解压后的Regular字体文件并复制
   cp <解压目录>/SourceHanSansCN-Regular.otf assets/fonts/
   ```

3. **提交并构建**：
   ```bash
   git add assets/fonts/
   git commit -m "添加中文字体文件"
   git push
   ```

4. **等待GitHub Actions构建完成**

## 字体文件大小参考

- 思源黑体 Regular: ~15-20MB
- Noto Sans CJK Regular: ~15-20MB
- 字体子集（仅常用汉字）: ~2-5MB

建议使用字体子集以减小APK大小。
---

# Pyjnius Fix

# Pyjnius 编译错误修复

## 问题描述

构建失败，错误信息：
- `clang-14: error: no such file or directory: 'jnius/jnius.c'`
- `Error compiling Cython file`
- `pyjnius first build failed`

## 可能的原因

1. **python-for-android版本问题** - 可能需要特定版本
2. **Cython版本不兼容** - 需要兼容的Cython版本
3. **NDK工具链问题** - clang编译器配置问题
4. **依赖缺失** - pyjnius的依赖未正确安装

## 已应用的修复

1. **明确指定bootstrap**
   ```spec
   p4a.bootstrap = sdl2
   ```

2. **明确指定分支**
   ```spec
   p4a.branch = master
   ```

3. **添加调试环境变量**
   ```yaml
   export NDK_DEBUG=1
   export P4A_DEBUG=1
   ```

## 如果仍然失败

### 方案1：指定python-for-android版本

在buildozer.spec中添加：
```spec
# 使用稳定版本
p4a.branch = release-2024.01.21
```

### 方案2：添加pyjnius到requirements

如果pyjnius需要单独安装，可以在requirements中添加：
```spec
requirements = python3,kivy,pyjnius
```

### 方案3：使用预编译的pyjnius

某些情况下，可能需要使用预编译的版本。

## 调试建议

1. 查看完整的build.log文件
2. 检查Cython版本是否兼容
3. 查看python-for-android的GitHub issues
4. 尝试使用不同的NDK版本
---

# Ubuntu 24 Fix

# Ubuntu 24.04 构建修复

## 问题

在 Ubuntu 24.04 (Noble) 中，`libtinfo5` 包已被移除，导致依赖安装失败。

## 解决方案

已从依赖列表中移除 `libtinfo5`，并添加 `libtinfo6` 作为替代（如果需要）。

## 修复内容

```yaml
# 之前（会失败）
libtinfo5

# 现在（已修复）
# libtinfo5 已移除
# 如果需要，会自动安装 libtinfo6
```

## 验证

构建应该能够成功安装所有系统依赖。

如果还有其他依赖问题，请检查：
1. 包名是否正确
2. 包是否在 Ubuntu 24.04 中可用
3. 是否有替代包
---

# Github Actions Guide

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
---

# Quick Github Setup

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
git remote add origin https://github.com/a17612058611-code/countapk.git
git branch -M main
git push -u origin main
```

### 4. 触发构建

1. 打开 https://github.com/a17612058611-code/countapk/actions
2. 点击 "Build Android APK"
3. 点击 "Run workflow" → "Run workflow"

### 5. 等待构建完成（30-60分钟）

### 6. 下载APK

在Actions页面底部，点击 "scoreapp-apk" 下载

## 完成！

现在每次推送代码都会自动构建APK 🎉
---

# Push To Github

# 推送到GitHub仓库

## 仓库信息

- **仓库地址**: https://github.com/a17612058611-code/countapk
- **状态**: 已配置远程仓库
- **分支**: main

## 推送步骤

### 方法1：使用HTTPS（推荐首次使用）

```bash
git push -u origin main
```

如果提示输入用户名和密码：
- **用户名**: 你的GitHub用户名
- **密码**: 使用Personal Access Token（不是GitHub密码）

### 方法2：使用SSH（如果已配置SSH密钥）

```bash
# 先更改远程URL为SSH
git remote set-url origin git@github.com:a17612058611-code/countapk.git

# 然后推送
git push -u origin main
```

## 创建Personal Access Token（如果需要）

如果使用HTTPS推送，需要创建Personal Access Token：

1. 访问 https://github.com/settings/tokens
2. 点击 **Generate new token (classic)**
3. 设置名称（如：countapk-push）
4. 选择权限：至少需要 `repo` 权限
5. 点击 **Generate token**
6. **复制token**（只显示一次！）
7. 推送时，密码处输入这个token

## 推送后操作

### 1. 触发GitHub Actions构建

推送完成后：

1. 访问 https://github.com/a17612058611-code/countapk/actions
2. 点击 **Build Android APK** workflow
3. 点击 **Run workflow** → **Run workflow**
4. 等待构建完成（30-60分钟）

### 2. 下载APK

构建完成后：
1. 在Actions页面找到完成的构建
2. 滚动到底部
3. 点击 **scoreapp-apk** 下载APK文件

## 当前状态

✅ Git仓库已初始化
✅ 远程仓库已配置
✅ 文件已添加到暂存区
✅ 提交已创建
✅ 分支已设置为main

**下一步**: 运行 `git push -u origin main` 推送代码

## 验证推送

推送成功后，访问 https://github.com/a17612058611-code/countapk 应该能看到所有文件。
---

# Troubleshooting

# GitHub Actions 构建故障排除

## 常见错误和解决方案

### 错误：Process completed with exit code 100

**原因**：buildozer构建过程中出现错误

**排查步骤**：

1. **查看构建日志**
   - 在GitHub Actions页面，点击失败的workflow
   - 查看"Build APK"步骤的详细日志
   - 查找ERROR或WARNING信息

2. **常见问题**：

   **问题1：依赖下载失败**
   ```
   ERROR: Failed to download...
   ```
   - **解决**：网络问题，重试构建即可
   - 首次构建需要下载大量依赖（2-3GB）

   **问题2：Python语法错误**
   ```
   SyntaxError: invalid syntax
   ```
   - **解决**：检查代码语法
   - 在本地运行：`python -m py_compile main.py`

   **问题3：缺少依赖**
   ```
   ModuleNotFoundError: No module named 'xxx'
   ```
   - **解决**：检查requirements.txt
   - 确保所有依赖都已列出

   **问题4：Android SDK/NDK下载失败**
   ```
   Failed to download Android SDK/NDK
   ```
   - **解决**：重试构建
   - 首次构建需要下载大量文件

   **问题5：内存不足**
   ```
   Out of memory
   ```
   - **解决**：GitHub Actions默认2GB内存
   - 可能需要优化构建过程

3. **本地测试**

   在本地测试构建可以帮助定位问题：

   ```bash
   # 在Linux环境（WSL2或虚拟机）中
   sudo apt-get update
   sudo apt-get install -y python3-pip buildozer
   buildozer android debug
   ```

### 错误：APK文件未找到

**原因**：构建过程中断或失败

**解决**：
- 查看构建日志找出失败原因
- 检查是否有部分文件生成
- 重新运行构建

### 优化建议

1. **增加超时时间**（已在配置中设置为120分钟）
2. **添加缓存**（可选，加快后续构建）
3. **分步构建**（如果构建时间过长）

## 获取帮助

如果问题持续存在：

1. 查看完整的构建日志
2. 检查GitHub Actions的构建环境限制
3. 尝试在本地Linux环境构建
4. 查看buildozer官方文档

## 构建成功检查清单

- [ ] 所有依赖正确安装
- [ ] Python代码无语法错误
- [ ] buildozer.spec配置正确
- [ ] Android SDK/NDK下载成功
- [ ] 编译过程无错误
- [ ] APK文件成功生成# JDK设置说明

## 手动设置JDK（需要sudo权限）

由于创建符号链接需要管理员权限，请**在终端中手动运行**以下命令：

### 步骤1：创建符号链接

```bash
sudo ln -sfn /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk
```

系统会提示输入密码，请输入你的Mac登录密码。

### 步骤2：验证JDK检测

运行以下命令验证JDK是否被系统识别：

```bash
/usr/libexec/java_home -V
```

应该能看到类似这样的输出：
```
Matching Java Virtual Machines (2):
    17.0.17 (arm64) "Homebrew" - "OpenJDK 17.0.17" /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
    1.8.421.09 (x86_64) "Oracle Corporation" - "Java" /Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home
/Library/Java/JavaVirtualMachines/openjdk-17.jdk/Contents/Home
```

### 步骤3：开始构建

JDK设置完成后，运行：

```bash
./tools/build_apk_macos.sh
```

## 如果JDK未安装

如果提示JDK路径不存在，请先安装：

```bash
brew install openjdk@17
```

然后重复上面的步骤。

## 验证当前状态

检查JDK是否已安装：
```bash
ls -la /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk
```

检查符号链接是否已创建：
```bash
ls -la /Library/Java/JavaVirtualMachines/openjdk-17.jdk
```


---
