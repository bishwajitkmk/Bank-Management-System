from app import db
from app.models import User
from app.utils.validators import validate_username, validate_password, validate_email, sanitize_input
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import datetime

class AuthService:
    @staticmethod
    def register_user(username, password, email=None, is_admin=False):
        """Register a new user"""
        # Validate input
        username = sanitize_input(username)
        email = sanitize_input(email) if email else None
        
        is_valid, error = validate_username(username)
        if not is_valid:
            return {'error': error}, 400
        
        is_valid, error = validate_password(password)
        if not is_valid:
            return {'error': error}, 400
        
        if email:
            is_valid, error = validate_email(email)
            if not is_valid:
                return {'error': error}, 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {'error': 'Username already exists'}, 409
        
        if email:
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                return {'error': 'Email already registered'}, 409
        
        try:
            # Create new user
            user = User(username=username, password=password, email=email, is_admin=is_admin)
            db.session.add(user)
            db.session.commit()
            
            # Create default account for user
            from app.models import Account
            account = Account(user_id=user.id)
            db.session.add(account)
            db.session.commit()
            
            return {
                'message': 'User registered successfully',
                'user_id': user.id,
                'account_id': account.id,
                'account_number': account.account_number
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': 'Registration failed'}, 500
    
    @staticmethod
    def login_user(username, password):
        """Authenticate user and return tokens"""
        username = sanitize_input(username)
        
        if not username or not password:
            return {'error': 'Username and password are required'}, 400
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return {'error': 'Invalid username or password'}, 401
        
        if not user.is_active:
            return {'error': 'Account is deactivated'}, 403
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return {
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }, 200
    
    @staticmethod
    def change_password(user_id, old_password, new_password):
        """Change user password"""
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        if not user.check_password(old_password):
            return {'error': 'Invalid old password'}, 401
        
        is_valid, error = validate_password(new_password)
        if not is_valid:
            return {'error': error}, 400
        
        try:
            user.set_password(new_password)
            db.session.commit()
            return {'message': 'Password changed successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': 'Password change failed'}, 500
    
    @staticmethod
    def reset_password(username, email=None):
        """Reset password (simplified version - in production would send email)"""
        username = sanitize_input(username)
        
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'error': 'User not found'}, 404
        
        if email and user.email != email:
            return {'error': 'Email does not match'}, 400
        
        # In a real application, you would:
        # 1. Generate a secure reset token
        # 2. Send email with reset link
        # 3. User clicks link and sets new password
        
        # For demo purposes, we'll just return a success message
        return {
            'message': 'Password reset instructions sent to your email',
            'note': 'In production, this would send an actual email'
        }, 200
    
    @staticmethod
    def get_user_profile(user_id):
        """Get user profile information"""
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        return {'user': user.to_dict()}, 200
