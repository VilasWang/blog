---
tags:
  - Linux
  - Bash
  - 命令行
  - Shell
  - 系统管理
  - Cheatsheet
title: Linux CLI 参考手册
categories:
  - 系统运维管理
  - Linux系统管理
description: 专业的技术文档，提供详细的操作指南、最佳实践和问题解决方案，助力开发者提升技术水平。
abbrlink: d7364a6b
date: 2025-12-04 22:48:22
---

# Linux CLI 参考手册
## 目录
- [文件和目录操作](#文件和目录操作)
- [文本处理](#文本处理)
- [系统管理](#系统管理)
- [网络操作](#网络操作)
- [用户与权限](#用户与权限)
- [进程管理](#进程管理)
- [包管理](#包管理)
- [文件压缩与归档](#文件压缩与归档)
- [系统监控与性能分析](#系统监控与性能分析)

## 文件和目录操作

### 导航与查看
- `pwd`: 显示当前工作目录。
- `ls -la`: 列出所有文件和目录（包括隐藏的），显示详细信息。
- `ls -lh`: 以人类可读的格式显示文件大小 (K, M, G)。
- `cd /path/to/dir`: 切换到指定目录。
- `cd ..`: 切换到上一级目录。
- `cd ~` 或 `cd`: 切换到当前用户的主目录。
- `cd -`: 切换到上一个工作目录。

### 创建与删除
- `touch file.txt`: 创建一个空文件或更新文件的时间戳。
- `mkdir new_dir`: 创建一个新目录。
- `mkdir -p path/to/new_dir`: 递归创建多级目录。
- `rm file.txt`: 删除一个文件（会提示）。
- `rm -f file.txt`: 强制删除一个文件。
- `rm -r my_dir`: 递归删除一个目录及其所有内容。
- `rm -rf my_dir`: 强制递归删除一个目录（**危险命令，请谨慎使用**）。

### 复制与移动
- `cp source.txt destination.txt`: 复制文件。
- `cp -r source_dir/ destination_dir/`: 递归复制目录。
- `mv old_name.txt new_name.txt`: 重命名文件或目录。
- `mv source.txt /path/to/destination/`: 移动文件或目录。

### 查找
- `find /path -name "*.log"`: 在指定路径下按名称查找文件。
- `find /path -type f -size +100M`: 查找大于 100MB 的文件。
- `find /path -name "*.log" -mtime +7`: 查找7天前修改的日志文件。
- `grep "pattern" file.txt`: 在文件中搜索包含特定模式的行。
- `grep -r "pattern" /path/to/dir`: 在目录中递归搜索。
- `grep -i "pattern" file.txt`: 忽略大小写搜索。
- `grep -n "pattern" file.txt`: 显示匹配行的行号。
- `grep -v "pattern" file.txt`: 显示不包含匹配模式的行。

## 文本处理

### 查看内容
- `cat file.txt`: 一次性显示整个文件的内容。
- `less file.txt`: 分页查看文件内容（功能比 `more` 更强大）。
- `head -n 20 file.txt`: 显示文件的前 20 行。
- `tail -n 20 file.txt`: 显示文件的后 20 行。
- `tail -f /var/log/syslog`: 实时跟踪文件的新增内容，常用于看日志。
- `tail -F /var/log/syslog`: 跟踪文件，如果文件被轮转会自动跟踪新文件。
- `less +F file.txt`: 在 less 中打开文件并进入跟踪模式（按 Ctrl+C 退出跟踪，按 F 重新进入）。

### 文本工具
- `wc -l file.txt`: 统计文件的行数。
- `wc -w file.txt`: 统计文件的单词数。
- `sort file.txt`: 对文件的行进行排序。
- `uniq file.txt`: 移除文件中的连续重复行（通常与 `sort` 配合使用：`sort file.txt | uniq`）。
- `cut -d',' -f1 data.csv`: 以逗号为分隔符，提取第一列。
- `tr 'a-z' 'A-Z' < file.txt`: 将文本转换为大写。
- `tr -d '\n' < file.txt`: 删除所有换行符。

### `sed` 与 `awk`
- `sed 's/old/new/g' file.txt`: 使用 `sed` 替换文件中的文本。
- `sed -i 's/old/new/g' file.txt`: 直接修改文件内容（注意备份）。
- `awk '{print $1}' file.txt`: 使用 `awk` 打印每一行的第一列（默认以空格分隔）。
- `awk -F',' '{print $2}' data.csv`: 以逗号为分隔符，打印第二列。
- `awk '{sum+=$1} END {print sum}' numbers.txt`: 计算第一列的总和。

## 系统管理

### 系统信息
- `uname -a`: 显示详细的内核和系统信息。
- `lsb_release -a` 或 `cat /etc/os-release`: 查看 Linux 发行版信息。
- `lscpu`: 显示 CPU 信息。
- `free -h`: 以人类可读格式显示内存使用情况。
- `df -h`: 以人类可读格式显示磁盘空间使用情况。
- `du -sh /path/to/dir`: 估算目录的总大小。
- `du -h --max-depth=1 /path/to/dir`: 显示目录下各子目录的大小。
- `df -i`: 显示磁盘 inode 使用情况。

### 时间与日期
- `date`: 显示当前日期和时间。
- `timedatectl`: 查看和设置系统时间与时区。
- `sudo timedatectl set-timezone Asia/Shanghai`: 设置时区为上海。
- `sudo timedatectl set-ntp true`: **(推荐)** 启用网络时间同步。

### 关机与重启
- `sudo shutdown -h now` 或 `sudo poweroff`: 立即关机。
- `sudo shutdown -r now` 或 `sudo reboot`: 立即重启。
- `sudo shutdown -c`: 取消一个已计划的关机或重启。
- `sudo shutdown -h +60 "System will shutdown in 60 minutes"`: 60分钟后关机并提示消息。
- `sudo init 0`: 关机（另一种方式）。
- `sudo init 6`: 重启（另一种方式）。

## 网络操作

- `ip addr show` 或 `ip a`: 显示所有网络接口的 IP 地址。
- `ping -c 4 google.com`: 发送4个ICMP包测试网络连通性。
- `netstat -tlnp`: 显示所有正在监听的 TCP 端口（注意：netstat 已被 ss 替代）。
- `ss -tuln`: 显示所有正在监听的 TCP 和 UDP 端口（netstat 的现代替代品）。
- `ss -tulpn`: 显示监听端口及对应的进程。
- `wget https://example.com/file.zip`: 下载文件。
- `wget -c https://example.com/largefile.zip`: 断点续传下载。
- `curl -I http://example.com`: 获取一个 URL 的 HTTP 头部信息。
- `curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' https://api.example.com`: 发送 POST 请求。
- `dig example.com`: DNS 查询工具，显示域名解析信息。
- `nslookup example.com`: 另一个 DNS 查询工具。

## 用户与权限

### 用户和组
- `whoami`: 显示当前登录的用户名。
- `sudo adduser newuser`: 创建一个新用户（交互式）。
- `sudo userdel -r olduser`: 删除一个用户及其主目录。
- `sudo usermod -aG sudo myuser`: 将用户 `myuser` 添加到 `sudo` 组。
- `sudo usermod -aG docker username`: 将用户添加到 docker 组。
- `groups username`: 查看用户所属的所有组。
- `passwd`: 修改当前用户的密码。
- `sudo passwd username`: 修改其他用户的密码（需要 root 权限）。

### 文件权限
- `chmod 755 script.sh`: 设置文件权限为 `rwxr-xr-x`。
- `chmod +x script.sh`: 为文件添加可执行权限。
- `chmod -R 755 /path/to/dir`: 递归设置目录权限。
- `chown user:group file.txt`: 更改文件的所有者和所属组。
- `chown -R user:group /path/to/dir`: 递归更改目录的所有权。
- `chmod u=rwx,g=rx,o=r file.txt`: 使用符号模式设置权限。
- `umask 022`: 设置新创建文件的默认权限掩码。

## 进程管理

- `ps aux`: 显示当前所有进程的快照。
- `ps -ef`: 显示所有进程的完整格式列表。
- `top` 或 `htop`: 实时、交互式地显示进程和系统资源。
- `kill <PID>`: 终止一个指定 PID 的进程。
- `kill -9 <PID>`: 强制终止一个进程（最后的手段）。
- `kill -15 <PID>`: 发送 SIGTERM 信号，优雅地终止进程。
- `pkill process_name`: 按名称终止进程。
- `pgrep process_name`: 查找进程的 PID。
- `command &`: 在后台运行一个命令。
- `nohup command &`: 后台运行命令，即使退出终端也继续运行。
- `jobs`: 显示在后台运行的作业。
- `bg %1`: 将作业1放到后台运行。
- `fg %1`: 将作业1调到前台运行。

## 包管理

### Debian/Ubuntu (`apt`)
- `sudo apt update`: 刷新可用的软件包列表。
- `sudo apt upgrade`: 升级所有已安装的软件包。
- `sudo apt full-upgrade`: 升级所有软件包（可能删除软件包）。
- `sudo apt install <package_name>`: 安装一个软件包。
- `sudo apt install --no-install-recommends <package_name>`: 只安装必要的依赖。
- `sudo apt remove <package_name>`: 卸载一个软件包（保留配置文件）。
- `sudo apt purge <package_name>`: 完全卸载软件包（包括配置文件）。
- `sudo apt autoremove`: 自动移除不需要的依赖包。
- `apt search <keyword>`: 搜索软件包。
- `apt show <package_name>`: 显示软件包的详细信息。

### Red Hat/CentOS/Fedora (`dnf`/`yum`)
- `sudo dnf update`: 升级所有已安装的软件包。
- `sudo dnf upgrade`: 升级软件包（不更新内核）。
- `sudo dnf install <package_name>`: 安装一个软件包。
- `sudo dnf remove <package_name>`: 卸载一个软件包。
- `sudo dnf autoremove`: 自动移除不需要的依赖包。
- `dnf search <keyword>`: 搜索软件包。
- `dnf info <package_name>`: 显示软件包信息。

### Arch Linux (`pacman`)
- `sudo pacman -Syu`: 同步仓库并升级系统。
- `sudo pacman -S <package_name>`: 安装软件包。
- `sudo pacman -R <package_name>`: 删除软件包。
- `sudo pacman -Rs <package_name>`: 删除软件包及其不需要的依赖。
- `pacman -Ss <keyword>`: 搜索软件包。
- `pacman -Qi <package_name>`: 查看软件包信息。

## 文件压缩与归档

### tar 归档
- `tar -czf archive.tar.gz files/`: 创建 gzip 压缩的 tar 归档。
- `tar -xzf archive.tar.gz`: 解压 gzip 压缩的 tar 归档。
- `tar -cjf archive.tar.bz2 files/`: 创建 bzip2 压缩的 tar 归档。
- `tar -xjf archive.tar.bz2`: 解压 bzip2 压缩的 tar 归档。
- `tar -czf archive.tar.gz --exclude='*.log' directory/`: 创建归档但排除日志文件。
- `tar -tzf archive.tar.gz`: 查看归档内容但不解压。

### zip 压缩
- `zip -r archive.zip files/`: 创建 zip 压缩包。
- `unzip archive.zip`: 解压 zip 文件。
- `unzip -l archive.zip`: 查看 zip 文件内容。
- `zip -r archive.zip files/ -x "*.log"`: 创建 zip 压缩包但排除日志文件。

### 其他压缩格式
- `gzip file.txt`: 压缩文件（原文件会被替换为 .gz）。
- `gzip -d file.txt.gz`: 解压 gzip 文件。
- `bzip2 file.txt`: 使用 bzip2 压缩（更高的压缩率）。
- `bzip2 -d file.txt.bz2`: 解压 bzip2 文件。
- `xz file.txt`: 使用 xz 压缩（现代高效率压缩）。
- `xz -d file.txt.xz`: 解压 xz 文件。

## 系统监控与性能分析

### 系统负载
- `uptime`: 显示系统运行时间、用户数和平均负载。
- `w`: 显示当前登录用户和系统负载。
- `load average`: 通过 `uptime` 或 `top` 查看 1、5、15分钟的平均负载。

### 内存使用分析
- `free -h`: 以人类可读格式显示内存使用情况。
- `free -m`: 以 MB 为单位显示内存使用。
- `vmstat 5`: 每5秒显示一次虚拟内存统计信息。

### CPU 使用分析
- `top`: 实时显示进程和 CPU 使用情况。
- `htop`: 更友好的交互式进程查看器（需要安装）。
- `mpstat 1`: 每秒显示一次 CPU 统计信息。

### 磁盘 I/O 监控
- `iostat`: 显示 CPU 和 I/O 统计信息。
- `iotop`: 显示进程的 I/O 使用情况（需要安装）。
- `df -h`: 查看磁盘空间使用情况。

### 网络监控
- `iftop`: 实时显示网络带宽使用（需要安装）。
- `nethogs`: 按进程显示网络使用（需要安装）。
- `tcpdump -i eth0`: 捕获网络包（需要 root 权限）。

### 日志查看
- `journalctl -xe`: 查看系统日志（systemd 系统）。
- `journalctl -u nginx`: 查看特定服务的日志。
- `tail -f /var/log/syslog`: 实时查看系统日志。
- `tail -100f /var/log/nginx/access.log`: 查看最后100行并实时跟踪。
