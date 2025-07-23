from database import get_db

def deposit(account_id, amount):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', (amount, account_id))
    cursor.execute('INSERT INTO transactions (account_id, type, amount) VALUES (?, ?, ?)', (account_id, 'deposit', amount))
    conn.commit()
    cursor.execute('SELECT balance FROM accounts WHERE id = ?', (account_id,))
    new_balance = cursor.fetchone()[0]
    conn.close()
    return {'message': 'Deposit successful', 'new_balance': new_balance}

def withdraw(account_id, amount):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT balance FROM accounts WHERE id = ?', (account_id,))
    balance = cursor.fetchone()[0]
    if balance >= amount:
        cursor.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?', (amount, account_id))
        cursor.execute('INSERT INTO transactions (account_id, type, amount) VALUES (?, ?, ?)', (account_id, 'withdraw', amount))
        conn.commit()
        cursor.execute('SELECT balance FROM accounts WHERE id = ?', (account_id,))
        new_balance = cursor.fetchone()[0]
        conn.close()
        return {'message': 'Withdrawal successful', 'new_balance': new_balance}
    else:
        conn.close()
        return {'error': 'Insufficient funds'}

def transfer(from_account_id, to_account_id, amount):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT balance FROM accounts WHERE id = ?', (from_account_id,))
    balance = cursor.fetchone()[0]
    if balance >= amount:
        cursor.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?', (amount, from_account_id))
        cursor.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', (amount, to_account_id))
        cursor.execute('INSERT INTO transactions (account_id, type, amount) VALUES (?, ?, ?)', (from_account_id, 'transfer_out', amount))
        cursor.execute('INSERT INTO transactions (account_id, type, amount) VALUES (?, ?, ?)', (to_account_id, 'transfer_in', amount))
        conn.commit()
        cursor.execute('SELECT balance FROM accounts WHERE id = ?', (from_account_id,))
        from_new_balance = cursor.fetchone()[0]
        cursor.execute('SELECT balance FROM accounts WHERE id = ?', (to_account_id,))
        to_new_balance = cursor.fetchone()[0]
        conn.close()
        return {'message': 'Transfer successful', 'from_new_balance': from_new_balance, 'to_new_balance': to_new_balance}
    else:
        conn.close()
        return {'error': 'Insufficient funds'}
