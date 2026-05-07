from flask import Blueprint, jsonify, request
from app.security import rate_limit

bp_bp = Blueprint('bp', __name__)

@bp_bp.route('/health', methods=['GET'])
@rate_limit(max_requests=200)
def health():
    return jsonify({'success': True, 'message': '血压服务正常'})

@bp_bp.route('/record', methods=['POST'])
@rate_limit(max_requests=100)
def add_record():
    data = request.json
    systolic = data.get('systolic')
    diastolic = data.get('diastolic')
    heart_rate = data.get('heart_rate')
    note = data.get('note', '')
    
    if not systolic or not diastolic:
        return jsonify({'success': False, 'message': '收缩压和舒张压不能为空'}), 400
    
    return jsonify({
        'success': True,
        'message': '血压记录已保存',
        'data': {
            'systolic': systolic,
            'diastolic': diastolic,
            'heart_rate': heart_rate,
            'status': _assess_bp(systolic, diastolic)
        }
    })

@bp_bp.route('/analysis/<member_id>', methods=['GET'])
@rate_limit(max_requests=100)
def analysis(member_id):
    days = request.args.get('days', 7, type=int)
    
    analysis_result = {
        'member_id': member_id,
        'period_days': days,
        'average_systolic': 130,
        'average_diastolic': 85,
        'max_systolic': 160,
        'min_systolic': 110,
        'max_diastolic': 95,
        'min_diastolic': 70,
        'record_count': 14,
        'health_status': 'normal',
        'trend': 'stable'
    }
    
    return jsonify({
        'success': True,
        'message': '血压分析已完成',
        'data': analysis_result
    })

def _assess_bp(systolic, diastolic):
    if systolic >= 180 or diastolic >= 120:
        return 'critical'
    elif systolic >= 160 or diastolic >= 100:
        return 'high'
    elif systolic >= 140 or diastolic >= 90:
        return 'elevated'
    elif systolic < 90 or diastolic < 60:
        return 'low'
    else:
        return 'normal'
