---
tags:
  - Git
  - 版本控制
  - 开发工具
title: Git 常用命令大全：从入门到精通的版本控制实战指南
categories:
  - 开发工具与流程
  - 版本控制
description: 专业技术完全指南，涵盖理论基础、实践操作、问题排查、性能优化等全方位内容，助力技能快速提升。
abbrlink: bae20393
date: 2025-12-04 22:52:05
---

# Git 常用命令指南

## 目录
- [仓库管理](#仓库管理)
- [代码提交](#代码提交)
- [分支管理](#分支管理)
- [远程操作](#远程操作)
- [文件/目录操作](#文件目录操作)
- [历史查看](#历史查看)
- [撤销与修改](#撤销与修改)
- [标签管理](#标签管理)
- [储藏工作](#储藏工作)
- [子模块管理](#子模块管理)

### 仓库管理

#### 克隆仓库
```bash
# 克隆包含子模块的仓库
git clone --recurse-submodules [url] [directory]
```

#### 初始化本地仓库
```bash
# 在当前目录初始化一个新仓库
git init
```

### 代码提交

#### 查看更改状态
```bash
# 查看工作区和暂存区的更改状态
git status

# 查看简洁的状态信息
git status -s

# 查看文件的具体更改内容
git diff
```

#### 暂存更改
```bash
# 添加所有更改到暂存区
git add .

# 添加特定文件到暂存区
git add <file>

# 交互式暂存文件的部分更改
git add -p <file>
```

#### 提交更改
```bash
# 提交到本地仓库
git commit -m "Your commit message"

# 提交并暂存所有已跟踪文件的更改
git commit -am "Your commit message"

# 查看即将提交的更改（预览）
git commit --dry-run
```

### 分支管理

#### 查看分支
```bash
# 列出所有本地分支
git branch

# 列出所有远程分支
git branch -r

# 列出所有本地和远程分支
git branch -a
```

#### 创建与切换分支
```bash
# 创建新分支
git branch [branch-name]

# 切换到指定分支
git checkout [branch-name]
# 或者使用更现代的 switch 命令
git switch [branch-name]

# 创建并立即切换到新分支
git checkout -b [new-branch-name]
# 或者使用更现代的 switch 命令
git switch -c [new-branch-name]
```

#### 合并与删除分支
```bash
# 将指定分支合并到当前分支
git merge [branch-name]

# 删除本地分支（需先切换到其他分支）
git branch -d [branch-name]
```

### 远程操作

#### 关联远程仓库
```bash
# 添加远程仓库并命名为 origin
# 注意：新仓库的默认分支可能为 main 而不是 master
git remote add origin https://github.com/用户名/仓库名.git

# 推送本地提交到远程仓库，并建立上游跟踪关系
git push -u origin main
```

#### 拉取远程代码
```bash
# 从远程拉取最新代码并与本地分支合并
git pull [remote] [branch]

# 从远程拉取最新代码并尝试将本地修改变基到其之上
git pull --rebase [remote] [branch]
```

#### 推送到远程仓库
```bash
# 推送当前分支的提交
git push [remote] [branch]

# 推送所有本地标签
git push [remote] --tags

# 删除远程分支
git push [remote] --delete [branch]

# 强制推送（高风险操作）
# 警告：这会覆盖远程历史记录，可能导致团队成员丢失提交。请仅在确知后果时使用。
git push [remote] [branch] --force
```

### 文件/目录操作

#### 重命名或移动文件/目录
```bash
# git mv 命令会同时更新 Git 的跟踪记录
git mv <old-path> <new-path>
```

### 历史查看

#### 查看提交历史
```bash
# 查看详细历史记录
git log

# 以单行、图形化方式显示历史记录
git log --oneline --graph --decorate

# 查看特定文件的修改历史
git log --follow <file>
```

### 撤销与修改

#### 修改最后一次提交
```bash
# 如果还未推送到远程，可以使用此命令来修改最后一次的提交信息或内容
git commit --amend
```

#### 撤销本地更改
```bash
# 撤销工作区中对某个文件的更改（恢复到暂存区版本）
git restore <file>

# 将文件从暂存区移回工作区（不改变文件内容）
git restore --staged <file>

# 撤销工作区中所有文件的更改
git restore .

# 恢复文件到指定提交
git restore --source=<commit> <file>
```

#### 修改历史提交
```bash
# 交互式变基，可以修改、合并或删除最近的N次提交（高风险操作）
# 警告：不要在已经推送到公共仓库的分支上执行此操作。
git rebase -i HEAD~3
```

### 标签管理

#### 创建标签
```bash
# 创建轻量标签
git tag <tag-name>

# 创建带注释的标签
git tag -a <tag-name> -m "Tag message"

# 为特定提交创建标签
git tag <tag-name> <commit-hash>
```

#### 查看标签
```bash
# 列出所有标签
git tag

# 查看标签详细信息
git show <tag-name>

# 搜索特定模式的标签
git tag -l "v*"
```

#### 推送标签
```bash
# 推送单个标签到远程
git push origin <tag-name>

# 推送所有标签到远程
git push origin --tags

# 推送标签并设置跟踪
git push --follow-tags
```

#### 删除标签
```bash
# 删除本地标签
git tag -d <tag-name>

# 删除远程标签
git push origin --delete <tag-name>
```

### 储藏工作

#### 储藏当前工作
```bash
# 储藏当前工作区的更改
git stash

# 储藏并添加消息
git stash save "Your stash message"

# 储藏包括未跟踪的文件
git stash -u
```

#### 查看和应用储藏
```bash
# 查看储藏列表
git stash list

# 应用最新的储藏
git stash apply

# 应用并删除最新的储藏
git stash pop

# 应用特定储藏
git stash apply stash@{0}
```

### 子模块管理

#### 添加子模块
```bash
# 添加子模块到仓库
git submodule add <repository-url> [path]

# 克隆包含子模块的仓库
git clone --recurse-submodules <repository-url>
```

#### 更新子模块
```bash
# 初始化并更新所有子模块
git submodule update --init --recursive

# 拉取子模块的最新更改
git submodule update --remote

# 进入子模块目录并拉取最新更改
cd <submodule-path> && git pull origin main
```
