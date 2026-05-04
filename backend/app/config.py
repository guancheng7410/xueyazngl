"""
血压守护 - 生产环境配置文件
用于服务器部署，包含数据库、安全、日志等配置
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / 'instance'
INSTANCE_DIR.mkdir(parents=True, exist_ok=True)

class Config:
    """基础配置"""
    # 应用配置
    APP_NAME = '血压守护'
    VERSION = '2.0.0'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-to-random-secret-key-in-production')
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'sqlite:///' + str(INSTANCE_DIR / 'blood_pressure_guardian.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 20  # 连接池大小
    SQLALCHEMY_POOL_RECYCLE = 3600  # 连接回收时间（秒）
    SQLALCHEMY_MAX_OVERFLOW = 10  # 最大溢出连接数
    
    # 安全配置
    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_SECURE = True  # 仅HTTPS传输cookie
    SESSION_COOKIE_HTTPONLY = True  # 防止XSS攻击
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF保护
    PERMANENT_SESSION_LIFETIME = 86400  # 会话过期时间（24小时）
    
    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/production.log')
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    
    # 缓存配置
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300  # 5分钟


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # 显示SQL语句
    LOG_LEVEL = 'DEBUG'
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    
    # 必须设置的环境变量
    # SECRET_KEY: 使用 openssl rand -base64 32 生成
    # DATABASE_URL: MySQL或PostgreSQL连接字符串
    # WECHAT_APP_ID: 微信服务号AppID
    # WECHAT_APP_SECRET: 微信服务号AppSecret


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# 配置字典
config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
