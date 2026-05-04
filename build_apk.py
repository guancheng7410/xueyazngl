#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
血压守护 APK 自动构建脚本
检查环境并尝试构建Android APK
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_command(cmd):
    """检查命令是否可用"""
    try:
        subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
        return True
    except:
        return False

def check_env():
    """检查构建环境"""
    print("=" * 50)
    print("检查构建环境")
    print("=" * 50)
    
    checks = {
        'Node.js': check_command('node --version'),
        'npm': check_command('npm --version'),
        'Java': check_command('java -version'),
        'Android SDK': os.environ.get('ANDROID_HOME') is not None
    }
    
    for tool, available in checks.items():
        status = '✓' if available else '✗'
        print(f"{status} {tool}")
    
    return checks

def create_www_dir():
    """创建www目录并复制必要文件"""
    print("\n" + "=" * 50)
    print("准备PWA应用文件")
    print("=" * 50)
    
    base_dir = Path(__file__).parent
    www_dir = base_dir / 'www'
    
    # 创建www目录
    www_dir.mkdir(exist_ok=True)
    
    # 复制app_pro.html到www/index.html
    src = base_dir / 'app_pro.html'
    dst = www_dir / 'index.html'
    
    if src.exists():
        shutil.copy2(src, dst)
        print(f"✓ 已复制 {src.name} -> www/index.html")
    else:
        print(f"✗ 源文件不存在: {src}")
        return False
    
    # 复制manifest.json
    manifest_src = base_dir / 'manifest_pro.json'
    if manifest_src.exists():
        shutil.copy2(manifest_src, www_dir / 'manifest.json')
        print(f"✓ 已复制 manifest.json")
    else:
        # 创建默认manifest
        manifest_content = {
            "name": "血压守护",
            "short_name": "血压守护",
            "description": "智能服药提醒与血压记录",
            "start_url": "./index.html",
            "display": "standalone",
            "background_color": "#f0f2f5",
            "theme_color": "#667eea",
            "icons": [
                {
                    "src": "icon-192.png",
                    "sizes": "192x192",
                    "type": "image/png"
                },
                {
                    "src": "icon-512.png",
                    "sizes": "512x512",
                    "type": "image/png"
                }
            ]
        }
        import json
        with open(www_dir / 'manifest.json', 'w', encoding='utf-8') as f:
            json.dump(manifest_content, f, ensure_ascii=False, indent=2)
        print(f"✓ 已创建默认 manifest.json")
    
    # 创建Service Worker
    sw_content = """
var CACHE_NAME = 'bp-guardian-v2';
var urlsToCache = [
  './',
  './index.html',
  './manifest.json'
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        if (response) return response;
        return fetch(event.request);
      })
  );
});
"""
    with open(www_dir / 'sw.js', 'w', encoding='utf-8') as f:
        f.write(sw_content)
    print(f"✓ 已创建 Service Worker")
    
    print(f"\n✓ PWA应用文件准备完成: {www_dir}")
    return True

def build_apk_capacitor():
    """使用Capacitor构建APK"""
    print("\n" + "=" * 50)
    print("使用Capacitor构建APK")
    print("=" * 50)
    
    base_dir = Path(__file__).parent
    os.chdir(base_dir)
    
    # 检查node_modules
    if not (base_dir / 'node_modules').exists():
        print("\n安装依赖...")
        subprocess.run('npm install', shell=True)
    
    # 添加Android平台
    android_dir = base_dir / 'android'
    if not android_dir.exists():
        print("\n添加Android平台...")
        result = subprocess.run('npx cap add android', shell=True)
        if result.returncode != 0:
            print("✗ 添加Android平台失败")
            return False
    
    # 同步项目
    print("\n同步项目...")
    result = subprocess.run('npx cap sync android', shell=True)
    if result.returncode != 0:
        print("✗ 同步项目失败")
        return False
    
    # 尝试构建APK
    print("\n构建APK...")
    os.chdir(android_dir)
    
    gradlew = android_dir / 'gradlew.bat'
    if gradlew.exists():
        result = subprocess.run('gradlew.bat assembleDebug', shell=True)
        if result.returncode == 0:
            apk_path = android_dir / 'app' / 'build' / 'outputs' / 'apk' / 'debug' / 'app-debug.apk'
            if apk_path.exists():
                # 复制到D:\APP
                dest_dir = Path('D:/APP')
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest = dest_dir / '血压守护.apk'
                shutil.copy2(apk_path, dest)
                print(f"\n✓ APK构建成功！")
                print(f"  位置: {dest}")
                return True
    
    print("✗ APK构建失败，请手动在Android Studio中构建")
    return False

def main():
    print("\n")
    print("=" * 50)
    print("    血压守护 APK 构建工具")
    print("=" * 50)
    print()
    
    # 检查环境
    env = check_env()
    
    # 创建www目录
    if not create_www_dir():
        print("\n✗ 准备PWA文件失败")
        return
    
    # 检查是否有Android环境
    if env['Node.js'] and env['Java'] and env['Android SDK']:
        print("\n✓ 检测到完整的Android开发环境")
        choice = input("是否立即构建APK？(y/n): ")
        if choice.lower() == 'y':
            build_apk_capacitor()
    else:
        print("\n✗ 缺少Android开发环境")
        print("\n您可以：")
        print("1. 安装 Android Studio 后重新运行此脚本")
        print("2. 使用 HBuilderX 云打包（推荐）")
        print("3. 使用 PWA 方式在手机上安装")
        print("\n详细说明请查看：血压守护APK构建指南.txt")
    
    print("\n" + "=" * 50)
    print("完成！")
    print("=" * 50)
    
    input("\n按回车键退出...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
        sys.exit(1)
