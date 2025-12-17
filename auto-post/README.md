# 自动文章发布系统

## 功能概述

本系统用于自动化处理 `unpost` 目录下的文档，并将其发布到 Hexo 博客。

## 目录结构

```
auto-post/
├── scripts/          # 脚本文件
│   ├── 01-reader.py          # 文档读取脚本
│   ├── 02-optimizer.py       # 标题和结构优化
│   ├── 03-blog-enhancer.py   # 博客优化（摘要等）
│   ├── 04-reviewer.py        # 内容审查和修正
│   ├── 05-privacy-checker.py # 隐私内容检测
│   ├── 06-publisher.py       # 自动发布脚本
│   └── utils.py              # 工具函数
├── templates/        # 文章模板
├── config/          # 配置文件
│   ├── keywords.json      # 关键词配置
│   ├── privacy.json       # 隐私检测规则
│   └── settings.json      # 系统设置
├── logs/            # 日志文件
└── auto-post.py     # 主控制脚本
```

## 使用方法

```bash
cd blog-source/auto-post
python auto-post.py
```

## 系统要求

- Python 3.8+
- hexo-cli
- 网络连接（用于内容审查）