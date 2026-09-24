import json
import random
import sys
import os

# File to store our bank data persistently
DATA_FILE = "bank_data.json"

class BankManagementSystem:
    def __init__(self):
        self.accounts = self.load_data()

    def load_data(self):
        """Loads account data from the JSON file if it exists."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return {}
        return {}

    def save_data(self):
        """Saves current account data to the JSON file."""
        with open(DATA_FILE, 'w') as file:
            json.dump(self.accounts, file, indent=4)

    def main_menu(self):
        """Main entry point for the application."""
        while True:
            print("\n" + "="*35)
            print("    BANK MANAGEMENT SYSTEM")
            print("="*35)
            print("1. Create New Account")
            print("2. Login to Existing Account")
            print("3. Exit")
            print("="*35)

            choice = input("Enter your choice (1-3): ").strip()

            if choice == '1':
                self.create_account()
            elif choice == '2':
                self.login()
            elif choice == '3':
                print("\nThank you for using our Bank Management System. Goodbye!")
                sys.exit()
            else:
                print("\nInvalid choice. Please enter 1, 2, or 3.")

    def create_account(self):
        """Handles the creation of a new bank account."""
        print("\n--- Create New Account ---")
        name = input("Enter your full name: ").strip()
        
        if not name:
            print("\nName cannot be empty. Account creation failed.")
            return

        # Generate a unique 5-digit account number
        while True:
            acc_num = str(random.randint(10000, 99999))
            if acc_num not in self.accounts:
                break
        
        pin = input("Set a 4-digit PIN: ").strip()
        if not pin.isdigit() or len(pin) != 4:
            print("\nPIN must be exactly 4 digits. Account creation failed.")
            return
        
        try:
            initial_deposit = float(input("Enter initial deposit amount (Min ₹0): "))
            if initial_deposit < 0:
                print("\nInitial deposit cannot be negative. Setting balance to ₹0.00.")
                initial_deposit = 0.0
        except ValueError:
            print("\nInvalid amount. Setting balance to ₹0.00.")
            initial_deposit = 0.0

        # Store account in memory and save to file
        self.accounts[acc_num] = {
            'name': name,
            'pin': pin,
            'balance': initial_deposit
        }
        self.save_data()

        print(f"\nAccount created successfully!")
        print(f"Account Holder: {name}")
        print(f"Account Number: {acc_num} (Please save this!)")
        print(f"Current Balance: ₹{initial_deposit:.2f}")

    def login(self):
        """Handles user authentication."""
        print("\n--- Login ---")
        acc_num = input("Enter your Account Number: ").strip()
        
        if acc_num not in self.accounts:
            print("\nAccount not found. Please check your account number.")
            return

        pin = input("Enter your PIN: ").strip()
        
        if self.accounts[acc_num]['pin'] == pin:
            print(f"\nLogin successful! Welcome back, {self.accounts[acc_num]['name']}.")
            self.account_menu(acc_num)
        else:
            print("\nIncorrect PIN. Access denied.")

    def account_menu(self, acc_num):
        """Displays the dashboard for logged-in users."""
        while True:
            print("\n" + "-"*35)
            print("       ACCOUNT DASHBOARD")
            print("-"*35)
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. View Account Details")
            print("5. Logout")
            print("-"*35)

            choice = input("Enter your choice (1-5): ").strip()

            if choice == '1':
                self.check_balance(acc_num)
            elif choice == '2':
                self.deposit(acc_num)
            elif choice == '3':
                self.withdraw(acc_num)
            elif choice == '4':
                self.view_details(acc_num)
            elif choice == '5':
                print(f"\nLogging out. Goodbye, {self.accounts[acc_num]['name']}!")
                break
            else:
                print("\nInvalid choice. Please enter a number between 1 and 5.")

    def check_balance(self, acc_num):
        """Displays current account balance."""
        balance = self.accounts[acc_num]['balance']
        print(f"\nYour current balance is: ₹{balance:.2f}")

    def deposit(self, acc_num):
        """Adds funds to the account."""
        try:
            amount = float(input("\nEnter amount to deposit: ₹"))
            if amount <= 0:
                print("\nDeposit amount must be greater than zero.")
            else:
                self.accounts[acc_num]['balance'] += amount
                self.save_data() # Save changes to file
                print(f"\nSuccessfully deposited ₹{amount:.2f}.")
                self.check_balance(acc_num)
        except ValueError:
            print("\nInvalid input. Please enter a valid numerical amount.")

    def withdraw(self, acc_num):
        """Deducts funds from the account if sufficient balance exists."""
        try:
            amount = float(input("\nEnter amount to withdraw: ₹"))
            if amount <= 0:
                print("\nWithdrawal amount must be greater than zero.")
            elif amount > self.accounts[acc_num]['balance']:
                print("\nInsufficient funds! Transaction failed.")
            else:
                self.accounts[acc_num]['balance'] -= amount
                self.save_data() # Save changes to file
                print(f"\nSuccessfully withdrew ₹{amount:.2f}.")
                self.check_balance(acc_num)
        except ValueError:
            print("\nInvalid input. Please enter a valid numerical amount.")

    def view_details(self, acc_num):
        """Prints the user's account information."""
        print("\n--- Account Details ---")
        print(f"Account Holder : {self.accounts[acc_num]['name']}")
        print(f"Account Number : {acc_num}")
        print(f"Current Balance: ₹{self.accounts[acc_num]['balance']:.2f}")


if __name__ == "__main__":
    try:
        bank_app = BankManagementSystem()
        bank_app.main_menu()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting safely...")
        sys.exit()