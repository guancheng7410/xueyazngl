from flask import Blueprint, jsonify, request
from app.security import rate_limit

medication_bp = Blueprint('medication', __name__)

@medication_bp.route('/health', methods=['GET'])
@rate_limit(max_requests=200)
def health():
    return jsonify({'success': True, 'message': '药物服务正常'})

@medication_bp.route('/log', methods=['POST'])
@rate_limit(max_requests=100)
def add_log():
    data = request.json
    member_id = data.get('member_id')
    med_name = data.get('med_name')
    dose = data.get('dose', '')
    taken = data.get('taken', True)
    note = data.get('note', '')
    
    if not member_id or not med_name:
        return jsonify({'success': False, 'message': '成员ID和药物名称不能为空'}), 400
    
    return jsonify({
        'success': True,
        'message': '服药日志已记录',
        'data': {
            'member_id': member_id,
            'med_name': med_name,
            'dose': dose,
            'taken': taken,
            'status': 'completed' if taken else 'skipped'
        }
    })

@medication_bp.route('/log/<member_id>', methods=['GET'])
@rate_limit(max_requests=100)
def get_log(member_id):
    days = request.args.get('days', 7, type=int)
    
    log_summary = {
        'member_id': member_id,
        'period_days': days,
        'total_planned': 21,
        'total_taken': 19,
        'total_missed': 2,
        'compliance_rate': 90.5,
        'medications': [
            {'name': '氨氯地平', 'dose': '5mg', 'frequency': '每日一次', 'compliance': 95},
            {'name': '美托洛尔', 'dose': '25mg', 'frequency': '每日两次', 'compliance': 85}
        ]
    }
    
    return jsonify({
        'success': True,
        'message': '服药日志已获取',
        'data': log_summary
    })
