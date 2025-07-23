from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.services.auth_service import AuthService
from app.utils.validators import sanitize_input

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    is_admin = data.get('is_admin', False)
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    result, status_code = AuthService.register_user(username, password, email, is_admin)
    return jsonify(result), status_code

@bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT tokens"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    result, status_code = AuthService.login_user(username, password)
    return jsonify(result), status_code

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    return jsonify({'access_token': access_token}), 200

@bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    if not old_password or not new_password:
        return jsonify({'error': 'Old and new passwords are required'}), 400
    
    result, status_code = AuthService.change_password(current_user_id, old_password, new_password)
    return jsonify(result), status_code

@bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Request password reset"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username')
    email = data.get('email')
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    result, status_code = AuthService.reset_password(username, email)
    return jsonify(result), status_code

@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    current_user_id = get_jwt_identity()
    result, status_code = AuthService.get_user_profile(current_user_id)
    return jsonify(result), status_code

@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user (client should discard tokens)"""
    # In a more advanced implementation, you might want to blacklist the token
    return jsonify({'message': 'Logged out successfully'}), 200 