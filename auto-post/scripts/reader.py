"""文档读取脚本"""
import os
import json
from pathlib import Path
import sys
from datetime import datetime

# 添加 scripts 目录到 Python 路径
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(script_dir, 'scripts'))

from utils import setup_logger, load_config, save_config

class DocumentReader:
    """文档读取器"""

    def __init__(self, config_dir):
        self.logger = setup_logger('DocumentReader', 'logs/reader.log')
        self.config_dir = config_dir
        self.unpost_dir = Path('../unpost')
        self.processed_docs_file = Path('config/processed_docs.json')

        # 加载已处理的文档记录
        self.processed_docs = load_config(self.processed_docs_file) if self.processed_docs_file.exists() else {}

        self.logger.info("文档读取器初始化完成")

    def scan_unpost_directory(self):
        """扫描 unpost 目录，获取所有未处理的文档"""
        if not self.unpost_dir.exists():
            self.logger.error(f"unpost 目录不存在: {self.unpost_dir}")
            return []

        documents = []

        # 遍历目录下的所有文件（不包括子目录）
        for file_path in self.unpost_dir.iterdir():
            if file_path.is_file() and not file_path.name.startswith('.'):
                # 检查文件扩展名
                if file_path.suffix.lower() in ['.md', '.txt', '.markdown']:
                    # 检查是否已经处理过
                    file_key = str(file_path.relative_to(self.unpost_dir))
                    if file_key not in self.processed_docs or not self.processed_docs[file_key].get('completed', False):
                        documents.append({
                            'path': str(file_path),  # 转换为字符串
                            'relative_path': file_key,
                            'filename': file_path.name,
                            'size': file_path.stat().st_size,
                            'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                        })

        self.logger.info(f"发现 {len(documents)} 个未处理的文档")
        return documents

    def read_document(self, doc_info):
        """读取单个文档内容"""
        try:
            file_path_str = doc_info['path']
            file_path = Path(file_path_str)  # 转换为 Path 对象

            # 尝试不同的编码
            encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16']
            content = None
            used_encoding = None

            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    used_encoding = encoding
                    self.logger.debug(f"使用 {encoding} 编码成功读取文件: {file_path.name}")
                    break
                except UnicodeDecodeError:
                    continue

            if content is None:
                self.logger.error(f"无法读取文件: {file_path.name}")
                return None

            # 更新文档信息
            doc_info.update({
                'path': file_path_str,  # 保存字符串
                'content': content,
                'encoding': used_encoding,
                'lines': len(content.split('\n')),
                'read_time': datetime.now().isoformat(),
                'status': 'read'
            })

            # 记录为已读取
            self.processed_docs[doc_info['relative_path']] = {
                'last_read': doc_info['read_time'],
                'completed': False,
                'steps_completed': ['read']
            }

            self.logger.info(f"成功读取文档: {doc_info['filename']}")
            return doc_info

        except Exception as e:
            self.logger.error(f"读取文档失败 {doc_info['filename']}: {e}")
            return None

    def save_document_batch(self, documents, batch_file):
        """保存一批文档到文件"""
        try:
            with open(batch_file, 'w', encoding='utf-8') as f:
                json.dump(documents, f, ensure_ascii=False, indent=2)
            self.logger.info(f"文档批次已保存到: {batch_file}")
            return True
        except Exception as e:
            self.logger.error(f"保存文档批次失败: {e}")
            return False

    def update_processed_docs(self):
        """更新已处理文档记录"""
        return save_config(self.processed_docs, self.processed_docs_file)

    def create_batch(self, documents, batch_size=10):
        """创建文档批次"""
        batches = []
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            batch_file = Path(f'batch_{datetime.now().strftime("%Y%m%d_%H%M%S")}_{i // batch_size + 1}.json')

            # 读取批次中的所有文档
            processed_batch = []
            for doc in batch:
                processed_doc = self.read_document(doc)
                if processed_doc:
                    processed_batch.append(processed_doc)

            if processed_batch:
                if self.save_document_batch(processed_batch, batch_file):
                    batches.append({
                        'batch_file': str(batch_file),
                        'count': len(processed_batch),
                        'documents': processed_batch
                    })

        return batches

    def run(self):
        """执行文档读取流程"""
        self.logger.info("开始文档读取流程")

        # 扫描 unpost 目录
        documents = self.scan_unpost_directory()

        if not documents:
            self.logger.info("没有发现新文档")
            return []

        # 创建批次
        batches = self.create_batch(documents)

        # 更新已处理文档记录
        self.update_processed_docs()

        self.logger.info(f"文档读取完成，共创建 {len(batches)} 个批次")
        return batches

if __name__ == "__main__":
    reader = DocumentReader(Path('config'))
    batches = reader.run()

    if batches:
        print(f"\n成功创建 {len(batches)} 个批次:")
        for i, batch in enumerate(batches, 1):
            print(f"  批次 {i}: {batch['count']} 个文档 -> {batch['batch_file']}")
    else:
        print("没有发现需要处理的文档")