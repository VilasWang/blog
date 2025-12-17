"""文档格式检查和修正脚本"""
import re
import json
from pathlib import Path
import sys
import os
from datetime import datetime

# 添加 scripts 目录到 Python 路径
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(script_dir, 'scripts'))

from utils import setup_logger

class FormatChecker:
    """文档格式检查器"""

    def __init__(self, config_dir):
        self.logger = setup_logger('FormatChecker', 'logs/format-checker.log')
        self.config_dir = Path(config_dir)
        self.logger.info("文档格式检查器初始化完成")

    def fix_front_matter(self, content):
        """修正 Front Matter 格式"""
        # 分离 Front Matter 和正文
        parts = content.split('---', 2)
        if len(parts) < 3:
            # 没有 Front Matter，创建一个
            title = self._extract_title_from_content(content)
            return f"""---
title: {title}
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
categories: [技术分享]
tags: []
excerpt:
cover: /img/default-cover.jpg
toc: true
top: false
comments: true
description: 本文分享了技术实践和经验总结。
keywords:
reading_time: 1 分钟
---

{content}"""

        front_matter = parts[1]
        body = parts[2]

        # 解析 YAML
        lines = front_matter.split('\n')
        fixed_lines = []

        # 确保必要的字段存在
        has_title = False
        has_excerpt = False
        has_description = False
        has_keywords = False
        has_reading_time = False

        for line in lines:
            line = line.rstrip()
            if line.startswith('title:'):
                # 清理标题格式
                title = line[6:].strip()
                title = self._clean_title(title)
                fixed_lines.append(f"title: {title}")
                has_title = True
            elif line.startswith('excerpt:'):
                # 检查 excerpt 是否被截断
                excerpt = line[8:].strip()
                if excerpt and len(excerpt) > 200:
                    # 截断过长的 excerpt
                    excerpt = excerpt[:197] + '...'
                fixed_lines.append(f"excerpt: {excerpt}")
                has_excerpt = True
            elif line.startswith('description:'):
                fixed_lines.append(line)
                has_description = True
            elif line.startswith('keywords:'):
                fixed_lines.append(line)
                has_keywords = True
            elif line.startswith('reading_time:'):
                fixed_lines.append(line)
                has_reading_time = True
            else:
                fixed_lines.append(line)

        # 添加缺失的字段
        if not has_title:
            title = self._extract_title_from_content(body)
            fixed_lines.insert(0, f"title: {title}")

        if not has_excerpt:
            excerpt = self._generate_excerpt(body)
            fixed_lines.append(f"excerpt: {excerpt}")

        if not has_description:
            fixed_lines.append("description: 本文分享了技术实践和经验总结。")

        if not has_keywords:
            category = self._extract_category(body)
            fixed_lines.append(f"keywords: {category}")

        if not has_reading_time:
            reading_time = max(1, len(body) // 300)  # 假设每分钟阅读300字
            fixed_lines.append(f"reading_time: {reading_time} 分钟")

        # 重新组装
        fixed_front_matter = '\n'.join(fixed_lines)

        # 清理正文，移除可能重复的内容
        body = self._clean_body_content(body)

        return f"---\n{fixed_front_matter}\n---\n\n{body}"

    def _clean_title(self, title):
        """清理标题格式"""
        # 移除多余空格
        title = re.sub(r'\s+', ' ', title.strip())

        # 确保标题长度合理
        if len(title) > 100:
            title = title[:97] + '...'

        return title

    def _extract_title_from_content(self, content):
        """从内容中提取标题"""
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()
            # 如果第一行非空，作为标题
            if line and not line.startswith('#') and not line.startswith('```'):
                # 限制长度
                if len(line) > 50:
                    return line[:47] + '...'
                return line
        return "未命名文档"

    def _generate_excerpt(self, content, max_length=200):
        """生成摘要"""
        # 移除 Markdown 语法
        content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        content = re.sub(r'^#+\s.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
        content = re.sub(r'[*_`]', '', content)

        # 分割成段落
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

        # 选择合适的段落
        excerpt = ""
        for para in paragraphs:
            if len(excerpt + para) <= max_length:
                excerpt += para + " "
            else:
                if excerpt:
                    break
                else:
                    excerpt = para[:max_length-3] + "..."
                    break

        excerpt = excerpt.strip()

        if not excerpt:
            excerpt = "技术文档分享"

        return excerpt

    def _extract_category(self, content):
        """提取关键词作为 keywords"""
        # 简单的关键词提取
        keywords = []
        tech_terms = ['API', 'REST', 'HTTP', 'JSON', '后端', '前端', '数据库', 'Python', 'JavaScript',
                     'Java', 'C++', 'Spring', 'React', 'Vue', 'Docker', 'Kubernetes', 'DevOps', 'AI']

        content_lower = content.lower()
        for term in tech_terms:
            if term.lower() in content_lower and term not in keywords:
                keywords.append(term)
                if len(keywords) >= 5:
                    break

        return ', '.join(keywords[:3]) if keywords else "技术分享"

    def _clean_body_content(self, body):
        """清理正文内容"""
        # 移除开头的空行
        body = body.lstrip('\n')

        # 移除重复的标题（如果已在 Front Matter 中）
        lines = body.split('\n')
        cleaned_lines = []
        skip_first_title = False

        for i, line in enumerate(lines):
            stripped = line.strip()

            # 跳过第一个标题（因为已在 Front Matter 中）
            if i < 3 and stripped.startswith('# '):
                if skip_first_title:
                    continue
                skip_first_title = True

            # 确保列表项格式正确
            if stripped.startswith(('-', '*', '+')):
                if not stripped.startswith(('- ', '* ', '+ ')):
                    # 修正列表格式
                    line = stripped[0] + ' ' + stripped[1:].strip()

            # 确保代码块格式
            if stripped.startswith('```'):
                # 确保代码块前后有空行
                if cleaned_lines and cleaned_lines[-1].strip():
                    cleaned_lines.append('')
                cleaned_lines.append(line)
                cleaned_lines.append('')
                continue

            cleaned_lines.append(line)

        return '\n'.join(cleaned_lines)

    def fix_markdown_formatting(self, content):
        """修正 Markdown 格式"""
        # 1. 确保标题后有正确空格
        content = re.sub(r'^(#{1,6})([^\s#])', r'\1 \2', content, flags=re.MULTILINE)

        # 2. 修正列表格式
        # 有序列表
        content = re.sub(r'^(\s*)(\d+)([^\s.])', r'\1\2. \3', content, flags=re.MULTILINE)
        # 无序列表
        content = re.sub(r'^(\s*)([-*+])([^\s])', r'\1\2 \3', content, flags=re.MULTILINE)

        # 3. 确保表格格式正确
        lines = content.split('\n')
        fixed_lines = []
        in_table = False

        for line in lines:
            # 检测表格
            if '|' in line and not line.strip().startswith('```'):
                if not in_table:
                    # 表格开始
                    in_table = True
                    fixed_lines.append(line)
                else:
                    # 检查是否是分隔行
                    if re.match(r'^[\s\|\-\:]+$', line):
                        # 确保分隔行格式正确
                        fixed_lines.append(line)
                    else:
                        # 普通表格行
                        fixed_lines.append(line)
            else:
                if in_table:
                    # 表格结束，添加空行
                    fixed_lines.append('')
                    in_table = False
                fixed_lines.append(line)

        # 4. 确保代码块语言正确
        content = '\n'.join(fixed_lines)
        content = re.sub(r'```(\w*)', lambda m: f"```{self._normalize_code_lang(m.group(1))}", content)

        # 5. 修复链接格式
        content = re.sub(r'\[([^\]]+)\]\s*\(\s*([^)]+)\s*\)', r'[\1](\2)', content)

        # 6. 移除多余的空行
        content = re.sub(r'\n{3,}', '\n\n', content)

        return content

    def _normalize_code_lang(self, lang):
        """标准化代码语言标识"""
        lang_map = {
            'js': 'javascript',
            'py': 'python',
            'sh': 'bash',
            'html': 'html',
            'css': 'css',
            'json': 'json',
            'xml': 'xml',
            'sql': 'sql',
            'java': 'java',
            'cpp': 'cpp',
            'c': 'c'
        }
        return lang_map.get(lang.lower(), lang)

    def check_document_format(self, doc_info):
        """检查并修正文档格式"""
        try:
            content = doc_info.get('optimized_content', doc_info.get('content', ''))

            if not content:
                self.logger.warning(f"文档内容为空: {doc_info.get('filename', 'unknown')}")
                return doc_info

            # 记录原始内容
            original_content = content

            # 1. 修正 Front Matter
            content = self.fix_front_matter(content)

            # 2. 修正 Markdown 格式
            content = self.fix_markdown_formatting(content)

            # 检查是否有修改
            changes_made = content != original_content

            # 更新文档信息
            doc_info.update({
                'format_checked_content': content,
                'format_changes_made': changes_made,
                'format_check_time': datetime.now().isoformat(),
                'status': 'format_checked'
            })

            # 保存格式检查后的内容
            doc_info['optimized_content'] = content

            self.logger.info(f"格式检查完成: {doc_info.get('filename', 'unknown')} {'(已修正)' if changes_made else '(无需修正)'}")
            return doc_info

        except Exception as e:
            self.logger.error(f"格式检查失败 {doc_info.get('filename', 'unknown')}: {e}")
            doc_info['status'] = 'format_check_failed'
            doc_info['error'] = str(e)
            return doc_info

    def process_batch(self, batch_file):
        """处理一批文档"""
        self.logger.info(f"开始格式检查批次: {batch_file}")

        # 加载批次文件
        try:
            with open(batch_file, 'r', encoding='utf-8') as f:
                documents = json.load(f)
        except Exception as e:
            self.logger.error(f"加载批次文件失败: {e}")
            return None

        # 处理每个文档
        format_checked_docs = []
        for doc in documents:
            # 检查文档状态：enhanced, reviewed, 或 privacy_checked 都需要格式检查
            if doc.get('status') in ['enhanced', 'reviewed', 'privacy_checked']:
                checked_doc = self.check_document_format(doc)
                format_checked_docs.append(checked_doc)
            else:
                format_checked_docs.append(doc)

        # 保存格式检查后的批次
        format_checked_batch_file = batch_file.replace('_privacy_checked.json', '_format_checked.json').replace('_reviewed.json', '_format_checked.json')
        try:
            with open(format_checked_batch_file, 'w', encoding='utf-8') as f:
                json.dump(format_checked_docs, f, ensure_ascii=False, indent=2)

            self.logger.info(f"格式检查完成，已保存到: {format_checked_batch_file}")
            return format_checked_batch_file

        except Exception as e:
            self.logger.error(f"保存格式检查批次失败: {e}")
            return None

    def run(self, batch_files):
        """运行格式检查流程"""
        self.logger.info("开始文档格式检查流程")

        format_checked_batches = []
        for batch_file in batch_files:
            format_checked_batch = self.process_batch(batch_file)
            if format_checked_batch:
                format_checked_batches.append(format_checked_batch)

        self.logger.info(f"文档格式检查完成，共处理 {len(format_checked_batches)} 个批次")
        return format_checked_batches

if __name__ == "__main__":
    checker = FormatChecker('config')

    # 查找需要格式检查的批次文件
    import glob
    batch_files = glob.glob('batch_*_reviewed.json') + glob.glob('batch_*_privacy_checked.json')

    if batch_files:
        checked = checker.run(batch_files)
        print(f"\n成功格式检查 {len(checked)} 个批次")
    else:
        print("没有找到需要格式检查的批次文件")