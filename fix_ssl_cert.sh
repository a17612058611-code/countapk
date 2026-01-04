#!/bin/bash
# 修复SSL证书问题

echo "=========================================="
echo "修复SSL证书问题"
echo "=========================================="

cd "$(dirname "$0")"

# 方法1: 安装/更新certifi
echo "1. 更新certifi..."
source venv/bin/activate
pip install --upgrade certifi

# 方法2: 运行Python证书安装脚本（如果存在）
if [ -f "/Applications/Python 3.13/Install Certificates.command" ]; then
    echo "2. 运行Python证书安装脚本..."
    /Applications/Python\ 3.13/Install\ Certificates.command
fi

# 方法3: 设置环境变量使用系统证书
echo "3. 设置SSL证书环境变量..."
export SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())")
export REQUESTS_CA_BUNDLE=$SSL_CERT_FILE

echo "✓ SSL证书已配置"
echo "证书路径: $SSL_CERT_FILE"

# 方法4: 禁用SSL验证（不推荐，但可以作为临时方案）
echo ""
echo "如果仍然失败，可以临时禁用SSL验证（不推荐）："
echo "export PYTHONHTTPSVERIFY=0"
echo "或"
echo "export CURL_CA_BUNDLE="

