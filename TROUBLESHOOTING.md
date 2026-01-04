# GitHub Actions 构建故障排除

## 常见错误和解决方案

### 错误：Process completed with exit code 100

**原因**：buildozer构建过程中出现错误

**排查步骤**：

1. **查看构建日志**
   - 在GitHub Actions页面，点击失败的workflow
   - 查看"Build APK"步骤的详细日志
   - 查找ERROR或WARNING信息

2. **常见问题**：

   **问题1：依赖下载失败**
   ```
   ERROR: Failed to download...
   ```
   - **解决**：网络问题，重试构建即可
   - 首次构建需要下载大量依赖（2-3GB）

   **问题2：Python语法错误**
   ```
   SyntaxError: invalid syntax
   ```
   - **解决**：检查代码语法
   - 在本地运行：`python -m py_compile main.py`

   **问题3：缺少依赖**
   ```
   ModuleNotFoundError: No module named 'xxx'
   ```
   - **解决**：检查requirements.txt
   - 确保所有依赖都已列出

   **问题4：Android SDK/NDK下载失败**
   ```
   Failed to download Android SDK/NDK
   ```
   - **解决**：重试构建
   - 首次构建需要下载大量文件

   **问题5：内存不足**
   ```
   Out of memory
   ```
   - **解决**：GitHub Actions默认2GB内存
   - 可能需要优化构建过程

3. **本地测试**

   在本地测试构建可以帮助定位问题：

   ```bash
   # 在Linux环境（WSL2或虚拟机）中
   sudo apt-get update
   sudo apt-get install -y python3-pip buildozer
   buildozer android debug
   ```

### 错误：APK文件未找到

**原因**：构建过程中断或失败

**解决**：
- 查看构建日志找出失败原因
- 检查是否有部分文件生成
- 重新运行构建

### 优化建议

1. **增加超时时间**（已在配置中设置为120分钟）
2. **添加缓存**（可选，加快后续构建）
3. **分步构建**（如果构建时间过长）

## 获取帮助

如果问题持续存在：

1. 查看完整的构建日志
2. 检查GitHub Actions的构建环境限制
3. 尝试在本地Linux环境构建
4. 查看buildozer官方文档

## 构建成功检查清单

- [ ] 所有依赖正确安装
- [ ] Python代码无语法错误
- [ ] buildozer.spec配置正确
- [ ] Android SDK/NDK下载成功
- [ ] 编译过程无错误
- [ ] APK文件成功生成

