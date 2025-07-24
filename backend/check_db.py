#!/usr/bin/env python3
"""
Simple script to check database state
"""

from app import create_app, db
from app.models import User, Account

def check_database():
    app = create_app()
    with app.app_context():
        print("=== Database Status ===")
        print(f"Users: {User.query.count()}")
        print(f"Accounts: {Account.query.count()}")
        
        if User.query.count() > 0:
            print("\n=== Existing Users ===")
            users = User.query.all()
            for user in users:
                print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Admin: {user.is_admin}")
        
        if Account.query.count() > 0:
            print("\n=== Existing Accounts ===")
            accounts = Account.query.all()
            for account in accounts:
                print(f"ID: {account.id}, Account Number: {account.account_number}, User ID: {account.user_id}, Balance: {account.balance}")

if __name__ == "__main__":
    check_database() 