"""内容审查和修正脚本"""
import json
import re
from pathlib import Path
import sys
from datetime import datetime
import os

# 添加 scripts 目录到 Python 路径
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(script_dir, 'scripts'))

from utils import setup_logger

class ContentReviewer:
    """内容审查器"""

    def __init__(self, config_dir):
        self.logger = setup_logger('ContentReviewer', 'logs/reviewer.log')
        self.config_dir = Path(config_dir)

        # 常见的技术术语修正
        self.tech_corrections = {
            # 框架和库
            'react': 'React',
            'vue': 'Vue',
            'angular': 'Angular',
            'nodejs': 'Node.js',
            'node.js': 'Node.js',
            'express': 'Express',
            'django': 'Django',
            'flask': 'Flask',
            'spring boot': 'Spring Boot',
            'springboot': 'Spring Boot',

            # 编程语言
            'python': 'Python',
            'javascript': 'JavaScript',
            'typescript': 'TypeScript',
            'java': 'Java',
            'c++': 'C++',
            'c#': 'C#',
            'csharp': 'C#',
            'golang': 'Go',
            'go lang': 'Go',
            'php': 'PHP',

            # 数据库
            'mysql': 'MySQL',
            'postgresql': 'PostgreSQL',
            'postgres': 'PostgreSQL',
            'mongodb': 'MongoDB',
            'redis': 'Redis',

            # 云服务
            'aws': 'AWS',
            'azure': 'Azure',
            'gcp': 'GCP',
            'amazon web services': 'AWS',

            # 工具
            'git': 'Git',
            'github': 'GitHub',
            'gitlab': 'GitLab',
            'docker': 'Docker',
            'kubernetes': 'Kubernetes',
            'k8s': 'Kubernetes',
            'jenkins': 'Jenkins',
            'vscode': 'VS Code',
            'visual studio code': 'VS Code',

            # 其他
            'api': 'API',
            'rest': 'REST',
            'restful': 'RESTful',
            'json': 'JSON',
            'xml': 'XML',
            'html': 'HTML',
            'css': 'CSS',
            'sql': 'SQL',
            'nosql': 'NoSQL',
            'ci/cd': 'CI/CD',
            'cicd': 'CI/CD',
            'devops': 'DevOps',
            'ai': 'AI',
            'ml': 'Machine Learning',
            'deep learning': 'Deep Learning',
            'ui': 'UI',
            'ux': 'UX',
            'gui': 'GUI',
            'cli': 'CLI',
            'ide': 'IDE',
            'sdk': 'SDK',
            'api key': 'API key',
            'apikey': 'API key',
            'openai': 'OpenAI',
            'gpt': 'GPT',
            'chatgpt': 'ChatGPT',
            'copilot': 'Copilot'
        }

        # 常见的语法错误修正
        self.grammar_corrections = [
            (r'的得', '的'),
            (r'得地', '地'),
            (r'和以及', '和'),
            (r'并且并且', '并且'),
            (r'然后然后', '然后'),
            (r'了了', '了'),
            (r'，，', '，'),
            (r'。。', '。'),
            (r'！！', '！'),
            (r'？？', '？'),
            (r'\s+，', '，'),  # 逗号前的空格
            (r'，\s+', '，'),  # 逗号后的空格
            (r'\s+。', '。'),  # 句号前的空格
            (r'\s+$', ''),     # 行尾空格
        ]

        self.logger.info("内容审查器初始化完成")

    def check_technical_terms(self, content):
        """检查并修正技术术语"""
        corrections_made = []

        # 处理技术术语
        for incorrect, correct in self.tech_corrections.items():
            # 使用正则表达式进行匹配，确保是独立的单词
            pattern = r'\b' + re.escape(incorrect) + r'\b'
            matches = re.findall(pattern, content, flags=re.IGNORECASE)
            if matches:
                content = re.sub(pattern, correct, content, flags=re.IGNORECASE)
                corrections_made.append(f"'{incorrect}' -> '{correct}'")

        return content, corrections_made

    def check_grammar(self, content):
        """检查并修正语法错误"""
        corrections_made = []

        # 处理语法错误
        for pattern, replacement in self.grammar_corrections:
            old_content = content
            content = re.sub(pattern, replacement, content)
            if content != old_content:
                corrections_made.append(f"语法修正: {pattern} -> '{replacement}'")

        return content, corrections_made

    def check_code_blocks(self, content):
        """检查代码块语法"""
        corrections_made = []
        lines = content.split('\n')
        corrected_lines = []
        in_code_block = False
        code_block_lang = None

        for line in lines:
            stripped = line.strip()

            # 检查代码块标记
            if stripped.startswith('```'):
                if not in_code_block:
                    # 开始代码块
                    lang = stripped[3:].strip() or 'text'
                    # 修正常见的语言名称错误
                    if lang.lower() in ['js', 'javascript']:
                        lang = 'javascript'
                    elif lang.lower() in ['py', 'python']:
                        lang = 'python'
                    elif lang.lower() in ['sh', 'bash', 'shell']:
                        lang = 'bash'
                    elif lang.lower() in ['html', 'htm']:
                        lang = 'html'
                    elif lang.lower() in ['css', 'stylesheet']:
                        lang = 'css'
                    elif lang.lower() in ['json', 'JSON']:
                        lang = 'json'
                    elif lang.lower() in ['xml', 'XML']:
                        lang = 'xml'
                    elif lang.lower() in ['sql', 'SQL']:
                        lang = 'sql'

                    corrected_lines.append(f"```{lang}")
                    in_code_block = True
                    code_block_lang = lang
                else:
                    # 结束代码块
                    corrected_lines.append('```')
                    in_code_block = False
                    code_block_lang = None
            else:
                corrected_lines.append(line)

        return '\n'.join(corrected_lines), corrections_made

    def check_markdown_syntax(self, content):
        """检查 Markdown 语法"""
        corrections_made = []

        # 检查标题格式
        content = re.sub(r'^(\s*#{1,6})([^#\s])', r'\1 \2', content, flags=re.MULTILINE)

        # 检查列表格式
        content = re.sub(r'^(\s*)([-*+])([^ \s])', r'\1\2 \3', content, flags=re.MULTILINE)
        content = re.sub(r'^(\s*)(\d+)([^ \s.])', r'\1\2. \3', content, flags=re.MULTILINE)

        # 检查链接格式
        content = re.sub(r'\[\s*([^\]]+)\s*\]\s*\(\s*([^)]+)\s*\)', r'[\1](\2)', content)

        # 检查图片格式
        content = re.sub(r'!\[\s*([^\]]*)\s*\]\s*\(\s*([^)]+)\s*\)', r'![\1](\2)', content)

        # 检查加粗和斜体
        content = re.sub(r'\*\*\s*([^*]+)\s*\*\*', r'**\1**', content)
        content = re.sub(r'\*\s*([^*]+)\s*\*', r'*\1*', content)

        return content, corrections_made

    def check_factual_accuracy(self, content):
        """检查事实准确性（简单版本）"""
        warnings = []

        # 检查一些明显的技术错误
        error_patterns = [
            (r'Python\s+是\s+编译型\s+语言', 'Python 是解释型语言，不是编译型语言'),
            (r'Java\s+是\s+解释型\s+语言', 'Java 是编译型语言，编译成字节码后在JVM上运行'),
            (r'C\+\+\s+是\s+解释型\s+语言', 'C++ 是编译型语言，不是解释型语言'),
            (r'JavaScript\s+是\s+编译型\s+语言', 'JavaScript 是解释型语言（JIT编译）'),
            (r'HTTP\s+是\s+有状态\s+协议', 'HTTP 是无状态协议'),
            (r'tcp\s+是\s+不可靠\s+协议', 'TCP 是可靠的传输协议'),
            (r'udp\s+是\s+可靠\s+协议', 'UDP 是不可靠的传输协议'),
        ]

        for pattern, warning in error_patterns:
            if re.search(pattern, content, flags=re.IGNORECASE):
                warnings.append(f"事实检查警告: {warning}")

        return warnings

    def review_content(self, doc_info):
        """审查文档内容"""
        try:
            content = doc_info['optimized_content']
            all_corrections = []
            all_warnings = []

            # 1. 检查技术术语
            content, tech_corrections = self.check_technical_terms(content)
            all_corrections.extend(tech_corrections)

            # 2. 检查语法
            content, grammar_corrections = self.check_grammar(content)
            all_corrections.extend(grammar_corrections)

            # 3. 检查代码块
            content, code_corrections = self.check_code_blocks(content)
            all_corrections.extend(code_corrections)

            # 4. 检查 Markdown 语法
            content, markdown_corrections = self.check_markdown_syntax(content)
            all_corrections.extend(markdown_corrections)

            # 5. 检查事实准确性
            factual_warnings = self.check_factual_accuracy(content)
            all_warnings.extend(factual_warnings)

            # 更新文档信息
            doc_info.update({
                'reviewed_content': content,
                'corrections': all_corrections,
                'warnings': all_warnings,
                'review_time': datetime.now().isoformat(),
                'status': 'reviewed'
            })

            # 保存修正后的内容到 optimized_content
            doc_info['optimized_content'] = content

            self.logger.info(f"内容审查完成: {doc_info['filename']} (修正: {len(all_corrections)}, 警告: {len(all_warnings)})")
            return doc_info

        except Exception as e:
            self.logger.error(f"内容审查失败 {doc_info.get('filename', 'unknown')}: {e}")
            doc_info['status'] = 'review_failed'
            doc_info['error'] = str(e)
            return doc_info

    def process_batch(self, batch_file):
        """处理一批文档"""
        self.logger.info(f"开始审查批次: {batch_file}")

        # 加载批次文件
        try:
            with open(batch_file, 'r', encoding='utf-8') as f:
                documents = json.load(f)
        except Exception as e:
            self.logger.error(f"加载批次文件失败: {e}")
            return None

        # 处理每个文档
        reviewed_docs = []
        for doc in documents:
            if doc.get('status') == 'enhanced':
                reviewed_doc = self.review_content(doc)
                reviewed_docs.append(reviewed_doc)
            else:
                reviewed_docs.append(doc)

        # 保存审查后的批次
        reviewed_batch_file = batch_file.replace('_enhanced.json', '_reviewed.json')
        try:
            with open(reviewed_batch_file, 'w', encoding='utf-8') as f:
                json.dump(reviewed_docs, f, ensure_ascii=False, indent=2)

            self.logger.info(f"批次审查完成，已保存到: {reviewed_batch_file}")
            return reviewed_batch_file

        except Exception as e:
            self.logger.error(f"保存审查批次失败: {e}")
            return None

    def run(self, batch_files):
        """运行内容审查流程"""
        self.logger.info("开始内容审查流程")

        reviewed_batches = []
        for batch_file in batch_files:
            reviewed_batch = self.process_batch(batch_file)
            if reviewed_batch:
                reviewed_batches.append(reviewed_batch)

        self.logger.info(f"内容审查完成，共处理 {len(reviewed_batches)} 个批次")
        return reviewed_batches

if __name__ == "__main__":
    reviewer = ContentReviewer('config')

    # 查找增强后的批次文件
    batch_files = list(Path('.').glob('batch_*_enhanced.json'))
    if batch_files:
        reviewed = reviewer.run([str(f) for f in batch_files])
        print(f"\n成功审查 {len(reviewed)} 个批次")
    else:
        print("没有找到增强后的批次文件")