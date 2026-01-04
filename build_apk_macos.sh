#!/bin/bash
# macOS APK打包脚本（修复版）

set -e

echo "=========================================="
echo "macOS APK打包（修复版）"
echo "=========================================="

cd "$(dirname "$0")"

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ 虚拟环境已激活"
else
    echo "✗ 错误: 虚拟环境不存在"
    exit 1
fi

# 设置JAVA_HOME
export JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
export PATH="$JAVA_HOME/bin:$PATH"

# 验证JDK
if [ ! -d "$JAVA_HOME" ]; then
    echo "✗ 错误: JDK 17未找到，请先安装:"
    echo "  brew install openjdk@17"
    exit 1
fi

echo "✓ JAVA_HOME: $JAVA_HOME"
java -version 2>&1 | head -3

# 修复证书问题（如果存在）
if [ -f ~/Downloads/cacert.pem ]; then
    mv ~/Downloads/cacert.pem ~/Downloads/cacert.pem.bak 2>/dev/null || true
    echo "✓ 证书文件已处理"
fi

# 设置环境变量
export P4A_ALLOW_PREREQUISITES=1
export ANDROID_ACCEPT_SDK_LICENSE=1
export CURL_CA_BUNDLE=""
export SSL_CERT_FILE=""

echo ""
echo "开始构建APK（这可能需要30-60分钟）"
echo "查看实时日志: tail -f build.log"
echo ""

# 清理旧的构建
echo "清理旧构建..."
buildozer android clean 2>&1 | grep -v "^D " || true

# 开始构建
echo "开始构建..."
yes | buildozer android debug 2>&1 | tee build.log

echo ""
echo "=========================================="
if ls bin/*.apk 2>/dev/null; then
    echo "✓ APK打包成功！"
    echo ""
    echo "APK文件:"
    ls -lh bin/*.apk
    echo ""
    echo "安装到设备:"
    echo "  adb install bin/*.apk"
else
    echo "✗ APK打包失败"
    echo "请查看 build.log 获取详细错误信息"
    echo ""
    echo "常见问题："
    echo "1. 如果遇到JDK问题，确保已安装: brew install openjdk@17"
    echo "2. 如果遇到证书问题，检查 ~/Downloads/cacert.pem"
    echo "3. 如果遇到AAB问题，可能需要更新buildozer配置"
fi
echo "=========================================="

