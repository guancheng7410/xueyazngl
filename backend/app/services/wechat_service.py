import requests
import hashlib
import time
from datetime import datetime

class WeChatService:
    def __init__(self):
        self.app_id = None
        self.app_secret = None
        self.access_token = None
        self.token_expires_at = 0
    
    def init_app(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
    
    def get_access_token(self):
        if not self.app_id or not self.app_secret:
            return None
        
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
        
        url = f'https://api.weixin.qq.com/cgi-bin/token'
        params = {
            'grant_type': 'client_credential',
            'appid': self.app_id,
            'secret': self.app_secret
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            if 'access_token' in data:
                self.access_token = data['access_token']
                self.token_expires_at = time.time() + data.get('expires_in', 7200) - 200
                return self.access_token
        except:
            pass
        
        return None
    
    def send_template_message(self, openid, template_id, data, miniprogram=None):
        token = self.get_access_token()
        if not token:
            return False
        
        url = f'https://api.weixin.qq.com/cgi-bin/message/template/send'
        params = {'access_token': token}
        
        payload = {
            'touser': openid,
            'template_id': template_id,
            'data': data
        }
        
        if miniprogram:
            payload['miniprogram'] = miniprogram
        
        try:
            response = requests.post(url, params=params, json=payload, timeout=5)
            result = response.json()
            return result.get('errcode') == 0
        except:
            return False
    
    def send_subscribe_message(self, openid, template_id, data):
        token = self.get_access_token()
        if not token:
            return False
        
        url = f'https://api.weixin.qq.com/cgi-bin/message/subscribe/send'
        params = {'access_token': token}
        
        payload = {
            'touser': openid,
            'template_id': template_id,
            'data': data
        }
        
        try:
            response = requests.post(url, params=params, json=payload, timeout=5)
            result = response.json()
            return result.get('errcode') == 0
        except:
            return False
    
    def generate_js_signature(self, url):
        token = self.get_access_token()
        if not token:
            return None
        
        timestamp = str(int(time.time()))
        nonce = hashlib.md5(str(time.time()).encode()).hexdigest()[:16]
        
        url_info = f'jsapi&noncestr={nonce}&timestamp={timestamp}&url={url}'
        
        return {
            'appId': self.app_id,
            'timestamp': timestamp,
            'nonceStr': nonce,
            'signature': hashlib.sha1(url_info.encode()).hexdigest()
        }


wechat_service = WeChatService()
