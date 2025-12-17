---
tags:
  - atop
  - 系统监控
  - 性能分析
  - Linux
  - Ubuntu
  - netatop
title: Linux atop 监控工具使用指南
categories:
  - 系统运维管理
  - 监控与诊断
description: 详细的技术安装与配置指南，提供从零开始的完整部署流程，包含环境检查、依赖安装、参数配置、测试验证等关键步骤。
abbrlink: cf6de084
date: 2025-12-04 13:13:19
---

# Linux atop 监控工具使用指南
## 目录
- [概述](#概述)
- [第一步：安装 atop](#第一步安装-atop)
- [第二步：安装 netatop 网络监控模块 (可选)](#第二步安装-netatop-网络监控模块-可选)
- [第三步：配置 atop 服务](#第三步配置-atop-服务)
- [第四步：使用 atop](#第四步使用-atop)
- [第五步：分析历史日志](#第五步分析历史日志)
- [附录：监控字段说明](#附录监控字段说明)
- [常见问题](#常见问题)

## 概述

`atop` 是一个高级的、可交互的 Linux 系统性能监控工具。与 `top`、`htop` 等工具相比，`atop` 最强大的特性是它能够**记录历史性能数据**，并允许你像播放视频一样“回放”系统在过去某个时间点的状态，极大地便利了问题排查和性能分析。

### 主要特性
- **全面监控**: 监控 CPU、内存、交换空间、磁盘 I/O、网络以及各个进程的资源使用情况。
- **历史记录**: 默认以10分钟为间隔，将系统快照记录到日志文件中，并保留28天。
- **进程级详情**: 记录每个进程的资源使用、状态、退出码等详细信息。
- **高亮显示**: 对过载的系统资源使用不同颜色高亮显示，一目了然。

## 第一步：安装 atop

### Ubuntu/Debian
```bash
# Linux atop 监控工具使用指南
sudo apt update

# Linux atop 监控工具使用指南
sudo apt install -y atop

# Linux atop 监控工具使用指南
atop --version
```

### CentOS/RHEL
```bash
# Linux atop 监控工具使用指南
sudo yum install -y epel-release

# Linux atop 监控工具使用指南
sudo yum install -y atop
# Linux atop 监控工具使用指南
# Linux atop 监控工具使用指南
```

## 第二步：安装 netatop 网络监控模块 (可选)

默认情况下，`atop` 只能显示系统总的网络流量。要查看**每个进程**的网络活动，你需要安装 `netatop` 内核模块。

### 1. 安装依赖
```bash
# Linux atop 监控工具使用指南
sudo apt install -y build-essential zlib1g-dev linux-headers-$(uname -r)

# Linux atop 监控工具使用指南
sudo yum groupinstall -y "Development Tools"
sudo yum install -y zlib-devel kernel-devel
```

### 2. 下载和编译
```bash
# Linux atop 监控工具使用指南
mkdir -p ~/build/netatop && cd ~/build/netatop

# Linux atop 监控工具使用指南
# Linux atop 监控工具使用指南
wget https://www.atoptool.nl/download/netatop-3.1.tar.gz --no-check-certificate

# Linux atop 监控工具使用指南
tar -zxvf netatop-3.1.tar.gz
cd netatop-3.1

# Linux atop 监控工具使用指南
sudo make && sudo make install
```

### 3. 加载模块并设为自启
```bash
# Linux atop 监控工具使用指南
sudo modprobe netatop

# Linux atop 监控工具使用指南
lsmod | grep netatop

# Linux atop 监控工具使用指南
echo "netatop" | sudo tee /etc/modules-load.d/netatop.conf

# Linux atop 监控工具使用指南
sudo systemctl start netatop
sudo systemctl enable netatop
```

## 第三步：配置 atop 服务

`atop` 安装后会作为一个后台服务运行，定期记录系统快照。我们可以优化其配置。

### 1. 编辑配置文件
- **Ubuntu/Debian**: `/etc/default/atop`
- **CentOS/RHEL**: `/etc/sysconfig/atop`

```bash
# Linux atop 监控工具使用指南
sudo nano /etc/default/atop
```

### 2. 修改核心参数
找到以下行并修改为你需要的值。推荐配置如下：

```
# Linux atop 监控工具使用指南
LOGPATH="/var/log/atop"

# Linux atop 监控工具使用指南
LOGINTERVAL=60

# Linux atop 监控工具使用指南
LOGGENERATIONS=14
```

### 3. 重启服务
修改配置后，重启 `atop` 服务使其生效。
```bash
sudo systemctl restart atop
```

## 第四步：使用 atop

直接在终端中运行 `atop` 即可进入交互式监控界面。

### 交互界面常用快捷键
- `g`: 默认视图，显示通用信息。
- `m`: 按**内存**使用率对进程排序。
- `d`: 按**磁盘**活动对进程排序。
- `n`: 按**网络**活动对进程排序 (需要 `netatop` 模块)。
- `c`: 显示进程的完整命令行。
- `u`: 按用户聚合资源使用情况。
- `p`: 恢复到按进程聚合的默认视图。
- `h` 或 `?`: 显示帮助信息。
- `q`: 退出。

## 第五步：分析历史日志

这是 `atop` 最强大的功能。

### 1. 读取日志文件
```bash
# Linux atop 监控工具使用指南
atop -r

# Linux atop 监控工具使用指南
# Linux atop 监控工具使用指南
atop -r /var/log/atop/atop_20240921

# Linux atop 监控工具使用指南
atop -r /var/log/atop/atop_$(date -d "yesterday" +%Y%m%d)
```

### 2. 在历史记录中导航
进入历史记录视图后，使用以下快捷键：
- `t`: 向**未来**跳转一个时间间隔（你在配置文件中设置的 `LOGINTERVAL`）。
- `T`: 向**过去**跳转一个时间间隔。
- `b`: （Begin）跳转到指定的时间点，例如输入 `14:30`。

通过这些命令，你可以精确地“回放”到系统出现问题的时间点，查看当时的 CPU、内存、磁盘和网络状况，以及是哪个进程导致的问题。

## 附录：监控字段说明

- **PRC (Process)**: 进程总体状态，包括 `sys` (内核态) 和 `user` (用户态) 的 CPU 时间占比，以及运行、休眠、僵尸进程的数量。
- **CPU**: 系统总的 CPU 使用情况。`wait` 占比过高通常表示磁盘 I/O 瓶颈。
- **CPL (CPU Load)**: CPU 负载情况，包括1、5、15分钟的平均负载，以及上下文切换 (`csw`) 和中断 (`intr`) 次数。
- **MEM**: 物理内存使用情况，包括总量 (`tot`)、空闲 (`free`)、缓存 (`cache`) 和缓冲 (`buff`)。
- **SWP**: 交换空间（虚拟内存）的使用情况。
- **DSK**: 磁盘活动。`busy` 百分比显示了磁盘的繁忙程度。
- **NET**: 网络活动。顶层显示传输层（TCP/UDP）的包统计，底层显示各个网络接口的流量。

## 常见问题

**Q1: `atop` 无法启动，或提示 `command not found`?**
**A**: 确认 `atop` 已正确安装 (`which atop`)。如果已安装但无法运行，检查 `PATH` 环境变量。

**Q2: 网络监控 (`n` 快捷键) 不显示任何信息?**
**A**: `netatop` 内核模块没有被正确加载。请运行 `lsmod | grep netatop` 检查，如果无输出，请尝试手动加载 `sudo modprobe netatop` 并启动服务 `sudo systemctl start netatop`。

**Q3: 日志文件过大，占用太多磁盘空间?**
**A**: 编辑 `atop` 的配置文件（见第三步），减小 `LOGGENERATIONS` 的值（例如改为 `7` 天），或者增大 `LOGINTERVAL` 的值（例如 `120` 秒）。
