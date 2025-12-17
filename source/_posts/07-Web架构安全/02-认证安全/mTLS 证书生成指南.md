---
title: mTLS 证书生成指南
categories:
  - Web架构安全
tags:
  - 技术文档
  - 指南
abbrlink: cb45c274
date: 2025-12-09 14:09:54
---

# mTLS 证书生成指南
## 生成 CA 证书

```bash
# mTLS 证书生成指南
openssl genrsa -aes256 -out ca-key.pem 4096

# mTLS 证书生成指南
openssl genrsa -out ca-key.pem 4096

# mTLS 证书生成指南
openssl req -new -x509 -days 3650 -key ca-key.pem -out ca-crt.pem -sha256
```

**CA 证书生成注意事项：**
- Common Name: 输入 CA 名称，如 "My-CA"
- Organization: 输入组织名称
- Country: 输入国家代码，如 "CN"
- 有效期建议设置为 10 年 (3650 天)

## 生成服务器证书

### 1. 生成服务器私钥

```bash
openssl genrsa -out server-key.pem 2048
```

### 2. 生成服务器证书签名请求

```bash
openssl req -new -sha256 -key server-key.pem -out server-csr.pem
```

**在提示输入信息时：**
- **Country Name**: 与 CA 证书相同
- **State or Province Name**: 省份名称
- **Locality Name**: 城市名称
- **Organization Name**: 服务器所属组织
- **Organizational Unit Name**: 部门名称（可选）
- **Common Name**: **重要！** 必须填写服务器的域名或 IP 地址
- **Email Address**: 邮箱地址（可选）

### 3. 创建服务器证书扩展配置文件

创建 `server_cert_ext.cnf` 文件：

```ini
[server_cert]
basicConstraints = critical, CA:FALSE
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = your-domain.com
IP.1 = 127.0.0.1
IP.2 = your-server-ip
```

### 4. 生成服务器证书

```bash
openssl x509 -req -in server-csr.pem -CA ca-crt.pem -CAkey ca-key.pem -CAcreateserial -out server-crt.pem -days 365 -sha256 -extfile server_cert_ext.cnf -extensions server_cert

# mTLS 证书生成指南
openssl verify -CAfile ca-crt.pem server-crt.pem
```

### 5. 查看证书详情

```bash
openssl x509 -in server-crt.pem -text -noout -purpose
```

## 生成客户端证书

### 1. 生成客户端私钥

```bash
openssl genrsa -out client-key.pem 2048
```

### 2. 生成客户端证书签名请求

```bash
openssl req -new -sha256 -key client-key.pem -out client-csr.pem
```

**在提示输入信息时：**
- **Country Name**: 与 CA 证书相同
- **State or Province Name**: 省份名称
- **Locality Name**: 城市名称
- **Organization Name**: 客户端所属组织
- **Organizational Unit Name**: 部门名称（可选）
- **Common Name**: 客户端标识名称（用于区分不同客户端）
- **Email Address**: 邮箱地址（可选）

### 3. 创建客户端证书扩展配置文件

创建 `client_cert_ext.cnf` 文件：

```ini
[client_cert]
basicConstraints = critical, CA:FALSE
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = clientAuth
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
subjectAltName = @alt_names

[alt_names]
DNS.1 = client
DNS.2 = localhost
```

### 4. 生成客户端证书

```bash
openssl x509 -req -in client-csr.pem -CA ca-crt.pem -CAkey ca-key.pem -CAcreateserial -out client-crt.pem -days 365 -sha256 -extfile client_cert_ext.cnf -extensions client_cert

# mTLS 证书生成指南
openssl verify -CAfile ca-crt.pem client-crt.pem
```

### 5. 查看证书详情

```bash
openssl x509 -in client-crt.pem -text -noout -purpose
```

## 证书验证测试

```bash
# mTLS 证书生成指南
openssl s_server -cert server-crt.pem -key server-key.pem -CAfile ca-crt.pem -Verify 1 -port 8443

# mTLS 证书生成指南
openssl s_client -connect localhost:8443 -cert client-crt.pem -key client-key.pem -CAfile ca-crt.pem
```

## 文件说明

- `ca-key.pem`: CA 私钥（妥善保管）
- `ca-crt.pem`: CA 根证书（客户端需要信任此证书）
- `ca.srl`: CA 序列号文件
- `server-key.pem`: 服务器私钥
- `server-csr.pem`: 服务器证书签名请求（可删除）
- `server-crt.pem`: 服务器证书
- `client-key.pem`: 客户端私钥
- `client-csr.pem`: 客户端证书签名请求（可删除）
- `client-crt.pem`: 客户端证书

## 安全注意事项

1. **私钥保护**: 所有 `.pem` 私钥文件必须严格保护，不要泄露
2. **证书有效期**: 定期检查和更新即将过期的证书
3. **Common Name**: 服务器证书的 Common Name 必须与实际访问的域名匹配
4. **SAN 扩展**: 现代浏览器要求使用 SAN (Subject Alternative Name) 而不是 CN
5. **密码保护**: 生产环境中建议为私钥设置密码保护

## 使用场景

- **服务器端**: 配置 web 服务器（Nginx、Apache 等）使用 `server-crt.pem` 和 `server-key.pem`
- **客户端**: 配置应用程序使用 `client-crt.pem` 和 `client-key.pem` 进行双向认证
- **信任链**: 客户端需要将 `ca-crt.pem` 添加到信任证书存储中