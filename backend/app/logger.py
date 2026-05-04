"""
血压守护 - 日志系统
提供结构化日志记录、日志轮转、错误追踪等功能
"""

import logging
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from datetime import datetime

class Logger:
    """日志管理器"""
    
    @staticmethod
    def setup_logger(app):
        """配置应用日志"""
        
        # 确保日志目录存在
        log_dir = Path(app.config.get('LOG_FILE', 'logs/production.log')).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = app.config.get('LOG_FILE', 'logs/production.log')
        log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO').upper())
        
        # 主日志记录器
        app_logger = logging.getLogger('bp_guardian')
        app_logger.setLevel(log_level)
        
        # 文件处理器（按大小轮转）
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=10,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        
        # 错误日志（单独文件）
        error_log_file = str(Path(log_file).parent / 'error.log')
        error_handler = RotatingFileHandler(
            error_log_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=10,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        
        # 访问日志
        access_log_file = str(Path(log_file).parent / 'access.log')
        access_handler = TimedRotatingFileHandler(
            access_log_file,
            when='midnight',
            interval=1,
            backupCount=30,
            encoding='utf-8'
        )
        access_handler.setLevel(logging.INFO)
        
        # 日志格式
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)
        access_handler.setFormatter(formatter)
        
        # 添加处理器
        app_logger.addHandler(file_handler)
        app_logger.addHandler(error_handler)
        app_logger.addHandler(access_handler)
        
        # 开发环境也输出到控制台
        if app.debug:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            app_logger.addHandler(console_handler)
        
        app.logger = app_logger
        
        app.logger.info('日志系统初始化完成')
        return app_logger

# ==================== 日志装饰器 ====================

def log_api_call(func):
    """API调用日志装饰器"""
    from functools import wraps
    from flask import request
    
    @wraps(func)
    def decorated_function(*args, **kwargs):
        import time
        start_time = time.time()
        
        # 记录请求
        app = kwargs.get('app') or func.__globals__.get('current_app')
        if app and hasattr(app, 'logger'):
            app.logger.info(
                f"API请求: {request.method} {request.path} "
                f"IP: {request.remote_addr}"
            )
        
        try:
            result = func(*args, **kwargs)
            duration = int((time.time() - start_time) * 1000)
            
            if app and hasattr(app, 'logger'):
                app.logger.info(
                    f"API响应: {request.method} {request.path} "
                    f"耗时: {duration}ms"
                )
            
            return result
        except Exception as e:
            duration = int((time.time() - start_time) * 1000)
            
            if app and hasattr(app, 'logger'):
                app.logger.error(
                    f"API错误: {request.method} {request.path} "
                    f"耗时: {duration}ms 错误: {str(e)}",
                    exc_info=True
                )
            
            raise
    
    return decorated_function

# ==================== 审计日志 ====================

class AuditLogger:
    """审计日志记录器"""
    
    @staticmethod
    def log_action(app, user_id, action, detail, ip_address=None):
        """记录用户操作"""
        if hasattr(app, 'logger'):
            app.logger.info(
                f"审计日志 | 用户:{user_id} | 操作:{action} "
                f"| 详情:{detail} | IP:{ip_address or 'unknown'}"
            )
    
    @staticmethod
    def log_security_event(app, event_type, detail, severity='high'):
        """记录安全事件"""
        if hasattr(app, 'logger'):
            log_func = app.logger.error if severity == 'high' else app.logger.warning
            log_func(
                f"安全事件 | 类型:{event_type} | 详情:{detail} "
                f"| 严重程度:{severity}"
            )
