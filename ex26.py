# SQLite Bank System v2: Transaction History

import sqlite3
import datetime
from dataclasses import dataclass

# Exceptions

class BankError(Exception):
    pass

class AccountNotFoundError(BankError):
    pass

class DuplicateAccountError(BankError):
    pass

class InvalidAccountDataError(BankError):
    pass

class InvalidAmountError(BankError):
    pass

class InsufficientFundsError(BankError):
    pass

class SourceAccountNotFoundError(BankError):
    pass

class DestinationAccountNotFoundError(BankError):
    pass

class NoAccountsFoundError(BankError):
    pass

class NoTransactionsFoundError(BankError):
    pass

# Data classes

@dataclass
class Account:
    account_id: str
    owner_name: str
    balance: float
    created_at: str

    def display(self, index):
        print(f"[{index}] "
              f"account_id: {self.account_id} | "
              f"owner_name: {self.owner_name} | "
              f"balance: {self.balance:.2f} | "
              f"created_at: {self.created_at}")

@dataclass
class Transaction:
    transaction_id: int
    transaction_type: str
    from_account_id: str
    to_account_id: str
    amount: float
    created_at: str

    def display(self, index):
        print(f"[{index}] "
              f"transaction_type: {self.transaction_type} | "
              f"from_account_id: {self.from_account_id} | "
              f"to_account_id: {self.to_account_id} | "
              f"amount: {self.amount:.2f} | "
              f"created_at: {self.created_at}")

# Database handler

class BankRepository:
    def __init__(self, db_name = "bank.db"):
        self.db_name = db_name
        self.create_account_table()
        self.create_transaction_table()

    def create_account_table(self):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts(
                    account_id TEXT PRIMARY KEY,
                    owner_name TEXT NOT NULL,
                    balance REAL NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

    def create_transaction_table(self):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions(
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_type TEXT NOT NULL,
                    from_account_id TEXT,
                    to_account_id TEXT,
                    amount REAL NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

    def add_account(self, account):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO accounts (account_id, owner_name, balance, created_at)
                VALUES (?, ?, ?, ?)
            """, (account.account_id,
                  account.owner_name,
                  account.balance,
                  account.created_at))

    def get_all_accounts(self):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT account_id, owner_name, balance, created_at
                FROM accounts
            """)
            rows = cursor.fetchall()
        if not rows:
            return None
        accounts = []
        for row in rows:
            accounts.append(Account(
                row[0],
                row[1],
                row[2],
                row[3]
            ))
        return accounts

    def get_account_by_id(self, account_id):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT account_id, owner_name, balance, created_at
                FROM accounts
                WHERE account_id = ?
            """, (account_id,))
            row = cursor.fetchone()
        if not row:
            return None
        return Account(
                row[0],
                row[1],
                row[2],
                row[3]
        )

    def update_balance(self, account_id, new_balance):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE accounts
                SET balance = ?
                WHERE account_id = ?
            """, (new_balance, account_id))

    def insert_transaction(self, transaction_type, from_account_id, to_account_id, amount, created_at):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO transactions 
                    (transaction_type, from_account_id, to_account_id, amount, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (transaction_type,
                  from_account_id,
                  to_account_id,
                  amount,
                  created_at))

    def deposit_with_transaction(self, account_id, new_balance, amount, created_at):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE accounts
                SET balance = ?
                WHERE account_id = ?
            """, (new_balance, account_id))

            cursor.execute("""
                INSERT INTO transactions 
                    (transaction_type, from_account_id, to_account_id, amount, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                "deposit",
                account_id,
                None,
                amount,
                created_at))

    def withdraw_with_transaction(self, account_id, new_balance, amount, created_at):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE accounts
                SET balance = ?
                WHERE account_id = ?
            """, (new_balance, account_id))

            cursor.execute("""
                INSERT INTO transactions 
                    (transaction_type, from_account_id, to_account_id, amount, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                "withdraw",
                account_id,
                None,
                amount,
                created_at))

    def transfer_with_transaction(self, from_account_id, to_account_id, new_from_balance, new_to_balance, amount, created_at):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE accounts
                SET balance = ?
                WHERE account_id = ?
            """, (new_from_balance, from_account_id))

            cursor.execute("""
                UPDATE accounts
                SET balance = ?
                WHERE account_id = ?
            """, (new_to_balance, to_account_id))

            cursor.execute("""
                INSERT INTO transactions 
                    (transaction_type, from_account_id, to_account_id, amount, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                "transfer",
                from_account_id,
                to_account_id,
                amount,
                created_at))

    def get_all_transactions(self):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT transaction_id, transaction_type, from_account_id, to_account_id, amount, created_at
                FROM transactions
                ORDER BY transaction_id
            """)
            rows = cursor.fetchall()
        if not rows:
            return None
        transactions = []
        for row in rows:
            transactions.append(Transaction(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5]
            ))
        return transactions

    def get_transactions_for_account(self, account_id):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT transaction_id, transaction_type, from_account_id, to_account_id, amount, created_at
                FROM transactions
                WHERE from_account_id = ? or to_account_id = ?
                ORDER BY transaction_id
            """, (account_id, account_id))
            rows = cursor.fetchall()
        if not rows:
            return None
        transactions = []
        for row in rows:
            transactions.append(Transaction(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5]
            ))
        return transactions

