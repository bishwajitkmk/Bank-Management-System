from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.account_service import AccountService
from app.utils.validators import validate_amount, sanitize_input

bp = Blueprint('accounts', __name__)

@bp.route('/', methods=['GET'])
@jwt_required()
def get_accounts():
    """Get all accounts for the current user"""
    current_user_id = get_jwt_identity()
    result, status_code = AccountService.get_user_accounts(current_user_id)
    return jsonify(result), status_code

@bp.route('/<int:account_id>', methods=['GET'])
@jwt_required()
def get_account(account_id):
    """Get a specific account by ID"""
    current_user_id = get_jwt_identity()
    result, status_code = AccountService.get_account(current_user_id, account_id)
    return jsonify(result), status_code

@bp.route('/', methods=['POST'])
@jwt_required()
def create_account():
    """Create a new account"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    account_type = data.get('account_type', 'savings')
    currency = data.get('currency', 'USD')
    
    if not account_type:
        return jsonify({'error': 'Account type is required'}), 400
    
    result, status_code = AccountService.create_account(current_user_id, account_type, currency)
    return jsonify(result), status_code

@bp.route('/<int:account_id>', methods=['PUT'])
@jwt_required()
def update_account(account_id):
    """Update account details"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    result, status_code = AccountService.update_account(current_user_id, account_id, data)
    return jsonify(result), status_code

@bp.route('/<int:account_id>', methods=['DELETE'])
@jwt_required()
def delete_account(account_id):
    """Delete an account"""
    current_user_id = get_jwt_identity()
    result, status_code = AccountService.delete_account(current_user_id, account_id)
    return jsonify(result), status_code

@bp.route('/<int:account_id>/balance', methods=['GET'])
@jwt_required()
def get_balance(account_id):
    """Get account balance"""
    current_user_id = get_jwt_identity()
    result, status_code = AccountService.get_balance(current_user_id, account_id)
    return jsonify(result), status_code

@bp.route('/<int:account_id>/deposit', methods=['POST'])
@jwt_required()
def deposit(account_id):
    """Deposit money into account"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    amount = data.get('amount')
    description = sanitize_input(data.get('description', ''))
    
    if not amount:
        return jsonify({'error': 'Amount is required'}), 400
    
    is_valid, error = validate_amount(amount)
    if not is_valid:
        return jsonify({'error': error}), 400
    
    result, status_code = AccountService.deposit(current_user_id, account_id, amount, description)
    return jsonify(result), status_code

@bp.route('/<int:account_id>/withdraw', methods=['POST'])
@jwt_required()
def withdraw(account_id):
    """Withdraw money from account"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    amount = data.get('amount')
    description = sanitize_input(data.get('description', ''))
    
    if not amount:
        return jsonify({'error': 'Amount is required'}), 400
    
    is_valid, error = validate_amount(amount)
    if not is_valid:
        return jsonify({'error': error}), 400
    
    result, status_code = AccountService.withdraw(current_user_id, account_id, amount, description)
    return jsonify(result), status_code

@bp.route('/<int:account_id>/transactions', methods=['GET'])
@jwt_required()
def get_account_transactions(account_id):
    """Get transactions for a specific account"""
    current_user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    result, status_code = AccountService.get_account_transactions(current_user_id, account_id, page, limit)
    return jsonify(result), status_code
