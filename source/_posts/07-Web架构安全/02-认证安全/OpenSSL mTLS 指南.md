---
tags:
  - OpenSSL
  - SSL
  - TLS
  - mTLS
  - 双向认证
  - CA
  - 证书
  - DH
title: OpenSSL mTLS 指南
categories:
  - 后端服务架构
  - 安全与证书
description: 专业技术完全指南，涵盖理论基础、实践操作、问题排查、性能优化等全方位内容，助力技能快速提升。
abbrlink: f4106d49
date: 2025-12-04 22:33:09
---

# OpenSSL mTLS 指南
## 目录
- [概述](#概述)
- [第一步：生成根证书 (CA)](#第一步生成根证书-ca)
- [第二步：生成服务器证书](#第二步生成服务器证书)
- [第三步：生成客户端证书](#第三步生成客户端证书)
- [第四步：验证与打包](#第四步验证与打包)
- [附录A：完整自动化脚本](#附录a完整自动化脚本)
- [附录B：在 Nginx 中配置双向认证](#附录b在-nginx-中配置双向认证)
- [附录C：生成 DH 参数 (可选)](#附录c生成-dh-参数-可选)
- [附录D：常用 OpenSSL 命令](#附录d常用-openssl-命令)

## 概述

双向认证（Mutual TLS, mTLS）是一种高安全性的认证模式，它要求客户端和服务器双方都出示并验证对方的数字证书，从而确保通信双方的身份都是可信的。本指南将详细介绍如何使用 OpenSSL 创建一套完整的、用于双向认证的证书。

### 证书体系
我们将创建以下三类证书：
1.  **根证书 (CA)**: 证书颁发机构，用于签发服务器和客户端证书。它是信任链的顶点。
2.  **服务器证书**: 用于向客户端证明服务器的身份。
3.  **客户端证书**: 用于向服务器证明客户端的身份。

## 第一步：生成根证书 (CA)

CA 是整个信任体系的基础，其私钥必须被严格保管。

### 1. 创建 CA 私钥
```bash
# OpenSSL mTLS 指南
openssl genrsa -out ca.key 4096

# OpenSSL mTLS 指南
chmod 400 ca.key
```

### 2. 创建自签名的 CA 证书
使用上一步的私钥，创建一个有效期为10年的根证书。
```bash
# OpenSSL mTLS 指南
openssl req -new -x509 -days 3650 -key ca.key -out ca.crt \
  -subj "/C=CN/ST=Beijing/L=Beijing/O=MyOrg CA/CN=MyRootCA"
```

## 第二步：生成服务器证书

服务器证书用于向客户端证明其身份，其 `CN` (Common Name) 或 `SAN` (Subject Alternative Name) 必须与服务器的域名或 IP 地址匹配。

### 1. 创建服务器私钥
```bash
openssl genrsa -out server.key 2048
chmod 400 server.key
```

### 2. 创建服务器证书签名请求 (CSR)
CSR 文件包含了服务器的公钥和身份信息，将用于向 CA 申请签名。
```bash
openssl req -new -key server.key -out server.csr \
  -subj "/C=CN/ST=Beijing/L=Beijing/O=MyOrg/CN=server.your_domain.com"
```

### 3. 创建扩展配置文件 (v3.ext)
为了让证书支持多域名或 IP 地址（`SAN`），并指定其用途为“服务器认证”，我们需要一个扩展配置文件。

`v3.ext`:
```ini
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = server.your_domain.com
DNS.2 = api.your_domain.com
IP.1 = 192.168.1.100
```

### 4. 使用 CA 签发服务器证书
```bash
# OpenSSL mTLS 指南
# OpenSSL mTLS 指南
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
  -days 365 -sha256 -extfile v3.ext -out server.crt

# OpenSSL mTLS 指南
chmod 644 server.crt
chmod 400 server.key
```

## 第三步：生成客户端证书

客户端证书用于向服务器证明客户端的身份。

### 1. 创建客户端私钥
```bash
openssl genrsa -out client.key 2048
chmod 400 client.key
```

### 2. 创建客户端 CSR
```bash
openssl req -new -key client.key -out client.csr \
  -subj "/C=CN/ST=Beijing/L=Beijing/O=MyOrg/CN=my_client_id"
```

### 3. 修改扩展配置文件
为了指定证书用于“客户端认证”，修改 `v3.ext` 文件中的 `extendedKeyUsage`。
```ini
# OpenSSL mTLS 指南
extendedKeyUsage = clientAuth
# OpenSSL mTLS 指南
```

### 4. 使用 CA 签发客户端证书
```bash
# OpenSSL mTLS 指南
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
  -days 365 -sha256 -extfile v3.ext -out client.crt

# OpenSSL mTLS 指南
chmod 644 client.crt
chmod 400 client.key
```

## 第四步：验证与打包

### 1. 验证证书链
```bash
# OpenSSL mTLS 指南
openssl verify -CAfile ca.crt server.crt
# OpenSSL mTLS 指南
# OpenSSL mTLS 指南
openssl verify -CAfile ca.crt client.crt
# OpenSSL mTLS 指南
```

### 2. 打包为 PKCS#12 (.p12) 格式 (可选)
`.p12` 文件是一个加密的容器，可以同时包含证书和私钥，方便在各种应用（如浏览器、Java KeyStore）中导入。

```bash
# OpenSSL mTLS 指南
echo "Creating PKCS#12 file..."
openssl pkcs12 -export -out client.p12 -inkey client.key -in client.crt -certfile ca.crt \
  -name "My Client Certificate"

# OpenSSL mTLS 指南
openssl pkcs12 -info -in client.p12 -nodes

# OpenSSL mTLS 指南
# OpenSSL mTLS 指南
# OpenSSL mTLS 指南
# OpenSSL mTLS 指南
```

## 附录A：完整自动化脚本

将以下内容保存为 `generate_certs.sh`，赋予执行权限 (`chmod +x`) 后运行即可一键生成所有证书。

```bash
#!/bin/bash
set -e

echo "=== Generating Mutual TLS Certificates ==="

# OpenSSL mTLS 指南
COUNTRY="CN"
STATE="Beijing"
CITY="Beijing"
ORG="MyOrganization"
DOMAIN="your_domain.com"
CERT_DAYS=365
KEY_SIZE=2048

# OpenSSL mTLS 指南
rm -f *.key *.crt *.csr *.p12 *.srl v3.ext

# OpenSSL mTLS 指南
echo "[1/4] Generating CA certificate..."
openssl genrsa -out ca.key $KEY_SIZE
chmod 400 ca.key
openssl req -new -x509 -days 3650 -key ca.key -out ca.crt \
  -subj "/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORG CA/CN=MyRootCA"

# OpenSSL mTLS 指南
echo "[2/4] Generating Server certificate..."
openssl genrsa -out server.key $KEY_SIZE
chmod 400 server.key
openssl req -new -key server.key -out server.csr \
  -subj "/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORG/CN=server.$DOMAIN"

cat > v3.ext << EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names
[alt_names]
DNS.1 = server.$DOMAIN
DNS.2 = localhost
IP.1 = 127.0.0.1
EOF

openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
  -days $CERT_DAYS -sha256 -extfile v3.ext -out server.crt

# OpenSSL mTLS 指南
echo "[3/4] Generating Client certificate..."
openssl genrsa -out client.key $KEY_SIZE
chmod 400 client.key
openssl req -new -key client.key -out client.csr \
  -subj "/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORG/CN=client1"

# OpenSSL mTLS 指南
sed -i -e 's/serverAuth/clientAuth/g' v3.ext

openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
  -days $CERT_DAYS -sha256 -extfile v3.ext -out client.crt

# OpenSSL mTLS 指南
echo "[4/4] Verifying and packaging certificates..."
openssl verify -CAfile ca.crt server.crt
openssl verify -CAfile ca.crt client.crt

# OpenSSL mTLS 指南
echo "Please enter password for PKCS#12 export:"
openssl pkcs12 -export -out client.p12 -inkey client.key -in client.crt -certfile ca.crt \
  -name "MyClientCert"

# OpenSSL mTLS 指南
echo "Cleaning up temporary files..."
rm -f *.csr *.srl v3.ext v3.ext-e

# OpenSSL mTLS 指南
chmod 400 *.key
chmod 644 *.crt
if [[ -f "client.p12" ]]; then
    chmod 400 client.p12
fi

echo ""
echo "=== All certificates generated successfully! ==="
echo ""
echo "Files created:"
echo "  ca.key    - CA private key (KEEP SECRET!)"
echo "  ca.crt    - CA certificate"
echo "  server.key - Server private key"
echo "  server.crt - Server certificate"
echo "  client.key - Client private key"
echo "  client.crt - Client certificate"
echo "  client.p12 - PKCS#12 bundle (if created)"
```

## 附录B：在 Nginx 中配置双向认证

### 基础配置
```nginx
server {
    listen 443 ssl http2;
    server_name server.your_domain.com;

    # SSL 证书配置
    ssl_certificate         /path/to/server.crt;
    ssl_certificate_key     /path/to/server.key;

    # mTLS 配置 - CA 证书用于验证客户端
    ssl_client_certificate  /path/to/ca.crt;
    ssl_verify_client       on;
    ssl_verify_depth        2;  # 验证深度

    # SSL 安全配置
    ssl_protocols           TLSv1.2 TLSv1.3;
    ssl_ciphers             ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers on;

    location / {
        # 设置客户端证书信息到环境变量
        proxy_set_header X-SSL-Client-S-DN $ssl_client_s_dn;
        proxy_set_header X-SSL-Client-Verify $ssl_client_verify;
        proxy_set_header X-SSL-Client-Cert $ssl_client_cert;

        # 你的应用逻辑
        proxy_pass http://backend;
    }
}
```

### 可选验证级别
```nginx
# OpenSSL mTLS 指南
ssl_verify_client on;

# OpenSSL mTLS 指南
ssl_verify_client optional;

# OpenSSL mTLS 指南
ssl_verify_client optional_no_ca;
```

## 附录C：生成 DH 参数 (可选)

Diffie-Hellman (DH) 参数用于密钥交换协议，以实现**完美前向保密 (Perfect Forward Secrecy, PFS)**。在 Nginx 等服务器上配置 DHE/EDH 加密套件时，推荐使用自定义的、强度更高的 DH 参数文件。

```bash
# OpenSSL mTLS 指南
# OpenSSL mTLS 指南
openssl dhparam -out dhparam.pem 2048

# OpenSSL mTLS 指南
# OpenSSL mTLS 指南
```

在 Nginx 配置中，你可以这样使用它：
```nginx
server {
    # ...
    ssl_certificate         /path/to/server.crt;
    ssl_certificate_key     /path/to/server.key;

    # 添加 DH 参数文件路径
    ssl_dhparam             /path/to/dhparam.pem;
    # ...
}
```

## 附录D：常用 OpenSSL 命令

- **查看证书内容**: `openssl x509 -in mycert.crt -text -noout`
- **查看证书有效期**: `openssl x509 -in mycert.crt -dates -noout`
- **查看证书序列号**: `openssl x509 -in mycert.crt -noout -serial`
- **查看证书指纹**: `openssl x509 -in mycert.crt -noout -fingerprint -sha256`
- **查看私钥内容**: `openssl rsa -in mykey.key -text -noout`
- **查看私钥模数**: `openssl rsa -in mykey.key -noout -modulus`
- **移除私钥密码**: `openssl rsa -in encrypted.key -out decrypted.key`
- **加密私钥**: `openssl rsa -in decrypted.key -aes256 -out encrypted.key`
- **验证证书链**: `openssl verify -CAfile ca.crt -untrusted intermediate.crt server.crt`
- **验证私钥与证书是否匹配**:
  ```bash
  # 方法1：比较模数
  openssl x509 -noout -modulus -in mycert.crt | openssl md5
  openssl rsa -noout -modulus -in mykey.key | openssl md5
  # 两个命令的输出应完全一致

  # 方法2：直接验证
  openssl x509 -noout -text -in mycert.crt | grep -A1 "RSA Public Key"
  openssl rsa -noout -text -in mykey.key | grep -A1 "publicExponent"
  ```

### 其他常用命令
```bash
# OpenSSL mTLS 指南
openssl x509 -pubkey -noout -in mycert.crt > pubkey.pem

# OpenSSL mTLS 指南
openssl rsa -pubout -in mykey.key -out pubkey.pem

# OpenSSL mTLS 指南
openssl x509 -checkend 0 -noout -in mycert.crt
# OpenSSL mTLS 指南
openssl x509 -checkend 2592000 -noout -in mycert.crt

# OpenSSL mTLS 指南
cat server.crt intermediate.crt ca.crt > fullchain.pem
```