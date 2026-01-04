# Pyjnius 编译错误修复

## 问题描述

构建失败，错误信息：
- `clang-14: error: no such file or directory: 'jnius/jnius.c'`
- `Error compiling Cython file`
- `pyjnius first build failed`

## 可能的原因

1. **python-for-android版本问题** - 可能需要特定版本
2. **Cython版本不兼容** - 需要兼容的Cython版本
3. **NDK工具链问题** - clang编译器配置问题
4. **依赖缺失** - pyjnius的依赖未正确安装

## 已应用的修复

1. **明确指定bootstrap**
   ```spec
   p4a.bootstrap = sdl2
   ```

2. **明确指定分支**
   ```spec
   p4a.branch = master
   ```

3. **添加调试环境变量**
   ```yaml
   export NDK_DEBUG=1
   export P4A_DEBUG=1
   ```

## 如果仍然失败

### 方案1：指定python-for-android版本

在buildozer.spec中添加：
```spec
# 使用稳定版本
p4a.branch = release-2024.01.21
```

### 方案2：添加pyjnius到requirements

如果pyjnius需要单独安装，可以在requirements中添加：
```spec
requirements = python3,kivy,pyjnius
```

### 方案3：使用预编译的pyjnius

某些情况下，可能需要使用预编译的版本。

## 调试建议

1. 查看完整的build.log文件
2. 检查Cython版本是否兼容
3. 查看python-for-android的GitHub issues
4. 尝试使用不同的NDK版本

