from flask import Blueprint, jsonify, request
from app.security import rate_limit
from datetime import datetime

medication_bp = Blueprint('medication', __name__)

# 模拟数据库存储
medications_db = {}
inventory_logs = []

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

@medication_bp.route('/add', methods=['POST'])
@rate_limit(max_requests=100)
def add_medication():
    data = request.json
    med_id = data.get('med_id')
    name = data.get('name')
    dose = data.get('dose')
    frequency = data.get('frequency', '每日一次')
    quantity = data.get('quantity', 0)
    member_id = data.get('member_id')
    
    if not name or not dose:
        return jsonify({'success': False, 'message': '药物名称和剂量不能为空'}), 400
    
    if not med_id:
        med_id = f"med_{datetime.now().timestamp()}"
    
    medications_db[med_id] = {
        'med_id': med_id,
        'name': name,
        'dose': dose,
        'frequency': frequency,
        'quantity': quantity,
        'member_id': member_id,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    return jsonify({
        'success': True,
        'message': '药物添加成功',
        'data': medications_db[med_id]
    })

@medication_bp.route('/list', methods=['GET'])
@rate_limit(max_requests=100)
def list_medications():
    member_id = request.args.get('member_id')
    
    meds = []
    for med_id, med in medications_db.items():
        if not member_id or med.get('member_id') == member_id:
            meds.append(med)
    
    return jsonify({
        'success': True,
        'message': '药物列表已获取',
        'data': {
            'medications': meds,
            'total': len(meds)
        }
    })

@medication_bp.route('/quantity/adjust', methods=['POST'])
@rate_limit(max_requests=100)
def adjust_quantity():
    data = request.json
    med_id = data.get('med_id')
    adjust_type = data.get('adjust_type')
    quantity = data.get('quantity', 0)
    reason = data.get('reason', '')
    
    if not med_id:
        return jsonify({'success': False, 'message': '药物ID不能为空'}), 400
    
    if med_id not in medications_db:
        return jsonify({'success': False, 'message': '药物不存在'}), 404
    
    med = medications_db[med_id]
    old_quantity = med['quantity']
    
    if adjust_type == 'increase':
        med['quantity'] += quantity
        log_action = '增加'
    elif adjust_type == 'decrease':
        if med['quantity'] < quantity:
            return jsonify({'success': False, 'message': f'当前库存不足，当前数量: {med["quantity"]}'}), 400
        med['quantity'] -= quantity
        log_action = '减少'
    elif adjust_type == 'set':
        med['quantity'] = quantity
        log_action = '设置'
    else:
        return jsonify({'success': False, 'message': '调整类型无效，支持: increase/decrease/set'}), 400
    
    med['updated_at'] = datetime.now().isoformat()
    
    log_entry = {
        'log_id': f"log_{datetime.now().timestamp()}",
        'med_id': med_id,
        'med_name': med['name'],
        'action': log_action,
        'old_quantity': old_quantity,
        'new_quantity': med['quantity'],
        'change': quantity,
        'reason': reason,
        'created_at': datetime.now().isoformat()
    }
    inventory_logs.append(log_entry)
    
    return jsonify({
        'success': True,
        'message': f'药物数量已{log_action}',
        'data': {
            'medication': med,
            'log': log_entry
        }
    })

@medication_bp.route('/quantity/replenish', methods=['POST'])
@rate_limit(max_requests=100)
def replenish_quantity():
    data = request.json
    med_id = data.get('med_id')
    purchase_quantity = data.get('purchase_quantity', 0)
    purchase_date = data.get('purchase_date')
    purchase_source = data.get('purchase_source', '')
    
    if not med_id:
        return jsonify({'success': False, 'message': '药物ID不能为空'}), 400
    
    if med_id not in medications_db:
        return jsonify({'success': False, 'message': '药物不存在'}), 404
    
    if purchase_quantity <= 0:
        return jsonify({'success': False, 'message': '购买数量必须大于0'}), 400
    
    med = medications_db[med_id]
    old_quantity = med['quantity']
    med['quantity'] += purchase_quantity
    med['updated_at'] = datetime.now().isoformat()
    
    log_entry = {
        'log_id': f"log_{datetime.now().timestamp()}",
        'med_id': med_id,
        'med_name': med['name'],
        'action': '购买补充',
        'old_quantity': old_quantity,
        'new_quantity': med['quantity'],
        'change': purchase_quantity,
        'reason': f'购买补充 (来源: {purchase_source})',
        'purchase_date': purchase_date or datetime.now().isoformat(),
        'purchase_source': purchase_source,
        'created_at': datetime.now().isoformat()
    }
    inventory_logs.append(log_entry)
    
    return jsonify({
        'success': True,
        'message': '药物库存已补充',
        'data': {
            'medication': med,
            'log': log_entry
        }
    })

@medication_bp.route('/quantity/history', methods=['GET'])
@rate_limit(max_requests=100)
def get_quantity_history():
    med_id = request.args.get('med_id')
    
    logs = inventory_logs
    if med_id:
        logs = [log for log in logs if log.get('med_id') == med_id]
    
    return jsonify({
        'success': True,
        'message': '库存历史已获取',
        'data': {
            'logs': logs,
            'total': len(logs)
        }
    })

@medication_bp.route('/quantity/warning', methods=['GET'])
@rate_limit(max_requests=100)
def get_quantity_warning():
    threshold = request.args.get('threshold', 10, type=int)
    
    warning_meds = []
    for med_id, med in medications_db.items():
        if med.get('quantity', 0) < threshold:
            warning_meds.append({
                'med_id': med_id,
                'name': med['name'],
                'dose': med['dose'],
                'quantity': med['quantity'],
                'threshold': threshold,
                'warning_level': 'critical' if med['quantity'] == 0 else 'warning'
            })
    
    return jsonify({
        'success': True,
        'message': '库存预警已获取',
        'data': {
            'warning_medications': warning_meds,
            'total_warnings': len(warning_meds),
            'threshold': threshold
        }
    })
