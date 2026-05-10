#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
血压守护 - 药物数量管理功能测试
"""

import sys
import json
import ast
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app import create_app

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
    print('💊 血压守护 - 药物数量管理功能测试')
    print('='*60)
    print()
    
    backend_path = Path(__file__).parent
    
    # 1. 代码完整性测试
    print('📁 药物管理文件完整性:')
    med_route = backend_path / 'app' / 'routes' / 'medication.py'
    
    if med_route.exists():
        with open(med_route, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 测试语法
        try:
            ast.parse(content)
            test('语法检查', True, '语法正确')
        except SyntaxError as e:
            test('语法检查', False, f'第{e.lineno}行: {e.msg}')
            return 1
        
        # 测试功能函数
        test('添加药物API', 'def add_medication' in content, '添加药物功能存在')
        test('药物列表API', 'def list_medications' in content, '药物列表功能存在')
        test('数量调整API', 'def adjust_quantity' in content, '数量调整功能存在')
        test('购买补充API', 'def replenish_quantity' in content, '购买补充功能存在')
        test('库存历史API', 'def get_quantity_history' in content, '库存历史功能存在')
        test('库存预警API', 'def get_quantity_warning' in content, '库存预警功能存在')
        test('调整类型支持', 'increase' in content and 'decrease' in content and 'set' in content, '支持增加/减少/设置三种调整')
        test('库存日志记录', 'inventory_logs' in content, '库存变动日志记录存在')
    else:
        test('药物管理文件', False, '文件不存在')
        return 1
    
    # 2. 运行时功能测试
    print('\n⚙️ 运行时功能测试:')
    
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        # 2.1 添加药物
        print('\n📦 添加药物测试:')
        resp = client.post('/api/medication/add',
            json={'name': '氨氯地平', 'dose': '5mg', 'frequency': '每日一次', 'quantity': 30, 'member_id': 1},
            content_type='application/json')
        data = json.loads(resp.data)
        test('添加药物', resp.status_code == 200 and data.get('success'), data.get('message'))
        med_id = data.get('data', {}).get('med_id')
        
        # 2.2 添加第二种药物
        resp = client.post('/api/medication/add',
            json={'name': '美托洛尔', 'dose': '25mg', 'frequency': '每日两次', 'quantity': 50, 'member_id': 1},
            content_type='application/json')
        data = json.loads(resp.data)
        test('添加第二种药物', resp.status_code == 200 and data.get('success'), data.get('message'))
        med_id2 = data.get('data', {}).get('med_id')
        
        # 2.3 获取药物列表
        print('\n📋 药物列表测试:')
        resp = client.get('/api/medication/list?member_id=1')
        data = json.loads(resp.data)
        test('获取药物列表', resp.status_code == 200 and data.get('success'), f'药物数量: {data.get("data", {}).get("total")}')
        
        # 2.4 数量调整 - 减少
        print('\n📉 数量调整测试:')
        resp = client.post('/api/medication/quantity/adjust',
            json={'med_id': med_id, 'adjust_type': 'decrease', 'quantity': 3, 'reason': '掉地上'},
            content_type='application/json')
        data = json.loads(resp.data)
        test('减少数量(掉地上)', resp.status_code == 200 and data.get('success'), f'新数量: {data.get("data", {}).get("medication", {}).get("quantity")}')
        
        # 2.5 数量调整 - 增加
        resp = client.post('/api/medication/quantity/adjust',
            json={'med_id': med_id, 'adjust_type': 'increase', 'quantity': 10, 'reason': '重新购买'},
            content_type='application/json')
        data = json.loads(resp.data)
        test('增加数量(重新购买)', resp.status_code == 200 and data.get('success'), f'新数量: {data.get("data", {}).get("medication", {}).get("quantity")}')
        
        # 2.6 数量调整 - 设置
        resp = client.post('/api/medication/quantity/adjust',
            json={'med_id': med_id, 'adjust_type': 'set', 'quantity': 20, 'reason': '盘点调整'},
            content_type='application/json')
        data = json.loads(resp.data)
        test('设置数量(盘点)', resp.status_code == 200 and data.get('success'), f'新数量: {data.get("data", {}).get("medication", {}).get("quantity")}')
        
        # 2.7 购买补充
        print('\n🛒 购买补充测试:')
        resp = client.post('/api/medication/quantity/replenish',
            json={'med_id': med_id, 'purchase_quantity': 30, 'purchase_source': '药店'},
            content_type='application/json')
        data = json.loads(resp.data)
        test('购买补充', resp.status_code == 200 and data.get('success'), f'新数量: {data.get("data", {}).get("medication", {}).get("quantity")}')
        
        # 2.8 库存历史
        print('\n📜 库存历史测试:')
        resp = client.get('/api/medication/quantity/history')
        data = json.loads(resp.data)
        test('获取库存历史', resp.status_code == 200 and data.get('success'), f'历史记录数: {data.get("data", {}).get("total")}')
        
        # 2.9 库存预警
        print('\n⚠️ 库存预警测试:')
        resp = client.get('/api/medication/quantity/warning?threshold=50')
        data = json.loads(resp.data)
        test('获取库存预警', resp.status_code == 200 and data.get('success'), f'预警药物数: {data.get("data", {}).get("total_warnings")}')
        
        # 2.10 新增药物品类
        print('\n💊 新增药物品类测试:')
        resp = client.post('/api/medication/add',
            json={'name': '硝苯地平', 'dose': '10mg', 'frequency': '每日三次', 'quantity': 60, 'member_id': 1},
            content_type='application/json')
        data = json.loads(resp.data)
        test('新增药物品类', resp.status_code == 200 and data.get('success'), data.get('message'))
        
        # 2.11 错误处理
        print('\n🚫 错误处理测试:')
        resp = client.post('/api/medication/add',
            json={'dose': '5mg'},
            content_type='application/json')
        test('缺少参数校验', resp.status_code == 400, '返回400错误')
        
        resp = client.post('/api/medication/quantity/adjust',
            json={'med_id': 'nonexistent', 'adjust_type': 'increase', 'quantity': 10},
            content_type='application/json')
        test('药物不存在校验', resp.status_code == 404, '返回404错误')
        
        resp = client.post('/api/medication/quantity/adjust',
            json={'med_id': med_id, 'adjust_type': 'decrease', 'quantity': 9999, 'reason': '测试不足'},
            content_type='application/json')
        test('库存不足校验', resp.status_code == 400, '返回库存不足错误')
    
    # 总结
    print()
    print('='*60)
    failed = total - passed
    if failed == 0:
        print(f'🎉 药物数量管理测试全部通过！{total} 项测试全部通过')
    else:
        print(f'❌ 测试存在失败: {passed}/{total} 通过, {failed} 失败')
    print('='*60)
    
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
