---
tags:
  - Nginx
  - 反向代理
  - HTTPS
  - SSL
  - Let's Encrypt
  - 负载均衡
  - Ubuntu
title: Nginx Ubuntu 反向代理指南
categories:
  - 后端服务架构
  - Web服务器配置
description: 详细的技术安装与配置指南，提供从零开始的完整部署流程，包含环境检查、依赖安装、参数配置、测试验证等关键步骤。
abbrlink: ebeb0722
date: 2025-12-04 22:25:54
---

# Nginx Ubuntu 反向代理指南
## 目录
- [第一步：安装 Nginx](#第一步安装-nginx)
- [第二步：设置基础 Web 服务器](#第二步设置基础-web-服务器)
- [第三步：配置反向代理与 HTTPS](#第三步配置反向代理与-https)
- [第四步：使用 Certbot 自动配置 SSL](#第四步使用-certbot-自动配置-ssl)
- [第五步：配置多个本地应用的反向代理 (可选)](#第五步配置多个本地应用的反向代理-可选)
- [第六步：配置负载均衡 (可选)](#第六步配置负载均衡-可选)
- [附录：性能与安全优化](#附录性能与安全优化)
- [常见问题](#常见问题)

## 第一步：安装 Nginx

```bash
# Nginx Ubuntu 反向代理指南
sudo apt update

# Nginx Ubuntu 反向代理指南
sudo apt install -y nginx

# Nginx Ubuntu 反向代理指南
sudo ufw allow 'Nginx Full'

# Nginx Ubuntu 反向代理指南
sudo systemctl status nginx
```
安装完成后，通过浏览器访问 `http://<你的服务器IP>`，应能看到 Nginx 的欢迎页面。

## 第二步：设置基础 Web 服务器

即使我们主要用 Nginx 做反向代理，创建一个基础的服务器块（Server Block）也是一个好习惯。

```bash
# Nginx Ubuntu 反向代理指南
sudo mkdir -p /var/www/your_domain.com/html
sudo chown -R $USER:$USER /var/www/your_domain.com

# Nginx Ubuntu 反向代理指南
sudo nano /etc/nginx/sites-available/your_domain.com
```

将以下基础配置粘贴进去：
```nginx
server {
    listen 80;
    listen [::]:80;

    root /var/www/your_domain.com/html;
    index index.html;

    server_name your_domain.com www.your_domain.com;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

```bash
# Nginx Ubuntu 反向代理指南
sudo ln -s /etc/nginx/sites-available/your_domain.com /etc/nginx/sites-enabled/

# Nginx Ubuntu 反向代理指南
sudo nginx -t

# Nginx Ubuntu 反向代理指南
sudo systemctl restart nginx
```

## 第三步：配置反向代理与 HTTPS

现在，我们将修改配置文件，使其将 HTTP 请求重定向到 HTTPS，并将所有流量反向代理到一个后端应用（例如，一个运行在 `localhost:8080` 的 Node.js 或 Java 应用）。

编辑你的配置文件：`sudo nano /etc/nginx/sites-available/your_domain.com`

```nginx
# Nginx Ubuntu 反向代理指南
server {
    listen 80;
    listen [::]:80;
    server_name your_domain.com www.your_domain.com;

    # 将所有 HTTP 请求 301 重定向到 HTTPS
    return 301 https://$host$request_uri;
}

# Nginx Ubuntu 反向代理指南
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name your_domain.com www.your_domain.com;

    # SSL 证书路径 (稍后由 Certbot 自动填充)
    ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;

    # --- SSL/TLS 安全增强配置 ---
    # 推荐只使用 TLS 1.2 和 1.3，这是当前的安全标准
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    # 现代 OpenSSL 兼容的安全加密套件（2024年推荐）
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;

    # SSL 会话缓存优化
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_session_tickets off;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;
    
    # --- 安全头 (Security Headers) ---
    # HSTS (HTTP Strict Transport Security): 强制客户端在指定时间内只能通过 HTTPS 访问
    add_header Strict-Transport-Security "max-age=15768000; includeSubDomains; preload" always;
    # X-Frame-Options: 防止点击劫持攻击
    add_header X-Frame-Options DENY;
    # X-Content-Type-Options: 防止 MIME 类型嗅探攻击
    add_header X-Content-Type-Options nosniff;
    # X-XSS-Protection: 启用 XSS 保护
    add_header X-XSS-Protection "1; mode=block";
    # Referrer Policy: 控制referrer信息发送
    add_header Referrer-Policy "strict-origin-when-cross-origin";
    # Content Security Policy: 防止代码注入攻击（基础配置）
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data: https:; connect-src 'self'; frame-ancestors 'none';";

    # 核心：反向代理配置
    location / {
        # 将请求转发到后端应用
        proxy_pass http://127.0.0.1:8080;

        # 设置必要的请求头，以便后端应用能获取到真实的客户端信息
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket 支持 (如果后端应用需要)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## 第四步：使用 Certbot 自动配置 SSL

Let's Encrypt 提供免费的 SSL 证书，`certbot` 是其官方推荐的客户端。

```bash
# Nginx Ubuntu 反向代理指南
sudo apt install -y certbot python3-certbot-nginx

# Nginx Ubuntu 反向代理指南
# Nginx Ubuntu 反向代理指南
sudo certbot --nginx -d your_domain.com -d www.your_domain.com

# Nginx Ubuntu 反向代理指南
# Nginx Ubuntu 反向代理指南
# Nginx Ubuntu 反向代理指南
sudo certbot renew --dry-run
```
执行完毕后，你的网站就应该可以通过 `https://your_domain.com` 访问了。

## 第五步：配置多个本地应用的反向代理 (可选)

如果你有多个本地应用需要通过同一个域名访问，可以基于不同的路径前缀进行反向代理配置。

编辑你的配置文件：`sudo nano /etc/nginx/sites-available/your_domain.com`

```nginx
# Nginx Ubuntu 反向代理指南
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name your_domain.com www.your_domain.com;

    # SSL 证书路径 (由 Certbot 自动配置)
    ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;

    # SSL/TLS 安全配置...
    # (同之前的配置)

    # --- 多个应用的反向代理配置 ---

    # API 服务 (运行在端口 3000)
    location /api/ {
        proxy_pass http://127.0.0.1:3000/;

        # 设置必要的请求头
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # API 服务优化配置
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }

    # 管理后台 (运行在端口 8080)
    location /admin/ {
        proxy_pass http://127.0.0.1:8080/;

        # 设置必要的请求头
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket 服务 (运行在端口 9090)
    location /ws/ {
        proxy_pass http://127.0.0.1:9090/;

        # WebSocket 特殊配置
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket 超时配置
        proxy_read_timeout 86400;
        proxy_send_timeout 86400;
    }

    # 静态文件服务 (前端应用，运行在端口 3001)
    location / {
        proxy_pass http://127.0.0.1:3001/;

        # 设置必要的请求头
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 静态文件优化
        proxy_cache_bypass $http_upgrade;
        proxy_set_header Connection "";
    }

    # 特定文件类型的缓存配置
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        proxy_pass http://127.0.0.1:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 缓存配置
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header Vary Accept-Encoding;
    }
}
```

### 配置说明

1. **路径匹配规则**：
   - `/api/` → 匹配所有以 `/api/` 开头的请求
   - `/admin/` → 匹配所有以 `/admin/` 开头的请求
   - `/ws/` → 匹配所有以 `/ws/` 开头的请求
   - `/` → 匹配所有其他请求（默认）

2. **proxy_pass 路径处理**：
   - `proxy_pass http://127.0.0.1:3000/` → 末尾的 `/` 会将匹配的 location 路径部分完全替换
   - 例如：`/api/users` → 转发到 `http://127.0.0.1:3000/users`（`/api/` 被完全移除）

   对比示例：

   ```nginx
   # 带末尾斜杠（移除匹配路径）
   location /api/ {
       proxy_pass http://127.0.0.1:3000/;
   }
   # /api/users → http://127.0.0.1:3000/users

   # 不带末尾斜杠（保留完整路径）
   location /api/ {
       proxy_pass http://127.0.0.1:3000;
   }
   # /api/users → http://127.0.0.1:3000/api/users
   ```

3. **WebSocket 支持注意事项**：
   - 必须设置 `proxy_http_version 1.1`
   - 必须添加 `Upgrade` 和 `Connection` 头
   - 建议增加超时时间，防止连接断开

4. **测试配置**：

```bash
# Nginx Ubuntu 反向代理指南
sudo nginx -t

# Nginx Ubuntu 反向代理指南
sudo systemctl restart nginx

# Nginx Ubuntu 反向代理指南
# Nginx Ubuntu 反向代理指南
# Nginx Ubuntu 反向代理指南
# Nginx Ubuntu 反向代理指南
# Nginx Ubuntu 反向代理指南
# Nginx Ubuntu 反向代理指南
curl -I https://your_domain.com
```

## 第六步：配置负载均衡 (可选)

如果你有多个后端应用服务器，可以使用 Nginx 的 `upstream` 模块来实现负载均衡。

编辑你的配置文件：`sudo nano /etc/nginx/sites-available/your_domain.com`

```nginx
# Nginx Ubuntu 反向代理指南
upstream backend_servers {
    # 默认策略是轮询 (Round Robin)
    server backend1.example.com:8080;
    server backend2.example.com:8080;

    # 也可以指定权重 (weight)
    # server backend1.example.com:8080 weight=3;
    # server backend2.example.com:8080 weight=1;

    # 或者使用 ip_hash 策略，确保同一客户端总是访问同一台服务器
    # ip_hash;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name your_domain.com;

    # SSL 证书配置（同前文）
    ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;

    # SSL 安全配置（同前文）
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;

    location / {
        # 将请求转发到上游服务器组
        proxy_pass http://backend_servers;

        # 设置必要的请求头
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
修改配置后，不要忘记测试和重启 Nginx：`sudo nginx -t && sudo systemctl restart nginx`。

## 附录：性能与安全优化

### Gzip 压缩
在 `/etc/nginx/nginx.conf` 的 `http` 块中添加或取消注释：
```nginx
http {
    # ...
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_min_length 1000;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/javascript
        application/xml+rss
        application/json
        application/xml
        image/svg+xml;
    # ...
}
```

### 隐藏 Nginx 版本号
同样在 `http` 块中添加：
```nginx
http {
    # ...
    server_tokens off;
    # ...
}
```

### 缓冲区优化
在 `http` 或 `server` 块中配置：
```nginx
# Nginx Ubuntu 反向代理指南
client_body_buffer_size 128k;
client_max_body_size 20m;

# Nginx Ubuntu 反向代理指南
proxy_buffering on;
proxy_buffer_size 4k;
proxy_buffers 8 4k;
proxy_busy_buffers_size 8k;

# Nginx Ubuntu 反向代理指南
client_header_timeout 10;
client_body_timeout 10;
keepalive_timeout 65;
send_timeout 10;
```

### 连接限制
防止 DoS 攻击：
```nginx
# Nginx Ubuntu 反向代理指南
limit_conn_zone $binary_remote_addr zone=addr:10m;

# Nginx Ubuntu 反向代理指南
limit_conn addr 10;
```

### 禁用不安全的 HTTP 方法
```nginx
server {
    # ...
    # 禁用 TRACE 和 TRACK 方法
    if ($request_method ~ ^(TRACE|TRACK)$) {
        return 405;
    }
}
```

## 常见问题

**Q: 502 Bad Gateway 错误?**
**A**: 这通常意味着 Nginx 无法连接到你的后端应用。请检查：
1.  你的后端应用（如 Node.js, Java）是否正在 `127.0.0.1:8080` 上正常运行。
2.  检查后端应用的防火墙设置。
3.  查看 Nginx 的错误日志 `sudo tail -f /var/log/nginx/error.log`。

**Q: HTTPS 网站提示不安全?**
**A**: 这通常是 SSL 证书配置问题。
1.  确保证书路径正确。
2.  确保证书链完整 (`fullchain.pem`)。
3.  使用 SSL Labs 的 [SSL Test](https://www.ssllabs.com/ssltest/) 工具来全面分析你的 HTTPS 配置。

**Q: 证书续期失败?**

**A**: 检查以下几点：

1.  确认服务器时间正确：`sudo timedatectl status`
2.  手动测试续期：`sudo certbot renew --dry-run`
3.  检查 cron 或 systemd timer 是否正常运行：`sudo systemctl status certbot.timer`

**Q: WebSocket 连接失败?**

**A**: 检查以下配置：
1.  确保设置了 `proxy_http_version 1.1`
2.  确保添加了正确的 `Upgrade` 和 `Connection` 头
3.  检查后端应用是否支持 WebSocket
4.  确认超时设置足够长

**Q: 静态文件 404 错误?**

**A**: 可能的原因：
1.  后端应用端口未正确启动
2.  静态文件路径不正确
3.  权限问题：检查 `sudo chown -R www-data:www-data /var/www/`
4.  检查 SELinux 或 AppArmor 是否阻止访问

**Q: 如何查看 Nginx 访问日志和错误日志?**

**A**: 日志文件位置：
- 访问日志：`/var/log/nginx/access.log`
- 错误日志：`/var/log/nginx/error.log`
- 实时监控：`sudo tail -f /var/log/nginx/error.log`

**Q: 如何重载 Nginx 配置而不中断服务?**

**A**: 使用重载命令：
```bash
sudo nginx -t && sudo systemctl reload nginx
```