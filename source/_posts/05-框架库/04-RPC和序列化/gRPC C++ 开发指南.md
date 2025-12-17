---
tags:
  - gRPC
  - C++
  - RPC
  - Protobuf
  - 网络编程
  - protoc
title: gRPC C++ 开发指南
categories:
  - C++核心开发
  - 网络编程与RPC
description: 专业技术完全指南，涵盖理论基础、实践操作、问题排查、性能优化等全方位内容，助力技能快速提升。
abbrlink: 4f30aaf4
date: 2025-12-04 13:13:21
---

# gRPC C++ 开发指南
## 目录
- [gRPC 概述](#grpc-概述)
- [环境配置](#环境配置)
- [第一步：定义服务 (.proto)](#第一步定义服务-proto)
- [第二步：生成代码 (protoc)](#第二步生成代码-protoc)
- [第三步：实现服务端](#第三步实现服务端)
- [第四步：实现客户端](#第四步实现客户端)
- [第五步：编译与运行](#第五步编译与运行)
- [高级主题](#高级主题)
- [常见问题](#常见问题)

## gRPC 概述

gRPC 是一个由 Google 开发的、基于 HTTP/2 的高性能、开源、通用的 RPC (远程过程调用) 框架。

### 核心特性
- **高性能**: 基于 HTTP/2，支持双向流、头部压缩、多路复用。
- **IDL (接口定义语言)**: 使用 Protocol Buffers (Protobuf) 来定义服务接口和消息结构，具有强类型约束。
- **跨语言**: 支持 C++, Java, Python, Go, C#, Node.js, Ruby, PHP 等多种语言。
- **四种服务类型**:
    1.  **简单 RPC (Unary RPC)**
    2.  **服务端流式 RPC (Server streaming RPC)**
    3.  **客户端流式 RPC (Client streaming RPC)**
    4.  **双向流式 RPC (Bidirectional streaming RPC)**

## 环境配置

### 选项 A: 使用包管理器 (快速入门)
这是最简单的方式，但 gRPC 和 Protobuf 的版本可能较旧。
```bash
# gRPC C++ 开发指南
sudo apt update
sudo apt install -y libgrpc++-dev protobuf-compiler libprotobuf-dev pkg-config
```

### 选项 B: 从源码编译 (推荐)
这是获取最新版本、完全控制编译选项的推荐方式。请参考我们知识库中的这篇独立指南：
- **[gRPC & Protobuf 源码编译指南 (Linux)](./gRPC-Source-Compilation-Guide-Linux.md)**

## 第一步：定义服务 (.proto)

使用 Protocol Buffers 语法创建一个 `.proto` 文件来定义你的服务。

`chatter.proto`:
```protobuf
syntax = "proto3";

package chatter;

// 定义聊天服务
service Chatter {
  // 简单 RPC: 发送一条消息
  rpc SendMessage(MessageRequest) returns (MessageReply);

  // 服务端流: 订阅消息
  rpc SubscribeMessages(SubscriptionRequest) returns (stream MessageReply);
}

// 发送消息的请求体
message MessageRequest {
  string user_name = 1;
  string content = 2;
}

// 订阅消息的请求体
message SubscriptionRequest {
  string user_name = 1;
}

// 通用回复体
message MessageReply {
  string server_id = 1;
  string confirmation_message = 2;
}
```

## 第二步：生成代码 (protoc)

使用 `protoc` 编译器和 gRPC C++ 插件从 `.proto` 文件生成 C++ 代码。

### 1. 命令详解
```bash
protoc -I=<proto_path> --cpp_out=<out_dir> --grpc_out=<out_dir> --plugin=protoc-gen-grpc=<plugin_path> <your_proto_file>
```
- **`-I=<proto_path>`**: 指定 `.proto` 文件的搜索目录，可以有多个 `-I` 参数。
- **`--cpp_out=<out_dir>`**: 指定生成的 C++ **消息类** (`.pb.h`, `.pb.cc`) 的输出目录。
- **`--grpc_out=<out_dir>`**: 指定生成的 C++ **服务类** (`.grpc.pb.h`, `.grpc.pb.cc`) 的输出目录。
- **`--plugin=protoc-gen-grpc=<plugin_path>`**: 指定 `grpc_cpp_plugin` 可执行文件的路径。

### 2. 执行生成
```bash
# gRPC C++ 开发指南
GRPC_CPP_PLUGIN_PATH=$(which grpc_cpp_plugin)

# gRPC C++ 开发指南
protoc -I. --cpp_out=. --grpc_out=. --plugin=protoc-gen-grpc=$GRPC_CPP_PLUGIN_PATH chatter.proto
```
这将生成四个文件：`chatter.pb.h`, `chatter.pb.cc`, `chatter.grpc.pb.h`, `chatter.grpc.pb.cc`。

### 3. 自动化脚本 (推荐)
在项目中，强烈建议使用脚本来自动化代码生成，以保证一致性。

`generate_grpc.sh`:
```bash
#!/bin/bash
set -e

# gRPC C++ 开发指南
PROTO_SRC_DIR="./protos"
GENERATED_DIR="./generated"
GRPC_CPP_PLUGIN_PATH=$(which grpc_cpp_plugin)

# gRPC C++ 开发指南
if [ ! -x "$GRPC_CPP_PLUGIN_PATH" ]; then
    echo "Error: grpc_cpp_plugin not found or not executable."
    exit 1
fi

# gRPC C++ 开发指南
echo "Cleaning old generated files..."
rm -rf "$GENERATED_DIR"
mkdir -p "$GENERATED_DIR"

echo "Generating gRPC C++ code from all .proto files in $PROTO_SRC_DIR..."

protoc -I "$PROTO_SRC_DIR" \
       --cpp_out="$GENERATED_DIR" \
       --grpc_out="$GENERATED_DIR" \
       --plugin=protoc-gen-grpc="$GRPC_CPP_PLUGIN_PATH" \
       $(find "$PROTO_SRC_DIR" -name "*.proto")

echo "Code generation complete. Files are in $GENERATED_DIR"
```

## 第三步：实现服务端
(此部分及后续部分与之前版本相同，为简洁省略... 如果需要我可以完整展示)
...

## 第四步：实现客户端
...

## 第五步：编译与运行
...

## 高级主题

### 1. 异步 API
gRPC C++ 提供了一套功能强大的异步 API，这里展示更现代的**回调式 (Callback) API**。

`async_client.cpp`:
```cpp
// ... (includes and using declarations as before)

void AsyncClient() {
    auto channel = grpc::CreateChannel("localhost:50051", grpc::InsecureChannelCredentials());
    auto stub = Chatter::NewStub(channel);

    MessageRequest request;
    request.set_user_name("AsyncAlice");
    request.set_content("Hello from async C++!");

    // 1. 创建回调函数
    auto on_reply = [](Status status, MessageReply reply) {
        if (status.ok()) {
            std::cout << "Async RPC successful. Server says: " << reply.confirmation_message() << std::endl;
        } else {
            std::cout << "Async RPC failed: " << status.error_code() << ": " << status.error_message() << std::endl;
        }
    };

    // 2. 发起异步调用
    stub->async()->SendMessage(new ClientContext(), &request, new MessageReply(), on_reply);

    std::cout << "Async call initiated. Waiting for reply..." << std::endl;
    // 在实际应用中，你需要一个机制来等待回调完成，例如条件变量或在事件循环中运行。
    std::this_thread::sleep_for(std::chrono::seconds(1));
}
```

### 2. 拦截器 (Interceptor)
> **注意**: 这是一个实验性 API，未来可能会有变动。

拦截器允许你在 RPC 调用的生命周期中注入自定义逻辑（如日志、认证、监控）。
```cpp
#include <grpcpp/experimental/server_interceptor.h>

class LoggingInterceptor : public grpc::experimental::Interceptor {
public:
    void Intercept(grpc::experimental::InterceptorBatchMethods* methods) override {
        if (methods->QueryInterceptionHookPoint(
            grpc::experimental::InterceptionHookPoints::PRE_SEND_INITIAL_METADATA)) {
            std::cout << "LOG: Server processing new request." << std::endl;
        }
        // 必须调用 Proceed() 来将控制权交还给 gRPC 框架
        methods->Proceed();
    }
};

// 在 ServerBuilder 中使用
// std::vector<std::unique_ptr<grpc::experimental::ServerInterceptorFactoryInterface>> creators;
// creators.push_back(std::make_unique<YourInterceptorFactory>());
// builder.experimental().SetInterceptorCreators(std::move(creators));
```

## 常见问题

**Q1: `protoc: command not found`?**
**A**: `protoc` 不在你的 `PATH` 中。
- 如果使用 `apt` 安装，请确保 `protobuf-compiler` 已安装。
- 如果从源码编译，请确保安装路径的 `bin` 目录（如 `/usr/local/grpc/bin`）已添加到 `PATH`。

**Q2: `protoc-gen-grpc: program not found or is not executable`?**
**A**: `protoc` 找不到 gRPC C++ 插件。
- 确保 `grpc_cpp_plugin` 存在于 `PATH` 中，或者在 `--plugin` 参数中提供其完整路径。
- 检查文件是否有执行权限 (`chmod +x <path_to_plugin>`)。

**Q3: 编译生成的代码时，提示找不到 gRPC 或 Protobuf 头文件?**
**A**: 你的编译器找不到所需的头文件。
- **pkg-config (推荐)**: 确保你的编译命令包含了 `$(pkg-config --cflags grpc++ protobuf)`。
- **CMake**: 检查 `find_package(gRPC)` 和 `find_package(Protobuf)` 是否成功。如果 gRPC 安装在非标准路径，你可能需要设置 `CMAKE_PREFIX_PATH`。
- **手动编译**: 使用 `-I/path/to/includes` 手动添加正确的包含路径。

**Q4: 链接时出现 `undefined reference to` 错误?**
**A**: 链接器找不到 gRPC 或 Protobuf 的库文件。
- **pkg-config (推荐)**: 确保你的链接命令包含了 `$(pkg-config --libs grpc++ protobuf)`。
- **CMake**: 确保 `target_link_libraries` 指令正确链接了 `gRPC::grpc++` 和 `protobuf::libprotobuf`。
- **手动编译**: 使用 `-L/path/to/libs -lgrpc++ -lprotobuf` 手动添加库路径和库。
