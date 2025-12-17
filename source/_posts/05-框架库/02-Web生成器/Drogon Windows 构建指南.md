---
title: Drogon Windows 构建指南
categories:
  - 框架库
tags:
  - 技术文档
  - 指南
abbrlink: 58c0a1f
date: 2025-12-09 14:09:55
---

# Drogon Windows 构建指南
> **文档创建时间**: 2025-11-14
> **最后更新**: 2025-11-14
> **标签**: `drogon`, `cpp`, `windows`, `source-build`, `cmake`, `conan`

## 📑 目录

- [1. 概述](#1-概述)
- [2. 环境准备](#2-环境准备)
- [3. 源码下载](#3-源码下载)
- [4. 依赖安装](#4-依赖安装)
- [5. 编译安装](#5-编译安装)
- [6. 环境配置](#6-环境配置)
- [7. 创建新项目](#7-创建新项目)
- [8. 常见问题](#8-常见问题)

---

## 1. 📖 概述

Drogon 是一个现代化的 C++ Web 框架。本指南介绍如何在 Windows 系统上从源码编译安装 Drogon。

### 🎯 安装目标
- ✅ 从源码编译 Drogon 框架
- ✅ 配置开发环境
- ✅ 创建第一个 Drogon 项目
- ✅ 验证安装成功

---

## 2. 🔧 环境准备

### 2.1 必需工具
- **Visual Studio 2019+** - C++ 编译器
- **Git** - 源码管理
- **CMake 3.15+** - 构建系统
- **Conan** - C++ 包管理器

### 2.2 安装 Conan
```bash
# Drogon Windows 构建指南
pip install conan

# Drogon Windows 构建指南
choco install conan
```

---

## 3. 📥 源码下载

```bash
# Drogon Windows 构建指南
cd %WORK_PATH%

# Drogon Windows 构建指南
git clone https://github.com/drogonframework/drogon
cd drogon

# Drogon Windows 构建指南
git submodule update --init
```

---

## 4. 📦 依赖安装

```bash
# Drogon Windows 构建指南
mkdir build
cd build

# Drogon Windows 构建指南
conan profile detect --force

# Drogon Windows 构建指南
conan install .. \
    -s compiler="msvc" \
    -s compiler.version=194 \
    -s compiler.cppstd=17 \
    -s build_type=Debug \
    --output-folder . \
    --build=missing
```

### 4.1 自定义依赖
编辑 `conanfile.txt` 可以添加或修改依赖：
```txt
[requires]
# Drogon Windows 构建指南
[generators]
CMakeDeps
CMakeToolchain

[options]
shared=False
```

---

## 5. 🔨 编译安装

```bash
# Drogon Windows 构建指南
cmake .. \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_TOOLCHAIN_FILE="conan_toolchain.cmake" \
    -DCMAKE_POLICY_DEFAULT_CMP0091=NEW \
    -DCMAKE_INSTALL_PREFIX="D:\ThirdParty\drogon"

# Drogon Windows 构建指南
cmake --build . --parallel --target install
```

### 5.1 ⚠️ 重要说明
- Conan 和 CMake 的 build type 必须保持一致
- Release 构建时将 `Debug` 改为 `Release`
- 可根据需要修改安装路径

---

## 6. 🔗 环境配置

### 6.1 安装结果
编译完成后，以下文件将被安装到指定目录：

| 文件类型 | 安装路径 | 说明 |
|----------|----------|------|
| **头文件** | `D:\ThirdParty\drogon\include\drogon` | Drogon 主要头文件 |
| **库文件** | `D:\ThirdParty\drogon\bin` | drogon.dll |
| **命令工具** | `D:\ThirdParty\drogon\bin` | drogon_ctl.exe |
| **Trantor头文件** | `D:\ThirdParty\drogon\include\trantor` | 依赖库头文件 |
| **Trantor库文件** | `D:\ThirdParty\drogon\bin` | trantor.dll |

### 6.2 环境变量
添加以下路径到系统 `PATH` 环境变量：
```cmd
D:\ThirdParty\drogon\bin
D:\ThirdParty\drogon\lib\cmake\Drogon
D:\ThirdParty\drogon\lib\cmake\Trantor
```

---

## 7. 🚀 创建新项目

### 7.1 使用命令行工具

```bash
# Drogon Windows 构建指南
drogon_ctl create project your_project_name

# Drogon Windows 构建指南
copy drogon\conanfile.txt your_project_name\

# Drogon Windows 构建指南
cd your_project_name

# Drogon Windows 构建指南
mkdir build
cd build
conan profile detect --force
conan install .. \
    -s compiler="msvc" \
    -s compiler.version=194 \
    -s compiler.cppstd=17 \
    -s build_type=Debug \
    --output-folder . \
    --build=missing

cmake .. \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_TOOLCHAIN_FILE="conan_toolchain.cmake" \
    -DCMAKE_POLICY_DEFAULT_CMP0091=NEW

cmake --build . --parallel
```

### 7.2 项目结构
```
your_project_name/
├── build/
├── config.json
├── CMakeLists.txt
├── conanfile.txt
├── main.cc
├── plugins/
├── run.bat
└── tests/
```

---

## 8. 🔧 常见问题

### 8.1 编译错误
- **VS 版本不匹配**: 确认 compiler.version 与安装的 Visual Studio 版本一致
- **C++ 标准问题**: 确保 compiler.cppstd 设置正确
- **依赖缺失**: 使用 `--build=missing` 强制构建缺失的依赖

### 8.2 链接错误
- **DLL 找不到**: 检查 PATH 环境变量设置
- **库文件路径**: 确认 CMAKE_PREFIX_PATH 设置正确

### 8.3 运行时错误
- **配置文件**: 检查 `config.json` 配置是否正确
- **端口占用**: 确认配置的端口未被占用

---

## 📚 相关资源

- [Drogon 官方文档](https://drogon.docs.sguanheng.com/)
- [Conan 包管理器](https://conan.io/)
- [CMake 官方文档](https://cmake.org/documentation/)

---

> **💡 提示**:
> - 首次编译可能需要较长时间
> - 建议使用 Release 模式进行生产构建
> - 定期更新 Drogon 源码以获得最新功能