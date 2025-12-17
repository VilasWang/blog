---
title: 添加 Github Mcp Http Stdio 类型视实现不同
date: 2025-12-18 00:12:22
updated: 2025-12-18 00:12:22
categories: [后端开发]
tags: ["API", "REST", "HTTP", "JSON"]
excerpt: 以下给出 HM MES Spring Boot 后端信息上报 API 的完整使用说明，覆盖扫码过站、设备数据、异常上报三大场景。
cover: /img/default-cover.jpg
toc: true
top: false
comments: true
description: 本文分享了后端开发相关的技术实践和经验总结。
keywords: API, REST, HTTP, JSON
reading_time: 3 分钟
---

<!-- more -->

-----------------------------------------...

excerpt: ----------------------------------------------- | -------------------- | -------------------------------------------------- | --------------------------------------------------------------------- |...

description: 本文分享了技术实践和经验总结。
keywords: API, HTTP, JSON
reading_time: 18 分钟
- --

- ---------------------------------------------- | -------------------- | -------------------------------------------------- | --------------------------------------------------------------------- |
| **clangd / clang-tidy MCP**                           | 静态检查 / 代码风格 / 报错定位   | 让 MCP 客户端（如 Gemini / Claude）在上下文里直接做代码分析、报告警告、建议重构 | 你可能需要一个 wrapper，
把 clangd / clang-tidy 封装为 MCP Server（stdio 或 HTTP 通信） |
| **Build System MCP (CMake / Bazel MCP)**              | 构建任务、依赖图查询、目标管理      | 可以让 MCP “知道”你项目的构建结构、依赖关系，
一些自动 build / test 操作     | 建议自己实现或用已有的通用工具、并加一个 MCP 接口层                                          |
| **Debugger MCP (GDB/LLDB 封装为 MCP 工具)**                | 在调试时提供断点、变量查询、回溯、栈信息 | 可以在 CLI / prompt 交互时邀请 MCP 帮你做复杂调试操作               | 可能需要一个中间服务或脚本把 GDB/LLDB 输出转换成 MCP 格式                                  |
| **GitHub / Git / PR 管理 MCP**                          | 管理 PR、Issue、代码变更     | 在 review、合并、码变操作时，
用 MCP 自动辅助                       | 通常已有现成的 GitHub MCP 实现                                                 |
| **Docs & API 查询 MCP（如 Context7、Perplexity、内部文档 MCP）** | 提供库、标准库、第三方库文档查询     | 在写 C++ 代码时，随时查标准库、第三方库 API，
减少频繁切换文档网站              | 可以接入公开文档 MCP 或内部知识库 MCP                                               |
| **测试 / 覆盖率 / 性能指标 MCP**                               | 执行单元测试、收集报告、展示覆盖率    | MCP 客户端可询问 “最近测试报告如何”、"哪些函数未覆盖" 等                  | 需你把测试工具包装为 MCP 接口                                                     |

> ⚠️ 这些 MCP 服务不一定开箱即用，很多时候你要写一个 wrapper 或服务，使之符合 MCP 协议（JSON-RPC，transport 为 stdio / HTTP / SSE 等）。

- --

## 目录

