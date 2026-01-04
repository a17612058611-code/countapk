#!/bin/bash
# 检查环境配置脚本

echo "=========================================="
echo "环境检查"
echo "=========================================="

cd "$(dirname "$0")"

# 检查虚拟环境
if [ -d "venv" ]; then
    echo "✓ 虚拟环境存在"
    source venv/bin/activate
    
    # 检查Python路径
    PYTHON_PATH=$(which python)
    echo "Python路径: $PYTHON_PATH"
    
    if [[ "$PYTHON_PATH" == *"venv"* ]]; then
        echo "✓ 使用虚拟环境中的Python"
    else
        echo "✗ 警告: 未使用虚拟环境中的Python"
        echo "请运行: source venv/bin/activate"
    fi
    
    # 检查Kivy
    if python -c "import kivy" 2>/dev/null; then
        KIVY_VERSION=$(python -c "import kivy; print(kivy.__version__)" 2>/dev/null)
        echo "✓ Kivy已安装 (版本: $KIVY_VERSION)"
    else
        echo "✗ Kivy未安装"
        echo "请运行: pip install -r requirements.txt"
    fi
else
    echo "✗ 虚拟环境不存在"
    echo "请运行: python3 -m venv venv"
fi

echo ""
echo "=========================================="
echo "运行应用: ./run_app.sh"
echo "=========================================="
