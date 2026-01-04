# JDK设置说明

## 手动设置JDK（需要sudo权限）

由于创建符号链接需要管理员权限，请**在终端中手动运行**以下命令：

### 步骤1：创建符号链接

```bash
sudo ln -sfn /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk
```

系统会提示输入密码，请输入你的Mac登录密码。

### 步骤2：验证JDK检测

运行以下命令验证JDK是否被系统识别：

```bash
/usr/libexec/java_home -V
```

应该能看到类似这样的输出：
```
Matching Java Virtual Machines (2):
    17.0.17 (arm64) "Homebrew" - "OpenJDK 17.0.17" /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
    1.8.421.09 (x86_64) "Oracle Corporation" - "Java" /Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home
/Library/Java/JavaVirtualMachines/openjdk-17.jdk/Contents/Home
```

### 步骤3：开始构建

JDK设置完成后，运行：

```bash
./build_apk_macos.sh
```

## 如果JDK未安装

如果提示JDK路径不存在，请先安装：

```bash
brew install openjdk@17
```

然后重复上面的步骤。

## 验证当前状态

检查JDK是否已安装：
```bash
ls -la /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk
```

检查符号链接是否已创建：
```bash
ls -la /Library/Java/JavaVirtualMachines/openjdk-17.jdk
```

