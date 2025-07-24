#!/usr/bin/env python3
"""
Script to clear database for testing
"""

from app import create_app, db
from app.models import User, Account, Transaction

def clear_database():
    app = create_app()
    with app.app_context():
        print("=== Clearing Database ===")
        
        # Delete all data
        Transaction.query.delete()
        Account.query.delete()
        User.query.delete()
        
        # Commit changes
        db.session.commit()
        
        print("Database cleared successfully!")
        print(f"Users: {User.query.count()}")
        print(f"Accounts: {Account.query.count()}")

if __name__ == "__main__":
    clear_database() 