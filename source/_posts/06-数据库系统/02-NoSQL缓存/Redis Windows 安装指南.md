---
tags:
  - Redis
  - 缓存
  - Windows
  - 服务配置
  - WSL2
title: Redis Windows 安装指南
categories:
  - 后端服务架构
  - 数据库与缓存
description: 详细的技术安装与配置指南，提供从零开始的完整部署流程，包含环境检查、依赖安装、参数配置、测试验证等关键步骤。
abbrlink: '4996968'
date: 2025-12-04 13:13:24
---

# Redis Windows 安装指南
## 目录
- [重要：Redis on Windows 现状](#重要redis-on-windows-现状)
- [方法一：在 WSL2 中运行 Redis (官方推荐)](#方法一在-wsl2-中运行-redis-官方推荐)
- [方法二：使用旧版 Redis for Windows](#方法二使用旧版-redis-for-windows)
- [客户端连接](#客户端连接)
- [常见问题](#常见问题)

## 重要：Redis on Windows 现状

Redis 官方**并未正式支持和维护**原生的 Windows 版本。

- **官方推荐方案**: 在 Windows 10/11 上，官方推荐使用 **WSL2 (Windows Subsystem for Linux)** 来安装和运行原生的、最新的 Linux 版 Redis。这能提供最佳的性能和兼容性。
- **旧的 Windows 版本**: 曾有一个由微软维护的 Windows 移植版 Redis (`MicrosoftArchive/redis`)，但该项目已于多年前停止更新，其最新版本仅为 3.x，与现代 Redis (6.x, 7.x) 相比功能陈旧且存在已知漏洞。

**本指南将优先介绍 WSL2 的方法，并将旧的原生 Windows 版本安装作为备用方案。**

## 方法一：在 WSL2 中运行 Redis (官方推荐)

### 1. 安装 WSL2 和一个 Linux 发行版
如果你的系统尚未安装 WSL2，请参照微软官方文档进行安装。推荐安装 `Ubuntu`。
[微软官方 WSL 安装指南](https://learn.microsoft.com/zh-cn/windows/wsl/install)

### 2. 在 Ubuntu (WSL) 中安装 Redis
打开你的 Ubuntu 终端，执行以下命令：
```bash
# Redis Windows 安装指南
sudo apt update

# Redis Windows 安装指南
sudo apt install redis-server
```

### 3. 配置和管理 Redis 服务
```bash
# Redis Windows 安装指南
sudo service redis-server start

# Redis Windows 安装指南
sudo service redis-server status
# Redis Windows 安装指南
redis-cli ping  # 应该返回 PONG

# Redis Windows 安装指南
# Redis Windows 安装指南
sudo nano /etc/redis/redis.conf
# Redis Windows 安装指南
# Redis Windows 安装指南
sudo service redis-server restart
```
在 WSL2 中运行的 Redis，你可以直接通过 `localhost` 从你的 Windows 主机访问它。

## 方法二：使用旧版 Redis for Windows

**警告**: 此方法安装的是一个过时的 Redis 3.x 版本，不推荐用于生产环境。

### 1. 下载
从 `MicrosoftArchive/redis` 的 GitHub Releases 页面下载最新的 `.msi` 或 `.zip` 文件。
- **下载地址**: [https://github.com/microsoftarchive/redis/releases](https://github.com/microsoftarchive/redis/releases)

### 2. 安装与配置
1.  **解压**: 将 ZIP 文件解压到一个稳定路径，例如 `C:\redis`。
2.  **重命名配置文件**: 将 `redis.windows.conf` 复制一份，并重命名为 `redis.conf`。
3.  **编辑 `redis.conf`**:
    ```conf
    # 设置密码
    requirepass your_strong_password
    
    # (可选) 修改端口
    # port 6379
    ```

### 3. 注册为 Windows 服务
以**管理员身份**打开命令提示符 (CMD)，并进入你的 Redis 目录。
```cmd
cd C:\redis

# Redis Windows 安装指南
redis-server.exe --service-install redis.conf --service-name Redis

# Redis Windows 安装指南
redis-server.exe --service-start --service-name Redis
```

### 4. 管理服务
```cmd
# Redis Windows 安装指南
redis-server.exe --service-stop --service-name Redis

# Redis Windows 安装指南
redis-server.exe --service-uninstall --service-name Redis

# Redis Windows 安装指南
```

## 客户端连接

无论你使用哪种方法安装，都可以使用 `redis-cli` 或图形化客户端进行连接。

### 使用 `redis-cli`
```cmd
# Redis Windows 安装指南
redis-cli -h localhost -p 6379

# Redis Windows 安装指南
redis-cli -h localhost -p 6379 -a your_strong_password
```

### 图形化客户端
推荐使用 `Another Redis Desktop Manager` 或 `TablePlus` 等现代 Redis 客户端。在连接时，主机地址填写 `localhost`，并填入对应的端口和密码即可。

## 常见问题

**Q: 为什么不直接在 Windows 上编译最新的 Redis 源码?**
**A**: Redis 源码严重依赖 Linux 的内核特性（如 `fork()`），使其很难被直接、稳定地移植到 Windows。官方已放弃这条路线，全面拥抱 WSL2。

**Q: WSL2 中的 Redis 如何与我的 Windows 应用通信?**
**A**: WSL2 与 Windows 主机共享网络。你的 Windows 应用可以直接通过 `localhost` 或 `127.0.0.1` 连接到在 WSL2 中运行的 Redis 服务，就像它在本地运行一样。

**Q: 旧版 Redis for Windows 有什么风险?**
**A**: 主要风险是它不再接收安全更新，可能存在已知的安全漏洞。同时，它也缺少许多现代 Redis 的新功能和性能改进。
