"""
血压守护 - 数据库模型
包含用户、药物、血压记录、预警等核心模型
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

db = SQLAlchemy()

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # 关系
    family_members = db.relationship('FamilyMember', backref='owner', lazy='dynamic')
    
    def set_password(self, password):
        """设置密码"""
        from app.security import PasswordHasher
        self.password_hash = PasswordHasher.hash_password(password)
    
    def check_password(self, password):
        """验证密码"""
        from app.security import PasswordHasher
        return PasswordHasher.verify_password(password, self.password_hash)


class FamilyMember(db.Model):
    """家庭成员模型"""
    __tablename__ = 'family_members'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    relation = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    medications = db.relationship('Medication', backref='member', lazy='dynamic')
    blood_pressure_records = db.relationship('BloodPressureRecord', backref='member', lazy='dynamic')


class Medication(db.Model):
    """药物模型"""
    __tablename__ = 'medications'
    __table_args__ = (
        db.Index('idx_member_med', 'member_id', 'name'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('family_members.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(100))
    frequency = db.Column(db.String(50))
    times = db.Column(db.Text)  # JSON格式存储服药时间
    quantity = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BloodPressureRecord(db.Model):
    """血压记录模型"""
    __tablename__ = 'blood_pressure_records'
    __table_args__ = (
        db.Index('idx_member_time', 'member_id', 'record_time'),
        db.Index('idx_record_time', 'record_time'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('family_members.id'), nullable=False, index=True)
    systolic = db.Column(db.Integer, nullable=False)
    diastolic = db.Column(db.Integer, nullable=False)
    heart_rate = db.Column(db.Integer)
    note = db.Column(db.Text)
    record_time = db.Column(db.DateTime, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Alert(db.Model):
    """预警模型"""
    __tablename__ = 'alerts'
    __table_args__ = (
        db.Index('idx_member_status', 'member_id', 'status'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('family_members.id'), nullable=False, index=True)
    log_id = db.Column(db.Integer)
    med_name = db.Column(db.String(100))
    diff = db.Column(db.Integer)
    level = db.Column(db.String(20))  # normal, warn, urgent, critical
    status = db.Column(db.String(20), default='active', index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)


class CollaborationLog(db.Model):
    """协作日志模型"""
    __tablename__ = 'collaboration_logs'
    __table_args__ = (
        db.Index('idx_member_time', 'member_id', 'created_at'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('family_members.id'), nullable=False, index=True)
    action = db.Column(db.String(100), nullable=False)
    detail = db.Column(db.Text)
    operator = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)


def init_db(app):
    """初始化数据库"""
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        # 创建索引（如果不存在）
        try:
            from sqlalchemy import text
            with db.engine.connect() as conn:
                conn.execute(text('ALTER TABLE users ADD INDEX idx_username (username)'))
                conn.execute(text('ALTER TABLE family_members ADD INDEX idx_user_id (user_id)'))
        except Exception:
            pass  # 索引可能已存在
