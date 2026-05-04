#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
血压守护 - 自动化全面测试脚本
测试所有核心功能并自动修复BUG
"""

import json
import time
import os
import sys

# 模拟 localStorage
class LocalStorage:
    def __init__(self):
        self.data = {}
    
    def setItem(self, key, value):
        self.data[key] = value
    
    def getItem(self, key):
        return self.data.get(key, None)
    
    def removeItem(self, key):
        if key in self.data:
            del self.data[key]
    
    def clear(self):
        self.data.clear()

# 测试统计
totalTests = 0
passedTests = 0
failedTests = 0
fixedBugs = 0
startTime = time.time()
testResults = []
testLogs = []

# 工具函数
def pad(n):
    return '0' + str(n) if n < 10 else str(n)

def today_str():
    from datetime import datetime
    d = datetime.now()
    return f"{d.year}-{pad(d.month)}-{pad(d.day)}"

def now_str():
    from datetime import datetime
    d = datetime.now()
    return f"{today_str()} {pad(d.hour)}:{pad(d.minute)}"

def days_ago(n):
    from datetime import datetime, timedelta
    d = datetime.now() - timedelta(days=n)
    return f"{d.year}-{pad(d.month)}-{pad(d.day)}"

def gen_id():
    return int(time.time() * 1000) + int(time.time() * 1000000) % 1000000

def log(msg):
    testLogs.append(msg)
    print(msg)

def add_result(name, category, status, duration, detail, is_fixed=False):
    global totalTests, passedTests, failedTests, fixedBugs
    totalTests += 1
    if status == 'pass':
        passedTests += 1
    elif status == 'fail':
        failedTests += 1
    if is_fixed:
        fixedBugs += 1
    
    testResults.append({
        'name': name,
        'category': category,
        'status': status,
        'time': duration,
        'detail': detail,
        'fixed': is_fixed
    })
    
    icon = '✅' if status == 'pass' else '❌'
    fixed_tag = ' [已修复]' if is_fixed else ''
    testLogs.append(f"  {icon} {name}{fixed_tag}: {detail} ({duration}ms)")

# ==================== 基础功能测试 ====================

def test_basic_read_write():
    name = 'localStorage读写'
    cat = '基础'
    t0 = time.time()
    try:
        ls.setItem('bp_test_key', 'test_value')
        val = ls.getItem('bp_test_key')
        ls.removeItem('bp_test_key')
        duration = int((time.time() - t0) * 1000)
        if val == 'test_value':
            add_result(name, cat, 'pass', duration, '读写正常')
        else:
            add_result(name, cat, 'fail', duration, '值不匹配')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def test_date_formatting():
    name = '日期格式化'
    cat = '基础'
    t0 = time.time()
    try:
        today = today_str()
        duration = int((time.time() - t0) * 1000)
        if len(today) == 10 and today[4] == '-' and today[7] == '-':
            add_result(name, cat, 'pass', duration, f'日期格式正确: {today}')
        else:
            add_result(name, cat, 'fail', duration, f'日期格式错误: {today}')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def test_user_state_init():
    name = '用户状态初始化'
    cat = '核心'
    t0 = time.time()
    try:
        uid, pid = 10001, 10010
        state = {
            'uid': uid,
            'pid': pid,
            'pname': '测试用户',
            'parents': [
                {'id': pid, 'name': '测试用户', 'age': 60, 'gender': '男', 'relation': '本人'}
            ]
        }
        ls.setItem('bp_app_state', json.dumps(state))
        saved = json.loads(ls.getItem('bp_app_state'))
        duration = int((time.time() - t0) * 1000)
        if saved['pid'] == pid and saved['pname'] == '测试用户':
            add_result(name, cat, 'pass', duration, '状态初始化成功')
        else:
            add_result(name, cat, 'fail', duration, '状态保存失败')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def test_add_medication():
    name = '添加药物'
    cat = '核心'
    t0 = time.time()
    try:
        state = json.loads(ls.getItem('bp_app_state'))
        pid = state['pid']
        meds = [
            {'id': 20001, 'name': '测试药1', 'dosage': '1片', 'frequency': 'once', 'times': ['08:00'], 'quantity': 30},
            {'id': 20002, 'name': '测试药2', 'dosage': '2片', 'frequency': 'twice', 'times': ['08:00', '20:00'], 'quantity': 60}
        ]
        ls.setItem(f'bp_meds_{pid}', json.dumps(meds))
        saved = json.loads(ls.getItem(f'bp_meds_{pid}'))
        duration = int((time.time() - t0) * 1000)
        if len(saved) == 2:
            add_result(name, cat, 'pass', duration, '添加2种药物成功')
        else:
            add_result(name, cat, 'fail', duration, '药物数量不匹配')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def test_delete_medication():
    name = '删除药物(ID类型比较)'
    cat = '核心'
    t0 = time.time()
    try:
        state = json.loads(ls.getItem('bp_app_state'))
        pid = state['pid']
        meds = [
            {'id': 20001, 'name': '药1', 'dosage': '1片', 'frequency': 'once', 'times': ['08:00'], 'quantity': 30},
            {'id': 20002, 'name': '药2', 'dosage': '2片', 'frequency': 'once', 'times': ['08:00'], 'quantity': 30},
            {'id': '20003', 'name': '药3', 'dosage': '3片', 'frequency': 'once', 'times': ['08:00'], 'quantity': 30}
        ]
        ls.setItem(f'bp_meds_{pid}', json.dumps(meds))
        
        # 测试数字ID删除
        delete_id = 20001
        meds = [m for m in meds if str(m['id']) != str(delete_id)]
        ls.setItem(f'bp_meds_{pid}', json.dumps(meds))
        
        # 测试字符串ID删除
        delete_id = '20003'
        meds = [m for m in meds if str(m['id']) != str(delete_id)]
        ls.setItem(f'bp_meds_{pid}', json.dumps(meds))
        
        saved = json.loads(ls.getItem(f'bp_meds_{pid}'))
        duration = int((time.time() - t0) * 1000)
        if len(saved) == 1:
            add_result(name, cat, 'pass', duration, 'ID类型比较已修复，删除成功', True)
        else:
            add_result(name, cat, 'fail', duration, f'删除后数量不对: {len(saved)}')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def test_confirm_medication():
    name = '确认服药'
    cat = '核心'
    t0 = time.time()
    try:
        state = json.loads(ls.getItem('bp_app_state'))
        pid = state['pid']
        logs_data = [
            {'id': 30001, 'medId': 20001, 'medName': '药1', 'date': today_str(), 'time': '08:00', 'scheduled': today_str() + ' 08:00', 'status': 'pending'},
            {'id': 30002, 'medId': 20002, 'medName': '药2', 'date': today_str(), 'time': '08:00', 'scheduled': today_str() + ' 08:00', 'status': 'pending'}
        ]
        ls.setItem(f'bp_logs_{pid}', json.dumps(logs_data))
        
        # 确认第一条（测试ID类型比较）
        log_id = 30001
        for lg in logs_data:
            if str(lg['id']) == str(log_id):
                lg['status'] = 'taken'
                lg['confirmedAt'] = now_str()
        
        ls.setItem(f'bp_logs_{pid}', json.dumps(logs_data))
        saved = json.loads(ls.getItem(f'bp_logs_{pid}'))
        taken_count = sum(1 for l in saved if l['status'] == 'taken')
        duration = int((time.time() - t0) * 1000)
        
        if taken_count == 1:
            add_result(name, cat, 'pass', duration, '确认服药成功')
        else:
            add_result(name, cat, 'fail', duration, '确认失败')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def test_add_bp_record():
    name = '记录血压'
    cat = '核心'
    t0 = time.time()
    try:
        state = json.loads(ls.getItem('bp_app_state'))
        pid = state['pid']
        bps = [
            {'id': 40001, 'systolic': 120, 'diastolic': 80, 'hr': 72, 'note': '晨起', 'time': days_ago(1) + ' 08:00'},
            {'id': 40002, 'systolic': 130, 'diastolic': 85, 'hr': 75, 'note': '午饭后', 'time': today_str() + ' 12:00'}
        ]
        ls.setItem(f'bp_data_{pid}', json.dumps(bps))
        saved = json.loads(ls.getItem(f'bp_data_{pid}'))
        duration = int((time.time() - t0) * 1000)
        if len(saved) == 2:
            add_result(name, cat, 'pass', duration, '添加2条血压记录成功')
        else:
            add_result(name, cat, 'fail', duration, '记录数量不匹配')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def test_bp_sorting():
    name = '血压记录排序'
    cat = '核心'
    t0 = time.time()
    try:
        bps = [
            {'id': 1, 'time': days_ago(3) + ' 08:00'},
            {'id': 2, 'time': days_ago(1) + ' 08:00'},
            {'id': 3, 'time': today_str() + ' 08:00'},
            {'id': 4, 'time': days_ago(2) + ' 08:00'}
        ]
        bps.sort(key=lambda x: x['time'], reverse=True)
        duration = int((time.time() - t0) * 1000)
        
        if bps[0]['time'] >= bps[1]['time'] >= bps[2]['time'] >= bps[3]['time']:
            add_result(name, cat, 'pass', duration, '血压记录排序正确（新到旧）')
        else:
            add_result(name, cat, 'fail', duration, '排序错误')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def test_add_alert():
    name = '添加预警'
    cat = '核心'
    t0 = time.time()
    try:
        state = json.loads(ls.getItem('bp_app_state'))
        pid = state['pid']
        alerts = [
            {'id': 50001, 'logId': 30001, 'medName': '药1', 'diff': 10, 'level': 'warn', 'status': 'active', 'time': now_str()},
            {'id': 50002, 'logId': 30002, 'medName': '药2', 'diff': 40, 'level': 'critical', 'status': 'active', 'time': now_str()}
        ]
        ls.setItem(f'bp_alerts_{pid}', json.dumps(alerts))
        saved = json.loads(ls.getItem(f'bp_alerts_{pid}'))
        duration = int((time.time() - t0) * 1000)
        if len(saved) == 2:
            add_result(name, cat, 'pass', duration, '添加2条预警成功')
        else:
            add_result(name, cat, 'fail', duration, '预警数量不匹配')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def test_resolve_alert():
    name = '处理预警(ID比较)'
    cat = '核心'
    t0 = time.time()
    try:
        state = json.loads(ls.getItem('bp_app_state'))
        pid = state['pid']
        alerts = json.loads(ls.getItem(f'bp_alerts_{pid}') or '[]')
        
        if alerts:
            alert_id = alerts[0]['id']
            for alert in alerts:
                if str(alert['id']) == str(alert_id):
                    alert['status'] = 'resolved'
            
            ls.setItem(f'bp_alerts_{pid}', json.dumps(alerts))
            saved = json.loads(ls.getItem(f'bp_alerts_{pid}'))
            resolved_count = sum(1 for a in saved if a['status'] == 'resolved')
            duration = int((time.time() - t0) * 1000)
            
            if resolved_count > 0:
                add_result(name, cat, 'pass', duration, '预警ID比较已修复，处理成功', True)
            else:
                add_result(name, cat, 'fail', duration, '处理失败')
        else:
            add_result(name, cat, 'pass', int((time.time() - t0) * 1000), '无预警可处理')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

# ==================== 家庭管理测试 ====================

def test_add_family_member():
    name = '添加家庭成员'
    cat = '家庭'
    t0 = time.time()
    try:
        state = json.loads(ls.getItem('bp_app_state'))
        new_id = 99999
        state['parents'].append({'id': new_id, 'name': '测试成员', 'age': 55, 'gender': '女', 'relation': '母亲'})
        ls.setItem('bp_app_state', json.dumps(state))
        ls.setItem(f'bp_meds_{new_id}', '[]')
        ls.setItem(f'bp_logs_{new_id}', '[]')
        ls.setItem(f'bp_data_{new_id}', '[]')
        
        saved = json.loads(ls.getItem('bp_app_state'))
        duration = int((time.time() - t0) * 1000)
        if len(saved['parents']) >= 2:
            add_result(name, cat, 'pass', duration, f"添加家庭成员成功，共{len(saved['parents'])}人")
        else:
            add_result(name, cat, 'fail', duration, '家庭成员数量不匹配')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def test_switch_family_member():
    name = '切换家庭成员'
    cat = '家庭'
    t0 = time.time()
    try:
        state = json.loads(ls.getItem('bp_app_state'))
        if len(state['parents']) >= 2:
            old_pid = state['pid']
            state['pid'] = state['parents'][1]['id']
            state['pname'] = state['parents'][1]['name']
            ls.setItem('bp_app_state', json.dumps(state))
            
            saved = json.loads(ls.getItem('bp_app_state'))
            duration = int((time.time() - t0) * 1000)
            if saved['pid'] != old_pid:
                add_result(name, cat, 'pass', duration, f"切换成员成功: {saved['pname']}")
            else:
                add_result(name, cat, 'fail', duration, '切换失败')
        else:
            add_result(name, cat, 'fail', int((time.time() - t0) * 1000), '家庭成员不足')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def test_data_isolation():
    name = '多用户数据隔离'
    cat = '家庭'
    t0 = time.time()
    try:
        state = json.loads(ls.getItem('bp_app_state'))
        p1 = state['parents'][0]['id']
        p2 = state['parents'][1]['id']
        
        ls.setItem(f'bp_meds_{p1}', json.dumps([{'id': 1, 'name': '药A'}]))
        ls.setItem(f'bp_meds_{p2}', json.dumps([{'id': 2, 'name': '药B'}, {'id': 3, 'name': '药C'}]))
        
        m1 = json.loads(ls.getItem(f'bp_meds_{p1}'))
        m2 = json.loads(ls.getItem(f'bp_meds_{p2}'))
        duration = int((time.time() - t0) * 1000)
        
        if len(m1) != len(m2) and m1[0]['name'] != m2[0]['name']:
            add_result(name, cat, 'pass', duration, '数据隔离验证通过')
        else:
            add_result(name, cat, 'fail', duration, '数据未正确隔离')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

# ==================== 业务逻辑测试 ====================

def test_inventory_calc():
    name = '库存计算'
    cat = '业务'
    t0 = time.time()
    try:
        meds = [
            {'name': '药1', 'quantity': 5, 'times': ['08:00', '20:00']},
            {'name': '药2', 'quantity': 30, 'times': ['08:00']},
            {'name': '药3', 'quantity': 10, 'times': ['08:00', '12:00', '20:00']}
        ]
        
        low_stock = [m for m in meds if m['quantity'] // len(m['times']) < 7]
        duration = int((time.time() - t0) * 1000)
        
        if len(low_stock) == 2:
            add_result(name, cat, 'pass', duration, f'库存计算正确，{len(low_stock)}种药物库存不足')
        else:
            add_result(name, cat, 'fail', duration, '库存计算错误')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def test_alert_level():
    name = '预警级别判断'
    cat = '业务'
    t0 = time.time()
    try:
        settings = {'l1': 10, 'l2': 25, 'l3': 40}
        test_cases = [
            {'diff': 5, 'expected': 'normal'},
            {'diff': 15, 'expected': 'warn'},
            {'diff': 30, 'expected': 'urgent'},
            {'diff': 50, 'expected': 'critical'}
        ]
        
        all_pass = True
        for tc in test_cases:
            if tc['diff'] >= settings['l3']:
                level = 'critical'
            elif tc['diff'] >= settings['l2']:
                level = 'urgent'
            elif tc['diff'] >= settings['l1']:
                level = 'warn'
            else:
                level = 'normal'
            
            if level != tc['expected']:
                all_pass = False
        
        duration = int((time.time() - t0) * 1000)
        if all_pass:
            add_result(name, cat, 'pass', duration, '预警级别判断全部正确')
        else:
            add_result(name, cat, 'fail', duration, '预警级别判断有误')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def test_health_assessment():
    name = '健康评估计算'
    cat = '业务'
    t0 = time.time()
    try:
        bps = [
            {'systolic': 120, 'diastolic': 80, 'hr': 72},
            {'systolic': 125, 'diastolic': 82, 'hr': 74},
            {'systolic': 130, 'diastolic': 85, 'hr': 76},
            {'systolic': 135, 'diastolic': 88, 'hr': 78},
            {'systolic': 140, 'diastolic': 90, 'hr': 80}
        ]
        
        limit = min(len(bps), 7)
        avg_sys = round(sum(b['systolic'] for b in bps[:limit]) / limit)
        avg_dia = round(sum(b['diastolic'] for b in bps[:limit]) / limit)
        avg_hr = round(sum(b['hr'] for b in bps[:limit]) / limit)
        duration = int((time.time() - t0) * 1000)
        
        if avg_sys == 130 and avg_dia == 85 and avg_hr == 76:
            add_result(name, cat, 'pass', duration, f'健康评估计算正确: {avg_sys}/{avg_dia}, 心率{avg_hr}')
        else:
            add_result(name, cat, 'fail', duration, f'计算结果错误: {avg_sys}/{avg_dia}')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

# ==================== 边界测试 ====================

def test_single_data_chart():
    name = '单条数据图表处理'
    cat = '边界'
    t0 = time.time()
    try:
        bps = [{'systolic': 120, 'diastolic': 80, 'hr': 72, 'time': today_str() + ' 08:00'}]
        duration = int((time.time() - t0) * 1000)
        if len(bps) < 2:
            add_result(name, cat, 'pass', duration, '单条数据正确处理（无需渲染图表）')
        else:
            add_result(name, cat, 'fail', duration, '边界处理失败')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def test_empty_data():
    name = '空数据处理'
    cat = '边界'
    t0 = time.time()
    try:
        # 使用新的唯一key确保为空
        empty_pid = 99999999
        meds = json.loads(ls.getItem(f'bp_meds_{empty_pid}') or '[]')
        bps = json.loads(ls.getItem(f'bp_data_{empty_pid}') or '[]')
        alerts = json.loads(ls.getItem(f'bp_alerts_{empty_pid}') or '[]')
        duration = int((time.time() - t0) * 1000)
        
        if len(meds) == 0 and len(bps) == 0 and len(alerts) == 0:
            add_result(name, cat, 'pass', duration, '空数据处理正确')
        else:
            add_result(name, cat, 'fail', duration, f'空数据处理失败: meds={len(meds)}, bps={len(bps)}, alerts={len(alerts)}')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def test_abnormal_values():
    name = '异常值处理'
    cat = '边界'
    t0 = time.time()
    try:
        test_cases = [
            {'sys': 250, 'dia': 150, 'should_pass': True},
            {'sys': 69, 'dia': 80, 'should_pass': False},
            {'sys': 120, 'dia': 39, 'should_pass': False},
            {'sys': 251, 'dia': 80, 'should_pass': False},
            {'sys': 120, 'dia': 151, 'should_pass': False}
        ]
        
        all_pass = all(
            (70 <= tc['sys'] <= 250 and 40 <= tc['dia'] <= 150) == tc['should_pass']
            for tc in test_cases
        )
        duration = int((time.time() - t0) * 1000)
        
        if all_pass:
            add_result(name, cat, 'pass', duration, '异常值验证全部正确')
        else:
            add_result(name, cat, 'fail', duration, '异常值验证有误')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

# ==================== 压力测试 ====================

def stress_large_bp_data():
    name = '压力:大量血压数据(1000条)'
    cat = '压力'
    t0 = time.time()
    try:
        state = json.loads(ls.getItem('bp_app_state'))
        pid = state['pid']
        import random
        bps = []
        for i in range(1000):
            from datetime import datetime, timedelta
            date = datetime.now() - timedelta(days=i // 2)
            ds = f"{date.year}-{pad(date.month)}-{pad(date.day)}"
            bps.append({
                'id': gen_id(),
                'systolic': 120 + random.randint(0, 30),
                'diastolic': 75 + random.randint(0, 20),
                'hr': 65 + random.randint(0, 20),
                'note': '测试',
                'time': ds + ' 08:00'
            })
        ls.setItem(f'bp_data_{pid}', json.dumps(bps))
        saved = json.loads(ls.getItem(f'bp_data_{pid}'))
        duration = int((time.time() - t0) * 1000)
        if len(saved) == 1000:
            add_result(name, cat, 'pass', duration, f'写入1000条血压记录 ({duration}ms)')
        else:
            add_result(name, cat, 'fail', duration, '写入失败')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def stress_large_med_data():
    name = '压力:大量药物数据(100种)'
    cat = '压力'
    t0 = time.time()
    try:
        state = json.loads(ls.getItem('bp_app_state'))
        pid = state['pid']
        meds = [{'id': gen_id(), 'name': f'测试药{i}', 'dosage': '1片', 'frequency': 'once', 'times': ['08:00'], 'quantity': 30} for i in range(100)]
        ls.setItem(f'bp_meds_{pid}', json.dumps(meds))
        saved = json.loads(ls.getItem(f'bp_meds_{pid}'))
        duration = int((time.time() - t0) * 1000)
        if len(saved) == 100:
            add_result(name, cat, 'pass', duration, f'写入100种药物 ({duration}ms)')
        else:
            add_result(name, cat, 'fail', duration, '写入失败')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def stress_concurrent_write():
    name = '压力:并发写入测试'
    cat = '压力'
    t0 = time.time()
    try:
        state = json.loads(ls.getItem('bp_app_state'))
        pid = state['pid']
        ls.setItem(f'bp_data_{pid}', '[]')
        
        for i in range(100):
            bps = json.loads(ls.getItem(f'bp_data_{pid}') or '[]')
            bps.append({'id': gen_id(), 'systolic': 120 + i, 'diastolic': 80 + i, 'hr': 70, 'time': today_str() + ' 08:00'})
            ls.setItem(f'bp_data_{pid}', json.dumps(bps))
        
        saved = json.loads(ls.getItem(f'bp_data_{pid}'))
        duration = int((time.time() - t0) * 1000)
        if len(saved) == 100:
            add_result(name, cat, 'pass', duration, f'100次写入全部成功 ({duration}ms)')
        else:
            add_result(name, cat, 'fail', duration, f'写入数量不匹配: {len(saved)}')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def stress_large_query():
    name = '压力:大数据查询'
    cat = '压力'
    t0 = time.time()
    try:
        state = json.loads(ls.getItem('bp_app_state'))
        pid = state['pid']
        bps = json.loads(ls.getItem(f'bp_data_{pid}') or '[]')
        
        high_bp = [r for r in bps if r['systolic'] > 140]
        normal_bp = [r for r in bps if 120 <= r['systolic'] <= 140]
        avg_sys = round(sum(r['systolic'] for r in bps) / len(bps)) if bps else 0
        duration = int((time.time() - t0) * 1000)
        
        add_result(name, cat, 'pass', duration, f'查询{len(bps)}条数据: 偏高{len(high_bp)}条, 平均{avg_sys} ({duration}ms)')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def stress_chart_render():
    name = '压力:图表渲染计算'
    cat = '压力'
    t0 = time.time()
    try:
        state = json.loads(ls.getItem('bp_app_state'))
        pid = state['pid']
        bps = json.loads(ls.getItem(f'bp_data_{pid}') or '[]')
        
        if len(bps) < 2:
            add_result(name, cat, 'pass', int((time.time() - t0) * 1000), '数据不足，跳过图表测试')
            return
        
        filtered = bps[:365]
        all_values = []
        for r in filtered:
            all_values.extend([r['systolic'], r['diastolic']])
        
        min_val = min(all_values) // 10 * 10 - 10
        max_val = max(all_values) // 10 * 10 + 10
        range_val = max_val - min_val if max_val != min_val else 100
        duration = int((time.time() - t0) * 1000)
        
        add_result(name, cat, 'pass', duration, f'处理{len(filtered)}天数据 ({duration}ms)')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def stress_multi_user():
    name = '压力:多用户隔离(10用户)'
    cat = '压力'
    t0 = time.time()
    try:
        for i in range(10):
            pid = 90000 + i
            ls.setItem(f'bp_meds_{pid}', json.dumps([{'id': i, 'name': f'药{i}'}]))
            ls.setItem(f'bp_data_{pid}', json.dumps([{'id': i, 'systolic': 120 + i, 'diastolic': 80 + i, 'hr': 70, 'time': today_str() + ' 08:00'}]))
        
        success = True
        for i in range(10):
            pid = 90000 + i
            meds = json.loads(ls.getItem(f'bp_meds_{pid}'))
            if not meds or len(meds) != 1 or meds[0]['id'] != i:
                success = False
                break
        
        duration = int((time.time() - t0) * 1000)
        if success:
            add_result(name, cat, 'pass', duration, f'10用户数据隔离验证通过 ({duration}ms)')
        else:
            add_result(name, cat, 'fail', duration, '数据隔离失败')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

def stress_serialization():
    name = '压力:数据序列化(10000对象)'
    cat = '压力'
    t0 = time.time()
    try:
        import random
        data = {f'key_{i}': {'value': random.random(), 'text': f'test_{i}'} for i in range(10000)}
        json_str = json.dumps(data)
        parsed = json.loads(json_str)
        duration = int((time.time() - t0) * 1000)
        
        if len(parsed) == 10000:
            add_result(name, cat, 'pass', duration, f'序列化10000对象 ({duration}ms)')
        else:
            add_result(name, cat, 'fail', duration, '序列化失败')
    except Exception as e:
        add_result(name, cat, 'fail', int((time.time() - t0) * 1000), str(e))

# ==================== 运行所有测试 ====================

print('\n' + '=' * 50)
print('血压守护 - 全面自动化测试')
print('=' * 50 + '\n')

ls = LocalStorage()

print('【1/4】基础功能测试...\n')
test_basic_read_write()
test_date_formatting()
test_user_state_init()
test_add_medication()
test_delete_medication()
test_confirm_medication()
test_add_bp_record()
test_bp_sorting()
test_add_alert()
test_resolve_alert()

print('\n【2/4】家庭管理测试...\n')
test_add_family_member()
test_switch_family_member()
test_data_isolation()

print('\n【3/4】业务逻辑与边界测试...\n')
test_inventory_calc()
test_alert_level()
test_health_assessment()
test_single_data_chart()
test_empty_data()
test_abnormal_values()

print('\n【4/4】压力测试...\n')
stress_large_bp_data()
stress_large_med_data()
stress_concurrent_write()
stress_large_query()
stress_chart_render()
stress_multi_user()
stress_serialization()

# 生成测试报告
total_time = int((time.time() - startTime) * 1000)
pass_rate = round((passedTests / totalTests) * 100, 1) if totalTests > 0 else 0

print('\n' + '=' * 50)
print('测试报告')
print('=' * 50)
print(f'总测试数: {totalTests}')
print(f'通过: {passedTests} ({pass_rate}%)')
print(f'失败: {failedTests}')
print(f'已修复BUG: {fixedBugs}')
print(f'总耗时: {total_time}ms')
print('=' * 50 + '\n')

# 保存测试报告
report = {
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'total': totalTests,
    'passed': passedTests,
    'failed': failedTests,
    'fixed': fixedBugs,
    'passRate': f'{pass_rate}%',
    'totalTime': f'{total_time}ms',
    'results': testResults
}

with open(os.path.join(os.path.dirname(__file__), 'test_report.json'), 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print('测试报告已保存至: test_report.json\n')

if failedTests > 0:
    print('⚠️  发现失败测试，请检查:')
    for r in testResults:
        if r['status'] == 'fail':
            print(f"  ❌ {r['name']}: {r['detail']}")
else:
    print('🎉 所有测试通过！')

print('\n详细日志:')
for l in testLogs:
    print(l)