- [一、C++ 开发提效 MCP 套件推荐清单](#一C-开发提效-MCP-套件推荐清单)
- [二、Gemini CLI 的 MCP 配置示例](#二Gemini-CLI-的-MCP-配置示例)
  - [1. 在 `.gemini/settings.json` 中注册 MCP Servers](#1-在-geminisettingsjson-中注册-MCP-Servers)
- [三、Claude Code CLI 的 MCP 配置示例](#三Claude-Code-CLI-的-MCP-配置示例)
  - [1. MCP 配置文件 `.mcp.json` 或 `claude_desktop_config.json`](#1-MCP-配置文件-mcpjson-或-claude_desktop_configjson)
  - [2. 使用 `claude mcp add` 命令添加 MCP（CLI 方式）](#2-使用-claude-mcp-add-命令添加-MCPCLI-方式)
  - [3. 验证 / 列表 / 测试 MCP 连接](#3-验证-列表-测试-MCP-连接)
- [四、如何把这两边的配置整合到你的 C++ 开发提效流程里](#四如何把这两边的配置整合到你的-C-开发提效流程里)

## 二、Gemini CLI 的 MCP 配置示例

Gemini CLI 对 MCP 的支持比较成熟，以下是用这套 C++ 提效 MCP 服务在 Gemini CLI 上的配置示例。

### 1. 在 `.gemini/settings.json` 中注册 MCP Servers

假设你做了下列几个 MCP Server：

* `clang-mcp`：封装 clangd / clang-tidy 的 MCP server（用 stdio 方式）
* `build-mcp`：CMake 构建系统的 MCP server（HTTP 接口）
* `gh-mcp`：GitHub MCP server（已有实现）

你的配置可能像这样：

```json

{
  "selectedAuthType": "vertex-ai",
  "theme": "GitHub",
  "mcpServers": {
    "clang-mcp": {
      "type": "stdio",
      "command": "/usr/local/bin/clang-mcp-server",   // 可执行文件
      "args": ["--stdio"],                              // 参数
      "env": {
        "PROJECT_ROOT": "${PWD}"                        // 可选环境变量
      }
    },
    "build-mcp": {
      "type": "http",
      "url": "http://localhost:8080/mcp",
      "headers": {
        "Authorization": "Bearer ${BUILD_MCP_TOKEN}"
      }
    },
    "gh-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}

```

在 Gemini CLI 中，你也可以用 `gemini mcp add` 命令来添加 MCP，但对于复杂配置通常还是直接编辑 JSON 更清晰。
FastMCP 也支持自动安装 / 集成：`fastmcp install gemini-cli server.py`。([谷歌开发者博客][1])
你可以在 Gemini CLI 内用 `/mcp` 命令查看当前 MCP 列表并验证是否连接成功。([Medium][2])

- --

## 三、Claude Code CLI 的 MCP 配置示例

Claude Code（CLI / “Code” 模式）也支持 MCP，配置方式稍有不同。官方文档说明支持 `.mcp.json`、环境变量扩展、同样支持 stdio / HTTP / SSE。([Claude 文档][3])

下面给出几种典型配置示例，以及使用 CLI 命令的方式。

### 1. MCP 配置文件 `.mcp.json` 或 `claude_desktop_config.json`

在你的用户目录或项目目录，可以创建或编辑 MCP 配置文件。示例如下：

```json

{
  "mcpServers": {
    "clang-mcp": {
      "type": "stdio",
      "command": "/usr/local/bin/clang-mcp-server",
      "args": ["--stdio"],
      "env": {
        "PROJECT_ROOT": "${PWD}"
      }
    },
    "build-mcp": {
      "type": "http",
      "url": "http://localhost:8080/mcp",
      "headers": {
        "Authorization": "Bearer ${BUILD_MCP_TOKEN}"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}

```

> Claude Code 支持在 `.mcp.json` 中使用环境变量替换（`${VAR}`、`${VAR:-default}`）([Claude 文档][3])。
> 配置文件的位置有多种：可以是用户范围，也可以是项目范围。若多个服务器同名，优先取局部项目配置（local > project > user）([Claude 文档][3])。

### 2. 使用 `claude mcp add` 命令添加 MCP（CLI 方式）

Claude Code 的 CLI 提供了一个命令来添加 MCP server 比较方便。示例：

```bash

# 添加 GitHub MCP（HTTP / stdio 类型视实现不同）
claude mcp add --transport http --scope local github https://your-mcp-github-server.com --env GITHUB_TOKEN="${GITHUB_TOKEN}"

```

或者，如果你是用 stdio 实现：

```bash

claude mcp add --transport stdio clang-mcp -- command /usr/local/bin/clang-mcp-server --args "--stdio" --scope project

```

一些参考资料提到：

* 你还可以用 `claude mcp add-json` 直接传 JSON 格式配置：([developer.sailpoint.com][4])
* 也有社区工具 `claude-code-mcp-init` 来简化配置流程：([GitHub][5])

### 3. 验证 / 列表 / 测试 MCP 连接

添加之后，你可以在 Claude Code CLI 中使用：

```bash

claude mcp list

```

查看已注册的 MCP servers，确保它们处于连接状态。
你也可以启动一个 Claude 会话，然后输入 `/mcp` 看看客户端能否与这些 MCP 通信。

- --

## 四、如何把这两边的配置整合到你的 C++ 开发提效流程里

下面是一个实际操作建议流程：

1. **先从一个简单 MCP 开始**
   例如用 clangd / clang-tidy 封装一个最简单的 MCP Server（stdio 通信），先在本地跑起来。

2. **在 Gemini CLI 上配置它**，确认能被 gemini 调用、能够处理代码片段分析请求。

3. **在 Claude Code CLI 上配置同一个 MCP**，确保无论你在 GEMINI 还是 Claude 环境下，都能调用相同的 MCP 功能。

4. **扩展更多 MCP（build / debugger / GitHub / docs）**，逐步把整个 C++ 开发流程的关键环节都覆盖。

5. **统一环境变量 / 认证机制**，用 `.env`、统一令牌管理，让两端配置尽量保持一致、可移植。

6. **监控 / 日志 /调试支持**：MCP Server 在开发初期应有调试输出、错误追踪机制，遇到通信问题时更容易定位。
