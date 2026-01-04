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
   ./run_app.sh
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

