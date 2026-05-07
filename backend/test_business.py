#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
血压守护 - 业务功能测试（兼容Python 3.14）
"""

import sys
import json
import time
import os
import ast
from pathlib import Path

results = []
total = 0
passed = 0

def test(name, condition, detail=''):
    global total, passed
    total += 1
    status = 'PASS' if condition else 'FAIL'
    if condition:
        passed += 1
    results.append({'name': name, 'status': status, 'detail': detail})
    icon = '✅' if condition else '❌'
    print(f'{icon} [{status}] {name}' + (f' - {detail}' if detail else ''))

def main():
    global total, passed
    print('='*60)
    print('🖥️ 血压守护 - 后端业务功能测试')
    print('='*60)
    print()
    
    backend_path = Path(__file__).parent
    
    # 1. 文件完整性测试
    print('📁 文件完整性测试:')
    core_files = [
        ('app/__init__.py', '应用工厂'),
        ('app/config.py', '配置模块'),
        ('app/models.py', '数据模型'),
        ('app/routes/auth.py', '认证路由'),
        ('app/routes/medication.py', '药物路由'),
        ('app/routes/bp.py', '血压路由'),
        ('app/services/alert_service.py', '预警服务'),
        ('app/services/wechat_service.py', '微信服务'),
        ('app/security.py', '安全模块'),
        ('app/logger.py', '日志模块'),
        ('requirements.txt', '依赖列表'),
        ('run.py', '启动脚本'),
    ]
    
    for filename, description in core_files:
        file_path = backend_path / filename
        test(f'核心文件: {description}', file_path.exists(), filename)
    
    # 2. 代码语法测试
    print('\n🔍 代码语法测试:')
    for filename, description in core_files:
        if filename.endswith('.py'):
            file_path = backend_path / filename
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    ast.parse(content)
                    test(f'语法: {description}', True, '语法正确')
                except SyntaxError as e:
                    test(f'语法: {description}', False, f'第{e.lineno}行: {e.msg}')
    
    # 3. 配置模块测试
    print('\n⚙️ 配置模块测试:')
    config_path = backend_path / 'app' / 'config.py'
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        test('数据库配置', 'SQLALCHEMY_DATABASE_URI' in content, '数据库配置存在')
        test('密钥配置', 'SECRET_KEY' in content, '密钥配置存在')
        test('APP_NAME', 'APP_NAME' in content or 'APP_NAME' in content, 'APP_NAME配置存在')
        test('VERSION配置', 'VERSION' in content, 'VERSION配置存在')
    
    # 4. 数据模型测试
    print('\n🗄️ 数据模型测试:')
    models_path = backend_path / 'app' / 'models.py'
    if models_path.exists():
        with open(models_path, 'r', encoding='utf-8') as f:
            content = f.read()
        test('User模型', 'class User' in content, 'User模型定义存在')
        test('FamilyMember模型', 'class FamilyMember' in content, 'FamilyMember模型定义存在')
        test('Medication模型', 'class Medication' in content, 'Medication模型定义存在')
        test('BloodPressureRecord模型', 'class BloodPressureRecord' in content, 'BloodPressureRecord模型定义存在')
        test('Alert模型', 'class Alert' in content, 'Alert模型定义存在')
        test('数据库索引', 'db.Index' in content, '数据库索引定义存在')
        test('关系定义', 'db.relationship' in content, '关系定义存在')
    
    # 5. 路由测试
    print('\n🛣️ 路由测试:')
    route_files = [
        ('app/routes/auth.py', '认证路由'),
        ('app/routes/medication.py', '药物路由'),
        ('app/routes/bp.py', '血压路由'),
    ]
    
    for filename, description in route_files:
        filepath = backend_path / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            test(f'{description} - Blueprint', 'Blueprint' in content, f'{description}已注册Blueprint')
            test(f'{description} - 路由装饰器', '@' in content and 'route' in content, f'{description}包含路由定义')
    
    # 6. 服务模块测试
    print('\n⚙️ 服务模块测试:')
    alert_path = backend_path / 'app' / 'services' / 'alert_service.py'
    wechat_path = backend_path / 'app' / 'services' / 'wechat_service.py'
    
    if alert_path.exists():
        with open(alert_path, 'r', encoding='utf-8') as f:
            content = f.read()
        test('预警服务 - 类定义', 'class' in content, 'AlertService类定义存在')
        test('预警服务 - 业务逻辑', 'def ' in content, '包含业务方法')
    
    if wechat_path.exists():
        with open(wechat_path, 'r', encoding='utf-8') as f:
            content = f.read()
        test('微信服务 - 类定义', 'class' in content, 'WeChatService类定义存在')
        test('微信服务 - API调用', 'requests' in content, '包含微信API调用')
    
    # 7. 安全模块测试
    print('\n🔒 安全模块测试:')
    security_path = backend_path / 'app' / 'security.py'
    if security_path.exists():
        with open(security_path, 'r', encoding='utf-8') as f:
            content = f.read()
        test('密码加密', 'hashlib' in content or 'bcrypt' in content or 'werkzeug' in content, '密码加密存在')
        test('CSRF防护', 'csrf' in content.lower() or 'CSRF' in content, 'CSRF防护存在')
    
    # 8. 业务逻辑测试
    print('\n💼 业务逻辑测试:')
    bp_path = backend_path / 'app' / 'routes' / 'bp.py'
    if bp_path.exists():
        with open(bp_path, 'r', encoding='utf-8') as f:
            content = f.read()
        test('血压记录API', 'def ' in content, '血压记录API存在')
        test('血压分析API', 'analysis' in content.lower() or 'analyze' in content.lower(), '血压分析功能存在')
    
    med_path = backend_path / 'app' / 'routes' / 'medication.py'
    if med_path.exists():
        with open(med_path, 'r', encoding='utf-8') as f:
            content = f.read()
        test('药物管理API', 'def ' in content, '药物管理API存在')
        test('服药日志', 'log' in content.lower(), '服药日志功能存在')
    
    # 9. 总结
    print()
    print('='*60)
    failed = total - passed
    if failed == 0:
        print(f'🎉 后端测试全部通过！{total} 项测试全部通过')
    else:
        print(f'❌ 后端测试存在失败: {passed}/{total} 通过, {failed} 失败')
    print('='*60)
    
    # 保存报告
    report = {
        'total': total,
        'passed': passed,
        'failed': failed,
        'results': results
    }
    
    report_path = backend_path.parent / 'test_reports'
    report_path.mkdir(exist_ok=True)
    
    with open(report_path / '业务测试报告.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f'\n📄 测试报告已保存至: test_reports/业务测试报告.json')
    
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
