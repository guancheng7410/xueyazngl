"""
血压守护 - 应用工厂
创建和配置Flask应用
"""

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

def create_app(config_class=None):
    """创建Flask应用"""
    
    load_dotenv()
    
    app = Flask(__name__)
    
    if config_class is None:
        from app.config import ProductionConfig
        config_class = ProductionConfig
    
    app.config.from_object(config_class)
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    from app.models import init_db
    init_db(app)
    
    from app.security import init_security
    init_security(app)
    
    from app.logger import Logger
    Logger.setup_logger(app)
    
    from app.routes.auth import auth_bp
    from app.routes.medication import medication_bp
    from app.routes.bp import bp_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(medication_bp, url_prefix='/api/medication')
    app.register_blueprint(bp_bp, url_prefix='/api/bp')
    
    @app.route('/api/health')
    def health_check():
        return {'status': 'ok', 'version': app.config.get('VERSION', '2.0.0')}
    
    @app.errorhandler(404)
    def not_found(error):
        return {'success': False, 'message': '资源不存在'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'服务器内部错误: {str(error)}')
        return {'success': False, 'message': '服务器内部错误'}, 500
    
    return app
