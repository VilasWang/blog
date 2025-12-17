---
tags:
  - 性能测试
  - 负载测试
  - 监控
  - 诊断
  - ab
  - wrk
  - Nginx
  - Apache
title: Web 服务器监控指南
categories:
  - 系统运维管理
  - 监控与诊断
description: 专业技术完全指南，涵盖理论基础、实践操作、问题排查、性能优化等全方位内容，助力技能快速提升。
abbrlink: d7f169a4
date: 2025-12-04 13:13:25
---

# Web 服务器监控指南
## 目录
- [概述](#概述)
- [第一部分：连接与健康检查](#第一部分连接与健康检查)
- [第二部分：性能与负载测试](#第二部分性能与负载测试)
- [第三部分：安全扫描与测试](#第三部分安全扫描与测试)
- [第四部分：实时系统监控](#第四部分实时系统监控)
- [第五部分：日志分析](#第五部分日志分析)

## 概述

本指南提供了一系列常用的命令行工具，用于测试、诊断和监控任何 Web 服务器（如 Nginx, Apache 等）的健康状况、性能和安全性。

## 第一部分：连接与健康检查

这些工具用于快速验证服务器是否在线、端口是否开放以及服务是否正常响应。

### `curl`
一个强大的 URL 传输工具，用于发送各种网络请求。

```bash
# Web 服务器监控指南
curl -I http://your_domain.com

# Web 服务器监控指南
curl -I -L http://your_domain.com

# Web 服务器监控指南
curl -v https://your_domain.com
```

### `telnet` / `nc` (Netcat)
用于测试特定端口是否可以建立 TCP 连接。

```bash
# Web 服务器监控指南
telnet your_domain.com 80

# Web 服务器监控指南
nc -zv your_domain.com 80
nc -zv your_domain.com 443
```

### `nmap`
一个网络扫描工具，用于发现主机和开放的端口。

```bash
# Web 服务器监控指南
nmap your_domain.com

# Web 服务器监控指南
nmap -p 80,443 your_domain.com
```

## 第二部分：性能与负载测试

这些工具用于向服务器施加压力，以评估其在负载下的性能表现。

### `ab` (Apache Bench)
Apache 自带的轻量级压力测试工具。

```bash
# Web 服务器监控指南
# Web 服务器监控指南
ab -n 1000 -c 100 https://your_domain.com/

# Web 服务器监控指南
ab -k -n 10000 -c 200 https://your_domain.com/
```

### `wrk` / `wrk2`
一个现代、高性能的 HTTP 压测工具，能产生极高的负载。

```bash
# Web 服务器监控指南
# Web 服务器监控指南
wrk -t12 -c400 -d30s https://your_domain.com/

# Web 服务器监控指南
# Web 服务器监控指南
# Web 服务器监控指南
```

### `siege`
一款功能丰富的压力测试工具，可以模拟大量用户并发访问。

```bash
# Web 服务器监控指南
siege -c 100 -t1M https://your_domain.com/

# Web 服务器监控指南
siege -c 50 -f urls.txt
```

## 第三部分：安全扫描与测试

### `openssl s_client`
用于调试 SSL/TLS 连接和检查证书信息。

```bash
# Web 服务器监控指南
openssl s_client -connect your_domain.com:443 -showcerts

# Web 服务器监控指南
openssl s_client -connect your_domain.com:443 -tls1_3
```

### 在线扫描工具
- **SSL Labs SSL Test**: 全面分析你网站的 SSL/TLS 配置，并给出评分和改进建议。
  - [https://www.ssllabs.com/ssltest/](https://www.ssllabs.com/ssltest/)
- **Security Headers**: 检查你网站的 HTTP 安全头配置。
  - [https://securityheaders.com/](https://securityheaders.com/)

## 第四部分：实时系统监控

这些是排查服务器性能问题时最常用的 Linux 命令。

### CPU 监控
- **`top`**: 实时显示系统中各个进程的资源占用状况。
- **`htop`**: `top` 的增强版，界面更友好，操作更方便。
- **`vmstat 1`**: 每秒报告一次虚拟内存、进程、CPU 活动等信息。

### 内存监控
- **`free -h`**: 以人类可读的格式显示内存使用情况（总量、已用、可用、缓存等）。
- **`cat /proc/meminfo`**: 显示内核追踪到的详细内存信息。

### 磁盘 I/O 监控
- **`df -h`**: 查看磁盘空间使用情况。
- **`iostat -x 1`**: 每秒显示一次磁盘的读写性能指标（如 `await`, `%util`）。

### 网络监控
- **`netstat -tlnp`**: 显示所有正在监听的 TCP 和 UDP 端口及其对应的程序。
- **`iftop`**: 实时监控网络接口的流量。
- **`nethogs`**: 按进程分组显示网络带宽占用情况。

## 第五部分：日志分析

日志是排查问题的金矿。`tail`, `grep`, `awk` 是最强大的组合。

### 实时查看日志
```bash
# Web 服务器监控指南
sudo tail -f /var/log/nginx/access.log

# Web 服务器监控指南
sudo tail -f /var/log/apache2/error.log
```

### 常用分析命令

```bash
# Web 服务器监控指南
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head -10

# Web 服务器监控指南
awk '{print $9}' /var/log/apache2/access.log | sort | uniq -c | sort -nr

# Web 服务器监控指南
grep ' 404 ' /var/log/nginx/access.log
```
