# 每日分数记录 Android APK

一个简单的Android应用，用于记录每日分数并计算总分和平均分。

## 功能特性

- 📅 显示当前日期
- 📝 记录当天分数（0-100）
- 📄 添加分数描述
- 📊 显示总分
- 📈 显示平均分
- 💾 数据持久化存储（JSON格式）

## 环境要求

### 开发环境（用于本地测试）

- Python 3.7+
- Kivy 2.1.0+

### 打包环境（用于生成APK）

- Linux 或 macOS
- Buildozer
- Android SDK
- Android NDK

## 安装步骤

### 1. 创建虚拟环境（推荐）

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows
```

### 2. 安装Python依赖

```bash
pip install -r requirements.txt
```

### 3. 本地运行测试

**方法1：使用运行脚本（推荐）**
```bash
./run_app.sh
```

**方法2：手动激活虚拟环境后运行**
```bash
source venv/bin/activate  # 激活虚拟环境
python main.py
```

**注意：** 如果遇到 `ModuleNotFoundError: No module named 'kivy'` 错误，请确保已激活虚拟环境！

### 3. 打包为Android APK

#### 安装Buildozer

```bash
pip install buildozer
```

#### 安装系统依赖（Ubuntu/Debian）

```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

#### 安装系统依赖（macOS）

```bash
brew install autoconf automake libtool pkg-config
brew install libffi openssl
```

#### 配置Android SDK和NDK

1. 下载并安装 Android SDK
2. 设置环境变量：
   ```bash
   export ANDROID_HOME=/path/to/android/sdk
   export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
   ```

#### 构建APK

```bash
# 首次构建（会下载很多依赖，需要较长时间）
buildozer android debug

# 构建完成后，APK文件在 bin/ 目录下
```

## 项目结构

```
countapk/
├── main.py              # 主应用文件
├── data_manager.py      # 数据管理模块
├── requirements.txt     # Python依赖
├── buildozer.spec      # Buildozer配置文件
├── README.md           # 说明文档
└── scores.json         # 数据文件（自动生成）
```

## 使用说明

1. **输入分数**：在"今天分数"输入框中输入0-100之间的数字
2. **添加描述**：在"分数描述"输入框中输入描述信息（可选）
3. **保存**：点击"保存"按钮保存当天的分数
4. **查看统计**：应用会自动显示总分和平均分

## 数据存储

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

## 注意事项

1. 首次使用Buildozer构建APK时，需要下载大量依赖，可能需要较长时间
2. 确保有足够的磁盘空间（至少5GB）
3. 建议在Linux系统上构建APK，macOS上可能需要额外配置
4. 如果遇到构建问题，可以查看 `buildozer.spec` 文件中的配置

## 常见问题

### Q: 如何在Windows上打包APK？
A: 建议使用WSL2（Windows Subsystem for Linux）或虚拟机运行Linux系统进行打包。

### Q: 构建失败怎么办？
A: 检查Android SDK和NDK是否正确安装，确保环境变量配置正确。查看构建日志获取详细错误信息。

### Q: 可以修改应用名称和图标吗？
A: 可以，在 `buildozer.spec` 文件中修改 `title` 和 `icon.filename` 配置。

## 许可证

MIT License

