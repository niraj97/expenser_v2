from .. import db
from datetime import datetime

class Group(db.Model):
    """Expense group model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    memberships = db.relationship('GroupMembership', back_populates='group', lazy='dynamic')
    expenses = db.relationship('Expense', back_populates='group', lazy='dynamic')

class GroupMembership(db.Model):
    """Association between users and groups"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    role = db.Column(db.String(20), default='member')  # admin, member
    
    # Relationships
    user = db.relationship('User', back_populates='group_memberships')
    group = db.relationship('Group', back_populates='memberships')
