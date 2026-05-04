#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
血压守护 - 云数据存储模块
支持腾讯云COS和阿里云OSS
"""

import os
import json
import time
from datetime import datetime

class CloudStorageManager:
    """云存储管理器，支持多平台"""

    def __init__(self, provider='local', config=None):
        """
        初始化云存储管理器

        Args:
            provider (str): 存储提供商 ('local', 'tencent', 'aliyun')
            config (dict): 配置参数
        """
        self.provider = provider
        self.config = config or {}
        self._client = None

        if provider == 'tencent':
            self._init_tencent()
        elif provider == 'aliyun':
            self._init_aliyun()

    def _init_tencent(self):
        """初始化腾讯云COS"""
        try:
            from qcloud_cos import CosConfig, CosS3Client
            config = CosConfig(
                Region=self.config.get('region', 'ap-guangzhou'),
                SecretId=self.config.get('secret_id', ''),
                SecretKey=self.config.get('secret_key', ''),
                Token=None,
                Scheme='https'
            )
            self._client = CosS3Client(config)
            self.bucket = self.config.get('bucket', 'bp-guardian-1234567890')
        except ImportError:
            print('请安装腾讯云SDK: pip install cos-python-sdk-v5')
            self._client = None

    def _init_aliyun(self):
        """初始化阿里云OSS"""
        try:
            import oss2
            auth = oss2.Auth(
                self.config.get('access_key_id', ''),
                self.config.get('access_key_secret', '')
            )
            self._client = oss2.Bucket(
                auth,
                self.config.get('endpoint', 'oss-cn-hangzhou.aliyuncs.com'),
                self.config.get('bucket', 'bp-guardian')
            )
        except ImportError:
            print('请安装阿里云SDK: pip install oss2')
            self._client = None

    def save_user_data(self, user_id, data):
        """
        保存用户数据到云端

        Args:
            user_id (int): 用户ID
            data (dict): 用户数据（meds, logs, bps, alerts等）

        Returns:
            dict: 操作结果
        """
        key = f'users/{user_id}/data.json'
        data_with_meta = {
            'user_id': user_id,
            'data': data,
            'sync_time': datetime.now().isoformat(),
            'version': '2.0.0'
        }

        if self.provider == 'local':
            return self._save_local(key, data_with_meta)
        elif self.provider == 'tencent':
            return self._save_tencent(key, data_with_meta)
        elif self.provider == 'aliyun':
            return self._save_aliyun(key, data_with_meta)

    def load_user_data(self, user_id):
        """
        从云端加载用户数据

        Args:
            user_id (int): 用户ID

        Returns:
            dict: 用户数据
        """
        key = f'users/{user_id}/data.json'

        if self.provider == 'local':
            return self._load_local(key)
        elif self.provider == 'tencent':
            return self._load_tencent(key)
        elif self.provider == 'aliyun':
            return self._load_aliyun(key)

    def sync_data(self, user_id, local_data, cloud_version=None):
        """
        数据同步（处理冲突）

        Args:
            user_id (int): 用户ID
            local_data (dict): 本地数据
            cloud_version (str): 云端版本号（可选）

        Returns:
            dict: 同步结果
        """
        cloud_data = self.load_user_data(user_id)

        if not cloud_data.get('success'):
            return self.save_user_data(user_id, local_data)

        cloud = cloud_data['data']['data']
        cloud_time = cloud_data['data'].get('sync_time', '')

        merged = self._merge_data(local_data, cloud)
        return self.save_user_data(user_id, merged)

    def _merge_data(self, local, cloud):
        """
        合并本地和云端数据（以后更新为准）

        Args:
            local (dict): 本地数据
            cloud (dict): 云端数据

        Returns:
            dict: 合并后的数据
        """
        merged = {
            'meds': cloud.get('meds', []),
            'logs': cloud.get('logs', []),
            'bps': cloud.get('bps', []),
            'alerts': cloud.get('alerts', []),
            'sync_time': datetime.now().isoformat()
        }

        if local.get('sync_time', '') > cloud.get('sync_time', ''):
            return local
        return merged

    def _save_local(self, key, data):
        """本地文件存储（开发测试用）"""
        try:
            local_dir = os.path.join(os.path.dirname(__file__), '..', 'cloud_data')
            os.makedirs(local_dir, exist_ok=True)
            file_path = os.path.join(local_dir, key.replace('/', os.sep))
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return {'success': True, 'path': file_path}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _load_local(self, key):
        """本地文件读取"""
        try:
            local_dir = os.path.join(os.path.dirname(__file__), '..', 'cloud_data')
            file_path = os.path.join(local_dir, key.replace('/', os.sep))
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return {'success': True, 'data': data}
            return {'success': False, 'error': '文件不存在'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _save_tencent(self, key, data):
        """腾讯云COS存储"""
        if not self._client:
            return {'success': False, 'error': 'COS客户端未初始化'}
        try:
            import json
            body = json.dumps(data, ensure_ascii=False).encode('utf-8')
            self._client.put_object(
                Bucket=self.bucket,
                Body=body,
                Key=key,
                ContentType='application/json'
            )
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _load_tencent(self, key):
        """腾讯云COS读取"""
        if not self._client:
            return {'success': False, 'error': 'COS客户端未初始化'}
        try:
            response = self._client.get_object(Bucket=self.bucket, Key=key)
            data = json.loads(response['Body'].read())
            return {'success': True, 'data': data}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _save_aliyun(self, key, data):
        """阿里云OSS存储"""
        if not self._client:
            return {'success': False, 'error': 'OSS客户端未初始化'}
        try:
            import json
            body = json.dumps(data, ensure_ascii=False).encode('utf-8')
            self._client.put_object(key, body)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _load_aliyun(self, key):
        """阿里云OSS读取"""
        if not self._client:
            return {'success': False, 'error': 'OSS客户端未初始化'}
        try:
            result = self._client.get_object(key)
            data = json.loads(result.read())
            return {'success': True, 'data': data}
        except Exception as e:
            return {'success': False, 'error': str(e)}


# 全局云存储实例
cloud_manager = None

def init_cloud_storage(provider='local', config=None):
    """
    初始化全局云存储实例

    Args:
        provider (str): 存储提供商
        config (dict): 配置参数
    """
    global cloud_manager
    cloud_manager = CloudStorageManager(provider, config)
    return cloud_manager

def get_cloud_storage():
    """获取全局云存储实例"""
    return cloud_manager
