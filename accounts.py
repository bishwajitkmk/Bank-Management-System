import sqlite3
from database import get_db

def create_account(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO accounts (user_id) VALUES (?)', (user_id,))
    conn.commit()
    return {'message': 'Account created successfully'}

def get_account_details(account_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accounts WHERE id = ?', (account_id,))
    account = cursor.fetchone()
    if account:
        return {'account_id': account[0], 'user_id': account[1], 'balance': account[2]}
    return {'error': 'Account not found'}
