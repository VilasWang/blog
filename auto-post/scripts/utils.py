"""工具函数模块"""
import os
import re
import json
import logging
from datetime import datetime
from pathlib import Path

def setup_logger(name, log_file, level=logging.INFO):
    """设置日志记录器"""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler(log_file, encoding='utf-8')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    # 同时输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

def load_config(config_file):
    """加载配置文件"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"加载配置文件失败: {e}")
        return {}

def save_config(config, config_file):
    """保存配置文件"""
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logging.error(f"保存配置文件失败: {e}")
        return False

def sanitize_filename(filename):
    """清理文件名，移除特殊字符"""
    # 移除或替换特殊字符
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = filename.replace(' ', '_')
    filename = re.sub(r'_+', '_', filename)  # 合并多个下划线
    filename = filename.strip('_')

    # 限制长度
    if len(filename) > 200:
        filename = filename[:200]

    return filename

def extract_title_from_content(content):
    """从内容中提取标题"""
    lines = content.split('\n')

    # 查找第一个一级标题
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()

    # 如果没有找到一级标题，尝试其他方式
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('```'):
            return line[:50] + '...' if len(line) > 50 else line

    return datetime.now().strftime("未命名文档_%Y%m%d_%H%M%S")

def generate_slug(title):
    """生成文章 slug"""
    # 转换为小写，替换空格和特殊字符
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    slug = slug.strip('-')

    # 限制长度
    if len(slug) > 50:
        words = slug.split('-')
        slug = '-'.join(words[:10])

    return slug

def create_backup(filepath):
    """创建文件备份"""
    try:
        backup_path = f"{filepath}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if os.path.exists(filepath):
            import shutil
            shutil.copy2(filepath, backup_path)
        return backup_path
    except Exception as e:
        logging.error(f"创建备份失败: {e}")
        return None

def count_words(content):
    """统计字数"""
    # 简单的中英文混合字数统计
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
    english_words = len(re.findall(r'[a-zA-Z]+', content))
    return chinese_chars + english_words