import sqlite3
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(username, password, is_admin=False):
    conn = get_db()
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password)
    try:
        cursor.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)', (username, hashed_password, is_admin))
        user_id = cursor.lastrowid
        cursor.execute('INSERT INTO accounts (user_id) VALUES (?)', (user_id,))
        account_id = cursor.lastrowid
        conn.commit()
        return {'message': 'User registered successfully', 'user_id': user_id, 'account_id': account_id}
    except sqlite3.IntegrityError:
        return {'error': 'User already exists'}
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    if user and check_password_hash(user[2], password):
        return {'message': 'Login successful', 'user_id': user[0], 'is_admin': user[3]}
    return {'error': 'Invalid username or password'}

def reset_password(username):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user:
            new_password = input("Enter new password: ")
            hashed_password = generate_password_hash(new_password)
            cursor.execute('UPDATE users SET password = ? WHERE username = ?', (hashed_password, username))
            conn.commit()
            return {'message': 'Password reset successful'}
        return {'error': 'User not found'}
    finally:
        conn.close()

def change_password(username, old_password, new_password):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user[2], old_password):
            hashed_password = generate_password_hash(new_password)
            cursor.execute('UPDATE users SET password = ? WHERE username = ?', (hashed_password, username))
            conn.commit()
            return {'message': 'Password change successful'}
        return {'error': 'Invalid old password'}
    finally:
        conn.close()

def recover_password(username):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user:
            print("Security question: What is your pet's name?")
            answer = input("Answer: ")
            if answer == "your_pet_name":  # Placeholder for actual security question logic
                new_password = input("Enter new password: ")
                hashed_password = generate_password_hash(new_password)
                cursor.execute('UPDATE users SET password = ? WHERE username = ?', (hashed_password, username))
                conn.commit()
                return {'message': 'Password recovery successful'}
            return {'error': 'Incorrect answer'}
        return {'error': 'User not found'}
    finally:
        conn.close()
