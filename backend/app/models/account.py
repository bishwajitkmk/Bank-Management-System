from app import db
from datetime import datetime

class Account(db.Model):
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    account_type = db.Column(db.String(20), default='savings')  # savings, checking, business
    balance = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(3), default='USD')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transactions = db.relationship('Transaction', backref='account', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, user_id, account_type='savings', currency='USD'):
        self.user_id = user_id
        self.account_type = account_type
        self.currency = currency
        self.account_number = self.generate_account_number()
    
    def generate_account_number(self):
        """Generate a unique account number"""
        import random
        import string
        # Generate a 10-digit account number
        account_number = ''.join(random.choices(string.digits, k=10))
        # Check if it already exists
        while Account.query.filter_by(account_number=account_number).first():
            account_number = ''.join(random.choices(string.digits, k=10))
        return account_number
    
    def deposit(self, amount):
        """Deposit money into account"""
        if amount > 0:
            self.balance += amount
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def withdraw(self, amount):
        """Withdraw money from account"""
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def get_balance(self):
        """Get current balance"""
        return self.balance
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'account_number': self.account_number,
            'account_type': self.account_type,
            'balance': self.balance,
            'currency': self.currency,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Account {self.account_number}>'
