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
./run_app.sh
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

