import os
import json
import random
import time
from datetime import datetime

DATA_FILE = "bank_data.json"
LOGIN_ATTEMPTS = 5
INTEREST_RATE = 0.08 

accounts = {}
logged_in = False

def save_data():
    """Save the accounts data to a file"""
    with open(DATA_FILE, 'w') as file:
        json.dump(accounts, file, indent=4)
    print("Data saved successfully")

def load_data():
    """Load the accounts data from a file"""
    global accounts
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as file:
                accounts = json.load(file)
            print("Data imported successfully")
        except json.JSONDecodeError:
            print("Error reading data file. Starting with empty accounts")
            accounts = {}
    else:
        print("No existing data found. Starting with empty accounts")
        accounts = {}

def login():
    """Authenticate the user"""
    global logged_in
    attempts = 0
    
    while attempts < LOGIN_ATTEMPTS and not logged_in:
        print("\n Login Required")
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        if username == "admin" and password == "1234":
            print("Login successful")
            logged_in = True
        else:
            attempts += 1
            remaining = LOGIN_ATTEMPTS - attempts
            print(f"Invalid credentials. {remaining} attempts remaining")
    
    if not logged_in:
        print("Too many failed attempts. Exiting program")
        exit()

def generate_account_number():
    """Generate a unique 8-digit account number"""
    while True:
        account_number = str(random.randint(10000000, 99999999))
        if account_number not in accounts:
            return account_number

def create_account():
    """Create a new bank account"""
    print("\nCreate New Account")
    holder_name = input("Enter account holder name: ")
    while True:
        try:
            initial_balance = float(input("Enter initial balance: $"))
            if initial_balance < 0:
                print("Initial balance cannot be negative")
                continue
            break
        except ValueError:
            print("Please enter a valid number")

    password = input("Create a password for this account: ")
    account_number = generate_account_number()

    accounts[account_number] = {
        "holder_name": holder_name,
        "balance": initial_balance,
        "password": password,
        "transactions": [],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_interest_date": datetime.now().strftime("%Y-%m-%d")
    }

    if initial_balance > 0:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        accounts[account_number]["transactions"].append({
            "type": "deposit",
            "amount": initial_balance,
            "timestamp": timestamp,
            "description": "Initial deposit"
        })
    save_data()
    print(f"\nAccount created successfully!")
    print(f"Account Number: {account_number}")
    print(f"Account Holder: {holder_name}")
    print(f"Initial Balance: ${initial_balance:.2f}")
    return account_number

def verify_account(account_number):
    """Verify account exists and password is correct"""
    if account_number not in accounts:
        print("Account not found")
        return False
    password = input("Enter account password: ")
    if password != accounts[account_number]["password"]:
        print("Incorrect password")
        return False
    return True

def deposit_money():
    """Deposit money into an account"""
    print("\nDeposit Money")
    account_number = input("Enter account number: ")
    
    if account_number not in accounts:
        print("Account not found")
        return
    if not verify_account(account_number):
        return
    try:
        amount = float(input("Enter deposit amount: $"))
        if amount <= 0:
            print("Deposit amount must be positive")
            return

        accounts[account_number]["balance"] += amount
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        description = input("Enter description (optional): ") or "Deposit"
        accounts[account_number]["transactions"].append({
            "type": "deposit",
            "amount": amount,
            "timestamp": timestamp,
            "description": description
        })
        
        save_data()
        print(f"\nDeposit successful")
        print(f"New balance: ${accounts[account_number]['balance']:.2f}")
    except ValueError:
        print("Please enter a valid amount")

def withdraw_money():
    """Withdraw money from an account"""
    print("\n Withdraw Money")
    account_number = input("Enter account number: ")
    if account_number not in accounts:
        print("Account not found")
        return
    if not verify_account(account_number):
        return  
    try:
        amount = float(input("Enter withdrawal amount: $"))
        if amount <= 0:
            print("Withdrawal amount must be positive")
            return
        
        if amount > accounts[account_number]["balance"]:
            print("Insufficient funds")
            return
        accounts[account_number]["balance"] -= amount
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        description = input("Enter description (optional): ") or "Withdrawal"
        accounts[account_number]["transactions"].append({
            "type": "withdrawal",
            "amount": amount,
            "timestamp": timestamp,
            "description": description
        }) 
        save_data()
        print(f"\nWithdrawal successful")
        print(f"New balance: ${accounts[account_number]['balance']:.2f}")
    except ValueError:
        print("Please enter a valid amount")

def check_balance():
    """Check the balance of an account"""
    print("\n Check Balance")
    account_number = input("Enter account number: ")
    
    if account_number not in accounts:
        print("Account not found")
        return
    if not verify_account(account_number):
        return
    
    print(f"\nAccount Number: {account_number}")
    print(f"Account Holder: {accounts[account_number]['holder_name']}")
    print(f"Current Balance: ${accounts[account_number]['balance']:.2f}")
    print(f"Account Created: {accounts[account_number]['created_at']}")

