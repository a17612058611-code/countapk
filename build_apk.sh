#!/bin/bash
# Android APK 打包脚本

set -e

echo "=========================================="
echo "开始打包 Android APK"
echo "=========================================="

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ 虚拟环境已激活"
else
    echo "✗ 错误: 虚拟环境不存在，请先运行: python3 -m venv venv"
    exit 1
fi

# 检查buildozer是否安装
if ! command -v buildozer &> /dev/null; then
    echo "✗ 错误: buildozer未安装，正在安装..."
    pip install buildozer
fi

# 接受Android SDK许可证（如果需要）
echo "检查Android SDK许可证..."
if [ -d "$HOME/.buildozer/android/platform/android-sdk" ]; then
    echo "y" | $HOME/.buildozer/android/platform/android-sdk/tools/bin/sdkmanager --licenses || true
fi

# 开始打包
echo ""
echo "开始构建APK（这可能需要较长时间，请耐心等待...）"
echo ""

# 使用非交互模式接受所有许可证
export ANDROID_ACCEPT_SDK_LICENSE=1

buildozer android debug

echo ""
echo "=========================================="
if [ -f "bin/*.apk" ]; then
    echo "✓ APK打包成功！"
    echo "APK文件位置: bin/"
    ls -lh bin/*.apk
else
    echo "检查构建日志以获取详细信息"
fi
echo "=========================================="
