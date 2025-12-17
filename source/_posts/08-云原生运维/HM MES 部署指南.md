---
tags:
  - MES
  - 制造执行系统
  - 编译部署
  - Java
  - Spring Boot
  - Tomcat
  - Nginx
title: HM MES 部署指南
categories:
  - 云服务与DevOps
  - 企业级应用
description: 专业技术完全指南，涵盖理论基础、实践操作、问题排查、性能优化等全方位内容，助力技能快速提升。
abbrlink: 616ce96e
date: 2025-12-04 22:56:54
---

# HM MES 部署指南
## 目录
- [概述](#概述)
- [环境准备](#环境准备)
- [后端编译与部署](#后端编译与部署)
- [前端部署与反向代理](#前端部署与反向代理)
- [常见问题排查](#常见问题排查)

## 概述

Hm-MES 是一个基于 Java Spring Boot 的制造执行系统（MES），提供生产管理、质量控制、设备管理等一系列功能。本指南提供在 Windows 和 Ubuntu 系统上完整编译和部署 Hm-MES 的详细步骤。

### 系统架构
- **后端**: Java Spring Boot + MyBatis
- **前端**: HTML5 + JavaScript
- **中间件**: Apache Tomcat
- **数据库**: MySQL 8.0
- **消息队列 (可选)**: RabbitMQ
- **反向代理 (可选)**: Nginx

## 环境准备

### 1. 软件依赖
- **JDK**: 11 (推荐，LTS版本)
- **Maven**: 3.6+
- **Tomcat**: 9.0+
- **MySQL**: 8.0+
- **Git**

### 2. 硬件要求
- **最小配置**: 2核CPU, 4GB内存, 20GB磁盘空间
- **推荐配置**: 4核CPU, 8GB内存, 50GB磁盘空间
- **生产环境**: 8核CPU, 16GB内存, 100GB SSD磁盘

### 2. Windows 环境准备
1.  **安装 JDK**: 从 [Adoptium](https://adoptium.net/) 下载并安装。确保 `JAVA_HOME` 环境变量已设置。
2.  **安装 Maven**: 从 [Maven 官网](https://maven.apache.org/download.cgi) 下载并解压到 `<Your-Maven-Path>`。将 `<Your-Maven-Path>\bin` 添加到系统 `Path` 环境变量。
3.  **安装 Tomcat**: 从 [Tomcat 官网](https://tomcat.apache.org/download-90.cgi) 下载并解压到 `<Your-Tomcat-Path>`。
4.  **安装 MySQL**: 使用 MySQL Installer 安装，并记住设置的 root 密码。

### 3. Ubuntu 环境准备
```bash
# HM MES 部署指南
sudo apt update && sudo apt upgrade -y
sudo apt install -y openjdk-11-jdk maven tomcat9 mysql-server git

# HM MES 部署指南
sudo mysql_secure_installation

# HM MES 部署指南
sudo systemctl start tomcat9 && sudo systemctl enable tomcat9
sudo systemctl start mysql && sudo systemctl enable mysql
```

## 后端编译与部署

### 1. 获取源码
```bash
git clone https://gitee.com/liangshengpan/hm-MES.git
cd hm-MES
```

### 2. 配置数据库
```bash
# HM MES 部署指南
mysql -u root -p

# HM MES 部署指南
CREATE DATABASE hm_mes CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'hm_user'@'localhost' IDENTIFIED BY 'your_strong_password';
GRANT ALL PRIVILEGES ON hm_mes.* TO 'hm_user'@'localhost';
# HM MES 部署指南
ALTER USER 'hm_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_strong_password';
FLUSH PRIVILEGES;
EXIT;

# HM MES 部署指南
# HM MES 部署指南
mysql -u hm_user -p hm_mes < doc/hm-mes.sql
```

### 3. 修改应用配置
编辑后端项目的核心配置文件：`mes-backend/src/main/resources/application.yml`

```yaml
spring:
  datasource:
    # 确保这里的地址、数据库名、用户名和密码正确
    url: jdbc:mysql://localhost:3306/hm_mes?useSSL=false&serverTimezone=Asia/Shanghai&characterEncoding=utf8&allowPublicKeyRetrieval=true
    username: hm_user # 使用我们刚创建的用户
    password: your_strong_password # 替换为你的密码
    driver-class-name: com.mysql.cj.jdbc.Driver
  # 文件上传配置
  servlet:
    multipart:
      max-file-size: 100MB
      max-request-size: 100MB

server:
  port: 8080
  servlet:
    # 应用的上下文路径，反向代理时会用到
    context-path: /hm-mes
```

### 4. 编译打包
使用 Maven 将后端项目打包成 `.war` 文件。

```bash
# HM MES 部署指南
cd mes-backend

# HM MES 部署指南
mvn clean package -DskipTests
```
成功后，你会在 `mes-backend/target/` 目录下找到 `hm-mes.war` 文件。

### 5. 部署到 Tomcat
1.  **停止 Tomcat**:
    - Windows: 运行 `<Your-Tomcat-Path>\bin\shutdown.bat`
    - Ubuntu: `sudo systemctl stop tomcat9`
2.  **部署 WAR 文件**:
    - 将 `hm-mes.war` 文件复制到 Tomcat 的 `webapps` 目录下。
    - Windows: `<Your-Tomcat-Path>\webapps\`
    - Ubuntu: `/var/lib/tomcat9/webapps/`
3.  **启动 Tomcat**:
    - Windows: 运行 `<Your-Tomcat-Path>\bin\startup.bat`
    - Ubuntu: `sudo systemctl start tomcat9`

Tomcat 启动时会自动解压 `.war` 文件。

### 6. 访问验证
打开浏览器，访问 `http://localhost:8080/hm-mes`。如果能看到登录页面，说明后端部署成功。

## 前端部署与反向代理

为了获得更好的性能和更方便的管理，推荐使用 Nginx 来托管前端静态文件，并将 API 请求反向代理到 Tomcat。

### 1. 部署前端文件
将源码中的 `mes-front` 文件夹复制到你的 Web 服务器根目录，例如 `/var/www/html/mes-front`。

### 2. 配置 Nginx
创建一个新的 Nginx 站点配置：

```nginx
server {
    listen 80;
    server_name your_domain.com;

    # 前端静态文件根目录
    root /var/www/html/mes-front;
    index index.html;

    # 安全头设置
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # 静态资源缓存
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # SPA (单页应用) 路由支持
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API 反向代理
    # 将所有 /api/ 开头的请求转发到 Tomcat
    location /api/ {
        # 注意：这里的 /hm-mes/ 必须与 application.yml 中的 context-path 一致
        proxy_pass http://localhost:8080/hm-mes/;

        # 设置超时时间
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 文件上传大小限制
        client_max_body_size 100M;
    }
}
```
重启 Nginx 后，你就可以通过域名直接访问前端页面，并且前端发出的 API 请求会被正确转发到后端。

## 常见问题排查

**Q1: 数据库连接失败?**
**A**: 检查 `application.yml` 中的数据库地址、端口、用户名和密码是否正确。确认数据库服务正在运行，并且防火墙允许 3306 端口的连接。

**Q2: 部署后访问 404?**
**A**:
1.  检查 Tomcat 的 `logs/catalina.out` 日志，看应用是否在启动时报错。
2.  确认你的访问地址包含了正确的上下文路径，即 `http://localhost:8080/hm-mes`。
3.  如果使用了 Nginx，请检查 `proxy_pass` 路径是否正确。

**Q3: 文件上传失败?**
**A**: 检查 `application.yml` 中的 `max-file-size` 配置，以及部署目录是否有写入权限。

**Q4: MySQL 8.0 连接认证失败?**
**A**: MySQL 8.0 默认使用 caching_sha2_password 认证插件，Java 驱动可能不支持。需要将用户认证方式改为 mysql_native_password。

**Q5: Tomcat 内存溢出?**
**A**: 编辑 Tomcat 的 `setenv.sh` (Linux) 或 `setenv.bat` (Windows)，设置合适的 JVM 参数：
```bash
export CATALINA_OPTS="$CATALINA_OPTS -Xms2G -Xmx4G -XX:+UseG1GC"
```

## 生产环境部署优化

### 1. JVM 参数优化

在 Tomcat 启动脚本中添加以下 JVM 参数：

```bash
# HM MES 部署指南
-Xms4g -Xmx8g

# HM MES 部署指南
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
-XX:G1HeapRegionSize=16m

# HM MES 部署指南
-XX:+UseStringDeduplication
-XX:+OptimizeStringConcat
-Djava.awt.headless=true
-Dfile.encoding=UTF-8
-Duser.timezone=Asia/Shanghai
```

### 2. 数据库连接池配置

在 `application.yml` 中优化数据源配置：

```yaml
spring:
  datasource:
    hikari:
      # 连接池大小
      maximum-pool-size: 20
      minimum-idle: 5
      # 连接超时
      connection-timeout: 20000
      # 空闲连接超时
      idle-timeout: 300000
      # 连接最大生命周期
      max-lifetime: 900000
      # 连接测试
      connection-test-query: SELECT 1
```

### 3. 日志配置优化

使用 Logback 配置文件 `logback-spring.xml`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <!-- 生产环境日志级别 -->
    <springProfile name="prod">
        <root level="INFO">
            <appender-ref ref="FILE"/>
        </root>
    </springProfile>

    <!-- 日志文件配置 -->
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>logs/hm-mes.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>logs/hm-mes.%d{yyyy-MM-dd}.%i.log.gz</fileNamePattern>
            <maxFileSize>100MB</maxFileSize>
            <maxHistory>30</maxHistory>
            <totalSizeCap>3GB</totalSizeCap>
        </rollingPolicy>
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
</configuration>
```

### 4. 安全配置清单

- [ ] 修改默认密码和密钥
- [ ] 启用 HTTPS（配置 SSL 证书）
- [ ] 配置防火墙规则
- [ ] 禁用不必要的服务端口
- [ ] 定期备份数据库
- [ ] 配置日志轮转
- [ ] 安装系统监控工具

### 5. 防火墙配置

```bash
# HM MES 部署指南
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 3306/tcp  # MySQL (仅内网)
sudo ufw enable

# HM MES 部署指南
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

## Docker 部署方案

### 1. Dockerfile

创建 `Dockerfile`：

```dockerfile
FROM openjdk:11-jre-slim

# HM MES 部署指南
WORKDIR /app

# HM MES 部署指南
COPY target/hm-mes.war app.war

# HM MES 部署指南
RUN mkdir -p /app/logs

# HM MES 部署指南
EXPOSE 8080

# HM MES 部署指南
ENTRYPOINT ["java", "-jar", "-Djava.security.egd=file:/dev/./urandom", "app.war"]
```

### 2. Docker Compose

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: hm_mes
      MYSQL_USER: hm_user
      MYSQL_PASSWORD: your_strong_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./doc/hm-mes.sql:/docker-entrypoint-initdb.d/init.sql
    command: --default-authentication-plugin=mysql_native_password

  mes-backend:
    build: .
    ports:
      - "8080:8080"
    depends_on:
      - mysql
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://mysql:3306/hm_mes?useSSL=false&serverTimezone=Asia/Shanghai&allowPublicKeyRetrieval=true
      SPRING_DATASOURCE_USERNAME: hm_user
      SPRING_DATASOURCE_PASSWORD: your_strong_password
    volumes:
      - ./logs:/app/logs

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./mes-front:/usr/share/nginx/html
    depends_on:
      - mes-backend

volumes:
  mysql_data:
```

### 3. Docker 部署命令

```bash
# HM MES 部署指南
docker-compose up -d

# HM MES 部署指南
docker-compose ps

# HM MES 部署指南
docker-compose logs -f mes-backend

# HM MES 部署指南
docker-compose down
```

## 监控与维护

### 1. 应用监控推荐

- **Prometheus + Grafana**: 系统和应用性能监控
- **ELK Stack**: 日志收集和分析
- **Zabbix**: 综合监控平台

### 2. 备份策略

```bash
# HM MES 部署指南
#!/bin/bash
BACKUP_DIR="/backup/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# HM MES 部署指南
mysqldump -u hm_user -p'your_strong_password' hm_mes | gzip > $BACKUP_DIR/hm_mes_$DATE.sql.gz

# HM MES 部署指南
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

# HM MES 部署指南
tar -czf $BACKUP_DIR/mes-front_$DATE.tar.gz /var/www/html/mes-front
```

### 3. 性能测试建议

使用 JMeter 或 LoadRunner 进行压力测试：

- 并发用户数：100-500
- 测试场景：登录、查询、数据录入
- 监控指标：响应时间、吞吐量、CPU/内存使用率

## 总结

本指南涵盖了 Hm-MES 系统从开发环境到生产环境的完整部署流程。在实际部署中，请根据：

1. **业务规模**：调整硬件配置和 JVM 参数
2. **安全要求**：实施相应的安全措施
3. **性能需求**：优化数据库和缓存配置
4. **运维要求**：建立完善的监控和备份机制

如有问题，请联系技术支持团队。
