from flask import Blueprint, jsonify
from app.security import rate_limit

medication_bp = Blueprint('medication', __name__)

@medication_bp.route('/health', methods=['GET'])
@rate_limit(max_requests=200)
def health():
    return jsonify({'success': True, 'message': '药物服务正常'})
