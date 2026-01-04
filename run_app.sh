#!/bin/bash
# 运行应用的脚本（自动激活虚拟环境）

cd "$(dirname "$0")"

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "错误: 虚拟环境不存在，正在创建..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "创建虚拟环境失败！"
        exit 1
    fi
    source venv/bin/activate
    echo "正在安装依赖..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "安装依赖失败！"
        exit 1
    fi
else
    # 激活虚拟环境
    source venv/bin/activate
fi

# 验证Kivy是否安装
if ! python -c "import kivy" 2>/dev/null; then
    echo "错误: Kivy未安装，正在安装..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "安装Kivy失败！"
        exit 1
    fi
fi

# 使用虚拟环境中的python运行应用
echo "启动应用..."
echo "使用Python: $(which python)"
python main.py

