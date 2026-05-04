"""
血压守护 - 安全增强模块
提供密码加密、CSRF防护、XSS防护、速率限制等功能
"""

import hashlib
import hmac
import secrets
import re
from functools import wraps
from flask import request, jsonify, session
from datetime import datetime

# ==================== 密码加密 ====================
class PasswordHasher:
    """密码加密和验证"""
    
    @staticmethod
    def hash_password(password):
        """加密密码"""
        salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return f"{salt}${hashed.hex()}"
    
    @staticmethod
    def verify_password(password, hashed):
        """验证密码"""
        try:
            salt, hash_value = hashed.split('$')
            new_hash = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt.encode('utf-8'),
                100000
            )
            return hmac.compare_digest(new_hash.hex(), hash_value)
        except Exception:
            return False

# ==================== XSS防护 ====================
class XSSProtector:
    """XSS攻击防护"""
    
    # 危险标签和属性
    DANGEROUS_PATTERNS = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
        r'<iframe[^>]*>.*?</iframe>',
        r'<object[^>]*>.*?</object>',
        r'<embed[^>]*>.*?</embed>',
        r'<form[^>]*>',
        r'<input[^>]*>',
    ]
    
    @classmethod
    def sanitize(cls, text):
        """清理XSS攻击代码"""
        if not text:
            return text
        
        # 替换危险模式
        for pattern in cls.DANGEROUS_PATTERNS:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
        
        # HTML实体编码
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#x27;')
        
        return text
    
    @classmethod
    def validate_input(cls, data):
        """验证输入数据"""
        if isinstance(data, str):
            return cls.sanitize(data)
        elif isinstance(data, dict):
            return {k: cls.validate_input(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [cls.validate_input(item) for item in data]
        return data

# ==================== CSRF防护 ====================
class CSRFProtector:
    """CSRF攻击防护"""
    
    @staticmethod
    def generate_token():
        """生成CSRF Token"""
        return secrets.token_hex(32)
    
    @staticmethod
    def validate_token(request):
        """验证CSRF Token"""
        token = request.headers.get('X-CSRF-Token')
        session_token = session.get('csrf_token')
        
        if not token or not session_token:
            return False
        
        return hmac.compare_digest(token, session_token)
    
    @staticmethod
    def init_csrf(app):
        """初始化CSRF保护"""
        @app.before_request
        def set_csrf_token():
            if 'csrf_token' not in session:
                session['csrf_token'] = CSRFProtector.generate_token()
        
        @app.before_request
        def check_csrf():
            if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
                if not CSRFProtector.validate_token(request):
                    return jsonify({
                        'success': False,
                        'message': 'CSRF token验证失败'
                    }), 403

# ==================== 速率限制 ====================
class RateLimiter:
    """API速率限制"""
    
    def __init__(self):
        self.requests = {}
    
    def is_allowed(self, key, max_requests=100, window=3600):
        """检查是否允许请求"""
        now = datetime.now()
        
        if key not in self.requests:
            self.requests[key] = []
        
        # 清理过期记录
        self.requests[key] = [
            t for t in self.requests[key]
            if (now - t).total_seconds() < window
        ]
        
        if len(self.requests[key]) >= max_requests:
            return False
        
        self.requests[key].append(now)
        return True

# 全局速率限制器
rate_limiter = RateLimiter()

def rate_limit(max_requests=100, window=3600):
    """速率限制装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            
            if not rate_limiter.is_allowed(client_ip, max_requests, window):
                return jsonify({
                    'success': False,
                    'message': '请求过于频繁，请稍后再试'
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ==================== SQL注入防护 ====================
class SQLInjectionProtector:
    """SQL注入防护"""
    
    DANGEROUS_PATTERNS = [
        r'(\b(UNION|SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|EXEC)\b)',
        r'(--|#|/\*|\*/)',
        r'(\bOR\b\s+\d+=\d+)',
    ]
    
    @classmethod
    def validate(cls, text):
        """检查SQL注入"""
        if not text:
            return True
        
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return False
        
        return True

# ==================== 安全中间件 ====================
def init_security(app):
    """初始化所有安全功能"""
    
    # CSRF保护
    CSRFProtector.init_csrf(app)
    
    # 安全响应头
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response
    
    # 输入验证
    @app.before_request
    def validate_input():
        if request.is_json:
            data = request.get_json()
            if data:
                XSSProtector.validate_input(data)
