---
tags:
  - Redis
  - C++
  - hiredis
  - Linux
  - 开发环境
title: Redis Hiredis Linux 安装指南
categories:
  - 后端服务架构
  - 数据库与缓存
description: 专业技术完全指南，涵盖理论基础、实践操作、问题排查、性能优化等全方位内容，助力技能快速提升。
abbrlink: f0a1549f
date: 2025-12-04 13:13:24
---

# Redis Hiredis Linux 安装指南
## 目录
- [概述](#概述)
- [第一步：安装和配置 Redis 服务](#第一步安装和配置-redis-服务)
- [第二步：安装 hiredis 客户端库](#第二步安装-hiredis-客户端库)
- [第三步：搭建 C++ 项目 (CMake)](#第三步搭建-c-项目-cmake)
- [第四步：编写 RedisClient 封装类](#第四步编写-redisclient-封装类)
- [第五步：编写主程序并测试](#第五步编写主程序并测试)
- [常见问题](#常见问题)
- [最佳实践](#最佳实践)

## 概述
本指南将介绍如何在 Linux (Ubuntu/Debian) 环境下，为 C++ 项目配置 Redis 开发环境。我们将使用 `hiredis` 这个官方推荐的、轻量级的 C 语言客户端库。

## 第一步：安装和配置 Redis 服务

### 1. 安装 Redis 服务器
```bash
# Redis Hiredis Linux 安装指南
sudo apt update
sudo apt install -y redis-server
```

### 2. 配置 Redis
为了安全和远程访问，建议修改配置文件。
```bash
# Redis Hiredis Linux 安装指南
sudo nano /etc/redis/redis.conf
```
找到并修改以下几行：
```conf
# Redis Hiredis Linux 安装指南
bind 0.0.0.0

# Redis Hiredis Linux 安装指南
requirepass your_strong_password

# Redis Hiredis Linux 安装指南
protected-mode no
```

### 3. 管理 Redis 服务
```bash
# Redis Hiredis Linux 安装指南
sudo systemctl restart redis-server

# Redis Hiredis Linux 安装指南
sudo systemctl status redis-server

# Redis Hiredis Linux 安装指南
sudo systemctl enable redis-server
```

## 第二步：安装 hiredis 客户端库

`hiredis` 是与 Redis 一同开发的官方 C 客户端库。

```bash
# Redis Hiredis Linux 安装指南
sudo apt install -y libhiredis-dev
```
这会自动将头文件和库文件安装到系统标准路径中。

## 第三步：搭建 C++ 项目 (CMake)

### 1. 创建项目结构
```bash
mkdir redis_cpp_demo && cd redis_cpp_demo
mkdir src include
touch CMakeLists.txt src/main.cpp src/redis_client.cpp include/redis_client.h
```

### 2. 编写 `CMakeLists.txt`
使用 `pkg-config` 来查找 `hiredis` 是最简单和最可移植的方式。

```cmake
cmake_minimum_required(VERSION 3.10)
project(RedisCppDemo)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Redis Hiredis Linux 安装指南
find_package(PkgConfig REQUIRED)
pkg_check_modules(HIREDIS REQUIRED hiredis)

# Redis Hiredis Linux 安装指南
include_directories(${HIREDIS_INCLUDE_DIRS})

# Redis Hiredis Linux 安装指南
add_executable(redis_demo src/main.cpp src/redis_client.cpp)

# Redis Hiredis Linux 安装指南
target_link_libraries(redis_demo PRIVATE ${HIREDIS_LIBRARIES})
```

## 第四步：编写 RedisClient 封装类

创建一个 C++ 类来封装 `hiredis` 的 C 风格 API，使其更易于使用。

`include/redis_client.h`:
```cpp
#ifndef REDIS_CLIENT_H
#define REDIS_CLIENT_H

#include <string>
#include <vector>
#include <hiredis/hiredis.h>

class RedisClient {
public:
    RedisClient(const std::string& host = "127.0.0.1", int port = 6379, const std::string& password = "");
    ~RedisClient();

    bool connect();
    void disconnect();
    bool isConnected() const;
    std::string getLastError() const;

    // String commands
    bool set(const std::string& key, const std::string& value);
    std::string get(const std::string& key);

    // Hash commands
    bool hset(const std::string& key, const std::string& field, const std::string& value);
    std::string hget(const std::string& key, const std::string& field);

    // Key commands
    bool del(const std::string& key);
    bool exists(const std::string& key);

private:
    redisContext* m_context;
    std::string m_host;
    int m_port;
    std::string m_password;

    bool authenticate();
};

#endif // REDIS_CLIENT_H
```

`src/redis_client.cpp`:
```cpp
#include "redis_client.h"
#include <iostream>
#include <cstring> // For strcmp

RedisClient::RedisClient(const std::string& host, int port, const std::string& password)
    : m_context(nullptr), m_host(host), m_port(port), m_password(password) {}

RedisClient::~RedisClient() {
    disconnect();
}

bool RedisClient::connect() {
    struct timeval timeout = {2, 0}; // 2 seconds
    m_context = redisConnectWithTimeout(m_host.c_str(), m_port, timeout);
    if (m_context == nullptr || m_context->err) {
        return false;
    }
    if (!m_password.empty() && !authenticate()) {
        disconnect();
        return false;
    }
    return true;
}

void RedisClient::disconnect() {
    if (m_context) {
        redisFree(m_context);
        m_context = nullptr;
    }
}

bool RedisClient::isConnected() const {
    return m_context != nullptr && m_context->err == 0;
}

std::string RedisClient::getLastError() const {
    return (m_context && m_context->errstr) ? m_context->errstr : "";
}

bool RedisClient::authenticate() {
    redisReply* reply = static_cast<redisReply*>(redisCommand(m_context, "AUTH %s", m_password.c_str()));
    if (!reply) return false;
    bool success = (reply->type == REDIS_REPLY_STATUS && strcmp(reply->str, "OK") == 0);
    freeReplyObject(reply);
    return success;
}

bool RedisClient::set(const std::string& key, const std::string& value) {
    if (!isConnected()) return false;
    redisReply* reply = static_cast<redisReply*>(redisCommand(m_context, "SET %s %s", key.c_str(), value.c_str()));
    if (!reply) return false;
    bool success = (reply->type == REDIS_REPLY_STATUS && strcmp(reply->str, "OK") == 0);
    freeReplyObject(reply);
    return success;
}

std::string RedisClient::get(const std::string& key) {
    if (!isConnected()) return "";
    redisReply* reply = static_cast<redisReply*>(redisCommand(m_context, "GET %s", key.c_str()));
    if (!reply || reply->type != REDIS_REPLY_STRING) {
        if (reply) freeReplyObject(reply);
        return "";
    }
    std::string result = reply->str;
    freeReplyObject(reply);
    return result;
}

bool RedisClient::del(const std::string& key) {
    if (!isConnected()) return false;
    redisReply* reply = static_cast<redisReply*>(redisCommand(m_context, "DEL %s", key.c_str()));
    if (!reply) return false;
    bool success = (reply->type == REDIS_REPLY_INTEGER && reply->integer > 0);
    freeReplyObject(reply);
    return success;
}

bool RedisClient::hset(const std::string& key, const std::string& field, const std::string& value) {
    if (!isConnected()) return false;
    redisReply* reply = static_cast<redisReply*>(redisCommand(m_context, "HSET %s %s %s", key.c_str(), field.c_str(), value.c_str()));
    if (!reply) return false;
    bool success = (reply->type == REDIS_REPLY_INTEGER);
    freeReplyObject(reply);
    return success;
}

std::string RedisClient::hget(const std::string& key, const std::string& field) {
    if (!isConnected()) return "";
    redisReply* reply = static_cast<redisReply*>(redisCommand(m_context, "HGET %s %s", key.c_str(), field.c_str()));
    if (!reply || reply->type != REDIS_REPLY_STRING) {
        if (reply) freeReplyObject(reply);
        return "";
    }
    std::string result = reply->str;
    freeReplyObject(reply);
    return result;
}

bool RedisClient::exists(const std::string& key) {
    if (!isConnected()) return false;
    redisReply* reply = static_cast<redisReply*>(redisCommand(m_context, "EXISTS %s", key.c_str()));
    if (!reply) return false;
    bool success = (reply->type == REDIS_REPLY_INTEGER && reply->integer == 1);
    freeReplyObject(reply);
    return success;
}
```

## 第五步：编写主程序并测试

`src/main.cpp`:
```cpp
#include "redis_client.h"
#include <iostream>

int main() {
    RedisClient redis("127.0.0.1", 6379, "your_strong_password");

    if (!redis.connect()) {
        std::cerr << "Failed to connect to Redis: " << redis.getLastError() << std::endl;
        return 1;
    }

    std::cout << "=== Redis C++ Client Test ===\n";

    // 1. String operations
    std::cout << "\n1. Testing string operations...\n";
    if (redis.set("test_key", "Hello from hiredis!")) {
        std::cout << "SET successful.\n";
        std::string value = redis.get("test_key");
        std::cout << "GET 'test_key': " << value << std::endl;
    }

    // 2. Hash operations
    std::cout << "\n2. Testing hash operations...\n";
    redis.hset("user:1001", "name", "Alice");
    redis.hset("user:1001", "age", "30");
    std::cout << "User name: " << redis.hget("user:1001", "name") << std::endl;

    // 3. Key operations
    std::cout << "\n3. Cleaning up...\n";
    if (redis.del("test_key")) {
        std::cout << "DEL 'test_key' successful.\n";
    }
    if (redis.del("user:1001")) {
        std::cout << "DEL 'user:1001' successful.\n";
    }

    return 0;
}
```

## 常见问题

**Q1: 连接被拒绝 (Connection refused)?**
**A**: 确认 Redis 服务正在运行，并且 `redis.conf` 中的 `bind` 指令允许你的 IP 访问。检查防火墙设置。

**Q2: 认证失败 (Authentication failed)?**
**A**: 确认 `redis.conf` 中的 `requirepass` 与你客户端代码中使用的密码完全一致。

**Q3: 编译时找不到 `hiredis/hiredis.h`?**
**A**: 确认 `libhiredis-dev` 已正确安装。运行 `pkg-config --cflags hiredis` 检查 `pkg-config` 是否能找到头文件路径。如果不能，你的 `pkg-config` 路径可能不完整。

## 最佳实践

- **连接管理**: 对于需要频繁操作 Redis 的长时运行应用，应使用**连接池**来复用 `RedisClient` 对象，避免频繁地建立和断开 TCP 连接。
- **错误处理**: 在每次 Redis 命令执行后，都应检查 `reply` 指针是否为 `nullptr` 以及 `m_context->err` 标志，以处理网络断开等问题。
- **异步操作**: `hiredis` 也提供了异步 API (`redisAsyncContext`)。对于高并发场景，应使用异步客户端以避免阻塞。
- **配置外置**: 不要将 Redis 的地址、端口和密码硬编码在代码中。将它们放在配置文件或环境变量中。
