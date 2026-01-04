# 快速开始指南

## 问题：ModuleNotFoundError: No module named 'kivy'

如果遇到这个错误，说明没有在虚拟环境中运行应用。

## 解决方案

### 方法1：使用运行脚本（推荐）⭐

```bash
./run_app.sh
```

这个脚本会自动：
- 检查并创建虚拟环境（如果需要）
- 安装依赖（如果需要）
- 激活虚拟环境
- 运行应用

### 方法2：手动激活虚拟环境

```bash
# 1. 进入项目目录
cd /Users/zmx/xzm/countapk

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 验证Kivy是否安装
python -c "import kivy; print('Kivy版本:', kivy.__version__)"

# 4. 运行应用
python main.py
```

### 方法3：在IDE中配置

如果你使用IDE（如VS Code、PyCharm等），需要：

1. **VS Code**:
   - 按 `Cmd+Shift+P` (macOS) 或 `Ctrl+Shift+P` (Windows/Linux)
   - 输入 "Python: Select Interpreter"
   - 选择 `./venv/bin/python` 或 `./venv/bin/python3`

2. **PyCharm**:
   - File → Settings → Project → Python Interpreter
   - 选择 `./venv/bin/python`

## 验证安装

运行测试脚本：

```bash
./test_installation.sh
```

如果看到 "✓ 所有测试通过！"，说明环境配置正确。

## 常见问题

### Q: 为什么需要虚拟环境？
A: 虚拟环境可以隔离项目依赖，避免不同项目之间的依赖冲突。

### Q: 每次都要激活虚拟环境吗？
A: 是的，每次运行应用前都需要激活。或者使用 `./run_app.sh` 脚本，它会自动处理。

### Q: 如何退出虚拟环境？
A: 输入 `deactivate` 命令。

### Q: 虚拟环境在哪里？
A: 在项目目录下的 `venv/` 文件夹中。

## 检查清单

- [ ] 虚拟环境已创建（`venv/` 目录存在）
- [ ] 虚拟环境已激活（命令行提示符前有 `(venv)`）
- [ ] Kivy已安装（运行 `python -c "import kivy"` 无错误）
- [ ] 使用正确的Python解释器（`which python` 指向 `venv/bin/python`）

