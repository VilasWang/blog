---
tags:
  - Boost
  - b2
  - bjam
  - 构建工具
  - 编译参数
title: Boost b2 参数参考
categories:
  - C++核心开发
  - C++基础与进阶
description: 专业的技术文档，提供详细的操作指南、最佳实践和问题解决方案，助力开发者提升技术水平。
abbrlink: 18f0987e
date: 2025-12-04 13:13:20
---

# Boost b2 参数参考
## 目录
- [概述](#概述)
- [核心参数](#核心参数)
- [库选择参数](#库选择参数)
- [构建属性参数](#构建属性参数)
- [路径与输出参数](#路径与输出参数)
- [平台与架构参数](#平台与架构参数)
- [实用编译示例](#实用编译示例)
- [脚本与最佳实践](#脚本与最佳实践)

## 概述

`b2`（其前身为 `bjam`）是 Boost C++ 库的官方构建引擎。它是一个功能强大的命令行工具，允许开发者通过丰富的参数精确控制编译过程。

### 基本语法
```bash
# Boost b2 参数参考
./b2 [options] [properties] [target]
```

### 获取帮助
```bash
# Boost b2 参数参考
./b2 --help

# Boost b2 参数参考
./b2 --show-libraries
```

## 核心参数

这些参数控制构建的基本行为。

- **`stage`**: 只编译库文件（例如 `.a`, `.so`, `.lib`, `.dll`），并将它们放置在 `stagedir` 指定的目录（默认为 `stage/lib`）。这是最常用的目标。
- **`install`**: 除了编译库文件，还会将 Boost 的头文件复制到 `prefix` 指定的目录。
- **`-j<N>`**: 设置并行编译的任务数，`<N>` 通常设为 CPU 的核心数以最大化编译速度。例如 `-j8` 或 `-j$(nproc)`。
- **`--clean`**: 清除上次的构建产物。

## 库选择参数

- **`--with-<library>`**: **白名单模式**。仅编译指定的库。可以多次使用。
- **`--without-<library>`**: **黑名单模式**。编译所有库，除了指定的这些。

```bash
# Boost b2 参数参考
./b2 --with-thread --with-filesystem

# Boost b2 参数参考
./b2 --without-python --without-wave
```

## 构建属性参数

这些属性通过 `property=value` 的形式指定，可以组合使用。

### `toolset=<compiler>`
指定使用的编译器。
- `gcc`: GNU C++ Compiler
- `clang`: Clang C++ Compiler
- `msvc-14.3`: Visual Studio 2022
- `msvc-14.2`: Visual Studio 2019
- `msvc-14.1`: Visual Studio 2017

### `variant=debug|release`
构建变体。
- `debug`: 包含调试信息，不优化。
- `release`: 开启优化，不含调试信息。

### `link=static|shared`
链接方式。
- `static`: 生成静态库（`.a`, `.lib`）。
- `shared`: 生成动态库/共享库（`.so`, `.dll`）。

### `runtime-link=static|shared`
C/C++ 运行时的链接方式。
- `static`: 静态链接 C/C++ 运行时库（例如，在 Windows 上使用 `/MT` 或 `/MTd`）。
- `shared`: 动态链接 C/C++ 运行时库（例如，在 Windows 上使用 `/MD` 或 `/MDd`）。

### `threading=single|multi`
线程支持。
- `single`: 编译为单线程版本（不推荐，已很少使用）。
- `multi`: 编译为多线程版本（现代应用的标准）。

## 路径与输出参数

- **`--stagedir=<path>`**: 与 `stage` 目标配合使用，指定库文件的输出目录。
- **`--prefix=<path>`**: 与 `install` 目标配合使用，指定头文件和库文件的安装根目录。
- **`--build-dir=<path>`**: 指定存放所有中间文件的目录（例如 `bin.v2`）。对于隔离不同构建环境的产物非常有用。

## 平台与架构参数

### `address-model=32|64`
指定编译为 32 位还是 64 位应用。

### `architecture=x86|arm|...`
指定目标 CPU 架构。通常 `b2` 会自动检测，但在交叉编译时需要手动指定。

### `cxxflags="..."` 和 `linkflags="..."`
传递自定义标志给编译器或链接器。
```bash
./b2 cxxflags="-std=c++17" linkflags="-s"
```

## 实用编译示例

### 示例 1: Linux GCC
编译用于 GCC 的 64 位多线程、动态链接、发布版 `thread` 和 `filesystem` 库。
```bash
./b2 -j8 toolset=gcc address-model=64 threading=multi link=shared variant=release --with-thread --with-filesystem stage
```

### 示例 2: Windows VS2022
编译用于 Visual Studio 2022 的 32 位、静态链接、调试版、且静态链接运行时的所有库（除了 python）。
```bash
./b2.exe -j8 toolset=msvc-14.3 address-model=32 link=static runtime-link=static variant=debug --without-python stage
```

### 示例 3: 为特定目录输出
将不同版本的库输出到不同目录，方便管理。
```bash
# Boost b2 参数参考
./b2.exe -j8 toolset=msvc-14.2 address-model=64 link=static variant=release --stagedir="lib/win-x64-msvc14.2-static-release"

# Boost b2 参数参考
./b2.exe -j8 toolset=msvc-14.2 address-model=64 link=shared variant=debug --stagedir="lib/win-x64-msvc14.2-shared-debug"
```

## 脚本与最佳实践

### 1. 使用构建脚本
创建一个脚本来编译所有你需要的版本，可以确保一致性。

`build_boost_linux.sh`:
```bash
#!/bin/bash
set -e # 如果任何命令失败则立即退出

# Boost b2 参数参考
./b2 -j$(nproc) toolset=gcc address-model=64 link=static variant=release \
    --stagedir="linux-x64-static-release" \
    --without-python

# Boost b2 参数参考
./b2 -j$(nproc) toolset=gcc address-model=64 link=shared variant=debug \
    --stagedir="linux-x64-shared-debug" \
    --without-python

echo "Boost build complete!"
```

### 2. 最佳实践
- **使用 `-j`**: 永远不要忘记使用 `-j` 参数，它能极大地缩短编译时间。
- **隔离构建目录**: 使用 `--build-dir` 为不同的构建版本（如 debug/release）指定不同的中间目录，避免冲突和不必要的重编。
- **精确选择库**: 使用 `--with-<library>` 只编译你项目需要的库，可以节省大量时间和磁盘空间。
- **清理**: 在切换差异巨大的编译选项（如编译器版本）之前，可以运行 `./b2 --clean` 来清理旧的构建产物。
