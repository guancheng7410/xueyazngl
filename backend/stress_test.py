#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
血压守护 - 压力测试工具
测试API性能、并发能力和响应时间
"""

import sys
import time
import threading
import requests
from datetime import datetime

BASE_URL = 'http://localhost:5000'
results = []
total_requests = 0
success_count = 0
fail_count = 0
response_times = []
start_time = None

def test_health_endpoint():
    """测试健康检查端点"""
    global total_requests, success_count, fail_count
    
    try:
        start = time.time()
        response = requests.get(f'{BASE_URL}/api/health', timeout=5)
        elapsed = (time.time() - start) * 1000
        
        total_requests += 1
        response_times.append(elapsed)
        
        if response.status_code == 200:
            success_count += 1
            results.append({
                'type': 'health',
                'success': True,
                'response_time': elapsed,
                'status_code': 200
            })
        else:
            fail_count += 1
            results.append({
                'type': 'health',
                'success': False,
                'response_time': elapsed,
                'status_code': response.status_code
            })
    except Exception as e:
        total_requests += 1
        fail_count += 1
        results.append({
            'type': 'health',
            'success': False,
            'response_time': 0,
            'error': str(e)
        })

def run_concurrent_tests(thread_count, requests_per_thread):
    """运行并发测试"""
    global start_time
    
    print(f'开始压力测试: {thread_count} 个线程, 每个线程 {requests_per_thread} 个请求')
    
    start_time = time.time()
    threads = []
    
    for _ in range(thread_count):
        t = threading.Thread(target=worker, args=(requests_per_thread,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    total_time = time.time() - start_time
    
    print(f'\n压力测试完成! 总耗时: {total_time:.2f} 秒')

def worker(request_count):
    """工作线程"""
    for _ in range(request_count):
        test_health_endpoint()
        time.sleep(0.01)  # 短暂延迟避免过于激进

def print_report():
    """打印测试报告"""
    print('\n' + '='*60)
    print('📊 血压守护 - 压力测试报告')
    print('='*60)
    
    total_time = time.time() - start_time if start_time else 0
    
    print(f'\n📈 请求统计:')
    print(f'  总请求数: {total_requests}')
    print(f'  成功: {success_count}')
    print(f'  失败: {fail_count}')
    print(f'  成功率: {success_count/total_requests*100:.2f}%' if total_requests > 0 else 0)
    print(f'  总耗时: {total_time:.2f} 秒')
    print(f'  每秒请求数 (QPS): {total_requests/total_time:.2f}' if total_time > 0 else 0)
    
    if response_times:
        print(f'\n⏱ 响应时间统计:')
        print(f'  最快: {min(response_times):.2f} ms')
        print(f'  最慢: {max(response_times):.2f} ms')
        print(f'  平均: {sum(response_times)/len(response_times):.2f} ms')
        sorted_times = sorted(response_times)
        print(f'  90% ≤: {sorted_times[int(len(sorted_times)*0.9)]:.2f} ms')
        print(f'  95% ≤: {sorted_times[int(len(sorted_times)*0.95)]:.2f} ms')
        print(f'  99% ≤: {sorted_times[int(len(sorted_times)*0.99)]:.2f} ms')
    
    print('\n✅ 压力测试完成!')

def main():
    """主函数"""
    print('🩺 血压守护 - 压力测试工具')
    print('='*60)
    
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'quick':
        thread_count = 10
        requests_per_thread = 20
    else:
        thread_count = 20
        requests_per_thread = 50
    
    print(f'\n配置: 线程数={thread_count}, 每线程请求数={requests_per_thread}')
    
    try:
        response = requests.get(f'{BASE_URL}/api/health', timeout=3)
        print(f'✅ 服务器连接正常: {response.status_code}')
    except Exception as e:
        print(f'❌ 无法连接到服务器: {e}')
        print('请先启动服务器: cd backend && python run.py')
        return 1
    
    run_concurrent_tests(thread_count, requests_per_thread)
    print_report()
    
    return 0 if success_count == total_requests else 1

if __name__ == '__main__':
    sys.exit(main())
