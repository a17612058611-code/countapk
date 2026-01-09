#!/bin/bash
# 测试安装脚本

echo "=========================================="
echo "测试Kivy安装"
echo "=========================================="

cd "$(dirname "$0")"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "✗ 虚拟环境不存在"
    echo "正在创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    echo "正在安装依赖..."
    pip install -r requirements.txt
else
    echo "✓ 虚拟环境存在"
    source venv/bin/activate
fi

echo ""
echo "测试导入Kivy..."
if python -c "import kivy; print('✓ Kivy版本:', kivy.__version__)" 2>/dev/null; then
    echo "✓ Kivy安装成功！"
else
    echo "✗ Kivy导入失败"
    echo "正在重新安装Kivy..."
    pip install --upgrade -r requirements.txt
    if python -c "import kivy; print('✓ Kivy版本:', kivy.__version__)" 2>/dev/null; then
        echo "✓ Kivy安装成功！"
    else
        echo "✗ Kivy安装失败，请检查错误信息"
        exit 1
    fi
fi

echo ""
echo "测试导入应用模块..."
if python -c "from data_manager import DataManager; print('✓ 数据管理模块导入成功')" 2>/dev/null; then
    echo "✓ 应用模块导入成功！"
else
    echo "✗ 应用模块导入失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ 所有测试通过！"
echo "=========================================="
echo ""
echo "现在可以运行应用："
echo "  ./run_app.sh"
echo "或"
echo "  source venv/bin/activate && python main.py"
echo ""

