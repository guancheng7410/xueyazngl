#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
血压守护 - 文件名乱码修复工具
用于修复被错误编码的中文文件名
"""
import os
import sys
from pathlib import Path

# 基于文件内容的文件名映射
FILENAME_MAPPINGS = {
    # 基于读取的文件内容的映射
    "╥╡╬ё╜т╛Ў╖╜░╕.md": "血压守护-业务解决方案.md",
    "╥╡╬ё╨ш╟є╦╡├ў╩щ.docx": "血压守护-系统设计文档.docx",
    "╥╡╬ё╜т╛Ў╖╜░╕.docx": "血压守护-业务解决方案.docx",
    
    # 基于文件内容推测的名称
    "┐к╖в╬─╡╡.md": "系统架构设计.md",
    "┐к╖в╬─╡╡.docx": "系统架构设计.docx",
    "╔╧╧▀╖в▓╝═ъ╒√╓╕─╧.md": "系统部署操作指南.md",
    "╔╧╧▀╖в▓╝┐ь╦┘╝ь▓щ╟х╡е.txt": "系统部署环境检查清单.txt",
    "╚л├ц╣ж─▄▓т╩╘.html": "压力测试工具.html",
    "╝ь▓щ╗╖╛│.bat": "环境配置.bat",
    "╞Ї╢п╩╓╗·╖├╬╩.bat": "快速启动脚本.bat",
    "╤к╤╣╩╪╗д-╧ю─┐╗у▒и.pptx": "家庭看护APP-产品演示.pptx",
    "╤к╤╣╩╪╗дAPK╣╣╜и╓╕─╧.txt": "家庭看护APP打包说明.txt",
    "╫╘╢п╣╣╜иAPK.bat": "一键打包APK.bat",
    "░▓╫░╡╜╩╓╗·.bat": "项目快速启动.bat",
    "APP╞Ї╢п.bat": "APP启动.bat",
    "README_░▓╫░╦╡├ў.txt": "README项目说明.txt",
    
    # backend目录下的文件
    "╓╪╞Ї▓в╞Ї╢п.bat": "生产环境启动.bat",
    "╞Ї╢п╖■╬ё╞ў.bat": "启动环境检查.bat",
    "╥╗╝№╞Ї╢п.bat": "调试模式启动.bat",
    
    # www目录下的文件
    "APK░▓╫░░№╦╡├ў.html": "APK项目说明文档.html",
    "╤к╤╣╩╪╗дAPP╧┬╘╪░▓╫░▓┘╫ў╩╓▓с.html": "家庭看护APP快速部署与使用.html",
    
    # test_reports目录下的文件
    "▓т╩╘▒и╕ц.txt": "测试报告.txt",
    "▓т╩╘▒и╕ц_═ъ╒√░ц.json": "测试报告_原始数据.json",
    "╣ж─▄▓т╩╘▒и╕ц.json": "压力测试报告.json",
    "╣ж─▄▓т╩╘▒и╕ц.txt": "压力测试报告.txt",
    "╤╣┴ж▓т╩╘▒и╕ц.json": "系统测试报告.json",
    "╤╣┴ж▓т╩╘▒и╕ц.txt": "系统测试报告.txt",
    "║є╢╦─г┐щ▓т╩╘▒и╕ц.json": "前端功能测试报告.json",
    "╫ю╓╒▓т╩╘▒и╕ц.txt": "性能测试报告.txt",
}

def is_garbled_name(name: str) -> bool:
    """检查文件名是否是乱码"""
    # 检查是否包含非ASCII的奇怪字符（乱码特征）
    garbled_chars = '║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬'
    return any(c in garbled_chars for c in name)

def fix_filenames(root_dir: str):
    """修复指定目录下的乱码文件名"""
    root = Path(root_dir)
    
    print(f"正在扫描目录: {root_dir}")
    print("-" * 60)
    
    # 收集所有需要重命名的文件
    to_rename = []
    
    for filepath in root.rglob('*'):
        if filepath.is_file():
            filename = filepath.name
            if is_garbled_name(filename):
                if filename in FILENAME_MAPPINGS:
                    new_name = FILENAME_MAPPINGS[filename]
                    to_rename.append((filepath, new_name))
                else:
                    print(f"⚠️ 未找到映射的乱码文件: {filename}")
    
    # 执行重命名
    renamed_count = 0
    for filepath, new_name in to_rename:
        new_path = filepath.parent / new_name
        
        # 检查目标文件是否已存在
        if new_path.exists():
            print(f"⚠️ 目标文件已存在，跳过: {new_name}")
            continue
        
        try:
            filepath.rename(new_path)
            print(f"✅ 重命名: {filepath.name} -> {new_name}")
            renamed_count += 1
        except Exception as e:
            print(f"❌ 重命名失败: {filepath.name} -> {new_name}, 错误: {e}")
    
    print("-" * 60)
    print(f"共修复 {renamed_count} 个文件名")

def scan_and_list_files(root_dir: str):
    """列出所有文件，帮助识别乱码文件"""
    root = Path(root_dir)
    print(f"扫描目录: {root_dir}")
    print("=" * 80)
    
    for filepath in sorted(root.rglob('*')):
        if filepath.is_file():
            if is_garbled_name(filepath.name):
                print(f"⚠️ 乱码文件名: {filepath.name}")

if __name__ == "__main__":
    project_root = "/workspace/blood-pressure-guardian"
    
    # 先扫描并列出文件
    print("=" * 80)
    print("血压守护 - 乱码文件名修复工具")
    print("=" * 80)
    scan_and_list_files(project_root)
    
    # 确认修复
    print("\n" + "=" * 80)
    response = input("\n是否执行文件名修复? (y/n): ").strip().lower()
    
    if response == 'y':
        fix_filenames(project_root)
        print("\n✅ 修复完成!")
    else:
        print("\n操作已取消.")
