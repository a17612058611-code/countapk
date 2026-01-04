#!/bin/bash
# 检查构建状态脚本

echo "=========================================="
echo "构建状态检查"
echo "=========================================="

# 检查buildozer进程
if pgrep -f "buildozer" > /dev/null; then
    echo "✓ Buildozer进程正在运行"
    echo ""
    echo "进程信息:"
    ps aux | grep -i buildozer | grep -v grep | head -3
else
    echo "✗ Buildozer进程未运行"
fi

echo ""
echo "----------------------------------------"

# 检查日志文件
if [ -f "build.log" ]; then
    echo "✓ 构建日志文件存在"
    echo ""
    echo "最新日志 (最后10行):"
    tail -10 build.log
else
    echo "✗ 构建日志文件不存在"
fi

echo ""
echo "----------------------------------------"

# 检查APK文件
if ls bin/*.apk 2>/dev/null; then
    echo "✓ APK文件已生成！"
    echo ""
    echo "APK文件:"
    ls -lh bin/*.apk
else
    echo "✗ APK文件尚未生成"
    echo "构建可能还在进行中，请稍候..."
fi

echo ""
echo "=========================================="
echo "提示: 查看完整日志: tail -f build.log"
echo "=========================================="

