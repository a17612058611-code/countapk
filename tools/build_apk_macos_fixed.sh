#!/bin/bash
# macOS APK打包脚本（修复SSL和JDK问题）

set -e

echo "=========================================="
echo "macOS APK打包（完整修复版）"
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

# 检查JDK符号链接
if [ ! -d "/Library/Java/JavaVirtualMachines/openjdk-17.jdk" ]; then
    echo ""
    echo "⚠ 警告: JDK符号链接未创建"
    echo "请运行: sudo ln -sfn /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk"
    echo "或运行: ./setup_jdk.sh"
    echo ""
    read -p "是否继续？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 修复SSL证书问题
echo ""
echo "配置SSL证书..."
export SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())" 2>/dev/null || echo "")
export REQUESTS_CA_BUNDLE=$SSL_CERT_FILE
export CURL_CA_BUNDLE=""
export PYTHONHTTPSVERIFY=1

if [ -n "$SSL_CERT_FILE" ]; then
    echo "✓ SSL证书路径: $SSL_CERT_FILE"
else
    echo "⚠ 警告: 未找到certifi，尝试安装..."
    pip install --upgrade certifi
    export SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())")
    export REQUESTS_CA_BUNDLE=$SSL_CERT_FILE
fi

# 设置环境变量
export P4A_ALLOW_PREREQUISITES=1
export ANDROID_ACCEPT_SDK_LICENSE=1

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
    echo "1. SSL证书问题 - 运行: ./fix_ssl_cert.sh"
    echo "2. JDK问题 - 运行: ./setup_jdk.sh"
    echo "3. 查看详细错误: tail -100 build.log"
fi
echo "=========================================="

