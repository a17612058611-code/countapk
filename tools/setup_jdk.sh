#!/bin/bash
# 设置JDK以便python-for-android能够检测到

echo "=========================================="
echo "设置JDK以便buildozer检测"
echo "=========================================="

# 检查JDK是否已安装
if [ ! -d "/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk" ]; then
    echo "✗ JDK 17未找到，请先安装:"
    echo "  brew install openjdk@17"
    exit 1
fi

# 创建符号链接（需要sudo权限）
echo "创建符号链接到 /Library/Java/JavaVirtualMachines/..."
echo "这需要sudo权限，请输入密码："

sudo ln -sfn /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk

if [ $? -eq 0 ]; then
    echo "✓ 符号链接创建成功"
    echo ""
    echo "验证JDK检测:"
    /usr/libexec/java_home -V
    echo ""
    echo "现在可以运行构建:"
    echo "  ./build_apk_macos.sh"
else
    echo "✗ 符号链接创建失败"
    exit 1
fi

