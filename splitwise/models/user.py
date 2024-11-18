from werkzeug.security import generate_password_hash, check_password_hash
from .. import db

class User(db.Model):
    """User account model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Relationships
    expenses = db.relationship('Expense', back_populates='paid_by', lazy='dynamic')
    group_memberships = db.relationship('GroupMembership', back_populates='user', lazy='dynamic')
    categories = db.relationship('ExpenseCategory', back_populates='user', lazy='dynamic')

    def set_password(self, password):
        """Create hashed password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password_hash, password)
