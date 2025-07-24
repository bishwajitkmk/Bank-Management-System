from app import db
from app.models import Transaction, Account, User
from app.utils.validators import validate_amount
from datetime import datetime
from sqlalchemy import func

class TransactionService:
    @staticmethod
    def get_user_transactions(user_id, page=1, limit=10):
        """Get all transactions for a user across all accounts"""
        try:
            # Get user's account IDs
            account_ids = [acc.id for acc in Account.query.filter_by(user_id=user_id, is_active=True).all()]
            
            if not account_ids:
                return {
                    'transactions': [],
                    'total': 0,
                    'page': page,
                    'limit': limit,
                    'pages': 0
                }, 200
            
            # Get transactions with pagination
            offset = (page - 1) * limit
            transactions = Transaction.query.filter(Transaction.account_id.in_(account_ids))\
                .order_by(Transaction.created_at.desc())\
                .offset(offset)\
                .limit(limit)\
                .all()
            
            total = Transaction.query.filter(Transaction.account_id.in_(account_ids)).count()
            
            return {
                'transactions': [transaction.to_dict() for transaction in transactions],
                'total': total,
                'page': page,
                'limit': limit,
                'pages': (total + limit - 1) // limit
            }, 200
        except Exception as e:
            return {'error': 'Failed to fetch transactions'}, 500

    @staticmethod
    def get_transaction(user_id, transaction_id):
        """Get a specific transaction by ID"""
        try:
            # Get user's account IDs
            account_ids = [acc.id for acc in Account.query.filter_by(user_id=user_id, is_active=True).all()]
            
            transaction = Transaction.query.filter(
                Transaction.id == transaction_id,
                Transaction.account_id.in_(account_ids)
            ).first()
            
            if not transaction:
                return {'error': 'Transaction not found'}, 404
            
            return {'transaction': transaction.to_dict()}, 200
        except Exception as e:
            return {'error': 'Failed to fetch transaction'}, 500

    @staticmethod
    def create_transaction(user_id, account_id, transaction_type, amount, description=''):
        """Create a new transaction"""
        try:
            # Verify account belongs to user
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
            
            # Validate transaction type
            valid_types = ['deposit', 'withdrawal', 'transfer']
            if transaction_type not in valid_types:
                return {'error': 'Invalid transaction type'}, 400
            
            # Handle different transaction types
            if transaction_type == 'deposit':
                if not account.deposit(amount):
                    return {'error': 'Deposit failed'}, 400
                transaction_amount = amount
            elif transaction_type == 'withdrawal':
                if account.balance < amount:
                    return {'error': 'Insufficient balance'}, 400
                if not account.withdraw(amount):
                    return {'error': 'Withdrawal failed'}, 400
                transaction_amount = -amount
            else:
                return {'error': 'Invalid transaction type for this endpoint'}, 400
            
            # Create transaction record
            transaction = Transaction(
                account_id=account_id,
                transaction_type=transaction_type,
                amount=transaction_amount,
                description=description or transaction_type.capitalize()
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            return {
                'message': f'{transaction_type.capitalize()} successful',
                'transaction': transaction.to_dict(),
                'new_balance': account.balance
            }, 201
        except Exception as e:
            db.session.rollback()
            return {'error': 'Transaction failed'}, 500

    @staticmethod
    def transfer(user_id, from_account_id, to_account_id, amount, description=''):
        """Transfer money between accounts"""
        try:
            # Verify both accounts belong to user
            from_account = Account.query.filter_by(
                id=from_account_id, 
                user_id=user_id, 
                is_active=True
            ).first()
            
            to_account = Account.query.filter_by(
                id=to_account_id, 
                user_id=user_id, 
                is_active=True
            ).first()
            
            if not from_account or not to_account:
                return {'error': 'One or both accounts not found'}, 404
            
            if from_account_id == to_account_id:
                return {'error': 'Cannot transfer to the same account'}, 400
            
            # Validate amount
            is_valid, error = validate_amount(amount)
            if not is_valid:
                return {'error': error}, 400
            
            # Check sufficient balance
            if from_account.balance < amount:
                return {'error': 'Insufficient balance in source account'}, 400
            
            # Perform transfer
            if from_account.withdraw(amount) and to_account.deposit(amount):
                # Create transaction records
                from_transaction = Transaction(
                    account_id=from_account_id,
                    transaction_type='transfer',
                    amount=-amount,
                    description=description or f'Transfer to {to_account.account_number}'
                )
                
                to_transaction = Transaction(
                    account_id=to_account_id,
                    transaction_type='transfer',
                    amount=amount,
                    description=description or f'Transfer from {from_account.account_number}'
                )
                
                db.session.add(from_transaction)
                db.session.add(to_transaction)
                db.session.commit()
                
                return {
                    'message': 'Transfer successful',
                    'from_transaction': from_transaction.to_dict(),
                    'to_transaction': to_transaction.to_dict(),
                    'from_balance': from_account.balance,
                    'to_balance': to_account.balance
                }, 200
            else:
                return {'error': 'Transfer failed'}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': 'Transfer failed'}, 500

    @staticmethod
    def get_transaction_stats(user_id, start_date=None, end_date=None):
        """Get transaction statistics for a user"""
        try:
            # Get user's account IDs
            account_ids = [acc.id for acc in Account.query.filter_by(user_id=user_id, is_active=True).all()]
            
            if not account_ids:
                return {
                    'total_transactions': 0,
                    'total_deposits': 0,
                    'total_withdrawals': 0,
                    'total_transfers': 0,
                    'total_deposited': 0,
                    'total_withdrawn': 0,
                    'net_amount': 0
                }, 200
            
            # Build query
            query = Transaction.query.filter(Transaction.account_id.in_(account_ids))
            
            if start_date:
                query = query.filter(Transaction.created_at >= start_date)
            if end_date:
                query = query.filter(Transaction.created_at <= end_date)
            
            # Get transaction counts by type
            stats = db.session.query(
                Transaction.transaction_type,
                func.count(Transaction.id).label('count'),
                func.sum(Transaction.amount).label('total_amount')
            ).filter(Transaction.account_id.in_(account_ids))
            
            if start_date:
                stats = stats.filter(Transaction.created_at >= start_date)
            if end_date:
                stats = stats.filter(Transaction.created_at <= end_date)
            
            stats = stats.group_by(Transaction.transaction_type).all()
            
            # Calculate totals
            total_transactions = sum(stat.count for stat in stats)
            total_deposits = sum(stat.count for stat in stats if stat.transaction_type == 'deposit')
            total_withdrawals = sum(stat.count for stat in stats if stat.transaction_type == 'withdrawal')
            total_transfers = sum(stat.count for stat in stats if stat.transaction_type == 'transfer')
            
            total_deposited = sum(stat.total_amount for stat in stats if stat.transaction_type == 'deposit' and stat.total_amount > 0)
            total_withdrawn = abs(sum(stat.total_amount for stat in stats if stat.transaction_type == 'withdrawal' and stat.total_amount < 0))
            
            net_amount = sum(stat.total_amount for stat in stats)
            
            return {
                'total_transactions': total_transactions,
                'total_deposits': total_deposits,
                'total_withdrawals': total_withdrawals,
                'total_transfers': total_transfers,
                'total_deposited': total_deposited,
                'total_withdrawn': total_withdrawn,
                'net_amount': net_amount
            }, 200
        except Exception as e:
            return {'error': 'Failed to get transaction statistics'}, 500

    @staticmethod
    def export_transactions(user_id, format_type='csv', start_date=None, end_date=None, account_id=None):
        """Export transactions (placeholder for future implementation)"""
        try:
            # This is a placeholder - in a real implementation, you would:
            # 1. Generate CSV/Excel file
            # 2. Return file as response
            # 3. Handle different export formats
            
            return {
                'message': 'Export functionality will be implemented in future versions',
                'format': format_type,
                'filters': {
                    'start_date': start_date,
                    'end_date': end_date,
                    'account_id': account_id
                }
            }, 200
        except Exception as e:
            return {'error': 'Export failed'}, 500
