---
title: Docker 部署指南
categories:
  - 开发工具与流程
  - 构建与部署
tags:
  - Docker
  - Linux
  - Nginx
  - Redis
  - Git
description: 详细介绍Docker容器化部署完整指南的技术实现、配置方法、最佳实践等内容。
author: vilas
abbrlink: 4beba163
date: 2025-12-09 12:46:41
---

# Docker 部署指南
## 概述

Docker容器化部署是现代应用部署的标准方式，本文详细介绍如何使用Docker进行应用容器化部署。

## Docker基础概念

### 什么是Docker

Docker是一个开源的容器化平台，可以将应用和依赖打包成轻量级、可移植的容器。

### 核心组件

- **Docker Engine**: 容器运行时
- **Docker Compose**: 多容器应用编排
- **Docker Registry**: 镜像仓库

## 安装Docker

### Ubuntu安装

```bash
# Docker 部署指南
sudo apt-get update

# Docker 部署指南
sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release

# Docker 部署指南
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Docker 部署指南
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Docker 部署指南
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

### CentOS安装

```bash
# Docker 部署指南
sudo yum install -y yum-utils

# Docker 部署指南
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Docker 部署指南
sudo yum install docker-ce docker-ce-cli containerd.io
```

## Dockerfile编写

### 基础Dockerfile示例

```dockerfile
# Docker 部署指南
FROM node:16-alpine

# Docker 部署指南
WORKDIR /app

# Docker 部署指南
COPY package*.json ./

# Docker 部署指南
RUN npm install

# Docker 部署指南
COPY . .

# Docker 部署指南
EXPOSE 3000

# Docker 部署指南
CMD ["npm", "start"]
```

### 多阶段构建

```dockerfile
# Docker 部署指南
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Docker 部署指南
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Docker Compose

### 基本配置文件

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### 高级配置

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.prod
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

## 部署最佳实践

### 1. 镜像优化

- 使用轻量级基础镜像
- 多阶段构建减少镜像大小
- .dockerignore文件排除不必要文件

### 2. 安全配置

- 使用非root用户运行容器
- 定期更新基础镜像
- 扫描镜像漏洞

### 3. 资源管理

- 设置内存和CPU限制
- 配置健康检查
- 实现优雅关闭

## 生产环境部署

### 环境变量配置

```bash
# Docker 部署指南
echo "NODE_ENV=production" > .env
echo "DATABASE_URL=postgresql://..." >> .env
echo "REDIS_URL=redis://..." >> .env
```

### 启动服务

```bash
# Docker 部署指南
docker-compose up -d --build

# Docker 部署指南
docker-compose ps

# Docker 部署指南
docker-compose logs -f app
```

### 更新部署

```bash
# Docker 部署指南
git pull origin main

# Docker 部署指南
docker-compose up -d --build --force-recreate
```

## 监控和日志

### 日志管理

```bash
# Docker 部署指南
docker-compose logs

# Docker 部署指南
docker-compose logs app

# Docker 部署指南
docker-compose logs -f --tail=100
```

### 性能监控

```bash
# Docker 部署指南
docker stats

# Docker 部署指南
docker inspect <container_id>
```

## 故障排查

### 常见问题解决

1. **容器启动失败**
   ```bash
   # 查看容器日志
   docker logs <container_id>

   # 进入容器调试
   docker exec -it <container_id> /bin/sh
   ```

2. **网络连接问题**
   ```bash
   # 检查网络配置
   docker network ls
   docker network inspect <network_name>
   ```

3. **资源不足**
   ```bash
   # 清理无用镜像
   docker image prune -a

   # 清理无用容器
   docker container prune
   ```

## 总结

Docker容器化部署提供了标准化的部署方式，大大简化了应用的部署和维护过程。通过合理配置Docker和Docker Compose，可以构建出高可用、可扩展的容器化应用架构。