from database import get_db

def view_all_accounts():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accounts')
    accounts = cursor.fetchall()
    conn.close()
    return accounts

def monitor_transactions():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def generate_report():
    accounts = view_all_accounts()
    transactions = monitor_transactions()
    report = {
        'total_accounts': len(accounts),
        'total_transactions': len(transactions),
        'transactions': transactions
    }
    return report

def handle_report():
    report = generate_report()
    print(f"Total accounts: {report['total_accounts']}")
    print(f"Total transactions: {report['total_transactions']}")
    for transaction in report['transactions']:
        print(transaction)