# Service handler

class BankService:
    def __init__(self):
        self.bank_repository = BankRepository()

    def create_account(self, account_id, owner_name, starting_balance):
        if not account_id:
            raise InvalidAccountDataError
        if self.get_account(account_id) is not None:
            raise DuplicateAccountError
        if not owner_name:
            raise InvalidAccountDataError
        if starting_balance < 0:
            raise InvalidAccountDataError
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.bank_repository.add_account(Account(
            account_id, owner_name, starting_balance, created_at
        ))

    def get_all_accounts(self):
        accounts = self.bank_repository.get_all_accounts()
        if accounts is None:
            raise NoAccountsFoundError
        return accounts

    def get_account(self, account_id):
        return self.bank_repository.get_account_by_id(account_id)

    def deposit(self, account_id, amount):
        account = self.get_account(account_id)
        if account is None:
            raise AccountNotFoundError
        if amount <= 0:
            raise InvalidAmountError
        new_balance = account.balance + amount
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.bank_repository.deposit_with_transaction(
            account_id,
            new_balance,
            amount,
            created_at
        )

    def withdraw(self, account_id, amount):
        account = self.get_account(account_id)
        if account is None:
            raise AccountNotFoundError
        if amount <= 0:
            raise InvalidAmountError
        if account.balance < amount:
            raise InsufficientFundsError
        new_balance = account.balance - amount
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.bank_repository.withdraw_with_transaction(
            account_id,
            new_balance,
            amount,
            created_at
        )

    def transfer(self, from_account_id, to_account_id, amount):
        from_account = self.get_account(from_account_id)
        if from_account is None:
            raise SourceAccountNotFoundError
        to_account = self.get_account(to_account_id)
        if to_account is None:
            raise DestinationAccountNotFoundError
        if amount <= 0:
            raise InvalidAmountError
        if from_account.balance < amount:
            raise InsufficientFundsError
        new_from_balance = from_account.balance - amount
        new_to_balance = to_account.balance + amount
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.bank_repository.transfer_with_transaction(
            from_account_id,
            to_account_id,
            new_from_balance,
            new_to_balance,
            amount,
            created_at
        )

    def get_all_transactions(self):
        transactions = self.bank_repository.get_all_transactions()
        if transactions is None:
            raise NoTransactionsFoundError
        return transactions

    def get_transactions_for_account(self, account_id):
        if self.get_account(account_id) is None:
            raise AccountNotFoundError
        transactions = self.bank_repository.get_transactions_for_account(account_id)
        if transactions is None:
            raise NoTransactionsFoundError
        return transactions

