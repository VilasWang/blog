#!/usr/bin/env python3
"""简化的启动脚本"""
import os
import sys
from pathlib import Path

# 确保在 auto-post 目录中
script_dir = Path(__file__).parent
os.chdir(script_dir)

# 添加 scripts 目录到 Python 路径
sys.path.insert(0, os.path.join(script_dir, 'scripts'))

# 创建必要的目录
Path('logs').mkdir(exist_ok=True)
Path('config').mkdir(exist_ok=True)

# 导入并运行主程序
if __name__ == '__main__':
    from auto_post import main
    main()