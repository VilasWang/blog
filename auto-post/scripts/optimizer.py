"""标题和结构优化脚本"""
import re
import json
from pathlib import Path
import sys
from datetime import datetime
import os

# 添加 scripts 目录到 Python 路径
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(script_dir, 'scripts'))

from utils import setup_logger, load_config, save_config, sanitize_filename, extract_title_from_content, generate_slug

class DocumentOptimizer:
    """文档优化器"""

    def __init__(self, config_dir):
        self.logger = setup_logger('DocumentOptimizer', 'logs/optimizer.log')
        self.config_dir = Path(config_dir)

        # 加载关键词配置
        keywords_file = self.config_dir / 'keywords.json'
        self.keywords_config = load_config(keywords_file) if keywords_file.exists() else {}
        self.tech_keywords = set(self.keywords_config.get('tech_keywords', []))
        self.stop_words = set(self.keywords_config.get('stop_words', []))

        self.logger.info("文档优化器初始化完成")

    def optimize_title(self, title, content):
        """优化标题"""
        if not title:
            title = extract_title_from_content(content)

        # 移除特殊字符和多余空格
        title = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', title)
        title = re.sub(r'\s+', ' ', title).strip()

        # 提取技术关键词
        words = re.findall(r'[\w]+|[\u4e00-\u9fff]+', title)

        # 保留技术关键词
        optimized_words = []
        for word in words:
            if word in self.tech_keywords or word not in self.stop_words:
                optimized_words.append(word)

        # 如果没有有效的词，使用原始标题
        if not optimized_words:
            optimized_title = title
        else:
            optimized_title = ' '.join(optimized_words)

        # 限制标题长度
        if len(optimized_title) > 100:
            optimized_title = optimized_title[:97] + '...'

        return optimized_title

    def optimize_document_structure(self, content):
        """优化文档结构"""
        lines = content.split('\n')
        optimized_lines = []
        in_code_block = False
        code_block_lang = None

        # 处理每一行
        for line in lines:
            stripped = line.strip()

            # 处理代码块
            if stripped.startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_block_lang = stripped[3:].strip() or 'text'
                    optimized_lines.append(f"```{code_block_lang}")
                else:
                    in_code_block = False
                    optimized_lines.append('```')
                    code_block_lang = None
                continue

            if in_code_block:
                optimized_lines.append(line)
                continue

            # 处理标题
            if stripped.startswith('#'):
                level = len(stripped) - len(stripped.lstrip('#'))
                title_text = stripped.lstrip('#').strip()

                # 确保标题后有空格
                if level <= 6:
                    optimized_lines.append(f"{'#' * level} {title_text}")
                else:
                    optimized_lines.append(f"###### {title_text}")
                continue

            # 处理空行
            if not stripped:
                optimized_lines.append('')
                continue

            # 处理列表
            if re.match(r'^[\d]+\.', stripped):
                optimized_lines.append(stripped)
                continue

            if stripped.startswith(('- ', '* ', '+ ')):
                optimized_lines.append(stripped)
                continue

            # 处理引用
            if stripped.startswith('>'):
                optimized_lines.append(stripped)
                continue

            # 处理普通文本
            # 确保段落不会过长
            if len(stripped) > 200:
                # 尝试在句号或逗号处分割
                sentences = re.split(r'([。！？，,.!?])', stripped)
                current_line = ''

                for i in range(0, len(sentences), 2):
                    if i + 1 < len(sentences):
                        sentence = sentences[i] + sentences[i + 1]
                    else:
                        sentence = sentences[i]

                    if current_line and len(current_line + sentence) > 150:
                        optimized_lines.append(current_line)
                        current_line = sentence
                    else:
                        current_line += sentence

                if current_line:
                    optimized_lines.append(current_line)
            else:
                optimized_lines.append(line)

        # 移除连续的空行
        final_lines = []
        prev_empty = False
        for line in optimized_lines:
            if line.strip() == '':
                if not prev_empty:
                    final_lines.append('')
                    prev_empty = True
            else:
                final_lines.append(line)
                prev_empty = False

        return '\n'.join(final_lines)

    def extract_summary(self, content, max_length=200):
        """提取摘要"""
        # 移除代码块
        content_no_code = re.sub(r'```.*?```', '', content, flags=re.DOTALL)

        # 移除标题
        content_no_title = re.sub(r'^#+\s.*$', '', content_no_code, flags=re.MULTILINE)

        # 分割成段落
        paragraphs = [p.strip() for p in content_no_title.split('\n\n') if p.strip()]

        # 取前几个段落
        summary = ''
        for para in paragraphs:
            if len(summary + para) > max_length:
                break
            summary += para + '\n\n'

        summary = summary.strip()

        # 如果太长，截断
        if len(summary) > max_length:
            summary = summary[:max_length-3] + '...'

        return summary or "技术文档分享"

    def extract_tags(self, content, title, max_tags=10):
        """提取标签"""
        # 合并标题和内容进行关键词提取
        text = (title + ' ' + content).lower()

        # 提取技术关键词
        found_tags = []

        # 查找技术关键词
        for keyword in self.tech_keywords:
            if keyword.lower() in text and keyword not in found_tags:
                found_tags.append(keyword)
                if len(found_tags) >= max_tags:
                    break

        # 如果关键词不够，提取一些常见的技术词汇
        if len(found_tags) < max_tags:
            # 查找编程语言、框架等
            patterns = [
                r'\b(Python|JavaScript|TypeScript|Java|C\+\+|C#|Go|Rust|PHP|Ruby|Swift|Kotlin)\b',
                r'\b(React|Vue|Angular|Node\.js|Express|Django|Flask|Spring|Laravel)\b',
                r'\b(MySQL|MongoDB|PostgreSQL|Redis|Elasticsearch|SQLite)\b',
                r'\b(Docker|Kubernetes|Jenkins|Git|GitHub|GitLab|CI\/CD)\b',
                r'\b(AWS|Azure|GCP|阿里云|腾讯云|华为云)\b'
            ]

            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    match = match.capitalize()
                    if match not in found_tags:
                        found_tags.append(match)
                        if len(found_tags) >= max_tags:
                            break
                if len(found_tags) >= max_tags:
                    break

        return found_tags[:max_tags]

    def optimize_document(self, doc_info):
        """优化单个文档"""
        try:
            content = doc_info['content']

            # 优化标题
            original_title = extract_title_from_content(content)
            optimized_title = self.optimize_title(original_title, content)

            # 优化文档结构
            optimized_content = self.optimize_document_structure(content)

            # 提取摘要
            summary = self.extract_summary(content)

            # 提取标签
            tags = self.extract_tags(content, optimized_title)

            # 生成 slug
            slug = generate_slug(optimized_title)

            # 更新文档信息
            doc_info.update({
                'original_title': original_title,
                'optimized_title': optimized_title,
                'slug': slug,
                'summary': summary,
                'tags': tags,
                'optimized_content': optimized_content,
                'optimization_time': datetime.now().isoformat(),
                'status': 'optimized'
            })

            self.logger.info(f"文档优化完成: {doc_info['filename']} -> {optimized_title}")
            return doc_info

        except Exception as e:
            self.logger.error(f"优化文档失败 {doc_info.get('filename', 'unknown')}: {e}")
            doc_info['status'] = 'optimization_failed'
            doc_info['error'] = str(e)
            return doc_info

    def process_batch(self, batch_file):
        """处理一批文档"""
        self.logger.info(f"开始处理批次: {batch_file}")

        # 加载批次文件
        try:
            with open(batch_file, 'r', encoding='utf-8') as f:
                documents = json.load(f)
        except Exception as e:
            self.logger.error(f"加载批次文件失败: {e}")
            return None

        # 处理每个文档
        processed_docs = []
        for doc in documents:
            if doc.get('status') == 'read':
                processed_doc = self.optimize_document(doc)
                processed_docs.append(processed_doc)
            else:
                processed_docs.append(doc)

        # 保存优化后的批次
        optimized_batch_file = batch_file.replace('.json', '_optimized.json')
        try:
            with open(optimized_batch_file, 'w', encoding='utf-8') as f:
                json.dump(processed_docs, f, ensure_ascii=False, indent=2)

            self.logger.info(f"批次优化完成，已保存到: {optimized_batch_file}")
            return optimized_batch_file

        except Exception as e:
            self.logger.error(f"保存优化批次失败: {e}")
            return None

    def run(self, batch_files):
        """运行优化流程"""
        self.logger.info("开始文档优化流程")

        optimized_batches = []
        for batch_file in batch_files:
            optimized_batch = self.process_batch(batch_file)
            if optimized_batch:
                optimized_batches.append(optimized_batch)

        self.logger.info(f"文档优化完成，共处理 {len(optimized_batches)} 个批次")
        return optimized_batches

if __name__ == "__main__":
    import os
    optimizer = DocumentOptimizer('config')

    # 查找批次文件
    batch_files = list(Path('.').glob('batch_*.json'))
    if batch_files:
        optimized = optimizer.run([str(f) for f in batch_files])
        print(f"\n成功优化 {len(optimized)} 个批次")
    else:
        print("没有找到批次文件")