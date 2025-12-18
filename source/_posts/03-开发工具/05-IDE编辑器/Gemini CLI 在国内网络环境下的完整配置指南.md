---
title: Gemini CLI 在国内网络环境下的完整配置指南
categories:
  - 开发工具
tags:
  - 技术文档
  - 指南
abbrlink: gemini-cli-proxy
date: 2025-12-18 09:09:23
---

# Gemini CLI 在国内网络环境下的完整配置指南
> **文档创建时间**: 2025-12-18
> **最后更新**: 2025-12-18
> **标签**: `gemini-cli`, `proxy`, `vpn`, `network`, `ai-tools`, `跨域访问`

## 📑 目录

- [1. 概述](#1-概述)
- [2. 系统要求](#2-系统要求)
- [3. 环境准备](#3-环境准备)
- [4. Gemini CLI 安装配置](#4-gemini-cli-安装配置)
- [5. 代理配置](#5-代理配置)
- [6. 认证流程](#6-认证流程)
- [7. 常见问题与解决方案](#7-常见问题与解决方案)
- [8. 最佳实践](#8-最佳实践)
- [9. 验证测试](#9-验证测试)
- [10. 总结](#10-总结)

---

## 1. 📖 概述

本文档提供了一套完整的 Gemini CLI 在国内网络环境下的配置解决方案，通过代理服务和 VPN 组合，实现稳定的 Google 服务访问。

## 2. ⚙️ 系统要求

## 系统要求

### 基础环境

| 组件 | 最低版本 | 推荐版本 | 验证方法 |
|------|----------|----------|----------|
| **Node.js** | v18.x | v20.x+ | `node --version` |
| **npm** | v9.x | v10.x+ | `npm --version` |
| **操作系统** | Windows 10+ | Windows 11/macOS/Linux | 系统信息 |

### 网络环境

#### 代理服务要求
| 要求项 | 规格 | 说明 |
|--------|------|------|
| **协议支持** | ✅ HTTPS | 必须支持 SSL/TLS |
| **端口配置** | ✅ 自定义端口 | 支持常用端口（8080, 7890, 10808等） |
| **连接稳定性** | ✅ 高可用 | 99%+ 连接成功率 |
| **带宽要求** | ✅ > 1Mbps | 满足 API 调用需求 |

#### VPN 服务要求
| 要求项 | 规格 | 说明 |
|--------|------|------|
| **地理位置** | ⚠️ **美国节点推荐** | 避免地理位置限制 |
| **协议支持** | ✅ OpenVPN/WireGuard | 确保兼容性 |
| **DNS 保护** | ✅ DNS leak防护 | 防止 DNS 泄露 |
| **Kill Switch** | ✅ 自动断网保护 | 意外断开时保护隐私 |

## 环境准备

### Node.js 安装

#### Windows 安装

1. 访问 [Node.js 官网](https://nodejs.org/)
2. 下载 Windows 安装包（.msi）
3. 运行安装程序，勾选 "Add to PATH"
4. 验证安装：

```bash
node --version
npm --version
```

#### macOS 安装

```bash
# 使用 Homebrew
brew install node

# 或下载官方安装包
```

#### Linux 安装

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 或使用 NodeSource
```

### 网络连接测试

```bash
# 测试 Google 可访问性
curl -I https://google.com

# 测试特定服务器连通性
ping 216.239.32.223

# 测试 HTTPS 代理
curl -x http://127.0.0.1:8080 https://www.google.com
```

## Gemini CLI 安装配置

### 全局安装

```bash
# 标准安装命令
npm install -g @google/gemini-cli

# 验证安装
gemini --version

# 查看帮助信息
gemini --help

# 测试调试模式
gemini -d --help
```

### 安装验证

```bash
# 验证 npm 包安装
npm list -g @google/gemini-cli

# 检查可执行文件
where gemini  # Windows
which gemini   # macOS/Linux

# 测试基本功能
gemini --version
```

## 代理配置

### 环境变量配置

#### Windows 系统

**CMD 环境**：

```batch
rem 设置 HTTP 代理
set HTTP_PROXY=http://127.0.0.1:8080
set HTTPS_PROXY=https://127.0.0.1:8080

rem 验证设置
echo %HTTP_PROXY%
echo %HTTPS_PROXY%
```

**PowerShell 环境**：

```powershell
# 设置代理环境变量
$env:HTTP_PROXY="http://127.0.0.1:8080"
$env:HTTPS_PROXY="https://127.0.0.1:8080"

# 验证设置
$env:HTTP_PROXY
$env:HTTPS_PROXY
```

#### macOS/Linux 系统

```bash
# Bash/Zsh 环境
export HTTP_PROXY=http://127.0.0.1:8090
export HTTPS_PROXY=https://127.0.0.1:8090

# 验证设置
echo $HTTP_PROXY
echo $HTTPS_PROXY

# 添加到配置文件（永久生效）
echo 'export HTTP_PROXY=http://127.0.0.1:8090' >> ~/.bashrc
echo 'export HTTPS_PROXY=https://127.0.0.1:8090' >> ~/.bashrc
source ~/.bashrc
```

### 代理排除设置

```bash
# Windows CMD
set NO_PROXY=localhost,127.0.0.1,.local

# Windows PowerShell
$env:NO_PROXY="localhost,127.0.0.1,.local"

# macOS/Linux
export NO_PROXY=localhost,127.0.0.1,.local
```

### 代理服务配置示例

#### Clash 配置

```yaml
# Gemini CLI 专用规则
rules:
  # Google 相关域名走代理
  - 'DOMAIN-SUFFIX,googleapis.com,🔰 节点选择'
  - 'DOMAIN-SUFFIX,google.com,🔰 节点选择'
  - 'DOMAIN,generativelanguage.googleapis.com,🔰 节点选择'
  - 'DOMAIN,aistudio.google.com,🔰 节点选择'

  # Gemini CLI 进程走代理
  - 'PROCESS-NAME,gemini,🔰 节点选择'

proxy-groups:
  - name: 🔰 节点选择
    type: select
    proxies:
      - 美国节点1
      - 美国节点2
      - 美国节点3
```

## 认证流程

### 启动 Gemini CLI

```bash
# 基础启动
gemini

# 调试模式启动
gemini -d

# 指定模型启动
gemini --model=gemini-1.5-flash
```

### 认证步骤

1. Gemini CLI 会自动打开浏览器进行 OAuth 认证
2. 登录 Google 账号
3. 授权 Gemini CLI 访问权限
4. 浏览器会跳转回本地端口（通常为 localhost:11101）
5. CLI 确认认证成功

## 常见问题与解决方案

### 连接超时问题

**症状**：
- 终端显示 "Waiting for auth..." 后自动退出
- 浏览器授权成功但 CLI 连接失败
- 错误日志显示 `AggregateError [ETIMEDOUT]`

**解决步骤**：

```bash
# 1. 启用调试模式
gemini -d

# 2. 检查代理设置
echo $HTTPS_PROXY  # Linux/macOS
echo %HTTPS_PROXY%  # Windows

# 3. 测试网络连通性
curl -x $HTTPS_PROXY https://google.com

# 4. 检查特定服务器
curl -x $HTTPS_PROXY https://216.239.32.223

# 5. 测试 DNS 解析
nslookup google.com 8.8.8.8
```

### 认证授权问题

**检查清单**：
- [ ] 防火墙是否阻止 localhost:11101
- [ ] 杀毒软件是否拦截 Gemini CLI
- [ ] 代理是否支持 WebSocket 连接
- [ ] 浏览器是否允许重定向

### 环境变量问题

**验证方法**：

```bash
# 检查当前环境变量
env | grep -i proxy  # Linux/macOS
set | findstr PROXY     # Windows

# 测试代理连接
curl -v -x $HTTPS_PROXY https://httpbin.org/ip
```

### 解决方案

```bash
# 临时设置（当前会话有效）
export HTTPS_PROXY=http://127.0.0.1:8090

# 永久设置（写入配置文件）
echo 'export HTTPS_PROXY=http://127.0.0.1:8090' >> ~/.profile
source ~/.profile

# 系统级设置（需要管理员权限）
sudo tee /etc/environment > /dev/null <<EOF
HTTPS_PROXY=http://127.0.0.1:8090
HTTP_PROXY=http://127.0.0.1:8090
NO_PROXY=localhost,127.0.0.1,.local
EOF
```

## 最佳实践

### 性能优化

#### 节点评估标准

| 指标 | 优秀 | 良好 | 可接受 |
|------|------|------|--------|
| **延迟** | < 100ms | 100-200ms | 200-500ms |
| **稳定性** | 99.9%+ | 99%+ | 95%+ |
| **带宽** | > 10Mbps | 5-10Mbps | > 1Mbps |
| **成功率** | 100% | 99%+ | 95%+ |

#### 自动切换配置

```yaml
# Clash 配置示例
proxy-groups:
  - name: "Auto-Best-Proxy"
    type: url-test
    url: "http://www.gstatic.com/generate_204"
    interval: 300
    tolerance: 50
    use:
      - proxy-nodes
```

### 安全策略

#### 网络安全
1. **选择可信服务商**：避免使用免费或不稳定的代理服务
2. **加密通信**：确保代理支持 HTTPS 协议
3. **日志审计**：定期检查代理连接日志
4. **访问控制**：限制代理服务的访问权限

#### 账号安全
1. **两步验证**：为 Google 账号启用 2FA
2. **应用密码**：使用应用专用密码而非主密码
3. **定期审查**：检查授权的应用列表
4. **安全监控**：监控异常登录活动

## 验证测试

### 基础环境验证

```bash
# 测试基础连接
curl -I https://www.google.com

# 测试代理连接
curl -x $HTTPS_PROXY -I https://www.google.com

# 测试特定服务器
curl -x $HTTPS_PROXY -I https://216.239.32.223

# 测试 API 端点
curl -x $HTTPS_PROXY https://generativelanguage.googleapis.com
```

### 端到端测试脚本

```bash
#!/bin/bash
# Gemini CLI 认证测试脚本

echo "开始 Gemini CLI 认证测试..."

# 1. 检查环境变量
if [ -z "$HTTPS_PROXY" ]; then
    echo "❌ 代理环境变量未设置"
    exit 1
fi

echo "✅ 代理环境变量: $HTTPS_PROXY"

# 2. 测试网络连接
if ! curl -s -x "$HTTPS_PROXY" https://www.google.com > /dev/null; then
    echo "❌ 代理连接失败"
    exit 1
fi

echo "✅ 代理连接正常"

# 3. 启动调试模式
echo "启动 Gemini CLI 调试模式..."
timeout 30 gemini -d &
GEMINI_PID=$!

# 4. 等待认证完成
sleep 5

# 5. 检查进程状态
if kill -0 $GEMINI_PID 2>/dev/null; then
    echo "✅ Gemini CLI 进程运行中"
    echo "请完成浏览器认证流程"
    wait $GEMINI_PID
    echo "✅ 认证流程完成"
else
    echo "❌ Gemini CLI 进程异常退出"
fi
```

## 总结

本文档提供了一套完整的 Gemini CLI 在国内网络环境下的配置解决方案，涵盖了从环境准备到最终验证的完整流程。

### 关键成功因素

- **代理服务稳定性**：选择可靠的代理服务提供商
- **环境变量配置**：正确设置 HTTPS_PROXY 和相关环境变量
- **网络兼容性**：确保代理服务支持 HTTPS 协议和 WebSocket 连接
- **系统权限配置**：正确配置防火墙和杀毒软件

通过遵循本文档的指导原则和最佳实践，用户可以在国内网络环境中稳定、高效地使用 Gemini CLI，享受 Google AI 技术带来的便利和强大功能。