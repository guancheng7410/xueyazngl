from datetime import datetime, timedelta
from app.models import db, Alert, FamilyMember, User

class AlertService:
    LEVEL_INFO = 'info'
    LEVEL_WARNING = 'warning'
    LEVEL_URGENT = 'urgent'
    LEVEL_EMERGENCY = 'emergency'
    
    @staticmethod
    def create_alert(member_id, level, message, log_id=None):
        alert = Alert(
            member_id=member_id,
            log_id=log_id,
            level=level,
            status='active',
            created_at=datetime.utcnow()
        )
        db.session.add(alert)
        db.session.commit()
        return alert
    
    @staticmethod
    def check_and_create_alerts():
        """检查并创建预警（简化版，未实现完整逻辑）"""
        pass
    
    @staticmethod
    def get_active_alerts(member_id=None):
        query = Alert.query.filter_by(status='active')
        
        if member_id:
            query = query.filter_by(member_id=member_id)
        
        return query.order_by(Alert.created_at.desc()).all()
    
    @staticmethod
    def resolve_alert(alert_id, user_id):
        alert = Alert.query.get_or_404(alert_id)
        alert.status = 'resolved'
        alert.resolved_at = datetime.utcnow()
        db.session.commit()
        return alert