# Main event stream and functions

def show_all_accounts(accounts):
    for index, account in enumerate(accounts, start=1):
        account.display(index)

def show_account(account):
    if account is None:
        raise AccountNotFoundError
    account.display(1)

def show_transactions(transactions):
    for index, transaction in enumerate(transactions, start=1):
        transaction.display(index)

def main():
    bank_service = BankService()
    while True:
        try:
            choice = int(input("1) Create account\n"
                               "2) Show all accounts\n"
                               "3) Show account by ID\n"
                               "4) Deposit money\n"
                               "5) Withdraw money\n"
                               "6) Transfer money\n"
                               "7) Show all transactions\n"
                               "8) Show transactions for one account\n"
                               "9) Exit\n"))
        except ValueError:
            print("Invalid choice. choose between 1 and 9")
            continue
        match choice:
            case 1:
                account_id = input("Enter account ID: ").strip()
                owner_name = input("Enter account owner: ").strip()
                try:
                    starting_balance = float(input("Enter initial balance: "))
                    bank_service.create_account(account_id, owner_name, starting_balance)
                    print("Account created")
                except ValueError:
                    print("Invalid account data")
                except InvalidAccountDataError:
                    print("Invalid account data")
                except DuplicateAccountError:
                    print("Account ID already exists")
            case 2:
                try:
                    accounts = bank_service.get_all_accounts()
                    show_all_accounts(accounts)
                except NoAccountsFoundError:
                    print("No accounts available")
            case 3:
                account_id = input("Enter account ID: ").strip()
                try:
                    account = bank_service.get_account(account_id)
                    show_account(account)
                except AccountNotFoundError:
                    print("Account not found")
            case 4:
                account_id = input("Enter account ID: ").strip()
                try:
                    amount = float(input("Enter the amount to deposit: "))
                    bank_service.deposit(account_id, amount)
                    print(f"{amount:.2f} deposited into {account_id}.")
                except ValueError:
                    print("Invalid amount")
                except AccountNotFoundError:
                    print("Account not found")
                except InvalidAmountError:
                    print("Invalid amount")
            case 5:
                account_id = input("Enter account ID: ").strip()
                try:
                    amount = float(input("Enter the amount to withdraw: "))
                    bank_service.withdraw(account_id, amount)
                    print(f"{amount:.2f} withdrawn from {account_id}.")
                except ValueError:
                    print("Invalid amount")
                except AccountNotFoundError:
                    print("Account not found")
                except InsufficientFundsError:
                    print("Insufficient funds")
                except InvalidAmountError:
                    print("Invalid amount")
            case 6:
                from_account_id = input("Enter account ID to withdraw from: ").strip()
                to_account_id = input("Enter account ID to deposit into: ").strip()
                try:
                    amount = float(input("Enter the amount to transfer: "))
                    bank_service.transfer(from_account_id, to_account_id, amount)
                    print(f"{amount:.2f} transferred from {from_account_id} to {to_account_id}.")
                except ValueError:
                    print("Invalid amount")
                except SourceAccountNotFoundError:
                    print("Source account not found")
                except DestinationAccountNotFoundError:
                    print("Destination account not found")
                except InsufficientFundsError:
                    print("Insufficient funds")
                except InvalidAmountError:
                    print("Invalid amount")
            case 7:
                try:
                    transactions = bank_service.get_all_transactions()
                    show_transactions(transactions)
                except NoTransactionsFoundError:
                    print("No transactions available")
            case 8:
                account_id = input("Enter account ID: ").strip()
                try:
                    transactions = bank_service.get_transactions_for_account(account_id)
                    show_transactions(transactions)
                except AccountNotFoundError:
                    print("Account not found")
                except NoTransactionsFoundError:
                    print("No transactions found for this account")
            case 9:
                print("Goodbye!")
                break
            case _:
                print("Invalid choice. choose between 1 and 9")

if __name__ == "__main__":
    main()