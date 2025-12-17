---
tags:
  - Drogon
  - C++
  - Web框架
  - Windows
  - 编译安装
title: Drogon 编译指南
categories:
  - C++核心开发
  - 系统库与框架
description: 详细的技术安装与配置指南，提供从零开始的完整部署流程，包含环境检查、依赖安装、参数配置、测试验证等关键步骤。
abbrlink: b47a5d97
date: 2025-12-04 13:13:21
---

# Drogon 编译指南
## 目录
- [概述](#概述)
- [系统要求](#系统要求)
- [环境准备](#环境准备)
- [下载源码](#下载源码)
- [依赖管理](#依赖管理)
- [编译安装](#编译安装)
- [配置环境变量](#配置环境变量)
- [验证安装](#验证安装)
- [项目配置](#项目配置)
- [常见问题](#常见问题)
- [最佳实践](#最佳实践)

## 概述

Drogon 是一个基于 C++17/20 的高性能 HTTP 应用框架，类似于 Python 的 Django 和 Flask。本指南详细介绍如何在 Windows 系统下从源码编译安装 Drogon 框架。

### 框架特性
- **高性能**: 基于 non-blocking I/O 和事件驱动
- **异步支持**: 完整的异步编程模型
- **ORM支持**: 内置对象关系映射
- **插件系统**: 灵活的插件扩展机制
- **RESTful API**: 天然支持 RESTful 风格
- **WebSocket**: 内置 WebSocket 支持
- **跨平台**: 支持 Windows、Linux、macOS

### 编译方式
- **源码编译**: 完全控制编译选项和依赖
- **包管理器**: 使用 vcpkg 或 Conan 管理依赖
- **预编译包**: 使用官方预编译的二进制包

## 系统要求

### 1. 硬件要求
- **CPU**: x64 架构，推荐 4 核心以上
- **内存**: 最少 8GB，推荐 16GB+
- **磁盘空间**: 最少 10GB，推荐 20GB+

### 2. 软件要求
- **操作系统**: Windows 10/11 (64位)
- **Visual Studio**: 2019 或 2022
- **CMake**: 3.15+
- **Python**: 3.7+ (用于 Conan 包管理器)
- **Git**: 最新版本

### 3. 开发工具
- **Visual Studio**: 完整的 C++ 开发环境
- **CMake**: 跨平台构建工具
- **Conan**: C++ 包管理器
- **Git**: 版本控制工具

## 环境准备

### 1. 安装 Visual Studio

#### 1.1 下载安装
访问 https://visualstudio.microsoft.com/downloads/ 下载 Visual Studio 2022

#### 1.2 工作负载选择
安装时选择以下工作负载：
- **使用 C++ 的桌面开发**
  - MSVC v143 编译器工具集
  - Windows 10/11 SDK
  - C++ CMake 工具

#### 1.3 验证安装
```cmd
# Drogon 编译指南
# Drogon 编译指南
cl
# Drogon 编译指南
# Drogon 编译指南
link
# Drogon 编译指南
```

### 2. 安装 CMake

#### 2.1 下载安装
访问 https://cmake.org/download/ 下载 CMake

#### 2.2 安装配置
- 选择 "Add CMake to the system PATH"
- 完成安装

#### 2.3 验证安装
```cmd
cmake --version
# Drogon 编译指南
```

### 3. 安装 Python 和 pip

#### 3.1 下载安装 Python
访问 https://python.org/downloads/ 下载 Python 3.9+

#### 3.2 配置 pip 源（国内加速）
```cmd
# Drogon 编译指南
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Drogon 编译指南
pip config list
```

### 4. 安装 Conan

#### 4.1 安装 Conan
```cmd
# Drogon 编译指南
pip install conan

# Drogon 编译指南
conan --version
# Drogon 编译指南
```

#### 4.2 配置 Conan
```cmd
# Drogon 编译指南
conan profile detect --force

# Drogon 编译指南
conan profile show default
```

### 5. 安装 Git

#### 5.1 下载安装
访问 https://git-scm.com/download/win 下载 Git

#### 5.2 验证安装
```cmd
git --version
# Drogon 编译指南
```

## 下载源码

### 1. 设置工作目录

#### 1.1 创建工作目录
```cmd
# Drogon 编译指南
mkdir D:\drogon
cd D:\drogon

# Drogon 编译指南
set WORK_PATH=D:\drogon
cd %WORK_PATH%
```

#### 1.2 克隆 Drogon 源码
```cmd
# Drogon 编译指南
git clone https://github.com/drogonframework/drogon
cd drogon

# Drogon 编译指南
git branch -a
git tag -l

# Drogon 编译指南
git checkout v1.8.4
```

### 2. 更新子模块

#### 2.1 初始化子模块
```cmd
# Drogon 编译指南
git submodule update --init --recursive

# Drogon 编译指南
git clone --recursive https://github.com/drogonframework/drogon
```

#### 2.2 验证子模块
```cmd
# Drogon 编译指南
git submodule status

# Drogon 编译指南
```

## 依赖管理

### 1. Conan 依赖管理

#### 1.1 创建构建目录
```cmd
# Drogon 编译指南
mkdir build
cd build
```

#### 1.2 安装依赖库
```cmd
# Drogon 编译指南
conan profile detect --force

# Drogon 编译指南
conan install .. ^
  -s compiler="msvc" ^
  -s compiler.version=193 ^
  -s compiler.cppstd=17 ^
  -s build_type=Debug ^
  --output-folder=. ^
  --build=missing

# Drogon 编译指南
conan install .. ^
  -s compiler="msvc" ^
  -s compiler.version=193 ^
  -s compiler.cppstd=17 ^
  -s build_type=Release ^
  --output-folder=. ^
  --build=missing
```

#### 1.3 Conan 配置说明
- **compiler="msvc"**: 使用 Microsoft Visual C++ 编译器
- **compiler.version=193**: VS2022 编译器版本（193对应VS2022）
- **compiler.cppstd=17**: C++17 标准
- **build_type=Debug/Release**: 构建类型
- **--build=missing**: 自动构建缺失的依赖
- **--output-folder=.**: 输出到当前目录

#### 1.4 编辑 conanfile.txt
```txt
# Drogon 编译指南
[requires]
# Drogon 编译指南
# Drogon 编译指南
# Drogon 编译指南
[generators]
cmake
cmake_find_package

[options]
# Drogon 编译指南
# Drogon 编译指南
```

### 2. vcpkg 依赖管理（可选）

#### 2.1 安装 vcpkg
```cmd
# Drogon 编译指南
git clone https://github.com/microsoft/vcpkg.git
cd vcpkg
.\bootstrap-vcpkg.bat

# Drogon 编译指南
.\vcpkg install drogon:x64-windows
```

#### 2.2 配置 CMake 使用 vcpkg
```cmd
cmake .. -DCMAKE_TOOLCHAIN_FILE=D:/vcpkg/scripts/buildsystems/vcpkg.cmake
```

## 编译安装

### 1. 基础编译

#### 1.1 仅编译（不安装）
```cmd
# Drogon 编译指南
cmake .. ^
  -DCMAKE_BUILD_TYPE=Debug ^
  -DCMAKE_TOOLCHAIN_FILE="conan_toolchain.cmake" ^
  -DCMAKE_POLICY_DEFAULT_CMP0091=NEW

# Drogon 编译指南
cmake --build . --parallel
```

#### 1.2 编译参数说明
- **CMAKE_BUILD_TYPE**: Debug/Release/RelWithDebInfo/MinSizeRel
- **CMAKE_TOOLCHAIN_FILE**: Conan 生成的工具链文件
- **CMAKE_POLICY_DEFAULT_CMP0091=NEW**: 处理 MSVC 运行时库策略

### 2. 完整编译并安装

#### 2.1 设置安装路径
```cmd
# Drogon 编译指南
set INSTALL_PREFIX=D:\Development\drogon

# Drogon 编译指南
cmake .. ^
  -DCMAKE_BUILD_TYPE=Debug ^
  -DCMAKE_TOOLCHAIN_FILE="conan_toolchain.cmake" ^
  -DCMAKE_POLICY_DEFAULT_CMP0091=NEW ^
  -DCMAKE_INSTALL_PREFIX="%INSTALL_PREFIX%"
```

#### 2.2 编译并安装
```cmd
# Drogon 编译指南
cmake --build . --parallel --target install

# Drogon 编译指南
cmake --build . --config Debug --target install
```

### 3. 多版本编译

#### 3.1 Debug 和 Release 版本
```cmd
# Drogon 编译指南
mkdir build-debug build-release

# Drogon 编译指南
cd build-debug
conan install .. -s build_type=Debug --output-folder=. --build=missing
cmake .. -DCMAKE_BUILD_TYPE=Debug -DCMAKE_TOOLCHAIN_FILE="conan_toolchain.cmake" -DCMAKE_INSTALL_PREFIX="D:/Development/drogon/debug"
cmake --build . --parallel --target install

# Drogon 编译指南
cd ../build-release
conan install .. -s build_type=Release --output-folder=. --build=missing
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE="conan_toolchain.cmake" -DCMAKE_INSTALL_PREFIX="D:/Development/drogon/release"
cmake --build . --parallel --target install
```

#### 3.2 静态库和动态库
```cmd
# Drogon 编译指南
cmake .. -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX="D:/Development/drogon/static"

# Drogon 编译指南
cmake .. -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX="D:/Development/drogon/shared"
```

## 安装结果

### 1. 安装的文件结构

#### 1.1 默认安装结构
```
D:\Development\drogon\
├── include\                 # 头文件
│   ├── drogon\              # Drogon 主框架头文件
│   └── trantor\             # Trantor 网络库头文件
├── bin\                     # 可执行文件和动态库
│   ├── drogon.dll           # Drogon 主库
│   ├── trantor.dll          # Trantor 网络库
│   └── drogon_ctl.exe       # 命令行工具
├── lib\                     # 静态库
│   ├── drogon.lib           # Drogon 静态库
│   └── trantor.lib          # Trantor 静态库
└── lib\cmake\               # CMake 配置文件
    ├── Drogon\              # Drogon CMake 配置
    └── Trantor\             # Trantor CMake 配置
```

#### 1.2 关键文件说明
- **drogon.dll**: Drogon 主库动态链接库
- **trantor.dll**: Trantor 网络库动态链接库
- **drogon_ctl.exe**: Drogon 命令行工具
- **drogon.lib**: Drogon 静态链接库
- **trantor.lib**: Trantor 静态链接库

### 2. 环境变量配置

#### 2.1 添加到 PATH
```cmd
# Drogon 编译指南
set PATH=%PATH%;D:\Development\drogon\bin

# Drogon 编译指南
setx PATH "%PATH%;D:\Development\drogon\bin"
setx DROGON_ROOT "D:\Development\drogon"
```

#### 2.2 添加 CMake 路径
```cmd
# Drogon 编译指南
setx CMAKE_PREFIX_PATH "%CMAKE_PREFIX_PATH%;D:\Development\drogon\lib\cmake"
```

#### 2.3 系统环境变量设置
1. 按 `Win + R`，输入 `sysdm.cpl`
2. 选择"高级"选项卡
3. 点击"环境变量"
4. 在"系统变量"中添加：
   - **DROGON_ROOT**: `D:\Development\drogon`
   - **PATH**: 添加 `%DROGON_ROOT%\bin`

## 验证安装

### 1. 基本验证

#### 1.1 检查安装文件
```cmd
# Drogon 编译指南
dir D:\Development\drogon\include\drogon

# Drogon 编译指南
dir D:\Development\drogon\bin\*.dll
dir D:\Development\drogon\lib\*.lib

# Drogon 编译指南
dir D:\Development\drogon\bin\drogon_ctl.exe
```

#### 1.2 测试命令行工具
```cmd
# Drogon 编译指南
drogon_ctl --version
drogon_ctl --help

# Drogon 编译指南
drogon_ctl create project test_project
cd test_project
```

### 2. 编译测试项目

#### 2.1 创建测试项目
```cmd
# Drogon 编译指南
drogon_ctl create project hello_drogon
cd hello_drogon

# Drogon 编译指南
mkdir build
cd build
cmake .. -DCMAKE_PREFIX_PATH=D:\Development\drogon
cmake --build . --config Debug
```

#### 2.2 运行测试项目
```cmd
# Drogon 编译指南
Debug\hello_drogon.exe

# Drogon 编译指南
# Drogon 编译指南
# Drogon 编译指南
```

#### 2.3 测试 HTTP 请求
```cmd
# Drogon 编译指南
curl http://localhost:8080

# Drogon 编译指南
# Drogon 编译指南
```

## 项目配置

### 1. CMake 项目配置

#### 1.1 基本项目配置
```cmake
cmake_minimum_required(VERSION 3.15)
project(MyDrogonApp)

# Drogon 编译指南
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Drogon 编译指南
find_package(Drogon REQUIRED)

# Drogon 编译指南
add_executable(my_app main.cc)

# Drogon 编译指南
target_link_libraries(my_app Drogon::Drogon)
```

#### 1.2 完整项目配置
```cmake
cmake_minimum_required(VERSION 3.15)
project(MyDrogonApp)

# Drogon 编译指南
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Drogon 编译指南
set(DROGON_ROOT "D:/Development/drogon")
set(CMAKE_PREFIX_PATH ${CMAKE_PREFIX_PATH} ${DROGON_ROOT})

# Drogon 编译指南
find_package(Drogon REQUIRED)

# Drogon 编译指南
add_executable(my_app
    src/main.cc
    src/controllers/HomeController.cc
    src/models/User.cc
)

# Drogon 编译指南
target_include_directories(my_app PRIVATE
    ${DROGON_ROOT}/include
)

# Drogon 编译指南
target_link_libraries(my_app Drogon::Drogon)

# Drogon 编译指南
if(WIN32)
    add_custom_command(TARGET my_app POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
        ${DROGON_ROOT}/bin/drogon.dll
        ${DROGON_ROOT}/bin/trantor.dll
        $<TARGET_FILE_DIR:my_app>
    )
endif()
```

### 2. Visual Studio 项目配置

#### 2.1 项目属性设置
1. 右键项目 → 属性
2. 配置属性 → C/C++ → 常规
   - **附加包含目录**: `D:\Development\drogon\include`
3. 配置属性 → 链接器 → 常规
   - **附加库目录**: `D:\Development\drogon\lib`
4. 配置属性 → 链接器 → 输入
   - **附加依赖项**: `drogon.lib;trantor.lib;`

#### 2.2 环境变量设置
```cmd
# Drogon 编译指南
set DROGON_ROOT=D:\Development\drogon
set PATH=%PATH%;%DROGON_ROOT%\bin
```

### 3. 代码示例

#### 3.1 简单的 HTTP 服务器
```cpp
// main.cc
#include <drogon/drogon.h>

using namespace drogon;

int main() {
    app().setLogPath("./")
        .setLogLevel(trantor::Logger::kWarn)
        .addListener("0.0.0.0", 8080)
        .setThreadNum(16);

    // 添加路由
    app().registerHandler(
        "/",
        [](const HttpRequestPtr &req,
           std::function<void(const HttpResponsePtr &)> &&callback) {
            auto resp = HttpResponse::newHttpResponse();
            resp->setBody("Hello, Drogon!");
            resp->setContentTypeCode(CT_TEXT_HTML);
            callback(resp);
        },
        {Get}
    );

    LOG_INFO << "Server running on port 8080";
    app().run();
    return 0;
}
```

#### 3.2 控制器示例
```cpp
// controllers/HomeController.h
#pragma once
#include <drogon/HttpController.h>

using namespace drogon;

namespace api {
class HomeController : public HttpController<HomeController> {
public:
    METHOD_LIST_BEGIN
    METHOD_ADD(HomeController::index, "/", Get);
    METHOD_ADD(HomeController::hello, "/hello", Get);
    METHOD_LIST_END

    void index(const HttpRequestPtr &req,
               std::function<void(const HttpResponsePtr &)> &&callback);

    void hello(const HttpRequestPtr &req,
               std::function<void(const HttpResponsePtr &)> &&callback,
               const std::string &name);
};
}
```

```cpp
// controllers/HomeController.cc
#include "HomeController.h"
#include <drogon/HttpResponse.h>

using namespace drogon;
using namespace api;

void HomeController::index(const HttpRequestPtr &req,
                          std::function<void(const HttpResponsePtr &)> &&callback) {
    auto resp = HttpResponse::newHttpResponse();
    resp->setBody("<h1>Welcome to Drogon!</h1>");
    resp->setContentTypeCode(CT_TEXT_HTML);
    callback(resp);
}

void HomeController::hello(const HttpRequestPtr &req,
                           std::function<void(const HttpResponsePtr &)> &&callback,
                           const std::string &name) {
    Json::Value ret;
    ret["message"] = "Hello, " + name + "!";
    auto resp = HttpResponse::newHttpJsonResponse(ret);
    callback(resp);
}
```

## 常见问题

### Q1: 编译器版本不匹配
**问题**: 提示 "MSVC version not supported" 或编译器版本错误

**解决方案**:
```cmd
# Drogon 编译指南
cl
# Drogon 编译指南
# Drogon 编译指南
conan profile update settings.compiler.version=192 default  # VS2019
conan profile update settings.compiler.version=193 default  # VS2022
```

### Q2: CMake 配置错误
**问题**: CMake 找不到 Conan 生成的工具链文件

**解决方案**:
```cmd
# Drogon 编译指南
dir conan_toolchain.cmake

# Drogon 编译指南
conan install .. --output-folder=. --build=missing

# Drogon 编译指南
cmake .. -DCMAKE_TOOLCHAIN_FILE="%CD%\conan_toolchain.cmake"
```

### Q3: 依赖库缺失
**问题**: 编译时提示找不到某些库文件

**解决方案**:
```cmd
# Drogon 编译指南
conan install .. --build=missing

# Drogon 编译指南
# Drogon 编译指南
[requires]
openssl/1.1.1q
zlib/1.2.11
```

### Q4: 链接错误
**问题**: 链接时提示 "unresolved external symbol"

**解决方案**:
```cmd
# Drogon 编译指南
cmake .. -DCMAKE_BUILD_TYPE=Debug -DCMAKE_TOOLCHAIN_FILE="conan_toolchain.cmake"

# Drogon 编译指南
rm -rf *
conan install .. --output-folder=. --build=missing
cmake .. -DCMAKE_BUILD_TYPE=Debug -DCMAKE_TOOLCHAIN_FILE="conan_toolchain.cmake"
cmake --build . --config Debug --target install
```

### Q5: 运行时错误
**问题**: 程序运行时提示 "找不到 drogon.dll"

**解决方案**:
```cmd
# Drogon 编译指南
echo %PATH%

# Drogon 编译指南
copy D:\Development\drogon\bin\*.dll .\

# Drogon 编译指南
set PATH=%PATH%;D:\Development\drogon\bin
```

### Q6: Python 和 pip 问题
**问题**: pip 安装 Conan 失败或速度慢

**解决方案**:
```cmd
# Drogon 编译指南
python -m pip install --upgrade pip

# Drogon 编译指南
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Drogon 编译指南
pip config list
```

## 最佳实践

### 1. 开发环境配置

#### 1.1 自动化脚本
```cmd
@echo off
REM install_drogon.bat

setlocal

set WORK_DIR=D:\Development\drogon
set BUILD_TYPE=Debug

echo Installing Drogon...

echo 1. Creating directories...
mkdir "%WORK_DIR%" 2>nul
cd "%WORK_DIR%"

echo 2. Cloning source code...
if not exist "drogon" (
    git clone https://github.com/drogonframework/drogon
    cd drogon
    git submodule update --init --recursive
) else (
    cd drogon
)

echo 3. Installing dependencies...
mkdir build 2>nul
cd build
conan profile detect --force
conan install .. -s build_type=%BUILD_TYPE% --output-folder=. --build=missing

echo 4. Building and installing...
cmake .. -DCMAKE_BUILD_TYPE=%BUILD_TYPE% -DCMAKE_TOOLCHAIN_FILE="conan_toolchain.cmake" -DCMAKE_INSTALL_PREFIX="%WORK_DIR%"
cmake --build . --parallel --target install

echo 5. Setting environment variables...
setx DROGON_ROOT "%WORK_DIR%"
setx PATH "%PATH%;%WORK_DIR%\bin"

echo Installation completed successfully!

endlocal
```

#### 1.2 开发环境检查
```cmd
@echo off
REM check_env.bat

echo Checking Drogon development environment...

echo 1. Checking Visual Studio...
cl >nul 2>&1
if %errorlevel% equ 0 (
    echo Visual Studio: OK
) else (
    echo Visual Studio: NOT FOUND
    echo Please run this script from Visual Studio Developer Command Prompt
    exit /b 1
)

echo 2. Checking CMake...
cmake --version >nul 2>&1
if %errorlevel% equ 0 (
    echo CMake: OK
) else (
    echo CMake: NOT FOUND
    exit /b 1
)

echo 3. Checking Conan...
conan --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Conan: OK
) else (
    echo Conan: NOT FOUND
    echo Run: pip install conan
    exit /b 1
)

echo 4. Checking Drogon installation...
if exist "%DROGON_ROOT%\bin\drogon_ctl.exe" (
    echo Drogon: OK
    drogon_ctl --version
) else (
    echo Drogon: NOT FOUND
    echo Please run install_drogon.bat first
    exit /b 1
)

echo All checks passed!
```

### 2. 项目管理

#### 2.1 版本管理
```cmd
# Drogon 编译指南
git clone https://github.com/drogonframework/drogon
cd drogon
git checkout v1.8.4  # 切换到稳定版本
git submodule update --init --recursive
```

#### 2.2 多项目配置
```cmake
# Drogon 编译指南
set(DROGON_ROOT "D:/Work/Development/Projects/ThirdParty/drogon")
set(CMAKE_PREFIX_PATH ${CMAKE_PREFIX_PATH} ${DROGON_ROOT})

find_package(Drogon REQUIRED)
message(STATUS "Found Drogon: ${Drogon_VERSION}")
```

### 3. 性能优化

#### 3.1 编译优化
```cmd
# Drogon 编译指南
conan install .. -s build_type=Release --output-folder=. --build=missing
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE="conan_toolchain.cmake"
cmake --build . --config Release --target install

# Drogon 编译指南
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE="conan_toolchain.cmake" -DCMAKE_INTERPROCEDURAL_OPTIMIZATION=ON
```

#### 3.2 运行时优化
```cpp
// 在应用启动时配置
app().setThreadNum(std::thread::hardware_concurrency())  // 使用所有CPU核心
     .setIoLoopNum(4)                                   // 设置I/O循环数量
     .setUseGzip(true)                                 // 启用Gzip压缩
     .setMaxConnectionNum(10000)                      // 最大连接数
     .setIdleConnectionTimeout(60);                   // 空闲连接超时
```

记住：Drogon 是一个功能强大的 C++ Web 框架，正确的编译安装是开始开发的基础。建议在开发环境中充分测试后再部署到生产环境！