from flask import Blueprint, jsonify
from app.security import rate_limit

bp_bp = Blueprint('bp', __name__)

@bp_bp.route('/health', methods=['GET'])
@rate_limit(max_requests=200)
def health():
    return jsonify({'success': True, 'message': '血压服务正常'})
