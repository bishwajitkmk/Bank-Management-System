from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.transaction_service import TransactionService
from app.utils.validators import validate_amount, sanitize_input

bp = Blueprint('transactions', __name__)

@bp.route('/', methods=['GET'])
@jwt_required()
def get_transactions():
    """Get all transactions for the current user"""
    current_user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    result, status_code = TransactionService.get_user_transactions(current_user_id, page, limit)
    return jsonify(result), status_code

@bp.route('/<int:transaction_id>', methods=['GET'])
@jwt_required()
def get_transaction(transaction_id):
    """Get a specific transaction by ID"""
    current_user_id = get_jwt_identity()
    result, status_code = TransactionService.get_transaction(current_user_id, transaction_id)
    return jsonify(result), status_code

@bp.route('/', methods=['POST'])
@jwt_required()
def create_transaction():
    """Create a new transaction"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    account_id = data.get('account_id')
    transaction_type = data.get('transaction_type')
    amount = data.get('amount')
    description = sanitize_input(data.get('description', ''))
    
    if not account_id or not transaction_type or not amount:
        return jsonify({'error': 'Account ID, transaction type, and amount are required'}), 400
    
    is_valid, error = validate_amount(amount)
    if not is_valid:
        return jsonify({'error': error}), 400
    
    result, status_code = TransactionService.create_transaction(
        current_user_id, account_id, transaction_type, amount, description
    )
    return jsonify(result), status_code

@bp.route('/transfer', methods=['POST'])
@jwt_required()
def transfer():
    """Transfer money between accounts"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    from_account_id = data.get('from_account_id')
    to_account_id = data.get('to_account_id')
    amount = data.get('amount')
    description = sanitize_input(data.get('description', ''))
    
    if not from_account_id or not to_account_id or not amount:
        return jsonify({'error': 'From account, to account, and amount are required'}), 400
    
    if from_account_id == to_account_id:
        return jsonify({'error': 'Cannot transfer to the same account'}), 400
    
    is_valid, error = validate_amount(amount)
    if not is_valid:
        return jsonify({'error': error}), 400
    
    result, status_code = TransactionService.transfer(
        current_user_id, from_account_id, to_account_id, amount, description
    )
    return jsonify(result), status_code

@bp.route('/stats', methods=['GET'])
@jwt_required()
def get_transaction_stats():
    """Get transaction statistics"""
    current_user_id = get_jwt_identity()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    result, status_code = TransactionService.get_transaction_stats(
        current_user_id, start_date, end_date
    )
    return jsonify(result), status_code

@bp.route('/export', methods=['GET'])
@jwt_required()
def export_transactions():
    """Export transactions"""
    current_user_id = get_jwt_identity()
    format_type = request.args.get('format', 'csv')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    account_id = request.args.get('account_id')
    
    result, status_code = TransactionService.export_transactions(
        current_user_id, format_type, start_date, end_date, account_id
    )
    return result, status_code
