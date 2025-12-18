---
title: Windows 环境下配置 GitHub MCP 服务器完整指南
categories:
  - 开发工具
tags:
  - 技术文档
  - 指南
abbrlink: windows-github-mcp
date: 2025-12-18 09:09:23
---

# Windows 环境下配置 GitHub MCP 服务器完整指南
> **文档创建时间**: 2025-12-18
> **最后更新**: 2025-12-18
> **标签**: `github`, `mcp`, `windows`, `powershell`, `gemini-cli`, `ai-tools`

## 📑 目录

- [1. 概述](#1-概述)
- [2. 生成 GitHub PAT](#2-生成-github-pat)
- [3. 设置环境变量](#3-设置环境变量)
- [4. 编辑 Gemini CLI 配置](#4-编辑-gemini-cli-配置)
- [5. 安装必要的依赖](#5-安装必要的依赖)
- [6. 验证配置](#6-验证配置)
- [7. 故障排除](#7-故障排除)
- [8. 最佳实践](#8-最佳实践)
- [9. 总结](#9-总结)

---

## 1. 📖 概述

本文将详细介绍在Windows环境下如何配置GitHub MCP (Model Context Protocol) 服务器，让您可以在Gemini CLI中直接操作GitHub仓库。

## 2. 🔑 生成 GitHub PAT

## 步骤 1：生成 GitHub PAT

按照以下步骤在GitHub创建一个**Fine-grained Token**（细粒度令牌）：

### 1.1 访问GitHub设置

1. 登录GitHub账户
2. 点击右上角头像
3. 选择 "Settings"（设置）
4. 在左侧菜单中选择 "Developer settings"
5. 点击 "Personal access tokens" → "Fine-grained tokens"

### 1.2 创建新令牌

1. 点击 "Generate new token"
2. 输入令牌名称（如："Gemini MCP Server"）
3. 设置过期时间（建议选择90天）

### 1.3 配置权限

**Repository access**：
- 选择你要访问的仓库
- 建议选择 "Only select repositories" 并指定相关仓库

**Permissions**（权限配置）：
- **Contents** → Read & Write（读写代码内容）
- **Issues** → Read & Write（管理Issues）
- **Pull requests** → Read & Write（管理PR）
- **Metadata** → Read（读取仓库元数据）

### 1.4 复制令牌

生成后立即复制并保存令牌，格式如下：
```
ghp_abcd1234efgh5678ijkl90mnopqrstuvwx
```

## 步骤 2：设置环境变量（Windows）

### 2.1 使用PowerShell设置

在Windows PowerShell中运行以下命令：

```powershell
# 设置用户级环境变量
setx GITHUB_PERSONAL_ACCESS_TOKEN "你的GitHub令牌"

# 设置会话级环境变量（立即生效）
$env:GITHUB_PERSONAL_ACCESS_TOKEN = "你的GitHub令牌"
```

### 2.2 验证设置

重新打开一个新的PowerShell窗口，验证环境变量：

```powershell
# 查看环境变量值
echo $env:GITHUB_PERSONAL_ACCESS_TOKEN

# 或者
Get-ChildItem Env:GITHUB_PERSONAL_ACCESS_TOKEN
```

## 步骤 3：编辑 Gemini CLI 配置

### 3.1 定位配置文件

- **全局配置路径**：`%USERPROFILE%\.gemini\settings.json`
- **项目级配置路径**：`你的项目目录\.gemini\settings.json`

### 3.2 创建配置文件

如果配置文件不存在，先创建：

```powershell
# 创建配置目录
mkdir $env:USERPROFILE\.gemini

# 编辑配置文件
notepad $env:USERPROFILE\.gemini\settings.json
```

### 3.3 配置MCP服务器

在 `settings.json` 中写入以下内容：

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

## 步骤 4：安装必要的依赖

### 4.1 安装Node.js（如果尚未安装）

访问 [Node.js官网](https://nodejs.org/) 下载并安装LTS版本。

### 4.2 安装GitHub MCP服务器

在PowerShell中执行：

```powershell
# 全局安装GitHub MCP服务器
npm install -g @modelcontextprotocol/server-github

# 验证安装
npx @modelcontextprotocol/server-github --help
```

## 步骤 5：验证配置

### 5.1 启动Gemini CLI

```powershell
# 启动Gemini CLI
gemini
```

### 5.2 测试MCP连接

在Gemini CLI中输入：

```
/mcp
```

如果配置成功，你应该能看到 "github mcp server connected" 的提示。

### 5.3 测试功能

尝试以下命令测试GitHub MCP功能：

```
列出我仓库中的open issues
查看我的个人资料信息
列出最近修改的仓库
```

## 故障排除

### 常见问题及解决方案

1. **MCP服务器连接失败**
   - 检查环境变量是否正确设置
   - 确认GitHub PAT权限配置正确
   - 验证网络连接

2. **权限错误**
   - 确保PAT包含必要的权限
   - 检查PAT是否已过期

3. **npx命令失败**
   - 确保Node.js已正确安装
   - 检查npm全局安装路径

## 最佳实践

1. **安全性**：
   - 定期更新PAT
   - 使用最小权限原则
   - 不要在代码中硬编码令牌

2. **性能优化**：
   - 使用项目级配置而非全局配置
   - 定期清理不必要的MCP服务器配置

3. **维护**：
   - 定期检查令牌有效性
   - 更新MCP服务器版本

## 总结

通过以上步骤，您已经在Windows环境下成功配置了GitHub MCP服务器，现在可以在Gemini CLI中直接操作GitHub仓库了。这个配置让您能够更高效地管理代码仓库，提升开发效率。

## 相关链接

- [GitHub Fine-grained tokens文档](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- [Model Context Protocol官网](https://modelcontextprotocol.io/)
- [Gemini CLI文档](https://ai.google.dev/gemini-api/docs/cli)