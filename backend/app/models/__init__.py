from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(100), unique=True, nullable=False)
    nickname = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), default='child')
    avatar_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    family_groups = db.relationship('FamilyMember', back_populates='user', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'openid': self.openid,
            'nickname': self.nickname,
            'phone': self.phone,
            'role': self.role,
            'avatar_url': self.avatar_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class FamilyGroup(db.Model):
    __tablename__ = 'family_groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    invite_code = db.Column(db.String(20), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    members = db.relationship('FamilyMember', back_populates='family_group', lazy='dynamic')
    parents = db.relationship('Parent', back_populates='family_group', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'creator_id': self.creator_id,
            'invite_code': self.invite_code,
            'member_count': self.members.count(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class FamilyMember(db.Model):
    __tablename__ = 'family_members'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    family_group_id = db.Column(db.Integer, db.ForeignKey('family_groups.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='family_groups')
    family_group = db.relationship('FamilyGroup', back_populates='members')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'family_group_id': self.family_group_id,
            'role': self.role,
            'user': self.user.to_dict() if self.user else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Parent(db.Model):
    __tablename__ = 'parents'

    id = db.Column(db.Integer, primary_key=True)
    family_group_id = db.Column(db.Integer, db.ForeignKey('family_groups.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    avatar_url = db.Column(db.String(200))
    health_status = db.Column(db.String(20), default='normal')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    family_group = db.relationship('FamilyGroup', back_populates='parents')
    medications = db.relationship('Medication', back_populates='parent', lazy='dynamic')
    blood_pressure_records = db.relationship('BloodPressureRecord', back_populates='parent', lazy='dynamic')
    medication_logs = db.relationship('MedicationLog', back_populates='parent', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'family_group_id': self.family_group_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'avatar_url': self.avatar_url,
            'health_status': self.health_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Medication(db.Model):
    __tablename__ = 'medications'
    __table_args__ = (
        db.Index('idx_parent_med', 'parent_id', 'name'),
    )

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50))
    frequency = db.Column(db.String(50))
    times = db.Column(db.JSON)
    duration = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    reminder_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    parent = db.relationship('Parent', back_populates='medications')
    logs = db.relationship('MedicationLog', back_populates='medication', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'name': self.name,
            'dosage': self.dosage,
            'frequency': self.frequency,
            'times': self.times,
            'duration': self.duration,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'reminder_enabled': self.reminder_enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class MedicationLog(db.Model):
    __tablename__ = 'medication_logs'
    __table_args__ = (
        db.Index('idx_med_log_parent_status', 'parent_id', 'status'),
    )

    id = db.Column(db.Integer, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey('medications.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    actual_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')
    confirmed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    medication = db.relationship('Medication', back_populates='logs')
    parent = db.relationship('Parent', back_populates='medication_logs')
    confirmer = db.relationship('User', foreign_keys=[confirmed_by])

    def to_dict(self):
        return {
            'id': self.id,
            'medication_id': self.medication_id,
            'parent_id': self.parent_id,
            'medication_name': self.medication.name if self.medication else (self.note or 'Manual'),
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'actual_time': self.actual_time.isoformat() if self.actual_time else None,
            'status': self.status,
            'confirmed_by': self.confirmed_by,
            'note': self.note,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class BloodPressureRecord(db.Model):
    __tablename__ = 'blood_pressure_records'
    __table_args__ = (
        db.Index('idx_parent_time', 'parent_id', 'measured_at'),
        db.Index('idx_measured_at', 'measured_at'),
    )

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False)
    systolic = db.Column(db.Integer, nullable=False)
    diastolic = db.Column(db.Integer, nullable=False)
    heart_rate = db.Column(db.Integer)
    measured_at = db.Column(db.DateTime, default=datetime.utcnow)
    recorded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    note = db.Column(db.Text)

    parent = db.relationship('Parent', back_populates='blood_pressure_records')
    recorder = db.relationship('User', foreign_keys=[recorded_by])

    def to_dict(self):
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'systolic': self.systolic,
            'diastolic': self.diastolic,
            'heart_rate': self.heart_rate,
            'measured_at': self.measured_at.isoformat() if self.measured_at else None,
            'recorded_by': self.recorded_by,
            'note': self.note
        }


class Alert(db.Model):
    __tablename__ = 'alerts'
    __table_args__ = (
        db.Index('idx_alert_parent_status', 'parent_id', 'status'),
    )

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False)
    medication_log_id = db.Column(db.Integer, db.ForeignKey('medication_logs.id'))
    level = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='active')
    resolved_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'medication_log_id': self.medication_log_id,
            'level': self.level,
            'message': self.message,
            'status': self.status,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'resolved_by': self.resolved_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class MedicationInventory(db.Model):
    __tablename__ = 'medication_inventory'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False)
    medication_id = db.Column(db.Integer, db.ForeignKey('medications.id'), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    unit = db.Column(db.String(20))
    remind_threshold = db.Column(db.Integer, default=7)
    last_reminded_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'medication_id': self.medication_id,
            'quantity': self.quantity,
            'unit': self.unit,
            'remind_threshold': self.remind_threshold,
            'last_reminded_at': self.last_reminded_at.isoformat() if self.last_reminded_at else None
        }


def init_db(app):
    """初始化数据库"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
