#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
血压守护 - 压力测试工具（修复版）
"""

import sys
import time
import threading
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app import create_app

results = []
total_requests = 0
success_count = 0
fail_count = 0
response_times = []
start_time = None
lock = threading.Lock()
errors = []

def test_endpoint(client, endpoint, method='GET', data=None):
    global total_requests, success_count, fail_count
    
    try:
        start = time.time()
        
        if method == 'GET':
            response = client.get(endpoint)
        else:
            response = client.post(endpoint,
                json=data,
                content_type='application/json')
        
        elapsed = (time.time() - start) * 1000
        
        with lock:
            total_requests += 1
            response_times.append(elapsed)
            
            if response.status_code in [200, 201, 204]:
                success_count += 1
            else:
                fail_count += 1
                if len(errors) < 10:
                    errors.append({
                        'endpoint': endpoint,
                        'status': response.status_code,
                        'data': response.data.decode('utf-8')[:200]
                    })
    except Exception as e:
        with lock:
            total_requests += 1
            fail_count += 1
            if len(errors) < 10:
                errors.append({
                    'endpoint': endpoint,
                    'error': str(e)
                })

def worker(client, request_count):
    for i in range(request_count):
        # 混合测试各种端点
        test_endpoint(client, '/api/health')
        test_endpoint(client, '/api/bp/health')
        test_endpoint(client, '/api/medication/health')
        test_endpoint(client, '/api/bp/analysis/1')
        test_endpoint(client, '/api/medication/log/1')

def run_stress_test(app, thread_count, requests_per_thread):
    global start_time
    
    print(f'开始压力测试: {thread_count} 个线程, 每线程 {requests_per_thread} 个请求')
    print(f'总请求数: {thread_count * requests_per_thread * 5}')
    
    with app.app_context():
        start_time = time.time()
        threads = []
        
        for _ in range(thread_count):
            client = app.test_client()
            t = threading.Thread(target=worker, args=(client, requests_per_thread))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        total_time = time.time() - start_time
        
    print(f'\n压力测试完成! 总耗时: {total_time:.2f} 秒')
    
    return total_time

def print_report(total_time):
    print('\n' + '='*60)
    print('📊 血压守护 - 压力测试报告')
    print('='*60)
    
    print(f'\n📈 请求统计:')
    print(f'  总请求数: {total_requests}')
    print(f'  成功: {success_count}')
    print(f'  失败: {fail_count}')
    print(f'  成功率: {success_count/total_requests*100:.2f}%' if total_requests > 0 else '  成功率: 0%')
    print(f'  总耗时: {total_time:.2f} 秒')
    print(f'  每秒请求数 (QPS): {total_requests/total_time:.2f}' if total_time > 0 else '  QPS: 0')
    
    if response_times:
        print(f'\n⏱ 响应时间统计:')
        print(f'  最快: {min(response_times):.2f} ms')
        print(f'  最慢: {max(response_times):.2f} ms')
        print(f'  平均: {sum(response_times)/len(response_times):.2f} ms')
        sorted_times = sorted(response_times)
        print(f'  90% ≤: {sorted_times[int(len(sorted_times)*0.9)]:.2f} ms')
        print(f'  95% ≤: {sorted_times[int(len(sorted_times)*0.95)]:.2f} ms')
        print(f'  99% ≤: {sorted_times[int(len(sorted_times)*0.99)]:.2f} ms')
    
    if errors:
        print(f'\n❌ 错误示例 (前{len(errors)}条):')
        for i, err in enumerate(errors[:5]):
            print(f'  {i+1}. {err}')
    
    print('\n✅ 压力测试完成!')

def main():
    global total_requests, success_count, fail_count, response_times
    
    print('🩺 血压守护 - 压力测试工具')
    print('='*60)
    
    thread_count = 10
    requests_per_thread = 50
    
    print(f'\n配置: 线程数={thread_count}, 每线程请求数={requests_per_thread}')
    
    # 创建压力测试专用应用配置（关闭CSRF等安全限制）
    from app.config import Config
    class TestConfig(Config):
        TESTING = True
        WTF_CSRF_ENABLED = False
    
    app = create_app(config_class=TestConfig)
    
    total_time = run_stress_test(app, thread_count, requests_per_thread)
    print_report(total_time)
    
    # 保存报告
    report = {
        'total_requests': total_requests,
        'success': success_count,
        'failed': fail_count,
        'success_rate': f'{success_count/total_requests*100:.2f}%' if total_requests > 0 else '0%',
        'total_time': f'{total_time:.2f}s',
        'qps': f'{total_requests/total_time:.2f}' if total_time > 0 else '0',
        'avg_response_time': f'{sum(response_times)/len(response_times):.2f}ms' if response_times else '0ms',
        'min_response_time': f'{min(response_times):.2f}ms' if response_times else '0ms',
        'max_response_time': f'{max(response_times):.2f}ms' if response_times else '0ms',
        'p90': f'{sorted(response_times)[int(len(response_times)*0.9)]:.2f}ms' if response_times else '0ms',
        'p95': f'{sorted(response_times)[int(len(response_times)*0.95)]:.2f}ms' if response_times else '0ms',
        'p99': f'{sorted(response_times)[int(len(response_times)*0.99)]:.2f}ms' if response_times else '0ms',
        'errors_sample': errors[:5]
    }
    
    report_path = Path(__file__).parent.parent / 'test_reports'
    report_path.mkdir(exist_ok=True)
    
    with open(report_path / '压力测试报告_new.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f'\n📄 报告已保存至: test_reports/压力测试报告_new.json')
    
    return 0 if fail_count == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