def view_transactions():
    """View transaction history for an account"""
    print("\n Transaction History ")
    account_number = input("Enter account number: ")
    
    if account_number not in accounts:
        print("Account not found")
        return
    if not verify_account(account_number):
        return
    
    transactions = accounts[account_number]["transactions"]
    
    if not transactions:
        print("No transactions found for this account")
        return
    
    print(f"\nTransaction History for Account {account_number}:")
    print(f"Account Holder: {accounts[account_number]['holder_name']}")
    print("-" * 80)
    print(f"{'Type':<12} {'Amount':<10} {'Date & Time':<22} {'Description':<30}")
    print("-" * 80)
    
    for transaction in transactions:
        type_str = transaction["type"].capitalize()
        amount_str = f"${transaction['amount']:.2f}"
        print(f"{type_str:<12} {amount_str:<10} {transaction['timestamp']:<22} {transaction['description']:<30}")   
    print("-" * 80)
    print(f"Current Balance: ${accounts[account_number]['balance']:.2f}")

def transfer_money():
    """Transfer money between accounts"""
    print("\n Transfer Money ")
    from_account = input("Enter sender's account number: ")
    
    if from_account not in accounts:
        print("Sender's account not found")
        return
    if not verify_account(from_account):
        return

    to_account = input("Enter recipient's account number: ")
    
    if to_account not in accounts:
        print("Recipient's account not found")
        return
    if from_account == to_account:
        print("Cannot transfer to the same account")
        return
    try:
        amount = float(input("Enter transfer amount: $"))
        if amount <= 0:
            print("Transfer amount must be positive")
            return
        if amount > accounts[from_account]["balance"]:
            print("Insufficient funds")
            return

        accounts[from_account]["balance"] -= amount
        accounts[to_account]["balance"] += amount
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        description = input("Enter description (optional): ") or "Transfer"
        accounts[from_account]["transactions"].append({
            "type": "transfer out",
            "amount": amount,
            "timestamp": timestamp,
            "description": f"{description} to Acct#{to_account}"
        })
        accounts[to_account]["transactions"].append({
            "type": "transfer in",
            "amount": amount,
            "timestamp": timestamp,
            "description": f"{description} from Acct#{from_account}"
        })
        save_data()
        print(f"\nTransfer successful")
        print(f"New balance for account {from_account}: ${accounts[from_account]['balance']:.2f}")
    except ValueError:
        print("Please enter a valid amount")

def calculate_interest():
    """Calculate and apply interest to all accounts."""
    print("\n Interest Calculation")
    today = datetime.now().strftime("%Y-%m-%d")
    interest_applied = False
    for account_number, account in accounts.items():
        if account["last_interest_date"] != today:
            daily_interest = account["balance"] * (INTEREST_RATE / 365)
            if daily_interest > 0:
                account["balance"] += daily_interest
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                account["transactions"].append({
                    "type": "interest", 
                    "amount": daily_interest,
                    "timestamp": timestamp,
                    "description": f"Daily interest at {INTEREST_RATE*100:.2f}% annual rate"
                })
                account["last_interest_date"] = today
                interest_applied = True
                print(f"Interest of ${daily_interest:.2f} applied to account {account_number}")
    
    if interest_applied:
        save_data()
        print("Interest calculation completed")
    else:
        print("No interest applied today")

def list_all_accounts():
    """List all accounts in the system"""
    print("\n All Accounts ")
    if not accounts:
        print("No accounts found in the system")
        return
    
    print(f"{'Account Number':<15} {'Account Holder':<25} {'Balance':<12}")
    print("-" * 52)
    for account_number, account in accounts.items():
        print(f"{account_number:<15} {account['holder_name']:<25} ${account['balance']:.2f}")

def change_password():
    """Change password for an account"""
    print("\n Change Password ")
    account_number = input("Enter account number: ")
    if account_number not in accounts:
        print("Account not found")
        return
    if not verify_account(account_number):
        return
    
    new_password = input("Enter new password: ")
    accounts[account_number]["password"] = new_password
    
    save_data()
    print("Password changed successfully")

def display_menu():
    """Display the main menu options"""
    print("\n BANKING SYSTEM MENU ")
    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Check Balance")
    print("5. Transaction History")
    print("6. Transfer Money")
    print("7. Calculate Interest")
    print("8. List All Accounts")
    print("9. Change Account Password")
    print("10. Exit")
    print("----------------------------------")

def main():
    """Main function to run the banking application"""
    print("Welcome to the Mini Banking System")

    login()
    load_data()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-10): ")
        if choice == '1':
            create_account()
        elif choice == '2':
            deposit_money()
        elif choice == '3':
            withdraw_money()
        elif choice == '4':
            check_balance()
        elif choice == '5':
            view_transactions()
        elif choice == '6':
            transfer_money()
        elif choice == '7':
            calculate_interest()
        elif choice == '8':
            list_all_accounts()
        elif choice == '9':
            change_password()
        elif choice == '10':
            print("\nThank you for using the Mini Banking System")
            break
        else:
            print("Invalid choice. Please try again")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
    