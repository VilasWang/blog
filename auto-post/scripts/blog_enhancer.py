"""博客优化脚本（添加摘要、分类等）"""
import json
import re
from pathlib import Path
import sys
from datetime import datetime
import os

# 添加 scripts 目录到 Python 路径
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(script_dir, 'scripts'))

from utils import setup_logger, count_words

class BlogEnhancer:
    """博客增强器"""

    def __init__(self, config_dir):
        self.logger = setup_logger('BlogEnhancer', 'logs/blog-enhancer.log')
        self.config_dir = Path(config_dir)

        # 加载分类配置
        self.categories = {
            "编程语言": ["Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust"],
            "前端开发": ["React", "Vue", "Angular", "HTML", "CSS", "Webpack", "前端"],
            "后端开发": ["Node.js", "Express", "Django", "Flask", "Spring", "后端", "API"],
            "数据库": ["MySQL", "MongoDB", "PostgreSQL", "Redis", "数据库", "SQL"],
            "DevOps": ["Docker", "Kubernetes", "CI/CD", "Jenkins", "Git", "DevOps"],
            "云计算": ["AWS", "Azure", "GCP", "阿里云", "腾讯云", "云计算"],
            "人工智能": ["AI", "机器学习", "深度学习", "TensorFlow", "PyTorch", "神经网络"],
            "移动开发": ["Android", "iOS", "React Native", "Flutter", "移动开发"],
            "软件架构": ["架构", "微服务", "分布式", "设计模式", "软件架构"],
            "测试": ["测试", "单元测试", "集成测试", "自动化测试", "测试框架"],
            "安全": ["安全", "加密", "认证", "授权", "网络安全"],
            "工具": ["Git", "VSCode", "IDE", "工具", "效率"]
        }

        self.logger.info("博客增强器初始化完成")

    def determine_category(self, title, tags, content):
        """确定文章分类"""
        # 分析标题、标签和内容，确定最适合的分类
        text = (title + ' ' + ' '.join(tags) + ' ' + content[:500]).lower()

        category_scores = {}
        for category, keywords in self.categories.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in text:
                    score += 1
            category_scores[category] = score

        # 找到得分最高的分类
        if category_scores:
            best_category = max(category_scores.items(), key=lambda x: x[1])
            if best_category[1] > 0:
                return best_category[0]

        return "技术分享"  # 默认分类

    def generate_excerpt(self, content, length=150):
        """生成文章摘要"""
        # 移除 Markdown 语法
        content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)  # 移除代码块
        content = re.sub(r'#+\s', '', content)  # 移除标题标记
        content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)  # 移除链接，保留文本
        content = re.sub(r'[*_`]', '', content)  # 移除其他 Markdown 标记

        # 分割成段落
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

        # 选择合适的段落
        excerpt = ""
        for para in paragraphs:
            if len(excerpt) + len(para) <= length:
                excerpt += para + " "
            else:
                if excerpt:  # 如果已经有内容，就停止
                    break
                else:  # 如果第一个段落就太长，截断它
                    excerpt = para[:length-3] + "..."
                    break

        excerpt = excerpt.strip()

        # 如果还是没有合适的摘要，使用默认
        if not excerpt:
            excerpt = "本文分享了技术实践和经验总结..."

        return excerpt

    def add_table_of_contents(self, content):
        """添加目录（如果文档结构复杂）"""
        # 提取所有标题
        headers = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)

        # 如果标题少于3个，不添加目录
        if len(headers) < 3:
            return content

        # 生成目录
        toc_lines = ["## 目录\n"]
        for level, title in headers:
            if level == '#':  # 跳过一级标题
                continue
            indent = '  ' * (len(level) - 2)
            # 生成锚点链接
            anchor = re.sub(r'[^\w\u4e00-\u9fff\s-]', '', title).strip()
            anchor = re.sub(r'[-\s]+', '-', anchor)
            toc_lines.append(f"{indent}- [{title}](#{anchor})")

        toc = '\n'.join(toc_lines) + '\n\n'

        # 在第一个二级标题前插入目录
        first_h2_pos = content.find('\n## ')
        if first_h2_pos > 0:
            return content[:first_h2_pos] + '\n' + toc + content[first_h2_pos:]
        else:
            return toc + content

    def add_reading_time(self, content):
        """估算阅读时间"""
        word_count = count_words(content)
        # 假设每分钟阅读200字（中英文混合）
        reading_time = max(1, round(word_count / 200))
        return reading_time

    def add_meta_data(self, doc_info):
        """添加博客元数据"""
        try:
            content = doc_info['optimized_content']
            title = doc_info['optimized_title']
            tags = doc_info['tags']

            # 确定分类
            category = self.determine_category(title, tags, content)

            # 生成摘要
            excerpt = self.generate_excerpt(content)

            # 估算阅读时间
            reading_time = self.add_reading_time(content)

            # 添加目录（如果需要）
            content_with_toc = self.add_table_of_contents(content)

            # 生成Hexo Front Matter
            front_matter = f"""---
title: {title}
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
categories: [{category}]
tags: {json.dumps(tags, ensure_ascii=False)}
excerpt: {excerpt}
cover: /img/default-cover.jpg
toc: true
top: false
comments: true
description: 本文分享了{category}相关的技术实践和经验总结。
keywords: {', '.join(tags[:5]) if tags else category}
reading_time: {reading_time} 分钟
---

<!-- more -->

{content_with_toc}"""

            # 更新文档信息
            doc_info.update({
                'category': category,
                'excerpt': excerpt,
                'reading_time': reading_time,
                'front_matter': front_matter,
                'blog_content': content_with_toc,
                'enhancement_time': datetime.now().isoformat(),
                'status': 'enhanced'
            })

            self.logger.info(f"博客增强完成: {title} (分类: {category}, 标签: {len(tags)}, 阅读时间: {reading_time}分钟)")
            return doc_info

        except Exception as e:
            self.logger.error(f"博客增强失败 {doc_info.get('filename', 'unknown')}: {e}")
            doc_info['status'] = 'enhancement_failed'
            doc_info['error'] = str(e)
            return doc_info

    def process_batch(self, batch_file):
        """处理一批文档"""
        self.logger.info(f"开始增强批次: {batch_file}")

        # 加载优化后的批次文件
        try:
            with open(batch_file, 'r', encoding='utf-8') as f:
                documents = json.load(f)
        except Exception as e:
            self.logger.error(f"加载批次文件失败: {e}")
            return None

        # 处理每个文档
        enhanced_docs = []
        for doc in documents:
            if doc.get('status') == 'optimized':
                enhanced_doc = self.add_meta_data(doc)
                enhanced_docs.append(enhanced_doc)
            else:
                enhanced_docs.append(doc)

        # 保存增强后的批次
        enhanced_batch_file = batch_file.replace('_optimized.json', '_enhanced.json')
        try:
            with open(enhanced_batch_file, 'w', encoding='utf-8') as f:
                json.dump(enhanced_docs, f, ensure_ascii=False, indent=2)

            self.logger.info(f"批次增强完成，已保存到: {enhanced_batch_file}")
            return enhanced_batch_file

        except Exception as e:
            self.logger.error(f"保存增强批次失败: {e}")
            return None

    def run(self, batch_files):
        """运行博客增强流程"""
        self.logger.info("开始博客增强流程")

        enhanced_batches = []
        for batch_file in batch_files:
            enhanced_batch = self.process_batch(batch_file)
            if enhanced_batch:
                enhanced_batches.append(enhanced_batch)

        self.logger.info(f"博客增强完成，共处理 {len(enhanced_batches)} 个批次")
        return enhanced_batches

if __name__ == "__main__":
    enhancer = BlogEnhancer('config')

    # 查找优化后的批次文件
    batch_files = list(Path('.').glob('batch_*_optimized.json'))
    if batch_files:
        enhanced = enhancer.run([str(f) for f in batch_files])
        print(f"\n成功增强 {len(enhanced)} 个批次")
    else:
        print("没有找到优化后的批次文件")