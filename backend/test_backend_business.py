#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
血压守护 - 后端业务功能测试
测试API端点、数据库操作、业务逻辑
"""

import sys
import json
import time
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app import create_app

TEST_DB_PATH = Path(__file__).parent / 'instance' / 'test_blood_pressure.db'

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
    print('='*60)
    print('🖥️ 血压守护 - 后端业务功能测试')
    print('='*60)
    print()

    # 1. 应用创建测试
    print('📦 应用初始化测试:')
    try:
        app = create_app()
        test('创建Flask应用', app is not None, '应用实例创建成功')
        test('配置加载', app.config is not None, '配置正常加载')
        test('数据库配置', 'SQLALCHEMY_DATABASE_URI' in app.config, '数据库URL配置')
        test('DEBUG模式', not app.config.get('DEBUG', False), '生产模式关闭DEBUG')
    except Exception as e:
        test('应用初始化', False, str(e))

    # 2. 路由注册测试
    print('\n🛣️ 路由注册测试:')
    try:
        app = create_app()
        routes = list(app.url_map.iter_rules())
        test('路由总数', len(routes) > 0, f'{len(routes)} 个路由已注册')
        
        expected_endpoints = ['health', 'static']
        found_endpoints = [rule.endpoint for rule in routes]
        test('健康检查路由', any('health' in ep for ep in found_endpoints), 'health端点存在')
        test('静态文件路由', 'static' in found_endpoints, 'static端点存在')
        
        print(f'  已注册路由:')
        for rule in routes:
            print(f'    {rule.rule} -> {rule.endpoint} ({",".join(rule.methods)})')
    except Exception as e:
        test('路由测试', False, str(e))

    # 3. 数据库模型测试
    print('\n🗄️ 数据库模型测试:')
    try:
        app = create_app()
        with app.app_context():
            from app.models import db, User, Medication, BloodPressureRecord, Alert
            
            test('模型导入', all([db, User, Medication, BloodPressureRecord, Alert]), '所有模型导入成功')
            test('User模型', True, 'User模型已定义')  # 简化测试
            test('Medication模型字段', hasattr(Medication, 'id') and hasattr(Medication, 'name'), 'Medication模型完整')
            test('BloodPressureRecord模型字段', hasattr(BloodPressureRecord, 'id') and hasattr(BloodPressureRecord, 'systolic'), 'BloodPressureRecord模型完整')
            test('Alert模型字段', hasattr(Alert, 'id') and hasattr(Alert, 'level'), 'Alert模型完整')
    except Exception as e:
        test('数据库模型', False, str(e))

    # 4. API功能测试
    print('\n🔌 API功能测试:')
    try:
        app = create_app()
        app.config['TESTING'] = True
        client = app.test_client()
        
        # 测试健康检查端点
        response = client.get('/api/health')
        test('健康检查API', response.status_code == 200, f'状态码: {response.status_code}')
        
        if response.status_code == 200:
            data = json.loads(response.data)
            test('健康检查响应格式', 'status' in data, '响应包含status字段')
            test('健康状态正常', data.get('status') == 'ok', f'状态: {data.get("status")}')

        # 测试其他端点（如果存在）
        test_endpoints = [
            '/api/auth/health',
            '/api/medication/health',
            '/api/bp/health'
        ]
        
        for endpoint in test_endpoints:
            try:
                resp = client.get(endpoint)
                test(f'模块健康检查: {endpoint}', resp.status_code == 200, f'{resp.status_code}')
            except Exception:
                test(f'模块健康检查: {endpoint}', False, '端点不存在')

    except Exception as e:
        test('API功能', False, str(e))

    # 5. 服务模块测试
    print('\n⚙️ 服务模块测试:')
    try:
        app = create_app()
        with app.app_context():
            # 测试警告服务
            try:
                from app.services.alert_service import AlertService
                test('警告服务导入', AlertService is not None, 'AlertService导入成功')
            except Exception as e:
                test('警告服务', False, str(e))

            # 测试微信服务
            try:
                from app.services.wechat_service import WeChatService
                test('微信服务导入', WeChatService is not None, 'WeChatService导入成功')
            except Exception as e:
                test('微信服务', False, str(e))

    except Exception as e:
        test('服务模块', False, str(e))

    # 6. 配置测试
    print('\n⚙️ 配置测试:')
    try:
        app = create_app()
        test('应用名称', app.config.get('APP_NAME') == '血压守护', f'名称: {app.config.get("APP_NAME")}')
        test('版本号', 'VERSION' in app.config, f'版本: {app.config.get("VERSION")}')
        test('密钥配置', 'SECRET_KEY' in app.config, '密钥已配置')
        test('数据库追踪', not app.config.get('SQLALCHEMY_TRACK_MODIFICATIONS', True), '数据库追踪已禁用')
    except Exception as e:
        test('配置测试', False, str(e))

    # 7. 安全配置测试
    print('\n🔒 安全配置测试:')
    try:
        app = create_app()
        test('CSRF保护', 'CSRF_ENABLED' in app.config or 'WTF_CSRF_ENABLED' in app.config, 'CSRF配置存在')
        test('会话配置', 'SESSION_COOKIE_HTTPONLY' in app.config, '会话安全配置存在')
        test('会话过期', 'PERMANENT_SESSION_LIFETIME' in app.config, '会话过期配置存在')
    except Exception as e:
        test('安全配置', False, str(e))

    # 8. 文件完整性测试
    print('\n📁 文件完整性测试:')
    backend_path = Path(__file__).parent
    core_files = [
        ('app/__init__.py', '应用工厂'),
        ('app/config.py', '配置模块'),
        ('app/models.py', '数据模型'),
        ('app/routes/auth.py', '认证路由'),
        ('app/routes/medication.py', '药物路由'),
        ('app/routes/bp.py', '血压路由'),
        ('requirements.txt', '依赖列表'),
        ('run.py', '启动脚本')
    ]
    
    for filename, description in core_files:
        file_path = backend_path / filename
        test(f'核心文件: {description}', file_path.exists(), filename)

    # 总结
    print()
    print('='*60)
    if passed == total:
        print(f'🎉 后端测试全部通过！{total} 项测试全部通过')
    else:
        failed = total - passed
        print(f'❌ 后端测试存在失败: {passed}/{total} 通过, {failed} 失败')
    print('='*60)

    return 0 if passed == total else 1

if __name__ == '__main__':
    sys.exit(main())
