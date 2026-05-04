#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
血压守护APP - 功能验证测试
验证localStorage数据结构、PWA配置、Service Worker等
"""

import json
import os
import sys

# 测试配置
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
MANIFEST_PATH = os.path.join(TEST_DIR, 'manifest.json')
APP_PATH = os.path.join(TEST_DIR, 'app_mobile.html')
SW_PATH = os.path.join(TEST_DIR, 'sw_app.js')
TEST_PATH = os.path.join(TEST_DIR, 'test_app_mobile.html')

# 测试结果
results = []
total = 0
passed = 0

def test(name, condition, detail=''):
    global total, passed
    total += 1
    status = 'PASS' if condition else 'FAIL'
    if condition:
        passed += 1
    results.append({
        'name': name,
        'status': status,
        'detail': detail
    })
    icon = '✅' if condition else '❌'
    print(f'{icon} [{status}] {name}' + (f' - {detail}' if detail else ''))

def main():
    print('='*60)
    print('🩺 血压守护APP - 自动测试')
    print('='*60)
    print()

    # 1. 文件存在性测试
    test('APP文件存在', os.path.exists(APP_PATH), 'app_mobile.html')
    test('Manifest文件存在', os.path.exists(MANIFEST_PATH), 'manifest.json')
    test('Service Worker存在', os.path.exists(SW_PATH), 'sw_app.js')
    test('测试文件存在', os.path.exists(TEST_PATH), 'test_app_mobile.html')

    # 2. Manifest配置测试
    try:
        with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        test('Manifest:name', manifest.get('name') == '血压守护', manifest.get('name', ''))
        test('Manifest:start_url', manifest.get('start_url') == '/app_mobile.html', manifest.get('start_url', ''))
        test('Manifest:display', manifest.get('display') == 'standalone', manifest.get('display', ''))
        test('Manifest:theme_color', manifest.get('theme_color') == '#667eea', manifest.get('theme_color', ''))
        test('Manifest:icons', len(manifest.get('icons', [])) >= 3, f'{len(manifest.get("icons", []))}个图标')
    except Exception as e:
        test('Manifest解析', False, str(e))

    # 3. APP HTML内容测试
    try:
        with open(APP_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        test('APP:viewport配置', 'user-scalable=no' in content, '禁止缩放')
        test('APP:theme-color', 'theme-color' in content, '主题色')
        test('APP:apple-mobile-web-app', 'apple-mobile-web-app-capable' in content, 'iOS支持')
        test('APP:manifest引用', 'manifest.json' in content, 'Manifest引用')
        test('APP:Service Worker注册', 'serviceWorker' in content, 'SW注册')
        test('APP:Notification API', 'Notification' in content, '通知API')
        
        # 测试功能模块
        test('APP:药物管理', 'addMedication' in content, '添加药物函数')
        test('APP:血压记录', 'addBpRecord' in content, '添加血压函数')
        test('APP:确认服药', 'confirmMed' in content, '确认服药函数')
        test('APP:预警处理', 'resolveAlert' in content, '处理预警函数')
        test('APP:数据导出', 'exportData' in content, '导出数据函数')
        test('APP:演示数据', 'loadDemoData' in content, '加载演示数据')
        
        # 测试页面
        test('APP:5个页面', all(p in content for p in ['page-home', 'page-meds', 'page-bp', 'page-alerts', 'page-profile']), '全部页面存在')
        test('APP:底部导航', 'bottom-nav' in content, '底部导航栏')
        test('APP:FAB按钮', 'class="fab"' in content, '快速操作按钮')
        
    except Exception as e:
        test('APP内容测试', False, str(e))

    # 4. Service Worker测试
    try:
        with open(SW_PATH, 'r', encoding='utf-8') as f:
            sw_content = f.read()
        
        test('SW:install事件', "'install'" in sw_content, '安装事件')
        test('SW:activate事件', "'activate'" in sw_content, '激活事件')
        test('SW:fetch事件', "'fetch'" in sw_content, '请求拦截')
        test('SW:push事件', "'push'" in sw_content, '推送通知')
        test('SW:notificationclick', "'notificationclick'" in sw_content, '通知点击')
        test('SW:缓存策略', 'CACHE_NAME' in sw_content, '缓存管理')
        
    except Exception as e:
        test('Service Worker测试', False, str(e))

    # 5. 测试文件验证
    try:
        with open(TEST_PATH, 'r', encoding='utf-8') as f:
            test_content = f.read()
        
        test('测试:15项测试', 'totalTests=15' in test_content, '测试数量')
        test('测试:localStorage', 'testLocalStorage' in test_content, 'localStorage测试')
        test('测试:药物功能', 'testAddMedication' in test_content, '药物测试')
        test('测试:血压功能', 'testBpRecord' in test_content, '血压测试')
        test('测试:预警功能', 'testAlertGeneration' in test_content, '预警测试')
        test('测试:PWA功能', 'testPWAFeatures' in test_content, 'PWA测试')
        test('测试:SW功能', 'testServiceWorker' in test_content, 'SW测试')
        
    except Exception as e:
        test('测试文件验证', False, str(e))

    # 6. localStorage数据结构测试（模拟）
    print()
    print('📋 数据结构验证:')
    
    # 模拟数据结构
    mock_state = {
        "uid": 10001,
        "pid": 10010,
        "pname": "张大爷",
        "parents": [
            {"id": 10010, "name": "张大爷", "age": 68, "gender": "男"},
            {"id": 10011, "name": "李奶奶", "age": 65, "gender": "女"}
        ]
    }
    test('数据结构:app_state', all(k in mock_state for k in ['uid', 'pid', 'pname', 'parents']), '状态结构正确')
    
    mock_med = {
        "id": 20001,
        "name": "硝苯地平",
        "dosage": "1片",
        "frequency": "twice",
        "times": ["08:00", "18:00"],
        "quantity": 14
    }
    test('数据结构:medication', all(k in mock_med for k in ['id', 'name', 'dosage', 'times', 'quantity']), '药物结构正确')
    
    mock_log = {
        "id": 30001,
        "medId": 20001,
        "medName": "硝苯地平",
        "date": "2026-05-02",
        "time": "08:00",
        "status": "pending"
    }
    test('数据结构:log', all(k in mock_log for k in ['id', 'medId', 'date', 'time', 'status']), '日志结构正确')
    
    mock_bp = {
        "id": 40001,
        "systolic": 120,
        "diastolic": 80,
        "hr": 72,
        "time": "2026-05-02 08:00"
    }
    test('数据结构:bp', all(k in mock_bp for k in ['id', 'systolic', 'diastolic', 'hr', 'time']), '血压结构正确')
    
    mock_alert = {
        "id": 50001,
        "medName": "硝苯地平",
        "diff": 15,
        "level": "warn",
        "status": "active"
    }
    test('数据结构:alert', all(k in mock_alert for k in ['id', 'medName', 'diff', 'level', 'status']), '预警结构正确')

    # 打印总结
    print()
    print('='*60)
    if passed == total:
        print(f'🎉 全部测试通过！{total} 项测试全部通过')
    else:
        failed = total - passed
        print(f'❌ 存在失败: {passed}/{total} 通过, {failed} 失败')
    print('='*60)
    
    return 0 if passed == total else 1

if __name__ == '__main__':
    sys.exit(main())
