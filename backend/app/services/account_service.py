from app import db
from app.models import Account, Transaction, User
from app.utils.validators import validate_amount
from datetime import datetime

class AccountService:
    @staticmethod
    def get_user_accounts(user_id):
        """Get all accounts for a user"""
        try:
            accounts = Account.query.filter_by(user_id=user_id, is_active=True).all()
            return {
                'accounts': [account.to_dict() for account in accounts],
                'total': len(accounts)
            }, 200
        except Exception as e:
            return {'error': 'Failed to fetch accounts'}, 500

    @staticmethod
    def get_account(user_id, account_id):
        """Get a specific account by ID"""
        try:
            account = Account.query.filter_by(
                id=account_id, 
                user_id=user_id, 
                is_active=True
            ).first()
            
            if not account:
                return {'error': 'Account not found'}, 404
            
            return {'account': account.to_dict()}, 200
        except Exception as e:
            return {'error': 'Failed to fetch account'}, 500

    @staticmethod
    def create_account(user_id, account_type, currency='USD'):
        """Create a new account for a user"""
        try:
            # Validate account type
            valid_types = ['savings', 'checking', 'business']
            if account_type not in valid_types:
                return {'error': 'Invalid account type'}, 400
            
            # Create new account
            account = Account(
                user_id=user_id,
                account_type=account_type,
                currency=currency
            )
            
            db.session.add(account)
            db.session.commit()
            
            return {
                'message': 'Account created successfully',
                'account': account.to_dict()
            }, 201
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to create account'}, 500

    @staticmethod
    def update_account(user_id, account_id, data):
        """Update account details"""
        try:
            account = Account.query.filter_by(
                id=account_id, 
                user_id=user_id, 
                is_active=True
            ).first()
            
            if not account:
                return {'error': 'Account not found'}, 404
            
            # Update allowed fields
            if 'account_type' in data:
                valid_types = ['savings', 'checking', 'business']
                if data['account_type'] not in valid_types:
                    return {'error': 'Invalid account type'}, 400
                account.account_type = data['account_type']
            
            if 'currency' in data:
                account.currency = data['currency']
            
            account.updated_at = datetime.utcnow()
            db.session.commit()
            
            return {
                'message': 'Account updated successfully',
                'account': account.to_dict()
            }, 200
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to update account'}, 500

    @staticmethod
    def delete_account(user_id, account_id):
        """Delete an account (soft delete)"""
        try:
            account = Account.query.filter_by(
                id=account_id, 
                user_id=user_id, 
                is_active=True
            ).first()
            
            if not account:
                return {'error': 'Account not found'}, 404
            
            # Check if account has balance
            if account.balance > 0:
                return {'error': 'Cannot delete account with positive balance'}, 400
            
            # Soft delete
            account.is_active = False
            account.updated_at = datetime.utcnow()
            db.session.commit()
            
            return {'message': 'Account deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to delete account'}, 500

    @staticmethod
    def get_balance(user_id, account_id):
        """Get account balance"""
        try:
            account = Account.query.filter_by(
                id=account_id, 
                user_id=user_id, 
                is_active=True
            ).first()
            
            if not account:
                return {'error': 'Account not found'}, 404
            
            return {
                'balance': account.balance,
                'currency': account.currency
            }, 200
        except Exception as e:
            return {'error': 'Failed to get balance'}, 500

    @staticmethod
    def deposit(user_id, account_id, amount, description=''):
        """Deposit money into account"""
        try:
            account = Account.query.filter_by(
                id=account_id, 
                user_id=user_id, 
                is_active=True
            ).first()
            
            if not account:
                return {'error': 'Account not found'}, 404
            
            # Validate amount
            is_valid, error = validate_amount(amount)
            if not is_valid:
                return {'error': error}, 400
            
            # Perform deposit
            if account.deposit(amount):
                # Create transaction record
                transaction = Transaction(
                    account_id=account_id,
                    transaction_type='deposit',
                    amount=amount,
                    description=description or 'Deposit'
                )
                
                db.session.add(transaction)
                db.session.commit()
                
                return {
                    'message': 'Deposit successful',
                    'new_balance': account.balance,
                    'transaction': transaction.to_dict()
                }, 200
            else:
                return {'error': 'Deposit failed'}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': 'Deposit failed'}, 500

    @staticmethod
    def withdraw(user_id, account_id, amount, description=''):
        """Withdraw money from account"""
        try:
            account = Account.query.filter_by(
                id=account_id, 
                user_id=user_id, 
                is_active=True
            ).first()
            
            if not account:
                return {'error': 'Account not found'}, 404
            
            # Validate amount
            is_valid, error = validate_amount(amount)
            if not is_valid:
                return {'error': error}, 400
            
            # Check sufficient balance
            if account.balance < amount:
                return {'error': 'Insufficient balance'}, 400
            
            # Perform withdrawal
            if account.withdraw(amount):
                # Create transaction record
                transaction = Transaction(
                    account_id=account_id,
                    transaction_type='withdrawal',
                    amount=-amount,  # Negative for withdrawal
                    description=description or 'Withdrawal'
                )
                
                db.session.add(transaction)
                db.session.commit()
                
                return {
                    'message': 'Withdrawal successful',
                    'new_balance': account.balance,
                    'transaction': transaction.to_dict()
                }, 200
            else:
                return {'error': 'Withdrawal failed'}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': 'Withdrawal failed'}, 500

    @staticmethod
    def get_account_transactions(user_id, account_id, page=1, limit=10):
        """Get transactions for a specific account"""
        try:
            # Verify account belongs to user
            account = Account.query.filter_by(
                id=account_id, 
                user_id=user_id, 
                is_active=True
            ).first()
            
            if not account:
                return {'error': 'Account not found'}, 404
            
            # Get transactions with pagination
            offset = (page - 1) * limit
            transactions = Transaction.query.filter_by(account_id=account_id)\
                .order_by(Transaction.created_at.desc())\
                .offset(offset)\
                .limit(limit)\
                .all()
            
            total = Transaction.query.filter_by(account_id=account_id).count()
            
            return {
                'transactions': [transaction.to_dict() for transaction in transactions],
                'total': total,
                'page': page,
                'limit': limit,
                'pages': (total + limit - 1) // limit
            }, 200
        except Exception as e:
            return {'error': 'Failed to fetch transactions'}, 500
