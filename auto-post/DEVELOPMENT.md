# Auto-Post 开发指南

## Git 提交说明

### ✅ 需要提交到 Git 仓库的文件：

#### 1. 核心程序文件
- `auto-post.py` - 主控制脚本
- `run.py` - 简化启动脚本

#### 2. 脚本目录 (`scripts/`)
- `utils.py` - 工具函数
- `reader.py` - 文档读取脚本
- `optimizer.py` - 标题和结构优化脚本
- `blog_enhancer.py` - 博客增强脚本
- `reviewer.py` - 内容审查脚本
- `privacy_checker.py` - 隐私检测脚本
- `publisher.py` - 发布脚本

#### 3. 配置目录 (`config/`)
- `keywords.json` - 关键词配置
- `privacy.json` - 隐私检测规则
- `settings.json` - 系统设置

#### 4. 文档文件
- `README.md` - 系统说明
- `DEVELOPMENT.md` - 开发指南（本文件）
- `.gitignore` - Git 忽略规则

#### 5. 可选目录
- `templates/` - 文章模板（如果有的话）

### ❌ 不需要提交的文件（已在 .gitignore 中排除）：

#### 1. 运行时生成的文件
- `batch_*.json` - 批处理文件
- `auto_post_report_*.json` - 处理报告
- `privacy_report_*.json` - 隐私检测报告

#### 2. 日志文件
- `logs/` - 所有日志文件
- `*.log` - 日志文件

#### 3. 处理记录
- `config/processed_docs.json` - 已处理文档记录

#### 4. Python 缓存
- `__pycache__/` - Python 字节码缓存
- `*.pyc` - 编译后的 Python 文件
- `*.pyo` - 优化的 Python 文件

#### 5. 环境相关
- `.env` - 环境变量
- `venv/` - Python 虚拟环境

## Git 提交命令

```bash
# 进入 auto-post 目录
cd blog-source/auto-post

# 添加所有需要的文件
git add .
git add config/.gitkeep  # 如果 config 目录为空，可能需要这个文件
git add logs/.gitkeep    # 如果 logs 目录为空，可能需要这个文件
git add templates/.gitkeep  # 如果 templates 目录为空，可能需要这个文件

# 检查状态
git status

# 提交
git commit -m "feat: 添加自动文章发布系统

- 实现文档自动读取和优化
- 支持自动分类和标签生成
- 包含隐私内容检测
- 支持自动发布到 Hexo 博客"
```

## 使用建议

1. **首次设置**：
   ```bash
   # 创建必要的 .keep 文件
   touch config/.gitkeep
   touch logs/.gitkeep
   touch templates/.gitkeep
   ```

2. **日常使用**：
   - 运行 `python auto-post.py` 发布文章
   - 所有临时文件会被自动忽略
   - 只提交代码更改，不提交运行时文件

3. **配置自定义**：
   - 修改 `config/` 目录下的配置文件
   - 记得提交配置文件的更改

## 目录结构说明

```
auto-post/
├── .gitignore              # Git 忽略规则（已配置）
├── auto-post.py            # 主控制脚本 ✓
├── run.py                  # 启动脚本 ✓
├── README.md               # 使用说明 ✓
├── DEVELOPMENT.md          # 开发指南 ✓
├── scripts/                # 功能脚本目录 ✓
│   ├── utils.py            # 工具函数
│   ├── reader.py           # 文档读取
│   ├── optimizer.py        # 优化处理
│   ├── blog_enhancer.py    # 博客增强
│   ├── reviewer.py         # 内容审查
│   ├── privacy_checker.py  # 隐私检测
│   └── publisher.py        # 文章发布
├── config/                 # 配置文件目录 ✓
│   ├── keywords.json       # 关键词配置
│   ├── privacy.json        # 隐私规则
│   └── settings.json       # 系统设置
├── logs/                   # 日志目录（忽略）
│   └── *.log              # 运行日志
└── templates/              # 模板目录（可为空）
```

**说明**：✓ = 需要提交到 Git，✗ = 已在 .gitignore 中排除