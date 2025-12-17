#!/usr/bin/env python3
"""自动文章发布系统 - 主控制脚本"""
import os
import sys
import json
import argparse
import re
from pathlib import Path
from datetime import datetime

# 添加 scripts 目录到 Python 路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, 'scripts'))

from utils import setup_logger, load_config
from reader import DocumentReader
from optimizer import DocumentOptimizer
from blog_enhancer import BlogEnhancer
from reviewer import ContentReviewer
from privacy_checker import PrivacyChecker
from publisher import BlogPublisher

class AutoPostSystem:
    """自动发布系统主控制器"""

    def __init__(self, config_dir='config'):
        self.logger = setup_logger('AutoPostSystem', 'logs/auto-post.log')
        self.config_dir = Path(config_dir)

        # 加载系统设置
        self.settings = load_config(self.config_dir / 'settings.json') or {}

        # 初始化各个模块
        self.reader = DocumentReader(self.config_dir)
        self.optimizer = DocumentOptimizer(self.config_dir)
        self.enhancer = BlogEnhancer(self.config_dir)
        self.reviewer = ContentReviewer(self.config_dir)
        self.privacy_checker = PrivacyChecker(self.config_dir)
        self.publisher = BlogPublisher(self.config_dir)

        self.logger.info("自动发布系统初始化完成")

    def run_full_pipeline(self):
        """运行完整的处理流程"""
        self.logger.info("=" * 50)
        self.logger.info("开始运行自动文章发布流程")
        self.logger.info("=" * 50)

        start_time = datetime.now()
        stats = {
            'start_time': start_time.isoformat(),
            'total_documents': 0,
            'processed_documents': 0,
            'published_documents': 0,
            'errors': []
        }

        try:
            # 步骤 1: 读取文档
            self.logger.info("\n[步骤 1/7] 读取 unpost 目录中的文档...")
            batches = self.reader.run()
            if not batches:
                self.logger.info("没有发现新文档，流程结束")
                return self._generate_report(stats)

            batch_files = [batch['batch_file'] for batch in batches]
            stats['total_documents'] = sum(batch['count'] for batch in batches)
            self.logger.info(f"发现 {stats['total_documents']} 个文档，创建了 {len(batches)} 个批次")

            # 步骤 2: 优化标题和结构
            if self.settings.get('processing', {}).get('enable_title_optimization', True):
                self.logger.info("\n[步骤 2/7] 优化标题和文档结构...")
                optimized_batches = self.optimizer.run(batch_files)
                if not optimized_batches:
                    raise RuntimeError("标题和结构优化失败")
                batch_files = optimized_batches
            else:
                self.logger.info("\n[步骤 2/7] 跳过标题和结构优化")

            # 步骤 3: 博客内容增强
            if self.settings.get('processing', {}).get('enable_blog_enhancement', True):
                self.logger.info("\n[步骤 3/7] 增强博客内容（摘要、分类、标签等）...")
                enhanced_batches = self.enhancer.run(batch_files)
                if not enhanced_batches:
                    raise RuntimeError("博客内容增强失败")
                batch_files = enhanced_batches
            else:
                self.logger.info("\n[步骤 3/7] 跳过博客内容增强")

            # 步骤 4: 内容审查和修正
            if self.settings.get('processing', {}).get('enable_content_review', True):
                self.logger.info("\n[步骤 4/7] 审查和修正文档内容...")
                reviewed_batches = self.reviewer.run(batch_files)
                if not reviewed_batches:
                    raise RuntimeError("内容审查失败")
                batch_files = reviewed_batches
            else:
                self.logger.info("\n[步骤 4/7] 跳过内容审查")

            # 步骤 5: 隐私内容检测
            if self.settings.get('processing', {}).get('enable_privacy_check', True):
                self.logger.info("\n[步骤 5/8] 检测和处理隐私内容...")
                checked_batches = self.privacy_checker.run(batch_files)
                if not checked_batches:
                    raise RuntimeError("隐私内容检测失败")

                # 检查是否有关键隐私问题
                critical_issues = 0
                for batch_file in checked_batches:
                    with open(batch_file, 'r', encoding='utf-8') as f:
                        documents = json.load(f)
                        for doc in documents:
                            if doc.get('has_critical_issues', False):
                                critical_issues += 1

                if critical_issues > 0:
                    error_msg = f"发现 {critical_issues} 个文档包含严重隐私问题，已停止发布"
                    self.logger.error(error_msg)
                    stats['errors'].append(error_msg)
                    return self._generate_report(stats)

                batch_files = checked_batches
            else:
                self.logger.info("\n[步骤 5/8] 跳过隐私内容检测")

            # 步骤 6: 文档格式检查
            self.logger.info("\n[步骤 6/8] 检查文档格式...")

            # 只做格式检查，不修改文档
            format_issues = 0
            for batch_file in batch_files:
                try:
                    with open(batch_file, 'r', encoding='utf-8') as f:
                        documents = json.load(f)

                    for doc in documents:
                        content = doc.get('optimized_content', '')
                        if self._check_format_issues(content):
                            format_issues += 1
                            self.logger.warning(f"文档 {doc.get('filename', 'unknown')} 存在格式问题")
                except:
                    pass

            if format_issues > 0:
                self.logger.warning(f"发现 {format_issues} 个文档存在格式问题，建议手动检查")
            else:
                self.logger.info("所有文档格式检查通过")

            # 步骤 7: 发布博客文章
            self.logger.info("\n[步骤 7/8] 发布博客文章...")
            published_batches = self.publisher.run(
                batch_files,
                test_local=self.settings.get('processing', {}).get('enable_local_test', True),
                deploy=self.settings.get('processing', {}).get('enable_auto_deploy', False)
            )
            if not published_batches:
                raise RuntimeError("博客发布失败")

            # 统计发布结果
            for batch_file in published_batches:
                with open(batch_file, 'r', encoding='utf-8') as f:
                    documents = json.load(f)
                    for doc in documents:
                        if doc.get('status') == 'published':
                            stats['published_documents'] += 1
                        elif doc.get('status') in ['read', 'optimized', 'enhanced', 'reviewed', 'privacy_checked']:
                            stats['processed_documents'] += 1
                        else:
                            stats['errors'].append(f"{doc.get('filename', 'unknown')}: {doc.get('error', 'Unknown error')}")

            # 步骤 8: 清理临时文件
            self.logger.info("\n[步骤 8/8] 清理临时文件...")
            self._cleanup_temp_files()

            # 完成统计
            end_time = datetime.now()
            stats['end_time'] = end_time.isoformat()
            stats['duration_seconds'] = (end_time - start_time).total_seconds()
            stats['success'] = len(stats['errors']) == 0

            # 生成报告
            self.logger.info("\n" + "=" * 50)
            self.logger.info("自动文章发布流程完成!")
            self.logger.info(f"总文档数: {stats['total_documents']}")
            self.logger.info(f"处理文档数: {stats['processed_documents']}")
            self.logger.info(f"发布文档数: {stats['published_documents']}")
            self.logger.info(f"耗时: {stats['duration_seconds']:.2f} 秒")
            if stats['errors']:
                self.logger.warning(f"错误数: {len(stats['errors'])}")
                for error in stats['errors']:
                    self.logger.warning(f"  - {error}")
            self.logger.info("=" * 50)

            return self._generate_report(stats)

        except Exception as e:
            self.logger.error(f"自动发布流程失败: {e}")
            stats['errors'].append(str(e))
            stats['success'] = False
            stats['end_time'] = datetime.now().isoformat()
            return self._generate_report(stats)

    def _check_format_issues(self, content):
        """检查文档是否存在格式问题"""
        issues = []

        # 检查1: Front Matter 是否损坏
        if '---' in content:
            parts = content.split('---', 3)
            if len(parts) >= 3:
                front_matter = parts[1]
                # 检查是否有表格内容混入
                if '|' in front_matter and '---' in front_matter:
                    issues.append("Front Matter 可能包含表格内容")
                # 检查是否有非法字符
                if '------' in front_matter or '--------' in front_matter:
                    issues.append("Front Matter 包含过多的横线")

        # 检查2: 摘要是否过长
        excerpt_match = re.search(r'^excerpt:\s*(.+)$', content, re.MULTILINE)
        if excerpt_match:
            excerpt = excerpt_match.group(1).strip()
            if len(excerpt) > 200:
                issues.append(f"摘要过长 ({len(excerpt)} 字符)")

        # 检查3: 是否有重复的标题
        lines = content.split('\n')
        titles = []
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                title = line[2:].strip()
                if title in titles:
                    issues.append(f"重复的标题: {title}")
                titles.append(title)

        # 检查4: 代码块格式
        code_blocks = re.findall(r'```(\w*)', content)
        code_block_ends = content.count('```')
        if len(code_blocks) * 2 != code_block_ends:
            issues.append("代码块标记不匹配")

        # 检查5: 表格格式
        tables = re.findall(r'^\|.*\|$', content, re.MULTILINE)
        if tables:
            for table in tables:
                if not re.search(r'\|[\s\-]+\|', table):
                    issues.append("表格缺少分隔行")

        return len(issues) > 0

    def _generate_report(self, stats):
        """生成处理报告"""
        report_file = Path(f"logs/auto_post_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        self.logger.info(f"处理报告已保存到: {report_file}")
        return stats

    def _cleanup_temp_files(self):
        """清理临时文件"""
        try:
            # 删除批次文件（可选）
            if self.settings.get('cleanup_temp_files', True):
                temp_patterns = [
                    'batch_*.json',
                    'batch_*_optimized.json',
                    'batch_*_enhanced.json',
                    'batch_*_reviewed.json',
                    'batch_*_privacy_checked.json'
                ]

                import glob
                for pattern in temp_patterns:
                    for file_path in glob.glob(pattern):
                        try:
                            os.remove(file_path)
                            self.logger.debug(f"删除临时文件: {file_path}")
                        except:
                            pass

        except Exception as e:
            self.logger.warning(f"清理临时文件时出错: {e}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='自动文章发布系统')
    parser.add_argument('--config', default='config', help='配置文件目录')
    parser.add_argument('--test-local', action='store_true', help='测试本地服务器')
    parser.add_argument('--deploy', action='store_true', help='部署到远程')
    parser.add_argument('--batch-size', type=int, help='批次大小')

    args = parser.parse_args()

    # 创建日志目录
    Path('logs').mkdir(exist_ok=True)

    # 初始化系统
    system = AutoPostSystem(args.config)

    # 更新设置
    if args.test_local:
        system.settings.setdefault('processing', {})['enable_local_test'] = True
    if args.deploy:
        system.settings.setdefault('processing', {})['enable_auto_deploy'] = True
    if args.batch_size:
        system.settings['system']['batch_size'] = args.batch_size

    # 运行流程
    stats = system.run_full_pipeline()

    # 设置退出码
    sys.exit(0 if stats.get('success', False) else 1)

if __name__ == '__main__':
    main()