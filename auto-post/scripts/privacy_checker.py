"""隐私内容检测脚本"""
import json
import re
from pathlib import Path
import sys
from datetime import datetime
import os

# 添加 scripts 目录到 Python 路径
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(script_dir, 'scripts'))

from utils import setup_logger, load_config

class PrivacyChecker:
    """隐私内容检测器"""

    def __init__(self, config_dir):
        self.logger = setup_logger('PrivacyChecker', 'logs/privacy-checker.log')
        self.config_dir = Path(config_dir)

        # 加载隐私检测配置
        privacy_file = self.config_dir / 'privacy.json'
        self.privacy_config = load_config(privacy_file) if privacy_file.exists() else {}

        self.sensitive_patterns = self.privacy_config.get('sensitive_patterns', {})
        self.replacement_texts = self.privacy_config.get('replacement_texts', {})
        self.allowed_domains = set(self.privacy_config.get('allowed_domains', []))
        self.exclusion_patterns = self.privacy_config.get('exclusion_patterns', [])

        # 预编译正则表达式
        self.compiled_patterns = {}
        for category, patterns in self.sensitive_patterns.items():
            self.compiled_patterns[category] = [re.compile(pattern, re.IGNORECASE | re.DOTALL) for pattern in patterns]

        self.logger.info("隐私内容检测器初始化完成")

    def is_allowed_domain(self, domain):
        """检查是否是允许的域名"""
        # 移除端口号
        domain = domain.split(':')[0].lower()
        return domain in self.allowed_domains or any(domain.endswith('.' + d) for d in self.allowed_domains)

    def is_excluded_pattern(self, text):
        """检查是否是排除的模式"""
        for pattern in self.exclusion_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def mask_sensitive_content(self, content):
        """屏蔽敏感内容"""
        masked_content = content
        detections = []

        # 检查各种类型的敏感信息
        for category, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                matches = pattern.finditer(masked_content)

                for match in matches:
                    matched_text = match.group()
                    start_pos = match.start()
                    end_pos = match.end()
                    context = masked_content[max(0, start_pos-30):start_pos] + matched_text + masked_content[end_pos:end_pos+30]

                    # 特殊处理域名
                    if category == 'domains':
                        # 检查是否是允许的域名或排除的模式
                        if self.is_allowed_domain(matched_text) or self.is_excluded_pattern(matched_text):
                            continue

                    # 记录检测结果
                    detection = {
                        'type': category,
                        'value': matched_text,
                        'position': (start_pos, end_pos),
                        'context': context,
                        'severity': self._get_severity(category)
                    }
                    detections.append(detection)

                    # 替换敏感内容
                    replacement = self.replacement_texts.get(category, f'[{category.upper()}_REMOVED]')
                    masked_content = masked_content[:start_pos] + replacement + masked_content[end_pos:]

        return masked_content, detections

    def _get_severity(self, category):
        """获取严重级别"""
        severity_map = {
            'api_keys': 'critical',
            'passwords': 'critical',
            'private_keys': 'critical',
            'certificates': 'critical',
            'jwt_tokens': 'high',
            'database_urls': 'high',
            'emails': 'medium',
            'phone_numbers': 'medium',
            'ip_addresses': 'low',
            'domains': 'low'
        }
        return severity_map.get(category, 'medium')

    def check_code_blocks(self, content):
        """检查代码块中的敏感信息"""
        lines = content.split('\n')
        checked_lines = []
        in_code_block = False
        detections = []

        for i, line in enumerate(lines):
            stripped = line.strip()

            # 检查代码块标记
            if stripped.startswith('```'):
                in_code_block = not in_code_block
                checked_lines.append(line)
                continue

            if in_code_block:
                # 在代码块中查找敏感信息
                masked_line, line_detections = self.mask_sensitive_content(line)
                checked_lines.append(masked_line)

                # 添加行号信息
                for detection in line_detections:
                    detection['line_number'] = i + 1
                    detection['in_code_block'] = True
                    detections.append(detection)
            else:
                checked_lines.append(line)

        return '\n'.join(checked_lines), detections

    def check_urls_and_links(self, content):
        """检查URL和链接中的敏感信息"""
        detections = []

        # 查找所有链接
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        matches = re.finditer(url_pattern, content)

        for match in matches:
            url = match.group()
            start_pos = match.start()
            end_pos = match.end()

            # 检查URL中是否包含敏感参数
            sensitive_params = ['api_key', 'apikey', 'key', 'token', 'secret', 'password', 'pwd']
            for param in sensitive_params:
                if f'{param}=' in url.lower():
                    detection = {
                        'type': 'sensitive_url',
                        'value': url,
                        'position': (start_pos, end_pos),
                        'context': content[max(0, start_pos-20):end_pos+20],
                        'severity': 'high',
                        'parameter': param
                    }
                    detections.append(detection)

                    # 屏蔽URL中的参数值
                    masked_url = re.sub(f'({param}=)[^&\\s]*', r'\1[REMOVED]', url, flags=re.IGNORECASE)
                    content = content[:start_pos] + masked_url + content[end_pos:]
                    break

        return content, detections

    def check_base64_content(self, content):
        """检查可能的Base64编码内容"""
        # 查找可能是Base64的长字符串
        base64_pattern = r'[A-Za-z0-9+/]{40,}={0,2}'
        matches = re.finditer(base64_pattern, content)

        detections = []
        for match in matches:
            base64_str = match.group()
            # 检查是否可能是敏感信息的Base64编码
            if len(base64_str) > 100:  # 很长的Base64字符串可能是编码的密钥或证书
                try:
                    import base64
                    decoded = base64.b64decode(base64_str)
                    decoded_str = decoded.decode('utf-8', errors='ignore')

                    # 检查解码后是否包含敏感关键词
                    sensitive_keywords = ['password', 'secret', 'key', 'token', 'private', 'api']
                    if any(keyword in decoded_str.lower() for keyword in sensitive_keywords):
                        detection = {
                            'type': 'base64_secret',
                            'value': base64_str[:50] + '...',
                            'position': (match.start(), match.end()),
                            'context': content[max(0, match.start()-20):match.end()+20],
                            'severity': 'high',
                            'decoded_contains': [kw for kw in sensitive_keywords if kw in decoded_str.lower()]
                        }
                        detections.append(detection)

                        # 替换Base64内容
                        content = content[:match.start()] + '[BASE64_SECRET_REMOVED]' + content[match.end():]

                except:
                    # 如果解码失败，可能不是Base64，跳过
                    pass

        return content, detections

    def check_privacy(self, doc_info):
        """检查文档的隐私内容"""
        try:
            content = doc_info['optimized_content']
            all_detections = []

            # 1. 基本敏感内容检测
            content, basic_detections = self.mask_sensitive_content(content)
            all_detections.extend(basic_detections)

            # 2. 检查代码块
            content, code_detections = self.check_code_blocks(content)
            all_detections.extend(code_detections)

            # 3. 检查URL和链接
            content, url_detections = self.check_urls_and_links(content)
            all_detections.extend(url_detections)

            # 4. 检查Base64内容
            content, base64_detections = self.check_base64_content(content)
            all_detections.extend(base64_detections)

            # 统计检测结果
            severity_count = {
                'critical': sum(1 for d in all_detections if d['severity'] == 'critical'),
                'high': sum(1 for d in all_detections if d['severity'] == 'high'),
                'medium': sum(1 for d in all_detections if d['severity'] == 'medium'),
                'low': sum(1 for d in all_detections if d['severity'] == 'low')
            }

            # 检查是否有关键安全问题
            has_critical_issues = severity_count['critical'] > 0

            # 更新文档信息
            doc_info.update({
                'privacy_checked_content': content,
                'privacy_detections': all_detections,
                'severity_count': severity_count,
                'has_critical_issues': has_critical_issues,
                'privacy_check_time': datetime.now().isoformat(),
                'status': 'privacy_checked'
            })

            # 保存检测后的内容到 optimized_content
            doc_info['optimized_content'] = content

            self.logger.info(f"隐私内容检测完成: {doc_info['filename']} (检测到: {len(all_detections)} 项, 严重: {severity_count['critical']})")
            return doc_info

        except Exception as e:
            self.logger.error(f"隐私内容检测失败 {doc_info.get('filename', 'unknown')}: {e}")
            doc_info['status'] = 'privacy_check_failed'
            doc_info['error'] = str(e)
            return doc_info

    def process_batch(self, batch_file):
        """处理一批文档"""
        self.logger.info(f"开始隐私检测批次: {batch_file}")

        # 加载批次文件
        try:
            with open(batch_file, 'r', encoding='utf-8') as f:
                documents = json.load(f)
        except Exception as e:
            self.logger.error(f"加载批次文件失败: {e}")
            return None

        # 处理每个文档
        checked_docs = []
        for doc in documents:
            if doc.get('status') == 'reviewed':
                checked_doc = self.check_privacy(doc)
                checked_docs.append(checked_doc)
            else:
                checked_docs.append(doc)

        # 保存检测后的批次
        checked_batch_file = batch_file.replace('_reviewed.json', '_privacy_checked.json')
        try:
            with open(checked_batch_file, 'w', encoding='utf-8') as f:
                json.dump(checked_docs, f, ensure_ascii=False, indent=2)

            # 生成隐私检测报告
            report_file = batch_file.replace('_reviewed.json', '_privacy_report.json')
            self._generate_report(checked_docs, report_file)

            self.logger.info(f"隐私检测完成，已保存到: {checked_batch_file}")
            return checked_batch_file

        except Exception as e:
            self.logger.error(f"保存隐私检测批次失败: {e}")
            return None

    def _generate_report(self, documents, report_file):
        """生成隐私检测报告"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_documents': len(documents),
            'documents_with_issues': 0,
            'total_detections': 0,
            'severity_breakdown': {
                'critical': 0,
                'high': 0,
                'medium': 0,
                'low': 0
            },
            'documents': []
        }

        for doc in documents:
            if 'privacy_detections' in doc:
                doc_report = {
                    'filename': doc.get('filename', 'unknown'),
                    'has_critical_issues': doc.get('has_critical_issues', False),
                    'detection_count': len(doc['privacy_detections']),
                    'severity_count': doc.get('severity_count', {}),
                    'detections': doc['privacy_detections']
                }
                report['documents'].append(doc_report)

                if doc['privacy_detections']:
                    report['documents_with_issues'] += 1
                    report['total_detections'] += len(doc['privacy_detections'])

                    # 更新严重性统计
                    for severity, count in doc.get('severity_count', {}).items():
                        if severity in report['severity_breakdown']:
                            report['severity_breakdown'][severity] += count

        # 保存报告
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        self.logger.info(f"隐私检测报告已生成: {report_file}")

    def run(self, batch_files):
        """运行隐私检测流程"""
        self.logger.info("开始隐私内容检测流程")

        checked_batches = []
        for batch_file in batch_files:
            checked_batch = self.process_batch(batch_file)
            if checked_batch:
                checked_batches.append(checked_batch)

        self.logger.info(f"隐私内容检测完成，共处理 {len(checked_batches)} 个批次")
        return checked_batches

if __name__ == "__main__":
    checker = PrivacyChecker('config')

    # 查找审查后的批次文件
    batch_files = list(Path('.').glob('batch_*_reviewed.json'))
    if batch_files:
        checked = checker.run([str(f) for f in batch_files])
        print(f"\n成功检测 {len(checked)} 个批次")

        # 打印摘要
        total_detections = 0
        for batch_file in checked:
            report_file = batch_file.replace('_privacy_checked.json', '_privacy_report.json')
            if Path(report_file).exists():
                with open(report_file, 'r', encoding='utf-8') as f:
                    report = json.load(f)
                    total_detections += report['total_detections']
                    print(f"  - {Path(batch_file).name}: {report['total_detections']} 个隐私问题")
        print(f"\n总共发现 {total_detections} 个隐私相关问题")
    else:
        print("没有找到审查后的批次文件")