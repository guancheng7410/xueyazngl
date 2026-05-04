from flask import Blueprint, jsonify
from app.security import rate_limit

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/health', methods=['GET'])
@rate_limit(max_requests=200)
def health():
    return jsonify({'success': True, 'message': '认证服务正常'})
