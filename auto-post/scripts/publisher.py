"""自动发布脚本"""
import json
import os
import subprocess
import shutil
from pathlib import Path
import sys
from datetime import datetime

# 添加 scripts 目录到 Python 路径
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(script_dir, 'scripts'))

from utils import setup_logger, load_config, save_config

class BlogPublisher:
    """博客发布器"""

    def __init__(self, config_dir):
        self.logger = setup_logger('BlogPublisher', 'logs/publisher.log')
        self.config_dir = Path(config_dir)

        # 路径配置
        self.blog_root = Path('..')
        self.source_posts_dir = self.blog_root / 'source' / '_posts'
        self.unpost_dir = self.blog_root / 'unpost'
        self.posted_dir = self.unpost_dir / 'posted'

        # 确保目录存在
        self.posted_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info("博客发布器初始化完成")

    def create_post_file(self, doc_info):
        """创建博客文章文件"""
        try:
            title = doc_info['optimized_title']
            slug = doc_info['slug']
            front_matter = doc_info['front_matter']

            # 生成文件名
            date_prefix = datetime.now().strftime('%Y-%m-%d')
            filename = f"{date_prefix}-{slug}.md"
            filepath = self.source_posts_dir / filename

            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(front_matter)

            self.logger.info(f"创建博客文章: {filename}")
            return filepath, filename

        except Exception as e:
            self.logger.error(f"创建博客文章失败 {doc_info.get('filename', 'unknown')}: {e}")
            return None, None

    def test_local_server(self, timeout=30):
        """测试本地服务器"""
        self.logger.info("启动本地服务器进行测试...")

        try:
            # 切换到博客根目录
            os.chdir(self.blog_root)

            # 生成静态文件
            result = subprocess.run(['npx', 'hexo', 'clean'], capture_output=True, text=True, encoding='utf-8')
            if result.returncode != 0:
                self.logger.error(f"清理失败: {result.stderr}")
                return False

            result = subprocess.run(['npx', 'hexo', 'generate'], capture_output=True, text=True, encoding='utf-8')
            if result.returncode != 0:
                self.logger.error(f"生成失败: {result.stderr}")
                return False

            # 启动本地服务器
            server_process = subprocess.Popen(['npx', 'hexo', 'server'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # 等待服务器启动
            import time
            time.sleep(5)

            # 检查服务器是否运行
            if server_process.poll() is None:
                self.logger.info("本地服务器启动成功，访问地址: http://localhost:4000")
                time.sleep(timeout)  # 保持运行一段时间
                server_process.terminate()
                return True
            else:
                self.logger.error("本地服务器启动失败")
                return False

        except Exception as e:
            self.logger.error(f"测试本地服务器失败: {e}")
            return False
        finally:
            # 切回原目录
            os.chdir(Path.cwd().parent / 'auto-post')

    def move_to_posted(self, original_file, doc_info):
        """将已发布的文档移动到 posted 目录"""
        try:
            if not original_file.exists():
                self.logger.warning(f"原始文件不存在: {original_file}")
                return False

            # 创建目标目录（按年月分类）
            date_prefix = datetime.now().strftime('%Y-%m')
            target_dir = self.posted_dir / date_prefix
            target_dir.mkdir(parents=True, exist_ok=True)

            # 移动文件
            target_file = target_dir / original_file.name
            shutil.move(str(original_file), str(target_file))

            self.logger.info(f"文档已移动到 posted 目录: {target_file}")
            return True

        except Exception as e:
            self.logger.error(f"移动文档到 posted 目录失败: {e}")
            return False

    def deploy_blog(self):
        """部署博客"""
        self.logger.info("开始部署博客...")

        try:
            # 切换到博客根目录
            os.chdir(self.blog_root)

            # 清理并生成
            result = subprocess.run(['npx', 'hexo', 'clean'], capture_output=True, text=True, encoding='utf-8')
            if result.returncode != 0:
                self.logger.error(f"清理失败: {result.stderr}")
                return False

            result = subprocess.run(['npx', 'hexo', 'generate'], capture_output=True, text=True, encoding='utf-8')
            if result.returncode != 0:
                self.logger.error(f"生成失败: {result.stderr}")
                return False

            # 部署
            result = subprocess.run(['npx', 'hexo', 'deploy'], capture_output=True, text=True, encoding='utf-8')
            if result.returncode != 0:
                self.logger.error(f"部署失败: {result.stderr}")
                return False

            self.logger.info("博客部署成功!")
            return True

        except Exception as e:
            self.logger.error(f"部署博客失败: {e}")
            return False
        finally:
            # 切回原目录
            os.chdir(Path.cwd().parent / 'auto-post')

    def process_document(self, doc_info):
        """处理单个文档的发布"""
        try:
            # 1. 创建博客文章文件
            post_file, filename = self.create_post_file(doc_info)
            if not post_file:
                return False

            # 2. 更新文档信息
            doc_info.update({
                'post_file': str(post_file),
                'post_filename': filename,
                'publish_time': datetime.now().isoformat(),
                'status': 'published'
            })

            # 3. 移动原始文档到 posted 目录
            original_file = Path(doc_info['path'])
            self.move_to_posted(original_file, doc_info)

            return True

        except Exception as e:
            self.logger.error(f"发布文档失败 {doc_info.get('filename', 'unknown')}: {e}")
            doc_info['status'] = 'publish_failed'
            doc_info['error'] = str(e)
            return False

    def process_batch(self, batch_file, test_local=False, deploy=False):
        """处理一批文档"""
        self.logger.info(f"开始发布批次: {batch_file}")

        # 加载增强后的批次文件
        try:
            with open(batch_file, 'r', encoding='utf-8') as f:
                documents = json.load(f)
        except Exception as e:
            self.logger.error(f"加载批次文件失败: {e}")
            return None

        # 处理每个文档
        published_docs = []
        successful_count = 0

        for doc in documents:
            # 检查文档状态：enhanced, reviewed, privacy_checked, 或 format_checked 都可以发布
            if doc.get('status') in ['enhanced', 'reviewed', 'privacy_checked', 'format_checked']:
                if self.process_document(doc):
                    successful_count += 1
                published_docs.append(doc)
            else:
                published_docs.append(doc)

        # 保存发布记录
        published_batch_file = batch_file.replace('_enhanced.json', '_published.json')
        try:
            with open(published_batch_file, 'w', encoding='utf-8') as f:
                json.dump(published_docs, f, ensure_ascii=False, indent=2)

            self.logger.info(f"批次发布完成，成功发布 {successful_count} 篇文章，记录已保存到: {published_batch_file}")

            # 测试本地服务器（可选）
            if test_local and successful_count > 0:
                self.test_local_server()

            # 部署到远程（可选）
            if deploy and successful_count > 0:
                self.deploy_blog()

            return published_batch_file

        except Exception as e:
            self.logger.error(f"保存发布记录失败: {e}")
            return None

    def run(self, batch_files, test_local=False, deploy=False):
        """运行发布流程"""
        self.logger.info("开始博客发布流程")

        published_batches = []
        for batch_file in batch_files:
            published_batch = self.process_batch(batch_file, test_local, deploy)
            if published_batch:
                published_batches.append(published_batch)

        self.logger.info(f"博客发布完成，共处理 {len(published_batches)} 个批次")
        return published_batches

if __name__ == "__main__":
    publisher = BlogPublisher('config')

    # 查找增强后的批次文件
    batch_files = list(Path('.').glob('batch_*_enhanced.json'))
    if batch_files:
        # 询问是否要测试和部署
        test_local = input("\n是否要测试本地服务器? (y/n): ").lower() == 'y'
        deploy = input("是否要部署到远程? (y/n): ").lower() == 'y'

        published = publisher.run([str(f) for f in batch_files], test_local, deploy)
        print(f"\n成功发布 {len(published)} 个批次")
    else:
        print("没有找到增强后的批次文件")