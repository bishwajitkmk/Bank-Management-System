import re
from datetime import datetime

def validate_username(username):
    """Validate username format"""
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters long"
    if len(username) > 20:
        return False, "Username must be less than 20 characters"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    return True, ""

def validate_password(password):
    """Validate password strength"""
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if len(password) > 128:
        return False, "Password must be less than 128 characters"
    return True, ""

def validate_email(email):
    """Validate email format"""
    if not email:
        return True, ""  # Email is optional
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    return True, ""

def validate_amount(amount):
    """Validate transaction amount"""
    try:
        amount = float(amount)
        if amount <= 0:
            return False, "Amount must be greater than 0"
        if amount > 1000000:  # $1M limit
            return False, "Amount cannot exceed $1,000,000"
        return True, ""
    except (ValueError, TypeError):
        return False, "Invalid amount format"

def validate_account_number(account_number):
    """Validate account number format"""
    if not account_number or len(account_number) != 10:
        return False, "Account number must be 10 digits"
    if not account_number.isdigit():
        return False, "Account number must contain only digits"
    return True, ""

def sanitize_input(text):
    """Sanitize user input"""
    if not text:
        return ""
    # Remove potentially dangerous characters
    text = re.sub(r'[<>"\']', '', text)
    return text.strip()

def validate_date_range(start_date, end_date):
    """Validate date range for reports"""
    try:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        if start > end:
            return False, "Start date must be before end date"
        
        # Check if range is not more than 1 year
        if (end - start).days > 365:
            return False, "Date range cannot exceed 1 year"
            
        return True, ""
    except ValueError:
        return False, "Invalid date format"
