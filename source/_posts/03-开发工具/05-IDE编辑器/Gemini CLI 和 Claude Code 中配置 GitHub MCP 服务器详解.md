---
title: Gemini CLI 和 Claude Code 中配置 GitHub MCP 服务器详解
categories:
  - 开发工具
tags:
  - 技术文档
  - 指南
abbrlink: mcp-github-config
date: 2025-12-18 09:09:23
---

# Gemini CLI 和 Claude Code 中配置 GitHub MCP 服务器详解
> **文档创建时间**: 2025-12-18
> **最后更新**: 2025-12-18
> **标签**: `github`, `mcp`, `gemini-cli`, `claude-code`, `http`, `stdio`, `ai-tools`

## 📑 目录

- [1. MCP传输方式对比](#1-mcp传输方式对比)
- [2. Gemini CLI 的 MCP 配置](#2-gemini-cli-的-mcp-配置)
- [3. Claude Code 的 MCP 配置](#3-claude-code-的-mcp-配置)
- [4. 实现差异详解](#4-实现差异详解)
- [5. 最佳实践建议](#5-最佳实践建议)
- [6. 故障排除](#6-故障排除)
- [7. 性能优化](#7-性能优化)
- [8. 总结](#8-总结)

---

## 1. 📖 MCP传输方式对比

## MCP传输方式对比

### HTTP vs stdio 传输方式

| 特性 | HTTP传输 | stdio传输 |
|------|-----------|------------|
| **实现复杂度** | 相对简单 | 较简单 |
| **调试便利性** | 容易调试（可用curl等工具） | 调试较困难 |
| **跨平台性** | 优秀 | 需考虑换行符问题 |
| **安全考虑** | 需要处理认证 | 通过stdin/stdout通信 |
| **性能** | 有网络开销 | 直接进程通信 |
| **扩展性** | 易于集群部署 | 单进程限制 |

## 一、Gemini CLI 的 MCP 配置

### 1.1 HTTP方式配置

HTTP方式适合已经实现了REST API的MCP服务器：

```json
{
  "selectedAuthType": "vertex-ai",
  "theme": "GitHub",
  "mcpServers": {
    "github-http": {
      "type": "http",
      "url": "http://localhost:8080/mcp",
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}",
        "Content-Type": "application/json"
      }
    }
  }
}
```

### 1.2 stdio方式配置

stdio方式适合直接命令行启动的MCP服务器：

```json
{
  "selectedAuthType": "vertex-ai",
  "theme": "GitHub",
  "mcpServers": {
    "github-stdio": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

### 1.3 混合配置示例

同时支持两种传输方式：

```json
{
  "selectedAuthType": "vertex-ai",
  "theme": "GitHub",
  "mcpServers": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    },
    "github-fallback": {
      "type": "http",
      "url": "http://localhost:8080/github-mcp",
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}"
      }
    }
  }
}
```

## 二、Claude Code 的 MCP 配置

### 2.1 配置文件位置

Claude Code支持多个配置文件位置：

- 用户级配置：`~/.claude/claude_desktop_config.json`
- 项目级配置：`.claude/claude_desktop_config.json`
- 临时配置：`./mcp.json`

### 2.2 HTTP方式配置

```json
{
  "mcpServers": {
    "github-api": {
      "type": "http",
      "url": "https://api.github.com/mcp",
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}",
        "X-GitHub-API-Version": "2022-11-28"
      }
    }
  }
}
```

### 2.3 stdio方式配置

```json
{
  "mcpServers": {
    "github-cli": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

### 2.4 使用CLI命令添加MCP

Claude Code提供了便捷的CLI命令：

```bash
# 添加HTTP类型的MCP服务器
claude mcp add --transport http \
  --name github-api \
  --url https://api.github.com/mcp \
  --env GITHUB_TOKEN="${GITHUB_TOKEN}"

# 添加stdio类型的MCP服务器
claude mcp add --transport stdio \
  --name github-cli \
  --command npx \
  --args "-y" "@modelcontextprotocol/server-github" \
  --env GITHUB_PERSONAL_ACCESS_TOKEN="${GITHUB_PERSONAL_ACCESS_TOKEN}"
```

## 三、实现差异详解

### 3.1 服务器端实现

#### HTTP服务器示例

```python
# github_mcp_http_server.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess

class GitHubMCPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # 处理MCP请求
        response = self.handle_mcp_request(json.loads(post_data))

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

def handle_mcp_request(self, request):
    # 实现MCP协议逻辑
    if request.get('method') == 'tools/list':
        return {'tools': list_available_tools()}
    elif request.get('method') == 'tools/call':
        return execute_tool_call(request)
    return {}

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), GitHubMCPHandler)
    server.serve_forever()
```

#### stdio服务器示例

```python
# github_mcp_stdio_server.py
import sys
import json

def main():
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            request = json.loads(line.strip())
            response = handle_mcp_request(request)

            print(json.dumps(response))
            sys.stdout.flush()

        except Exception as e:
            error_response = {
                'error': {
                    'code': -32603,
                    'message': str(e)
                }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == '__main__':
    main()
```

### 3.2 认证处理差异

#### HTTP认证

```json
{
  "headers": {
    "Authorization": "Bearer ${GITHUB_TOKEN}",
    "X-API-Key": "${API_KEY}"
  }
}
```

#### stdio认证

```json
{
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}",
    "API_KEY": "${API_KEY}"
  }
}
```

## 四、最佳实践建议

### 4.1 选择传输方式的考虑因素

1. **开发阶段**：使用stdio，便于调试
2. **生产环境**：使用HTTP，便于监控和扩展
3. **网络环境**：受限环境可能需要stdio
4. **性能要求**：高频调用使用stdio

### 4.2 错误处理策略

```json
{
  "mcpServers": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}",
        "NODE_ENV": "production"
      },
      "retries": 3,
      "timeout": 30000
    },
    "github-backup": {
      "type": "http",
      "url": "http://backup-server:8080/mcp",
      "fallback": true
    }
  }
}
```

### 4.3 安全考虑

1. **令牌管理**：
   - 使用环境变量，避免硬编码
   - 定期轮换访问令牌
   - 使用最小权限原则

2. **网络安全**：
   - HTTP方式使用HTTPS
   - 验证服务器证书
   - 限制访问来源

3. **数据保护**：
   - 敏感数据脱敏
   - 日志记录控制
   - 临时文件清理

## 五、故障排除

### 5.1 常见问题

1. **连接超时**
   ```json
   {
     "timeout": 60000,
     "retries": 5,
     "retryDelay": 1000
   }
   ```

2. **认证失败**
   - 检查环境变量设置
   - 验证令牌有效性
   - 确认权限配置

3. **通信错误**
   - stdio：检查换行符（\n vs \r\n）
   - HTTP：检查Content-Type头

### 5.2 调试技巧

#### HTTP方式调试

```bash
# 测试连接
curl -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -d '{"jsonrpc": "2.0", "method": "tools/list"}'
```

#### stdio方式调试

```bash
# 手动测试
echo '{"jsonrpc": "2.0", "method": "tools/list"}' | npx -y @modelcontextprotocol/server-github
```

## 六、性能优化

### 6.1 HTTP优化

```json
{
  "headers": {
    "Connection": "keep-alive",
    "Keep-Alive": "timeout=60, max=100"
  },
  "timeout": 30000
}
```

### 6.2 stdio优化

```python
# 批量处理请求
def batch_process_requests(requests):
    results = []
    for request in requests:
        results.append(handle_request(request))
    return results
```

## 七、总结

HTTP和stdio两种传输方式各有优势：

- **HTTP**：易于调试、扩展性好、适合分布式部署
- **stdio**：性能高、实现简单、适合本地开发

根据实际需求选择合适的传输方式，并做好错误处理和安全防护。通过合理的配置和优化，可以在Gemini CLI和Claude Code中稳定地使用GitHub MCP服务器，提升开发效率。

## 参考资料

- [Model Context Protocol官方文档](https://modelcontextprotocol.io/)
- [Gemini CLI文档](https://ai.google.dev/gemini-api/docs/cli)
- [Claude Code文档](https://docs.anthropic.com/claude/docs/claude-for-developers)