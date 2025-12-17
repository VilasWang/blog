---
tags:
  - GDB
  - 调试
  - C++
  - 开发工具
title: GDB 调试工具完整使用指南
categories:
  - 开发工具与流程
  - 调试工具
description: 专业技术完全指南，涵盖理论基础、实践操作、问题排查、性能优化等全方位内容，助力技能快速提升。
abbrlink: b33ae3e9
date: 2025-12-04 22:52:02
---

# GDB (GNU Debugger) 调试指南

## 目录
- [编译调试版本](#编译调试版本)
- [启动 GDB](#启动-gdb)
- [断点](#断点)
- [执行控制](#执行控制)
- [查看数据](#查看数据)
- [高级技巧](#高级技巧)
- [常见问题](#常见问题)

## 编译调试版本
为了让 GDB 能够获取足够的信息，你必须在编译时加入 `-g` 参数。为了获得最佳调试体验，建议关闭优化 (`-O0`) 并开启所有警告。

```bash
# 使用 -g 参数生成调试信息
g++ -g -o my_app my_app.cpp

# 推荐的调试编译选项
g++ -g -O0 -Wall -Wextra -o my_app my_app.cpp

# CMake 构建系统的调试模式
cmake -DCMAKE_BUILD_TYPE=Debug .
make

# 禁用某些优化但保留调试信息
g++ -g -O1 -fno-omit-frame-pointer -o my_app my_app.cpp
```

## 启动 GDB

```bash
# 1. 调试可执行文件
gdb ./my_app

# 2. 附加到正在运行的进程 (需要进程ID)
gdb -p <pid>

# 3. 调试程序崩溃产生的核心转储文件 (core dump)
gdb ./my_app core.<pid>

# 4. 使用参数启动程序
gdb --args ./my_app arg1 arg2

# 5. 在 GDB 中设置程序的参数
(gdb) set args arg1 arg2
```

## 断点 (Breakpoints)

### 设置断点
```bash
# 在函数入口设置断点
break function_name
b main

# 在指定文件的指定行号设置断点
break file.cpp:42
b 42

# 设置条件断点 (当 a > 10 时触发)
break 42 if a > 10
b file.cpp:50 if count == 0

# 设置临时断点 (命中后自动删除)
tbreak function_name

# 在内存地址设置断点
break *0x400500
```

### 管理断点
```bash
# 查看所有断点
info breakpoints
info b

# 禁用断点 (num 为断点编号)
disable <num>

# 启用断点
enable <num>

# 删除断点
delete <num>
d <num>

# 清除所有断点
delete
clear

# 清除指定行的断点
clear 42
clear function_name
```

## 执行控制

```bash
# 运行程序 (可跟参数)
run [args]
r

# 继续执行直到下一个断点
continue
c

# 单步执行，会进入函数内部
step
s

# 单步执行，不会进入函数内部
next
n

# 执行到当前函数返回
finish

# 执行到当前循环结束
until

# 继续执行直到当前函数返回（与 finish 类似）
return [expression]

# 重新开始执行程序
restart

# 退出 GDB
quit
q
```

## 查看数据

### 查看代码与调用栈
```bash
# 显示当前位置附近的源代码
list
l

# 显示指定函数或行的源代码
list function_name
list file.cpp:42

# 查看当前函数的调用栈帧信息
info frame

# 查看完整的函数调用栈
backtrace
bt

# 限制显示的栈帧数量
backtrace 10
bt 10

# 查看 N 个栈帧的详细信息
backtrace full
bt full
```

### 查看变量与内存
```bash
# 打印变量/表达式的值
print variable
p i * 2

# 以特定格式打印 (x:十六进制, d:十进制, t:二进制, c:字符)
p/x variable

# 查看变量类型
ptype variable

# 查看当前栈帧的局部变量
info locals

# 查看当前函数的参数
info args

# 检查内存地址 (x: examine)
# 格式: x/[N][F][U] address
# N: 显示数量, F: 格式, U: 单位大小 (b:字节, h:半字, w:字, g:双字)
x/16xw 0x7fffffffe3c0  # 从地址开始，以16进制格式显示16个字(word)

# 更多 examine 格式示例
x/10xb 0x7fffffffe3c0      # 显示10个字节，16进制
x/20i 0x400500              # 显示20条指令，汇编格式
x/4xg &main                 # 以16进制显示4个8字节组(&main地址)

# 查看数组内容
p *array@len                 # 显示数组array的前len个元素
p *(int(*)[10])ptr           # 将ptr转换为int[10]指针并查看

# 查看寄存器值
info registers
info r

# 设置变量值
set variable = 100
set i = i + 1
```

## 高级技巧

### 文本用户界面 (TUI) 模式
TUI 模式可以在一个窗口内同时显示源代码、汇编和 GDB 命令，非常方便。

```bash
# 启动时进入 TUI 模式
gdb -tui ./my_app

# 在 GDB 内部切换 TUI 模式
# 按下 Ctrl + x, 然后再按 a
```
TUI 模式下常用快捷键：
- `Ctrl + x, 2`: 切换焦点到下一个窗口
- `上/下箭头`: 滚动当前窗口内容

### 观察点 (Watchpoints)
当一个变量被读取或写入时，程序会暂停。
```bash
# 变量被写入时暂停
watch my_var

# 变量被读取时暂停
rwatch my_var

# 变量被读取或写入时暂停
awatch my_var
```

### 多线程调试
```bash
# 查看所有线程
info threads

# 切换到指定线程 (num 为线程编号)
thread <num>

# 对所有线程执行同一个命令
thread apply all bt  # 查看所有线程的调用栈
thread apply all backtrace full  # 详细信息

# 应用命令到指定线程
thread apply 3-5 bt  # 对线程3到5执行bt

# 查看线程锁定信息
info lock
```

### 异常处理
```bash
# 捕获 C++ 异常
catch throw
catch catch

# 捕获信号
catch signal SIGSEGV
catch signal SIGINT

# 忽略信号
handle SIGUSR1 nostop noprint pass

# 查看信号处理设置
info signals
```

### 宏调试
```bash
# 展开宏
macro expand MACRO_NAME

# 显示宏定义
info macro MACRO_NAME

# 查看所有宏定义
info macros
```

### 其他高级功能
```bash
# 查看共享库信息
info sharedlibrary

# 加载符号
symbol-file /path/to/library.so

# 设置打印数组的最大元素数
set print elements 100

# 设置打印字符串的最大长度
set print null-stop
set print elements 0  # 无限制

# 自动显示表达式的值
display variable
display *ptr

# 查看所有显示的表达式
info display

# 取消显示
undisplay <num>
```

## 常见问题

**Q1: 如何调试段错误 (Segmentation Fault)?**
**A**: 首先，开启 core dump 生成。
```bash
# 允许生成无限大的 core dump 文件
ulimit -c unlimited
```
然后正常运行你的程序，当它崩溃时，会在当前目录生成一个 `core` 文件。最后使用 GDB 加载它进行分析。
```bash
# 进入 GDB 后，立即使用 backtrace 查看崩溃时的调用栈
(gdb) bt
```

**Q2: 如何使用 Valgrind 进行内存泄漏检测?**
**A**: `Valgrind` 是一个独立的工具，应在 Shell 中使用，而不是在 GDB 内部。它会运行你的程序并监控内存使用。
```bash
# --leak-check=full 提供最详细的泄漏报告
valgrind --leak-check=full ./my_app
```

**Q3: 如何调试多进程程序 (fork)?**
**A**: 默认情况下，GDB 会继续调试父进程，而子进程会正常运行。你可以修改这个行为。
```gdb
# 设置 GDB 在 fork 后调试子进程
set follow-fork-mode child

# (可选) 设置 GDB 同时调试父子进程，需要 GDB 7.0+
set detach-on-fork off
```

**Q4: 如何调试动态链接库中的问题?**
**A**: 使用以下方法：

```gdb
# 加载共享库的调试符号
(gdb) symbol-file /usr/lib/debug/libfoo.so

# 设置断点到共享库函数
(gdb) break shared_function

# 查看动态链接信息
(gdb) info sharedlibrary
```

**Q5: GDB 显示 "No symbol table is loaded" 怎么办?**
**A**: 这是因为编译时没有包含调试信息。

1. 确保使用 `-g` 参数编译：
```bash
g++ -g program.cpp -o program
```

2. 对于已编译的程序，检查是否有调试信息：

```bash
file program  # 查看是否包含调试信息
objdump -h program | grep .debug  # 查看调试段
```

3. 重新编译程序包含调试信息。

**Q6: 如何查看 STL 容器的内容?**
**A**: 使用 Pretty Printers（需要 GDB 7.0+ 和 Python 支持）：

```gdb
# 启用 pretty printing
(gdb) set print pretty on

# 查看 vector
(gdb) p my_vector

# 查看 map
(gdb) p my_map

# 查看 string
(gdb) p my_string
```

**Q7: 如何在 GDB 中执行 shell 命令?**
**A**: 使用 `shell` 命令：

```gdb
(gdb) shell ls -la
(gdb) shell ps aux | grep my_program
(gdb) shell cat /proc/$(pidof my_program)/status
```
```
