#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
血压守护 - 微信服务号推送集成
实现模板消息推送功能
"""

import json
import time
import hashlib
import requests
from datetime import datetime

class WeChatPushService:
    """微信服务号推送服务"""

    def __init__(self, app_id, app_secret, template_id=None):
        """
        初始化微信推送服务

        Args:
            app_id (str): 微信公众号AppID
            app_secret (str): 微信公众号AppSecret
            template_id (str): 模板消息ID（可选）
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.template_id = template_id or 'YOUR_TEMPLATE_ID'
        self.access_token = None
        self.token_expires_at = 0
        self.base_url = 'https://api.weixin.qq.com/cgi-bin'

    def get_access_token(self):
        """
        获取access_token（带缓存）
        access_token有效期为7200秒

        Returns:
            str: access_token
        """
        now = time.time()
        if self.access_token and now < self.token_expires_at:
            return self.access_token

        url = f'{self.base_url}/token'
        params = {
            'grant_type': 'client_credential',
            'appid': self.app_id,
            'secret': self.app_secret
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if 'access_token' in data:
                self.access_token = data['access_token']
                self.token_expires_at = now + data.get('expires_in', 7200) - 300  # 提前5分钟刷新
                return self.access_token
            else:
                print(f'获取access_token失败: {data}')
                return None
        except Exception as e:
            print(f'获取access_token异常: {e}')
            return None

    def send_medication_reminder(self, openid, med_name, dosage, scheduled_time, user_level=1):
        """
        发送服药提醒模板消息

        Args:
            openid (str): 用户openid
            med_name (str): 药物名称
            dosage (str): 剂量
            scheduled_time (str): 计划服药时间
            user_level (int): 用户等级

        Returns:
            dict: 推送结果
        """
        template_data = {
            'touser': openid,
            'template_id': self.template_id,
            'url': 'https://your-domain.com/app.html',
            'data': {
                'first': {
                    'value': f'您有一条服药提醒',
                    'color': '#667eea'
                },
                'keyword1': {
                    'value': med_name,
                    'color': '#333'
                },
                'keyword2': {
                    'value': dosage,
                    'color': '#333'
                },
                'keyword3': {
                    'value': scheduled_time,
                    'color': '#333'
                },
                'keyword4': {
                    'value': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'color': '#999'
                },
                'remark': {
                    'value': '请及时服药，保持健康！',
                    'color': '#51cf66'
                }
            }
        }

        return self._send_template_message(template_data)

    def send_alert_notification(self, openid, med_name, alert_level, overdue_minutes):
        """
        发送预警通知模板消息

        Args:
            openid (str): 用户openid
            med_name (str): 药物名称
            alert_level (str): 预警等级（warn/urgent/critical）
            overdue_minutes (int): 超时分钟数

        Returns:
            dict: 推送结果
        """
        level_map = {
            'warn': '提醒',
            'urgent': '重要',
            'critical': '紧急'
        }
        level_text = level_map.get(alert_level, '提醒')
        color_map = {
            'warn': '#ffc107',
            'urgent': '#ff9800',
            'critical': '#ff5757'
        }
        color = color_map.get(alert_level, '#333')

        template_data = {
            'touser': openid,
            'template_id': self.template_id,
            'url': 'https://your-domain.com/app.html#alerts',
            'data': {
                'first': {
                    'value': f'【{level_text}】您有服药预警',
                    'color': color
                },
                'keyword1': {
                    'value': med_name,
                    'color': '#333'
                },
                'keyword2': {
                    'value': f'已超时 {overdue_minutes} 分钟',
                    'color': color
                },
                'keyword3': {
                    'value': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'color': '#999'
                },
                'remark': {
                    'value': '请尽快确认服药状态！',
                    'color': '#ff5757'
                }
            }
        }

        return self._send_template_message(template_data)

    def send_bp_report(self, openid, avg_sys, avg_dia, avg_hr, status):
        """
        发送血压报告模板消息

        Args:
            openid (str): 用户openid
            avg_sys (int): 平均收缩压
            avg_dia (int): 平均舒张压
            avg_hr (int): 平均心率
            status (str): 健康状态

        Returns:
            dict: 推送结果
        """
        template_data = {
            'touser': openid,
            'template_id': self.template_id,
            'url': 'https://your-domain.com/app.html#bp',
            'data': {
                'first': {
                    'value': '您的血压周报已生成',
                    'color': '#667eea'
                },
                'keyword1': {
                    'value': f'{avg_sys}/{avg_dia} mmHg',
                    'color': '#333'
                },
                'keyword2': {
                    'value': f'{avg_hr} 次/分',
                    'color': '#333'
                },
                'keyword3': {
                    'value': status,
                    'color': '#51cf66' if status == '正常' else '#ff5757'
                },
                'keyword4': {
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'color': '#999'
                },
                'remark': {
                    'value': '点击查看详细报告',
                    'color': '#667eea'
                }
            }
        }

        return self._send_template_message(template_data)

    def _send_template_message(self, template_data):
        """
        发送模板消息（内部方法）

        Args:
            template_data (dict): 模板数据

        Returns:
            dict: 推送结果
        """
        access_token = self.get_access_token()
        if not access_token:
            return {'success': False, 'error': '获取access_token失败'}

        url = f'{self.base_url}/message/template/send?access_token={access_token}'

        try:
            response = requests.post(
                url,
                json=template_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            data = response.json()

            if data.get('errcode') == 0:
                return {'success': True, 'msgid': data.get('msgid')}
            else:
                return {
                    'success': False,
                    'error': data.get('errmsg', '未知错误'),
                    'errcode': data.get('errcode')
                }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def verify_signature(self, signature, timestamp, nonce, token):
        """
        验证微信服务器签名（用于服务器配置验证）

        Args:
            signature (str): 微信加密签名
            timestamp (str): 时间戳
            nonce (str): 随机数
            token (str): 微信服务器配置的Token

        Returns:
            bool: 验证是否通过
        """
        try:
            tmp_list = [token, timestamp, nonce]
            tmp_list.sort()
            tmp_str = ''.join(tmp_list)
            tmp_str = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()
            return tmp_str == signature
        except Exception:
            return False
