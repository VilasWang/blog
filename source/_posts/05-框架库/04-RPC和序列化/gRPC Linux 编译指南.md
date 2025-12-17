---
tags:
  - gRPC
  - Protobuf
  - 编译
  - Linux
  - C++
  - 源码编译
title: gRPC Linux 编译指南
categories:
  - C++核心开发
  - 网络编程与RPC
description: 专业技术完全指南，涵盖理论基础、实践操作、问题排查、性能优化等全方位内容，助力技能快速提升。
abbrlink: 2a876257
date: 2025-12-04 13:13:21
---

# gRPC Linux 编译指南
## 目录
- [概述](#概述)
- [环境准备](#环境准备)
- [获取源码](#获取源码)
- [编译与安装](#编译与安装)
- [配置环境](#配置环境)
- [验证安装](#验证安装)
- [常见问题](#常见问题)

## 概述

本指南详细介绍如何在 Linux 系统（以 Ubuntu/Debian 为例）下，通过 CMake 从源码编译和安装 gRPC 及其核心依赖 Protobuf。

此方法遵循 gRPC 官方推荐的流程，通过 Git 子模块来构建其依赖，确保版本兼容性，过程最简单、最可靠。

### 系统要求
- **操作系统**: Ubuntu 20.04+ / Debian 10+
- **编译器**: GCC 9+ 或 Clang 9+
- **CMake**: 3.13+
- **内存**: 建议 8GB+
- **磁盘空间**: 建议 15GB+ 可用空间

## 环境准备

```bash
# gRPC Linux 编译指南
sudo apt update

# gRPC Linux 编译指南
sudo apt install -y \
    build-essential \
    autoconf \
    libtool \
    pkg-config \
    cmake \
    git \
    zlib1g-dev
```

## 获取源码

> **提示**: 本文以 gRPC **v1.64.0** 为例。你可以从 gRPC 的 [GitHub Releases](https://github.com/grpc/grpc/releases) 页面选择一个你需要的稳定版本标签。

```bash
# gRPC Linux 编译指南
mkdir -p ~/dev/grpc-build && cd ~/dev/grpc-build

# gRPC Linux 编译指南
# gRPC Linux 编译指南
# gRPC Linux 编译指南
# gRPC Linux 编译指南
git clone --recurse-submodules --depth 1 --shallow-submodules -b v1.64.0 https://github.com/grpc/grpc.git

# gRPC Linux 编译指南
# gRPC Linux 编译指南
# gRPC Linux 编译指南
```
*国内用户如果访问 GitHub 速度慢，可以搜索 gRPC 的 Gitee 镜像，并相应地修改 `.gitmodules` 文件中的子模块 URL。*

## 编译与安装

整个编译过程在 gRPC 源码目录内完成。

```bash
# gRPC Linux 编译指南
cd grpc

# gRPC Linux 编译指南
mkdir -p cmake/build
cd cmake/build

# gRPC Linux 编译指南
# gRPC Linux 编译指南
# gRPC Linux 编译指南
# gRPC Linux 编译指南
cmake -DCMAKE_BUILD_TYPE=Release \
      -DgRPC_INSTALL=ON \
      -DCMAKE_INSTALL_PREFIX=/usr/local/grpc \
      ../..

# gRPC Linux 编译指南
# gRPC Linux 编译指南
make -j$(nproc)

# gRPC Linux 编译指南
sudo make install
```

## 配置环境

### 1. 配置动态链接器
为了让系统能在运行时找到刚刚安装的 gRPC 和 Protobuf 库文件。

```bash
# gRPC Linux 编译指南
sudo tee /etc/ld.so.conf.d/grpc.conf > /dev/null <<EOF
/usr/local/grpc/lib
EOF

# gRPC Linux 编译指南
sudo ldconfig

# gRPC Linux 编译指南
ldconfig -p | grep grpc
ldconfig -p | grep protobuf
```

### 2. 配置 PATH 环境变量
为了能直接使用 `protoc` 和 `grpc_cpp_plugin` 等命令行工具。

```bash
# gRPC Linux 编译指南
echo 'export PATH="/usr/local/grpc/bin:$PATH"' >> ~/.bashrc

# gRPC Linux 编译指南
source ~/.bashrc
```

## 验证安装

```bash
# gRPC Linux 编译指南
protoc --version
# gRPC Linux 编译指南
# gRPC Linux 编译指南
which grpc_cpp_plugin
# gRPC Linux 编译指南
# gRPC Linux 编译指南
cd ~/dev/grpc-build/grpc/examples/cpp/helloworld
mkdir -p cmake/build && cd cmake/build

# gRPC Linux 编译指南
cmake -DCMAKE_PREFIX_PATH=/usr/local/grpc ../..
make -j$(nproc)

# gRPC Linux 编译指南
./greeter_server &

# gRPC Linux 编译指南
./greeter_client
# gRPC Linux 编译指南
```
如果客户端成功输出了 "Hello world"，则说明你的 gRPC 环境已成功编译并可以正常工作。

## 常见问题

**Q1: Git 克隆或子模块更新非常慢或失败?**
**A**: 这是国内常见的网络问题。你可以尝试为 Git 配置代理，或者查找并使用 Gitee 上的镜像。如果使用镜像，你可能需要手动修改 `.gitmodules` 文件中各个子模块的 `url`，然后再次运行 `git submodule sync` 和 `git submodule update --init`。

**Q2: 编译过程中提示内存不足 (Killed) ?**
**A**: gRPC 编译需要大量内存。如果你的机器内存小于 8GB，可能会发生这种情况。
- **减少并行任务数**: 尝试 `make -j2` 或 `make -j1`。
- **增加交换空间 (Swap)**:
  ```bash
  sudo fallocate -l 4G /swapfile
  sudo chmod 600 /swapfile
  sudo mkswap /swapfile
  sudo swapon /swapfile
  # 编译完成后可以禁用并删除
  # sudo swapoff /swapfile && sudo rm /swapfile
  ```

**Q3: `sudo make install` 后，`protoc --version` 仍然显示旧版本?**
**A**: 这通常是因为你的 `PATH` 环境变量中，系统自带的旧版本 `protoc` (如 `/usr/bin/protoc`) 位于你新安装的 `/usr/local/grpc/bin` 之前。
- 运行 `which protoc` 确认你正在使用的是哪个 `protoc`。
- 确保 `/usr/local/grpc/bin` 在 `PATH` 的最前面。
- 或者，卸载系统自带的 `protobuf-compiler` (`sudo apt remove protobuf-compiler`)

```
