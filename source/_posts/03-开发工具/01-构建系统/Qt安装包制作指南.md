---
tags:
  - QtInstallerFramework
  - 安装包制作
  - 部署工具
  - Qt
title: QtInstallerFramework 安装包制作指南
categories:
  - C++核心开发
  - Qt框架
description: 详细的技术安装与配置指南，提供从零开始的完整部署流程，包含环境检查、依赖安装、参数配置、测试验证等关键步骤。
abbrlink: '3097e686'
date: 2025-12-04 22:50:20
---

# QtInstallerFramework 安装包制作指南

## 目录
- [工具概述](#工具概述)
- [安装准备](#安装准备)
- [项目结构](#项目结构)
- [配置文件详解](#配置文件详解)
- [安装脚本详解](#安装脚本详解)
- [生成安装包](#生成安装包)
- [高级功能](#高级功能)
- [常见问题](#常见问题)
- [最佳实践](#最佳实践)

## 工具概述

QtInstallerFramework 是 Qt 官方提供的跨平台安装包制作工具，支持 Windows、macOS 和 Linux 平台。

### 特点
- 跨平台支持
- 图形化安装向导
- 强大的组件和依赖管理
- 支持在线和离线安装模式
- 可通过脚本（qs）高度自定义安装过程
- 支持多语言

## 安装准备

### 1. 获取 QtInstallerFramework
QtInstallerFramework 通常包含在 Qt 的在线安装器中，作为一个可选组件。也可以从 Qt 官网单独下载。

它的默认安装路径通常在 Qt 的 `Tools` 目录下，例如：`<Qt安装目录>\Tools\QtInstallerFramework\4.8\bin`。

### 2. 环境变量配置
为了方便在任何路径下使用命令行工具，建议将 QtInstallerFramework 的 `bin` 目录添加到系统的 `PATH` 环境变量中。

**Windows 示例:**
```
# 将 <Your-Qt-InstallerFramework-Path> 替换为你的实际路径
set PATH=%PATH%;<Your-Qt-InstallerFramework-Path>\bin
```

## 项目结构

一个典型的安装包项目结构如下：
```
YourAppInstaller/
├── config/
│   └── config.xml          # 1. 主配置文件
└── packages/
    └── com.yourcompany.yourapp/
        ├── meta/
        │   ├── package.xml         # 2. 包（组件）配置文件
        │   └── installscript.qs     # 3. 安装脚本 (可选)
        └── data/                    # 4. 要安装的实际文件
            ├── YourApp.exe
            ├── Qt6Core.dll
            └── ...
```

## 配置文件详解

### 1. 主配置文件 (config/config.xml)
该文件定义了安装器的整体行为和外观。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Installer>
    <!-- 应用名称 -->
    <Name>YourApp</Name>
    <!-- 应用版本 -->
    <Version>1.0.0</Version>
    <!-- 安装器标题 -->
    <Title>YourApp Installer</Title>
    <!-- 发行商 -->
    <Publisher>YourCompany</Publisher>
    <!-- 开始菜单目录 -->
    <StartMenuDir>YourApp</StartMenuDir>
    <!-- 默认安装路径, @ApplicationsDir@ 是预定义变量 -->
    <TargetDir>@ApplicationsDir@/YourApp</TargetDir>
    
    <!-- (可选) 安装程序图标 -->
    <InstallerWindowIcon>installer_icon.ico</InstallerWindowIcon>
    <!-- (可选) 应用图标 -->
    <InstallerApplicationIcon>app_icon.ico</InstallerApplicationIcon>
    <!-- (可选) Logo图片 -->
    <Logo>logo.png</Logo>
</Installer>
```

### 2. 包配置文件 (packages/.../meta/package.xml)
每个组件（包）都有一个 `package.xml`，用于描述该组件。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package>
    <!-- 显示名称 -->
    <DisplayName>Main Application</DisplayName>
    <!-- 组件描述 -->
    <Description>The main application files.</Description>
    <!-- 组件版本 -->
    <Version>1.0.0</Version>
    <!-- 发布日期 -->
    <ReleaseDate>2024-01-01</ReleaseDate>
    <!-- 默认选中 -->
    <Default>true</Default>
    <!-- 关联的安装脚本 -->
    <Script>installscript.qs</Script>
</Package>
```

## 安装脚本详解 (meta/installscript.qs)
安装脚本使用类 QML 的语法（`qs`），允许你完全自定义安装和卸载过程。

```javascript
// installscript.qs

function Component() {
    // 构造函数，可以在此获取安装器核心对象
}

// 定义安装操作
Component.prototype.createOperations = function() {
    // 必须先调用父类的同名方法
    component.createOperations();

    // 示例：在Windows上创建桌面快捷方式
    if (systemInfo.kernelType === "winnt") {
        component.addOperation(
            "CreateShortcut",                               // 操作类型
            "@TargetDir@/YourApp.exe",                      // 目标文件
            "@DesktopDir@/YourApp.lnk",                     // 快捷方式路径
            "workingDirectory=@TargetDir@",                 // 工作目录
            "iconPath=@TargetDir@/app_icon.ico",            // 快捷方式图标
            "iconIndex=0"                                   // 图标索引
        );
    }

    // 示例：在Windows上创建开始菜单快捷方式
    if (systemInfo.kernelType === "winnt") {
        component.addOperation(
            "CreateShortcut",
            "@TargetDir@/YourApp.exe",
            "@StartMenuDir@/YourApp.lnk",
            "workingDirectory=@TargetDir@"
        );
    }
}
```

## 生成安装包

在项目根目录（例如 `YourAppInstaller/`）打开命令行，执行以下命令：

### 1. 生成在线安装包

在线安装包体积小，安装时从服务器下载组件数据。需要预先将组件上传到服务器。

```bash
# binarycreator 是 QtInstallerFramework 的核心工具
binarycreator --online-only -c config/config.xml -p packages YourAppInstaller_Online.exe
```

### 2. 生成离线安装包

离线安装包包含所有文件，体积较大，无需联网即可安装。

```bash
# -f 是 --offline-only 的简写
binarycreator -f -c config/config.xml -p packages YourAppInstaller_Offline.exe
```

## 高级功能

### 多语言支持

在 `config.xml` 中添加语言包文件（`.ts` 文件编译后的 `.qm` 文件）。

```xml
<Installer>
    ...
    <Translations>
        <Translation>zh_CN.qm</Translation>
        <Translation>en_US.qm</Translation>
    </Translations>
</Installer>
```

### 静默/无人值守安装

使用命令行参数进行自动化安装。

```bash
# --unattended 是关键参数
YourAppInstaller.exe --unattended

# 也可以结合脚本实现更复杂的自动安装
# YourAppInstaller.exe --unattended --script your_script.qs

# 指定安装目录
YourAppInstaller.exe --unattended --target "C:\Path\To\Install"
```

## 常见问题

**Q1: 如何打包 VC++ 运行时库?**
**A**: 推荐在 `installscript.qs` 中添加一个操作来静默安装 VC++ 运行时（`vc_redist.x64.exe`）。首先将 `vc_redist.x64.exe` 放入 `data` 目录，然后添加操作：

```javascript
component.addOperation("Execute",
    "@TargetDir@/vc_redist.x64.exe",
    "/quiet",
    "/norestart"
);
```

**Q2: 如何使用 `windeployqt` 自动收集 Qt 依赖?**
**A**: `windeployqt` 是一个非常方便的工具。

```bash
# 1. 先在一个临时目录生成你的 Release 版本的 exe
# 2. 在该目录运行 windeployqt
windeployqt YourApp.exe

# 3. 将所有生成的文件和目录（platforms, styles, translations等）复制到你的组件的 data 目录下
```

**Q3: 快捷方式无法创建?**
**A**: 检查 `installscript.qs` 中的路径是否正确，特别是 `@TargetDir@/YourApp.exe` 是否指向了正确的可执行文件。确保 `CreateShortcut` 操作在 `component.createOperations()` 之后调用。

## 最佳实践

1. **组件化**: 将大型应用拆分为多个组件（packages），例如主程序、文档、快捷方式等。这让用户可以选择性安装，也便于维护。
2. **环境变量**: 避免在脚本中硬编码路径，多使用预定义变量如 `@TargetDir@`, `@DesktopDir@` 等。
3. **卸载逻辑**: 在 `installscript.qs` 中为自定义的安装操作（如添加注册表、配置文件）编写对应的卸载逻辑。
4. **测试**: 在干净的虚拟机中（特别是 Windows）测试你的安装、卸载和更新流程。
