from auth import register_user, authenticate_user, reset_password, change_password, recover_password
from accounts import create_account, get_account_details
from transactions import deposit, withdraw, transfer
from admin import view_all_accounts, monitor_transactions, handle_report

def main():
    while True:
        print("Welcome to the Bank Management System")
        print("1. Register")
        print("2. Login")
        print("3. Reset Password")
        print("4. Change Password")
        print("5. Recover Password")
        print("6. Admin Login")
        print("7. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            is_admin = input("Is this an admin account? (yes/no): ").lower() == 'yes'
            response = register_user(username, password, is_admin)
            if 'account_id' in response:
                print(f"User registered successfully. Account ID: {response['account_id']}")
            else:
                print(response.get('error', 'An error occurred during registration'))
        
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            auth_response = authenticate_user(username, password)
            print(auth_response)
            if 'user_id' in auth_response:
                user_id = auth_response['user_id']
                is_admin = auth_response['is_admin']
                if is_admin:
                    print("Admin users should log in via the Admin Login option.")
                else:
                    while True:
                        print("1. Create Account")
                        print("2. View Account Details")
                        print("3. Deposit")
                        print("4. Withdraw")
                        print("5. Transfer")
                        print("6. Logout")
                        user_choice = input("Choose an option: ")

                        if user_choice == '1':
                            print(create_account(user_id))
                        elif user_choice == '2':
                            account_id = int(input("Enter account ID: "))
                            print(get_account_details(account_id))
                        elif user_choice == '3':
                            account_id = int(input("Enter account ID: "))
                            amount = float(input("Enter amount: "))
                            response = deposit(account_id, amount)
                            if 'new_balance' in response:
                                print(f"Deposit successful. New balance: {response['new_balance']}")
                            else:
                                print(response.get('error', 'An error occurred during deposit'))
                        elif user_choice == '4':
                            account_id = int(input("Enter account ID: "))
                            amount = float(input("Enter amount: "))
                            response = withdraw(account_id, amount)
                            if 'new_balance' in response:
                                print(f"Withdrawal successful. Remaining balance: {response['new_balance']}")
                            else:
                                print(response.get('error', 'An error occurred during withdrawal'))
                        elif user_choice == '5':
                            from_account_id = int(input("Enter from account ID: "))
                            to_account_id = int(input("Enter to account ID: "))
                            amount = float(input("Enter amount: "))
                            response = transfer(from_account_id, to_account_id, amount)
                            if 'from_new_balance' in response and 'to_new_balance' in response:
                                print(f"Transfer successful. New balance of from account: {response['from_new_balance']}, New balance of to account: {response['to_new_balance']}")
                            else:
                                print(response.get('error', 'An error occurred during transfer'))
                        elif user_choice == '6':
                            break

        elif choice == '3':
            username = input("Enter username: ")
            response = reset_password(username)
            print(response)

        elif choice == '4':
            username = input("Enter username: ")
            old_password = input("Enter old password: ")
            new_password = input("Enter new password: ")
            response = change_password(username, old_password, new_password)
            print(response)

        elif choice == '5':
            username = input("Enter username: ")
            response = recover_password(username)
            print(response)

        elif choice == '6':
            username = input("Enter admin username: ")
            password = input("Enter admin password: ")
            auth_response = authenticate_user(username, password)
            if 'user_id' in auth_response and auth_response.get('is_admin'):
                while True:
                    print("Admin Panel")
                    print("1. View All Accounts")
                    print("2. Monitor Transactions")
                    print("3. Generate Report")
                    print("4. Logout")
                    admin_choice = input("Choose an option: ")

                    if admin_choice == '1':
                        accounts = view_all_accounts()
                        for account in accounts:
                            print(account)
                    elif admin_choice == '2':
                        transactions = monitor_transactions()
                        for transaction in transactions:
                            print(transaction)
                    elif admin_choice == '3':
                        handle_report()
                    elif admin_choice == '4':
                        break
            else:
                print("Invalid admin credentials")

        elif choice == '7':
            break

if __name__ == '__main__':
    main()
