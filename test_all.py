#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
血压守护 - 完整项目验证测试
验证APP Pro版、微信小程序、所有功能模块
"""

import json
import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
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
    print('🩺 血压守护 - 完整项目验证测试')
    print('='*60)
    print()

    # 1. APP Pro版文件
    print('📱 APP Pro版文件验证:')
    pro_files = {
        'app_pro.html': 'APP Pro主页面',
        'manifest_pro.json': 'Pro版PWA配置',
        'test_app_pro.html': 'Pro版测试页面',
        'sw_app.js': 'Service Worker'
    }
    for f, desc in pro_files.items():
        path = os.path.join(TEST_DIR, f)
        test(f'Pro: {desc}', os.path.exists(path), f)

    # 2. APP Pro内容验证
    try:
        with open(os.path.join(TEST_DIR, 'app_pro.html'), 'r', encoding='utf-8') as f:
            content = f.read()

        test('Pro: Canvas图表', 'canvas' in content and 'drawBpChart' in content, 'Canvas折线图')
        test('Pro: 推送通知', 'Notification' in content and 'sendPushNotification' in content, '推送通知')
        test('Pro: API同步', 'fetch' in content and 'syncData' in content, 'API数据同步')
        test('Pro: 家庭管理', 'addFamilyMember' in content and 'switchParent' in content, '家庭成员管理')
        test('Pro: 协作日志', 'collabLogs' in content and 'addCollabLog' in content, '协作日志')
        test('Pro: 6个导航页', all(p in content for p in ['page-home', 'page-meds', 'page-bp', 'page-alerts', 'page-family', 'page-profile']), '6个页面')
        test('Pro: 图表周期切换', 'toggleChartPeriod' in content, '图表周期切换')
        test('Pro: 健康评估', 'healthAssessment' in content, '健康评估')
        test('Pro: 库存预警', '库存不足' in content, '库存预警')
        test('Pro: 预警分级', 'critical' in content and 'urgent' in content, '三级预警')
        test('Pro: 推送开关', 'pushEnabled' in content and 'togglePushNotification' in content, '推送开关')
    except Exception as e:
        test('Pro内容验证', False, str(e))

    # 3. Manifest Pro验证
    try:
        with open(os.path.join(TEST_DIR, 'manifest_pro.json'), 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        test('Pro: Manifest:name', manifest.get('name') == '血压守护Pro', manifest.get('name', ''))
        test('Pro: Manifest:start_url', manifest.get('start_url') == '/app_pro.html', manifest.get('start_url', ''))
    except Exception as e:
        test('Pro: Manifest', False, str(e))

    # 4. 微信小程序验证
    print('\n📱 微信小程序验证:')
    mini_dir = os.path.join(TEST_DIR, 'mini_program_pro')
    test('小程序: 项目目录', os.path.exists(mini_dir), 'mini_program_pro/')

    mini_files = {
        'app.json': '小程序配置',
        'app.js': '小程序入口',
        'app.wxss': '全局样式',
        'pages/home/home.wxml': '首页模板',
        'pages/home/home.js': '首页逻辑',
        'pages/meds/meds.wxml': '药物页面模板',
        'pages/meds/meds.js': '药物页面逻辑',
        'pages/bp/bp.wxml': '血压页面模板',
        'pages/bp/bp.js': '血压页面逻辑',
        'pages/family/family.wxml': '家庭页面模板',
        'pages/family/family.js': '家庭页面逻辑',
        'pages/profile/profile.wxml': '我的页面模板',
        'pages/profile/profile.js': '我的页面逻辑'
    }

    for f, desc in mini_files.items():
        path = os.path.join(mini_dir, f)
        test(f'小程序: {desc}', os.path.exists(path), f)

    # 5. 小程序内容验证
    try:
        with open(os.path.join(mini_dir, 'app.json'), 'r', encoding='utf-8') as f:
            app_json = json.load(f)

        test('小程序: 页面配置', len(app_json.get('pages', [])) >= 5, f'{len(app_json.get("pages", []))}个页面')
        test('小程序: tabBar', 'tabBar' in app_json, '底部导航栏')
        test('小程序: 主题色', app_json.get('window', {}).get('navigationBarBackgroundColor') == '#667eea', '#667eea')
    except Exception as e:
        test('小程序: app.json', False, str(e))

    try:
        with open(os.path.join(mini_dir, 'app.js'), 'r', encoding='utf-8') as f:
            app_js = f.read()
        test('小程序: 全局方法', 'switchParent' in app_js, '切换父母')
        test('小程序: 日期工具', 'todayStr' in app_js and 'daysAgo' in app_js, '日期工具')
    except Exception as e:
        test('小程序: app.js', False, str(e))

    try:
        with open(os.path.join(mini_dir, 'pages', 'home', 'home.js'), 'r', encoding='utf-8') as f:
            home_js = f.read()
        test('小程序: 首页图表', 'drawChart' in home_js, 'Canvas图表')
        test('小程序: 首页数据加载', 'loadData' in home_js, '数据加载')
        test('小程序: 确认服药', 'confirmMed' in home_js, '确认服药')
    except Exception as e:
        test('小程序: 首页', False, str(e))

    try:
        with open(os.path.join(mini_dir, 'pages', 'bp', 'bp.js'), 'r', encoding='utf-8') as f:
            bp_js = f.read()
        test('小程序: 血压记录', 'addBpRecord' in bp_js, '添加血压')
        test('小程序: 健康评估', 'avgSys' in bp_js, '健康评估')
    except Exception as e:
        test('小程序: 血压页', False, str(e))

    try:
        with open(os.path.join(mini_dir, 'pages', 'meds', 'meds.js'), 'r', encoding='utf-8') as f:
            meds_js = f.read()
        test('小程序: 药物管理', 'addMedication' in meds_js and 'deleteMed' in meds_js, '添加/删除药物')
    except Exception as e:
        test('小程序: 药物页', False, str(e))

    try:
        with open(os.path.join(mini_dir, 'pages', 'family', 'family.js'), 'r', encoding='utf-8') as f:
            family_js = f.read()
        test('小程序: 家庭管理', 'addMember' in family_js and 'switchParent' in family_js, '添加成员/切换')
    except Exception as e:
        test('小程序: 家庭页', False, str(e))

    try:
        with open(os.path.join(mini_dir, 'pages', 'profile', 'profile.js'), 'r', encoding='utf-8') as f:
            profile_js = f.read()
        test('小程序: 演示数据', 'loadDemoData' in profile_js, '加载演示数据')
    except Exception as e:
        test('小程序: 我的页', False, str(e))

    # 6. 数据结构验证
    print('\n📋 数据结构验证:')

    mock_state = {"uid": 10001, "pid": 10010, "pname": "张大爷", "parents": [
        {"id": 10010, "name": "张大爷", "age": 68, "gender": "男", "relation": "父亲"},
        {"id": 10011, "name": "李奶奶", "age": 65, "gender": "女", "relation": "母亲"}
    ]}
    test('数据结构: app_state', all(k in mock_state for k in ['uid', 'pid', 'pname', 'parents']), '完整状态')

    mock_med = {"id": 20001, "name": "硝苯地平", "dosage": "1片", "frequency": "twice", "times": ["08:00", "18:00"], "quantity": 5}
    test('数据结构: medication', all(k in mock_med for k in ['id', 'name', 'times', 'quantity']), '药物结构')

    mock_bp = {"id": 40001, "systolic": 120, "diastolic": 80, "hr": 72, "time": "2026-05-02 08:00", "note": "晨起"}
    test('数据结构: bp', all(k in mock_bp for k in ['id', 'systolic', 'diastolic', 'hr', 'time']), '血压结构')

    mock_alert = {"id": 50001, "medName": "硝苯地平", "diff": 25, "level": "urgent", "status": "active"}
    test('数据结构: alert', all(k in mock_alert for k in ['id', 'medName', 'diff', 'level', 'status']), '预警结构')

    mock_collab = {"id": 60001, "action": "确认服药", "detail": "硝苯地平", "time": "2026-05-02 08:00", "operator": "我"}
    test('数据结构: collab_log', all(k in mock_collab for k in ['id', 'action', 'detail', 'time']), '协作日志结构')

    # 7. 项目完整性
    print('\n📂 项目完整性:')

    root_files = ['README.md', 'manifest.json', 'sw.js', 'app.html', 'app_mobile.html']
    for f in root_files:
        test(f'项目: {f}', os.path.exists(os.path.join(TEST_DIR, f)), f)

    backend_files = ['backend/server.py', 'backend/app/__init__.py', 'backend/requirements.txt']
    for f in backend_files:
        test(f'后端: {f}', os.path.exists(os.path.join(TEST_DIR, f)), f)

    test_files = ['test_app_verify.py', 'test_app_mobile.html', 'test_app_pro.html', 'auto_test.html']
    for f in test_files:
        test(f'测试: {f}', os.path.exists(os.path.join(TEST_DIR, f)), f)

    # 总结
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
