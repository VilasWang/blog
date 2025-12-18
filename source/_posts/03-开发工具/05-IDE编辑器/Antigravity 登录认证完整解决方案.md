---
title: Antigravity 登录认证完整解决方案（非TUN方法）
categories:
  - 开发工具
  - IDE编辑器
tags:
  - Antigravity
  - 代理配置
  - OAuth认证
  - Clash
  - Proxifier
  - 网络配置
  - 企业环境
abbrlink: 56a10ecb
date: 2025-12-17 06:30:00
---

> **系统架构**：Windows 10/11 + Clash Proxy + Proxifier + Microsoft Edge
>
> **协议支持**：SOCKS5 代理 + OAuth 2.0 认证
>
> **适用场景**：国内网络环境 + 第三方服务认证
>
> **文档版本**：v2.0.0
>
> **最后更新**：2025-12-17

---

## 📋 目录

- [概述](#-概述)
- [环境准备](#-环境准备)
- [配置步骤](#-配置步骤)
- [故障排除](#-故障排除)
- [核心验证测试](#-核心验证测试)

---

## 📖 概述

### 1.1 解决方案背景

Antigravity 是一款基于云原生的开发平台，采用 OAuth 2.0 标准进行用户认证。由于国内网络环境的网络限制，直接访问 Google 认证服务存在技术壁垒，需要通过专业的代理架构实现认证链路的打通。

### 1.2 核心要求

- **Google 账号归属地必须为美国** - Antigravity 认证的硬性要求
- **代理节点必须为美国地区** - 确保与账号归属地匹配
- **企业网络环境兼容** - 适应企业防火墙和网络安全策略

### 1.3 技术架构

```ascii
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Antigravity.exe │───▶│  Proxifier      │───▶│  Clash Proxy    │
│  (OAuth Client) │    │  (Process Rule) │    │ (SOCKS5:7890)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                    │
                                               ┌─────────────┐
                                               │  US Proxy    │
                                               │  (Google API)│
                                               └─────────────┘
                                                    │
                                               ┌─────────────┐
                                               │ Google OAuth  │
                                               │  (US Region)   │
                                               └─────────────┘
```

---

## 🔧 环境准备

### 2.1 Google 账号要求

| 要求项 | 状态 | 说明 |
|--------|------|------|
| **账号归属地** | ⚠️ **必须为美国** | Antigravity 认证的硬性要求 |
| **账号状态** | ✅ 正常 | 无封禁、限制或安全警告 |
| **双重认证** | ✅ 推荐 | 建议开启 2FA 提高安全性 |
| **浏览器登录** | ✅ 已完成 | Edge 浏览器已登录目标账号 |

**⚠️ 重要提醒**：
- **非美国账号会被直接拒绝认证**
- **归属地不匹配会导致认证失败**
- **频繁切换地区会被标记为异常**

### 2.2 代理服务要求

| 要求项 | 规格 | 说明 |
|--------|------|------|
| **地理位置** | ⚠️ **必须为美国本土** | 确保与账号归属地匹配 |
| **IP 类型** | ✅ 住宅级 IP | 避免数据中心 IP 被识别 |
| **服务类型** | ✅ 专业付费服务 | 免费节点通常不可靠 |
| **协议支持** | ✅ SOCKS5 | 与 Clash 兼容 |

**推荐节点选择**：
1. **首选节点**：洛杉矶、纽约、西雅图、芝加哥
2. **备选节点**：旧金山、达拉斯、迈阿密
3. **避免使用**：香港、日本、新加坡等亚洲节点

### 2.3 软件环境要求

| 软件 | 版本要求 | 用途 |
|------|----------|------|
| **Clash** | v1.18.0+ | SOCKS5 代理服务 |
| **Proxifier** | v4.0+ | 进程级代理管理 |
| **Edge 浏览器** | v118.0+ | OAuth 认证浏览器 |
| **Antigravity** | Latest | 目标应用程序 |

---

## ⚙️ 配置步骤

### 3.1 Clash 代理配置

#### 3.1.1 节点选择
确保 Clash 客户端连接到美国地区节点，避免使用香港、日本等亚洲节点。

#### 3.1.2 规则配置
更新 Clash 配置文件，添加 Antigravity 相关规则：

```yaml
# Google Auth & Antigravity 必须走代理
rules:
  - 'DOMAIN-SUFFIX,googleapis.com,🔰 节点选择'
  - 'DOMAIN-SUFFIX,sandbox.googleapis.com,🔰 节点选择'
  - 'DOMAIN,oauth2.googleapis.com,🔰 节点选择'
  - 'DOMAIN,accounts.google.com,🔰 节点选择'
  - 'DOMAIN,daily-cloudcode-pa.sandbox.googleapis.com,🔰 节点选择'
  - 'PROCESS-NAME,Antigravity.exe,🔰 节点选择'
```

### 3.2 Proxifier 配置

#### 3.2.1 添加代理服务器
1. 打开 Proxifier → `Profile → Proxy Servers… → Add`
2. 配置参数：
   - **Address**: 127.0.0.1
   - **Port**: 7890
   - **Protocol**: SOCKS5
   - **Authentication**: NO
3. 点击 **Check** 验证连接，确认显示 "Socks5 server is available"

#### 3.2.2 创建代理规则

**规则1：Edge 浏览器直连（最高优先级）**
- **Rule name**: Edge Direct
- **Applications**: msedge.exe
- **Action**: Direct
- **Priority**: Highest

**规则2：Clash 进程直连（避免代理循环）**
- **Rule name**: Clash Processes Direct
- **Applications**: clash_*.exe
- **Action**: Direct
- **Priority**: High

**规则3：Antigravity 应用走代理**
- **Rule name**: Antigravity via Clash
- **Applications**: Antigravity.exe, language_server_windows_x64.exe
- **Action**: 127.0.0.1:7890
- **Priority**: Normal

#### 3.2.3 规则优先级确认
确保规则按以下顺序排列：
1. **Edge Direct** (最高优先级)
2. **Clash Processes Direct** (高优先级)
3. **Antigravity via Clash** (普通优先级)

### 3.3 系统环境配置

#### 3.3.1 清理环境变量
必须清空以下系统环境变量：

```bash
# Windows 命令行
set HTTP_PROXY=""
set HTTPS_PROXY=""
set NO_PROXY=""
```

或者在系统属性中永久删除这些变量。

#### 3.3.2 防火墙配置
确保防火墙允许以下连接：
- Clash.exe (TCP:7890 入站)
- Proxifier.exe (TCP 动态端口 出站)
- msedge.exe (TCP/UDP:80/443 出站)
- Antigravity.exe (TCP/UDP 动态端口 出站)

---

## 🔧 故障排除

### 4.1 认证流程问题

**问题：Edge 浏览器无法打开 Google 登录页面**

| 症状 | 可能原因 | 解决方案 |
|------|----------|----------|
| Edge 无响应 | Proxifier 规则冲突 | 检查规则顺序，Edge Direct 置顶 |
| 页面加载失败 | 环境变量污染 | 清空 HTTP_PROXY/HTTPS_PROXY |
| 连接超时 | 网络防火墙限制 | 检查防火墙配置 |

**问题：Google 登录成功但无法跳转回 Antigravity**

| 检查点 | 验证方法 | 解决方案 |
|--------|----------|----------|
| OAuth 流程 | Clash Connections 日志 | 检查 Clash 规则配置 |
| 应用代理 | Proxifier 实时日志 | 重新配置应用规则 |
| 代理循环 | Proxifier 连接日志 | 添加 Clash 直连规则 |

### 4.2 网络连接问题

**问题：代理节点连接不稳定**

```bash
# 基础连接测试
curl --proxy socks5://127.0.0.1:7890 https://www.google.com

# IP 地理位置检测
curl --proxy socks5://127.0.0.1:7890 "https://httpbin.org/ip"

# 连接稳定性测试
ping -n 10 8.8.8.8
```

**节点质量标准**：
| 指标 | 优秀 | 可接受 | 需更换 |
|------|------|--------|--------|
| **延迟** | < 100ms | 100-200ms | > 200ms |
| **稳定性** | 99.9%+ | 99%+ | < 99% |
| **成功率** | 100% | 99%+ | < 99% |

### 4.3 账号相关问题

**Google 账号安全检查清单**：
- [ ] 登录地点是否为美国地区
- [ ] 登录设备是否为已知设备
- [ ] 是否启用了两步验证
- [ ] 应用权限是否正确授权

如果账号归属地检测失败，根本原因通常是：
- **账号创建地**：非美国地区创建（困难解决）
- **常用登录地**：长期非美国登录（中等解决）
- **登录行为**：频繁切换地区（简单解决）

---

## 🧪 核心验证测试

### 5.1 基础环境验证

| 组件 | 检查命令 | 预期结果 |
|------|----------|----------|
| **Clash** | `tasklist | findstr Clash` | 进程运行 |
| **端口监听** | `netstat -an | findstr :7890` | LISTEN 状态 |
| **代理连接** | `curl -x socks5://127.0.0.1:7890 https://www.google.com` | HTTP 200 |
| **Proxifier** | 任务管理器检查 | 进程运行 |
| **环境变量** | `echo %HTTP_PROXY%` | 空值 |

### 5.2 OAuth 认证测试

**完整认证流程测试步骤**：

1. **启动 Antigravity 客户端**
   - 确认程序正常启动
   - 检查 Proxifier 日志显示代理连接

2. **触发 Google 登录**
   - 点击 OAuth 登录按钮
   - 确认 Edge 浏览器自动打开

3. **浏览器验证**
   - Edge 应直连打开 Google 登录页
   - 地址栏 URL: `accounts.google.com`
   - 页面加载正常，无代理错误

4. **账号认证**
   - 输入美国归属地 Google 账号凭据
   - 完成两步验证（如已启用）
   - 授权 Antigravity 应用访问权限

5. **回跳验证**
   - 自动跳转回 Antigravity 应用
   - 应用显示登录成功状态
   - Clash 日志显示 OAuth API 代理请求

### 5.3 关键验证点

| 检查节点 | 验证方法 | 成功状态 |
|----------|----------|----------|
| **Clash 状态** | 控制面板 | 绿色连接 |
| **端口监听** | `netstat -an` | `:7890` 处于 LISTEN |
| **代理规则** | Proxifier 规则列表 | Edge 规则置顶 |
| **浏览器访问** | 直接访问 Google | 正常加载 |
| **IP 检测** | 在线 IP 检测 | 美国地址 |
| **OAuth 请求** | Clash Connections | 显示 `googleapis.com` |

---

## 📋 核心检查清单

### 6.1 部署前检查

**Google 账号验证**：
- [ ] 账号归属地为美国地区
- [ ] 账号状态正常，无安全警告
- [ ] 已启用两步验证
- [ ] 浏览器已登录目标账号

**代理服务验证**：
- [ ] 代理节点位于美国地区
- [ ] 节点支持 Google 全套服务
- [ ] 节点连接稳定性 > 99%
- [ ] IP 地址未被 Google 标记

**软件环境验证**：
- [ ] Clash v1.18.0+ 正常运行
- [ ] Proxifier v4.0+ 已安装
- [ ] Microsoft Edge v118.0+ 已安装
- [ ] 系统环境变量已清空

### 6.2 功能验证

**基础功能测试**：
- [ ] Clash 控制面板显示连接正常
- [ ] 端口 7890 处于监听状态
- [ ] Google 服务访问正常
- [ ] IP 地址显示为美国地区

**OAuth 流程测试**：
- [ ] Antigravity 启动正常
- [ ] 点击登录按钮触发 Edge 打开
- [ ] Edge 直连访问 Google 登录页
- [ ] Google 账号登录成功
- [ ] 自动跳转回 Antigravity 应用
- [ ] 应用显示登录成功状态

---

## 📝 总结

### 7.1 关键成功因素

**成功的两大前提**：
- **Google 账号归属地必须为美国**：这是 Antigravity 认证的硬性要求
- **代理节点必须为美国地区且支持 Google 全套服务**：确保认证流量的地理合规性

**技术实施要点**：
- Proxifier 规则优先级配置是关键，Edge 浏览器必须直连
- Clash 规则需要精确匹配 Google OAuth 相关域名
- 系统环境变量必须清空，避免代理冲突
- Clash 相关进程必须直连，避免代理循环

### 7.2 快速故障排除指南

**认证失败的常见原因**：
1. **Google 账号归属地不是美国** → 更换美国账号或重新注册
2. **代理节点不在美国地区** → 切换到美国节点
3. **Edge 浏览器被代理** → 检查 Proxifier 规则优先级
4. **系统环境变量冲突** → 清空 HTTP_PROXY/HTTPS_PROXY
5. **代理循环** → 添加 clash_*.exe 直连规则

**验证成功的标志**：
- ✅ Edge OAuth 页面成功打开（直连）
- ✅ 登录后成功回跳到 Antigravity
- ✅ Clash Connections 能看到 oauth2.googleapis.com 走代理

通过遵循本文档的核心配置步骤和验证方法，可以建立一个稳定、可靠的 Antigravity 认证环境。