from app import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # deposit, withdraw, transfer_in, transfer_out
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    reference_number = db.Column(db.String(50), unique=True)
    status = db.Column(db.String(20), default='completed')  # pending, completed, failed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # For transfers
    related_transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=True)
    related_transaction = db.relationship('Transaction', remote_side=[id], backref='related_transactions')
    
    def __init__(self, account_id, transaction_type, amount, description=None):
        self.account_id = account_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.description = description
        self.reference_number = self.generate_reference_number()
    
    def generate_reference_number(self):
        """Generate a unique reference number"""
        import random
        import string
        # Generate a 12-character reference number
        ref_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        # Check if it already exists
        while Transaction.query.filter_by(reference_number=ref_number).first():
            ref_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        return ref_number
    
    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'transaction_type': self.transaction_type,
            'amount': self.amount,
            'description': self.description,
            'reference_number': self.reference_number,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'related_transaction_id': self.related_transaction_id
        }
    
    def __repr__(self):
        return f'<Transaction {self.reference_number}>'
