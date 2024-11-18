from enum import Enum
from datetime import datetime
from .. import db

class SplitType(Enum):
    EQUAL = 'equal'
    EXACT = 'exact'
    PERCENTAGE = 'percentage'

class ExpenseCategory(db.Model):
    """Expense category model"""
    __tablename__ = 'expense_category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_category_user_id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='categories')
    expenses = db.relationship('Expense', back_populates='category', lazy='dynamic')

class Expense(db.Model):
    """Expense model"""
    __tablename__ = 'expense'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Foreign Keys
    paid_by_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_expense_paid_by_id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id', name='fk_expense_group_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('expense_category.id', name='fk_expense_category_id'))
    
    # Relationships
    paid_by = db.relationship('User', back_populates='expenses')
    group = db.relationship('Group', back_populates='expenses')
    splits = db.relationship('ExpenseSplit', back_populates='expense', lazy='dynamic')
    category = db.relationship('ExpenseCategory', back_populates='expenses')

class ExpenseSplit(db.Model):
    """Expense split model"""
    __tablename__ = 'expense_split'
    
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id', name='fk_split_expense_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_split_user_id'), nullable=False)
    split_type = db.Column(db.Enum(SplitType), nullable=False)
    amount_or_percentage = db.Column(db.Float, nullable=False)
    
    # Relationships
    expense = db.relationship('Expense', back_populates='splits')
    user = db.relationship('User')
