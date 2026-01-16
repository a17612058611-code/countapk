#!/bin/bash
# 修复后的APK打包脚本

set -e

echo "=========================================="
echo "开始打包 Android APK"
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
if [ -z "$JAVA_HOME" ]; then
    # 尝试查找JDK 17
    JAVA_HOME=$(/usr/libexec/java_home -v 17 2>/dev/null || /usr/libexec/java_home -v 11 2>/dev/null || echo "")
    if [ -n "$JAVA_HOME" ]; then
        export JAVA_HOME
        echo "✓ 设置JAVA_HOME: $JAVA_HOME"
    else
        echo "⚠ 警告: 未找到JDK，尝试安装..."
        brew install openjdk@17 || brew install openjdk@11
        JAVA_HOME=$(/usr/libexec/java_home -v 17 2>/dev/null || /usr/libexec/java_home -v 11 2>/dev/null)
        export JAVA_HOME
    fi
fi

# 设置环境变量
export P4A_ALLOW_PREREQUISITES=1
export ANDROID_ACCEPT_SDK_LICENSE=1

echo ""
echo "开始构建APK（这可能需要较长时间，请耐心等待...）"
echo "查看实时日志: tail -f build.log"
echo ""

# 使用非交互模式构建
yes | buildozer android debug 2>&1 | tee build.log

echo ""
echo "=========================================="
if ls bin/*.apk 2>/dev/null; then
    echo "✓ APK打包成功！"
    echo ""
    
    # 生成时间戳（格式：YYYYMMDDHHmm，例如：202601061522）
    TIMESTAMP=$(date +"%Y%m%d%H%M")
    
    # 重命名APK文件
    for apk_file in bin/*.apk; do
        if [ -f "$apk_file" ]; then
            # 新文件名：acoreapp_1.0.000_{时间戳}_debug.apk
            new_name="bin/acoreapp_1.0.000_${TIMESTAMP}_debug.apk"
            mv "$apk_file" "$new_name"
            echo "✓ APK已重命名为: $(basename "$new_name")"
        fi
    done
    
    echo ""
    echo "APK文件位置:"
    ls -lh bin/acoreapp_*.apk 2>/dev/null || ls -lh bin/*.apk
    echo ""
    echo "安装到设备:"
    echo "  adb install bin/acoreapp_*.apk"
else
    echo "✗ APK打包失败"
    echo "请查看 build.log 获取详细错误信息"
fi
echo "=========================================="

