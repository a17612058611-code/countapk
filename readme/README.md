# 拾光ZM - 每日分数记录

一个简单的Android应用，用于记录每日分数并计算总分和平均分。

## 功能特性

- 📅 显示当前日期
- 📝 记录当天分数（0-100）
- 📄 添加分数描述
- 📊 显示总分和平均分
- 📜 查看历史记录
- ✏️ 编辑和删除历史记录
- 💾 数据持久化存储（JSON格式）

## 🚀 快速开始

### 方法1：使用运行脚本（推荐）⭐

```bash
./tools/run_app.sh
```

这个脚本会自动：
- 检查并创建虚拟环境（如果需要）
- 安装依赖（如果需要）
- 激活虚拟环境
- 运行应用

### 方法2：手动运行

```bash
# 1. 创建虚拟环境（如果还没有）
python3 -m venv venv

# 2. 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行应用
python main.py
```

**注意：** 如果遇到 `ModuleNotFoundError: No module named 'kivy'` 错误，请确保已激活虚拟环境！

## 📱 使用说明

### 基本操作

1. **输入分数**：在"今天分数"输入框中输入0-100之间的数字
2. **添加描述**：在"分数描述"输入框中输入描述信息（可选）
3. **保存**：点击"保存"按钮保存当天的分数
4. **查看统计**：应用会自动显示总分和平均分

### 历史记录功能

- **查看历史记录**：点击"查看历史记录"按钮查看所有历史记录
- **编辑记录**：在历史记录页面点击"编辑"按钮，可以修改指定日期的分数和描述
- **删除记录**：在历史记录页面点击"删除"按钮，可以删除指定日期的记录
- **修改历史记录**：点击"修改历史记录"按钮，可以通过日期选择器修改任意日期的记录

## 📋 环境要求

### 开发环境（用于本地测试）

- Python 3.7+
- Kivy 2.1.0+

### 打包环境（用于生成APK）

- Linux 或 macOS
- Buildozer
- Android SDK
- Android NDK

详细的环境配置和构建说明请参考 [DEVELOPMENT.md](DEVELOPMENT.md)

## 📁 项目结构

```
countapk/
├── main.py              # 主应用文件
├── data_manager.py      # 数据管理模块
├── requirements.txt     # Python依赖
├── buildozer.spec      # Buildozer配置文件
├── readme/              # 文档目录
│   ├── README.md        # 说明文档
│   ├── DEVELOPMENT.md   # 开发文档
│   └── FEATURES.md      # 功能文档
├── tools/               # 脚本工具目录
│   ├── run_app.sh       # 运行脚本
│   ├── build_apk_fixed.sh          # Linux构建脚本
│   ├── build_apk_macos_fixed.sh    # macOS构建脚本
│   └── ...              # 其他工具脚本
└── scores.json         # 数据文件（自动生成）
```

## 💾 数据存储

所有分数数据存储在 `scores.json` 文件中，格式如下：

```json
{
  "2024-01-01": {
    "score": 85,
    "desc": "今天表现不错"
  },
  "2024-01-02": {
    "score": 90,
    "desc": "非常棒"
  }
}
```

## ❓ 常见问题

### Q: 如何在Windows上打包APK？
A: 建议使用WSL2（Windows Subsystem for Linux）或虚拟机运行Linux系统进行打包。

### Q: 构建失败怎么办？
A: 检查Android SDK和NDK是否正确安装，确保环境变量配置正确。查看构建日志获取详细错误信息。更多故障排除信息请参考 [DEVELOPMENT.md](DEVELOPMENT.md)。

### Q: 可以修改应用名称和图标吗？
A: 可以，在 `buildozer.spec` 文件中修改 `title` 和 `icon.filename` 配置。

### Q: 为什么需要虚拟环境？
A: 虚拟环境可以隔离项目依赖，避免不同项目之间的依赖冲突。

### Q: 如何退出虚拟环境？
A: 输入 `deactivate` 命令。

## 📚 更多文档

- [DEVELOPMENT.md](DEVELOPMENT.md) - 开发环境配置、构建说明、故障排除等
- [FEATURES.md](FEATURES.md) - 功能详细说明

## 📄 许可证

MIT License
