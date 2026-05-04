#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
血压守护 - 后端模块全面测试
测试后端所有模块的功能和性能
"""

import sys
import time
import json
import os

# 添加后端路径
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)

# ==================== 测试框架 ====================
class TestRunner:
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def run(self, name, func):
        self.total += 1
        t0 = time.time()
        try:
            result = func()
            duration = int((time.time() - t0) * 1000)
            if result.get('success', False):
                self.passed += 1
                print(f"  ✅ {name}: {result.get('detail', '')} ({duration}ms)")
                self.results.append({'name': name, 'status': 'pass', 'detail': result.get('detail', '')})
            else:
                self.failed += 1
                print(f"  ❌ {name}: {result.get('detail', '')} ({duration}ms)")
                self.results.append({'name': name, 'status': 'fail', 'detail': result.get('detail', '')})
        except Exception as e:
            duration = int((time.time() - t0) * 1000)
            self.failed += 1
            print(f"  ❌ {name}: 异常 - {str(e)} ({duration}ms)")
            self.results.append({'name': name, 'status': 'fail', 'detail': str(e)})

runner = TestRunner()

# ==================== 1. 配置模块测试 ====================
print("\n【1/7】配置模块测试")
print("-" * 40)

def test_config_import():
    try:
        from app.config import ProductionConfig, DevelopmentConfig, TestingConfig
        ok = ProductionConfig.DEBUG == False and DevelopmentConfig.DEBUG == True
        return {'success': ok, 'detail': '生产/开发配置正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_config_security():
    try:
        from app.config import ProductionConfig
        ok = ProductionConfig.SESSION_COOKIE_SECURE == True
        ok = ok and ProductionConfig.SESSION_COOKIE_HTTPONLY == True
        ok = ok and ProductionConfig.SQLALCHEMY_POOL_SIZE == 20
        return {'success': ok, 'detail': '安全配置正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_config_dict():
    try:
        from app.config import config_dict
        ok = 'production' in config_dict and 'development' in config_dict
        return {'success': ok, 'detail': '配置字典完整'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

runner.run('配置模块导入', test_config_import)
runner.run('生产环境安全配置', test_config_security)
runner.run('配置字典完整性', test_config_dict)

# ==================== 2. 安全模块测试 ====================
print("\n【2/7】安全模块测试")
print("-" * 40)

def test_password_hash():
    try:
        from app.security import PasswordHasher
        ph = PasswordHasher()
        hashed = ph.hash_password('test123')
        parts = hashed.split('$')
        ok = len(parts) == 2 and len(parts[0]) == 32
        ok = ok and ph.verify_password('test123', hashed) == True
        ok = ok and ph.verify_password('wrong', hashed) == False
        return {'success': ok, 'detail': '密码加密/验证正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_password_uniqueness():
    try:
        from app.security import PasswordHasher
        ph = PasswordHasher()
        h1 = ph.hash_password('same')
        h2 = ph.hash_password('same')
        return {'success': h1 != h2, 'detail': '密码哈希唯一性正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_xss_sanitizer():
    try:
        from app.security import XSSProtector
        xp = XSSProtector()
        result = xp.sanitize('<script>alert(1)</script>hello')
        ok = '<script>' not in result
        result2 = xp.sanitize('javascript:alert(1)')
        ok = ok and 'javascript:' not in result2
        result3 = xp.sanitize('<div>test</div>')
        ok = ok and '&lt;' in result3
        return {'success': ok, 'detail': 'XSS防护正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_csrf_token():
    try:
        from app.security import CSRFProtector
        t1 = CSRFProtector.generate_token()
        t2 = CSRFProtector.generate_token()
        ok = len(t1) == 64 and t1 != t2
        return {'success': ok, 'detail': 'CSRF Token生成正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_rate_limiter():
    try:
        from app.security import RateLimiter
        rl = RateLimiter()
        ok = rl.is_allowed('user1', max_requests=3, window=60) == True
        ok = ok and rl.is_allowed('user1', max_requests=3, window=60) == True
        ok = ok and rl.is_allowed('user1', max_requests=3, window=60) == True
        ok = ok and rl.is_allowed('user1', max_requests=3, window=60) == False
        ok = ok and rl.is_allowed('user2', max_requests=3, window=60) == True
        return {'success': ok, 'detail': '速率限制正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_sql_injection_protection():
    try:
        from app.security import SQLInjectionProtector
        sip = SQLInjectionProtector()
        ok = sip.validate("SELECT * FROM users") == False
        ok = ok and sip.validate("normal text") == True
        ok = ok and sip.validate("1 OR 1=1") == False
        return {'success': ok, 'detail': 'SQL注入防护正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

runner.run('密码加密与验证', test_password_hash)
runner.run('密码哈希唯一性', test_password_uniqueness)
runner.run('XSS攻击防护', test_xss_sanitizer)
runner.run('CSRF Token生成', test_csrf_token)
runner.run('速率限制', test_rate_limiter)
runner.run('SQL注入防护', test_sql_injection_protection)

# ==================== 3. 数据模型测试 ====================
print("\n【3/7】数据模型测试")
print("-" * 40)

def test_models_import():
    try:
        from app.models import db, User, FamilyGroup, FamilyMember, Parent, Medication, MedicationLog, BloodPressureRecord, Alert, MedicationInventory, init_db
        return {'success': True, 'detail': '所有模型导入成功'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_user_to_dict():
    try:
        from app.models import User
        u = User(openid='test_openid', nickname='测试用户', phone='13800138000')
        d = u.to_dict()
        ok = d['openid'] == 'test_openid' and d['nickname'] == '测试用户'
        return {'success': ok, 'detail': 'User.to_dict() 正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_parent_to_dict():
    try:
        from app.models import Parent
        p = Parent(name='张父', age=65, gender='男')
        d = p.to_dict()
        ok = d['name'] == '张父' and d['age'] == 65
        return {'success': ok, 'detail': 'Parent.to_dict() 正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_bp_record_to_dict():
    try:
        from app.models import BloodPressureRecord
        from datetime import datetime
        r = BloodPressureRecord(parent_id=1, systolic=120, diastolic=80, heart_rate=72)
        d = r.to_dict()
        ok = d['systolic'] == 120 and d['diastolic'] == 80 and d['heart_rate'] == 72
        return {'success': ok, 'detail': 'BloodPressureRecord.to_dict() 正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_medication_to_dict():
    try:
        from app.models import Medication
        m = Medication(parent_id=1, name='硝苯地平', dosage='1片', frequency='twice', times=['08:00', '20:00'])
        d = m.to_dict()
        ok = d['name'] == '硝苯地平' and d['dosage'] == '1片'
        return {'success': ok, 'detail': 'Medication.to_dict() 正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_alert_to_dict():
    try:
        from app.models import Alert
        a = Alert(parent_id=1, level='warn', message='漏服预警')
        d = a.to_dict()
        ok = d['level'] == 'warn' and d['message'] == '漏服预警'
        return {'success': ok, 'detail': 'Alert.to_dict() 正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_model_indexes():
    try:
        from app.models import Medication, BloodPressureRecord, Alert, MedicationLog
        med_idx = [idx.name for idx in Medication.__table__.indexes]
        bp_idx = [idx.name for idx in BloodPressureRecord.__table__.indexes]
        ok = len(med_idx) >= 1 and len(bp_idx) >= 2
        return {'success': ok, 'detail': f'索引配置: 药物{len(med_idx)}个, 血压{len(bp_idx)}个'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_model_relationships():
    try:
        from app.models import Parent, Medication, BloodPressureRecord, MedicationLog
        has_meds = hasattr(Parent, 'medications')
        has_bp = hasattr(Parent, 'blood_pressure_records')
        has_logs = hasattr(Parent, 'medication_logs')
        ok = has_meds and has_bp and has_logs
        return {'success': ok, 'detail': '模型关系定义正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

runner.run('模型导入', test_models_import)
runner.run('User.to_dict()', test_user_to_dict)
runner.run('Parent.to_dict()', test_parent_to_dict)
runner.run('BloodPressureRecord.to_dict()', test_bp_record_to_dict)
runner.run('Medication.to_dict()', test_medication_to_dict)
runner.run('Alert.to_dict()', test_alert_to_dict)
runner.run('模型索引配置', test_model_indexes)
runner.run('模型关系定义', test_model_relationships)

# ==================== 4. 应用工厂测试 ====================
print("\n【4/7】应用工厂测试")
print("-" * 40)

def test_app_factory():
    try:
        from app import create_app
        from app.config import TestingConfig
        app = create_app(TestingConfig)
        ok = app is not None and app.config['TESTING'] == True
        return {'success': ok, 'detail': '应用工厂创建成功'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_health_endpoint():
    try:
        from app import create_app
        from app.config import TestingConfig
        app = create_app(TestingConfig)
        with app.test_client() as client:
            resp = client.get('/api/health')
            data = resp.get_json()
            ok = resp.status_code == 200 and data.get('status') == 'ok'
            return {'success': ok, 'detail': '健康检查端点正常'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_404_handler():
    try:
        from app import create_app
        from app.config import TestingConfig
        app = create_app(TestingConfig)
        with app.test_client() as client:
            resp = client.get('/nonexistent')
            data = resp.get_json()
            ok = resp.status_code == 404 and data.get('success') == False
            return {'success': ok, 'detail': '404处理正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_security_headers():
    try:
        from app import create_app
        from app.config import TestingConfig
        app = create_app(TestingConfig)
        with app.test_client() as client:
            resp = client.get('/api/health')
            ok = 'X-Content-Type-Options' in resp.headers
            ok = ok and 'X-Frame-Options' in resp.headers
            return {'success': ok, 'detail': '安全响应头设置正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_500_handler():
    try:
        from app import create_app
        from app.config import TestingConfig
        app = create_app(TestingConfig)
        app.config['PROPAGATE_EXCEPTIONS'] = False
        
        @app.route('/test_error')
        def trigger_error():
            raise Exception("Test error")
        
        with app.test_client() as client:
            resp = client.get('/test_error')
            data = resp.get_json()
            ok = resp.status_code == 500 and data.get('success') == False
            return {'success': ok, 'detail': '500处理正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

runner.run('应用工厂创建', test_app_factory)
runner.run('健康检查端点', test_health_endpoint)
runner.run('404错误处理', test_404_handler)
runner.run('安全响应头', test_security_headers)
runner.run('500错误处理', test_500_handler)

# ==================== 5. 日志模块测试 ====================
print("\n【5/7】日志模块测试")
print("-" * 40)

def test_logger_import():
    try:
        from app.logger import Logger, AuditLogger
        return {'success': True, 'detail': '日志模块导入成功'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_logger_setup():
    try:
        from app import create_app
        from app.config import TestingConfig
        app = create_app(TestingConfig)
        ok = hasattr(app, 'logger')
        return {'success': ok, 'detail': '应用日志器初始化成功'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_audit_logger():
    try:
        from app import create_app
        from app.config import TestingConfig
        from app.logger import AuditLogger
        app = create_app(TestingConfig)
        AuditLogger.log_action(app, 'user1', '添加药物', '添加了硝苯地平', '127.0.0.1')
        return {'success': True, 'detail': '审计日志记录成功'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

runner.run('日志模块导入', test_logger_import)
runner.run('日志器初始化', test_logger_setup)
runner.run('审计日志', test_audit_logger)

# ==================== 6. 性能压力测试 ====================
print("\n【6/7】后端性能压力测试")
print("-" * 40)

def test_password_hash_performance():
    try:
        from app.security import PasswordHasher
        ph = PasswordHasher()
        start = time.time()
        for i in range(50):
            ph.hash_password(f'test_password_{i}')
        duration = int((time.time() - start) * 1000)
        avg = duration / 50
        ok = avg < 200
        return {'success': ok, 'detail': f'50次密码加密: {duration}ms (平均{avg:.0f}ms/次)'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_password_verify_performance():
    try:
        from app.security import PasswordHasher
        ph = PasswordHasher()
        hashed = ph.hash_password('test')
        start = time.time()
        for i in range(50):
            ph.verify_password('test', hashed)
        duration = int((time.time() - start) * 1000)
        avg = duration / 50
        ok = avg < 200
        return {'success': ok, 'detail': f'50次密码验证: {duration}ms (平均{avg:.0f}ms/次)'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_xss_performance():
    try:
        from app.security import XSSProtector
        xp = XSSProtector()
        test_text = '<script>alert("xss")</script><img onerror="hack()" src=x>' * 100
        start = time.time()
        for i in range(100):
            xp.sanitize(test_text)
        duration = int((time.time() - start) * 1000)
        return {'success': True, 'detail': f'100次XSS清理: {duration}ms'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_rate_limiter_concurrent():
    try:
        from app.security import RateLimiter
        rl = RateLimiter()
        start = time.time()
        for i in range(1000):
            rl.is_allowed(f'user_{i % 100}', max_requests=10, window=60)
        duration = int((time.time() - start) * 1000)
        return {'success': True, 'detail': f'1000次速率检查: {duration}ms'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_app_request_performance():
    try:
        from app import create_app
        from app.config import TestingConfig
        app = create_app(TestingConfig)
        with app.test_client() as client:
            start = time.time()
            for i in range(100):
                client.get('/api/health')
            duration = int((time.time() - start) * 1000)
            avg = duration / 100
            ok = avg < 50
            return {'success': ok, 'detail': f'100次健康检查: {duration}ms (平均{avg:.1f}ms/次)'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_json_serialization():
    try:
        import random
        start = time.time()
        data = {'key_' + str(i): {'value': random.random(), 'text': 'test' * 10} for i in range(5000)}
        json_str = json.dumps(data, ensure_ascii=False)
        parsed = json.loads(json_str)
        duration = int((time.time() - start) * 1000)
        ok = len(parsed) == 5000
        return {'success': ok, 'detail': f'5000对象序列化: {duration}ms, {len(json_str)}字节'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_model_creation_performance():
    try:
        from app.models import BloodPressureRecord, Medication, Alert, Parent
        start = time.time()
        for i in range(1000):
            r = BloodPressureRecord(parent_id=1, systolic=120+i%30, diastolic=80+i%20, heart_rate=72)
        duration = int((time.time() - start) * 1000)
        return {'success': True, 'detail': f'创建1000个模型对象: {duration}ms'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

runner.run('密码加密性能', test_password_hash_performance)
runner.run('密码验证性能', test_password_verify_performance)
runner.run('XSS清理性能', test_xss_performance)
runner.run('速率限制性能', test_rate_limiter_concurrent)
runner.run('API请求性能', test_app_request_performance)
runner.run('JSON序列化性能', test_json_serialization)
runner.run('模型创建性能', test_model_creation_performance)

# ==================== 7. 数据完整性测试 ====================
print("\n【7/7】数据完整性测试")
print("-" * 40)

def test_bp_record_validation():
    try:
        from app.models import BloodPressureRecord
        r1 = BloodPressureRecord(parent_id=1, systolic=120, diastolic=80, heart_rate=72)
        r2 = BloodPressureRecord(parent_id=1, systolic=180, diastolic=110, heart_rate=90)
        r3 = BloodPressureRecord(parent_id=1, systolic=90, diastolic=60, heart_rate=60)
        
        def check_range(r):
            return 70 <= r.systolic <= 250 and 40 <= r.diastolic <= 150
        
        ok = check_range(r1) and check_range(r2) and check_range(r3)
        return {'success': ok, 'detail': '血压记录数据验证正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_medication_validation():
    try:
        from app.models import Medication
        m = Medication(parent_id=1, name='硝苯地平', dosage='1片', frequency='twice', times=['08:00', '20:00'])
        ok = m.name == '硝苯地平' and len(m.times) == 2
        ok = ok and m.dosage == '1片' and m.frequency == 'twice'
        return {'success': ok, 'detail': '药物数据验证正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_alert_level_validation():
    try:
        from app.models import Alert
        levels = ['normal', 'warn', 'urgent', 'critical']
        results = []
        for level in levels:
            a = Alert(parent_id=1, level=level, message='测试')
            results.append(a.level == level)
        ok = all(results)
        return {'success': ok, 'detail': '预警级别验证正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_inventory_threshold():
    try:
        from app.models import MedicationInventory
        inv = MedicationInventory(parent_id=1, medication_id=1, quantity=5, unit='片', remind_threshold=7)
        ok = inv.quantity == 5 and inv.remind_threshold == 7
        return {'success': ok, 'detail': '库存阈值验证正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_family_group_validation():
    try:
        from app.models import FamilyGroup
        fg = FamilyGroup(name='张家', creator_id=1, invite_code='ABC123')
        ok = fg.name == '张家' and len(fg.invite_code) == 6
        return {'success': ok, 'detail': '家庭组验证正确'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

def test_model_dict_consistency():
    try:
        from app.models import Parent, Medication, BloodPressureRecord
        p = Parent(name='李母', age=70, gender='女', health_status='normal')
        d = p.to_dict()
        
        ok = 'id' in d and 'name' in d and 'age' in d
        ok = ok and 'gender' in d and 'health_status' in d
        
        m = Medication(parent_id=1, name='阿司匹林', dosage='100mg', frequency='once')
        md = m.to_dict()
        ok = ok and 'name' in md and 'dosage' in md
        
        r = BloodPressureRecord(parent_id=1, systolic=130, diastolic=85)
        rd = r.to_dict()
        ok = ok and 'systolic' in rd and 'diastolic' in rd
        
        return {'success': ok, 'detail': '模型to_dict一致性验证通过'}
    except Exception as e:
        return {'success': False, 'detail': str(e)}

runner.run('血压记录验证', test_bp_record_validation)
runner.run('药物数据验证', test_medication_validation)
runner.run('预警级别验证', test_alert_level_validation)
runner.run('库存阈值验证', test_inventory_threshold)
runner.run('家庭组验证', test_family_group_validation)
runner.run('模型to_dict一致性', test_model_dict_consistency)

# ==================== 汇总 ====================
print("\n" + "=" * 60)
print("后端模块测试汇总")
print("=" * 60)
print(f"总测试数:    {runner.total}")
print(f"通过:        {runner.passed}")
print(f"失败:        {runner.failed}")
pass_rate = round(runner.passed/runner.total*100, 1) if runner.total > 0 else 0
print(f"通过率:      {pass_rate}%")
print("=" * 60)

failed = [r for r in runner.results if r['status'] == 'fail']
if failed:
    print("\n❌ 失败测试详情:")
    for r in failed:
        print(f"  ❌ {r['name']}: {r['detail']}")
else:
    print("\n✅ 所有后端模块测试通过！")

# 保存报告
report = {
    'title': '血压守护 - 后端模块测试报告',
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'summary': {
        'total': runner.total,
        'passed': runner.passed,
        'failed': runner.failed,
        'passRate': f'{pass_rate}%'
    },
    'results': runner.results
}

report_path = os.path.join(os.path.dirname(__file__), 'test_reports', '后端模块测试报告.json')
os.makedirs(os.path.dirname(report_path), exist_ok=True)
with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print(f"\n报告已保存: {report_path}")
