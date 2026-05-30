# SQLite Bank Account System with Service + Repository Layers

import sqlite3
from dataclasses import dataclass
import datetime

# -------------------------
# Custom Exceptions
# -------------------------

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

# -------------------------
# Model
# -------------------------

@dataclass
class Account:
    account_id: str
    owner_name: str
    balance: float
    created_at: str

    def display(self, index):
        print(
            f"[{index}] "
            f"Account ID: {self.account_id} | "
            f"Owner: {self.owner_name} | "
            f"Balance: {self.balance:.2f} | "
            f"Created at: {self.created_at}"
        )

# -------------------------
# Repository Layer
# -------------------------

class AccountRepository:
    def __init__(self, db_name="bank.db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    account_id TEXT PRIMARY KEY,
                    owner_name TEXT NOT NULL,
                    balance REAL NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

    def add_account(self, account):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO accounts (account_id, owner_name, balance, created_at)
                VALUES (?, ?, ?, ?)
            """, (
                account.account_id,
                account.owner_name,
                account.balance,
                account.created_at
            ))

    def get_all_accounts(self):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT account_id, owner_name, balance, created_at
                FROM accounts
            """)
            rows = cursor.fetchall()
        accounts = []
        for row in rows:
            accounts.append(Account(
                account_id=row[0],
                owner_name=row[1],
                balance=row[2],
                created_at=row[3]
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
        if row is None:
            return None
        return Account(
            account_id=row[0],
            owner_name=row[1],
            balance=row[2],
            created_at=row[3]
        )

    def update_balance(self, account_id, new_balance):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE accounts
                SET balance = ?
                WHERE account_id = ?
            """, (new_balance, account_id))

    def transfer_balances(self, from_account_id, to_account_id, new_from_balance, new_to_balance):
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

# -------------------------
# Service Layer
# -------------------------

class BankService:
    def __init__(self):
        self.account_repository = AccountRepository()

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
        account = Account(
            account_id=account_id,
            owner_name=owner_name,
            balance=starting_balance,
            created_at=created_at
        )
        self.account_repository.add_account(account)

    def deposit(self, account_id, amount):
        account = self.get_account(account_id)
        if account is None:
            raise AccountNotFoundError
        if amount <= 0:
            raise InvalidAmountError
        new_balance = account.balance + amount
        self.account_repository.update_balance(account_id, new_balance)

    def withdraw(self, account_id, amount):
        account = self.get_account(account_id)
        if account is None:
            raise AccountNotFoundError
        if amount <= 0:
            raise InvalidAmountError
        if amount > account.balance:
            raise InsufficientFundsError
        new_balance = account.balance - amount
        self.account_repository.update_balance(account_id, new_balance)

    def transfer(self, from_account_id, to_account_id, amount):
        from_account = self.get_account(from_account_id)
        if from_account is None:
            raise SourceAccountNotFoundError
        to_account = self.get_account(to_account_id)
        if to_account is None:
            raise DestinationAccountNotFoundError
        if amount <= 0:
            raise InvalidAmountError
        if amount > from_account.balance:
            raise InsufficientFundsError
        new_from_balance = from_account.balance - amount
        new_to_balance = to_account.balance + amount
        self.account_repository.transfer_balances(
            from_account_id,
            to_account_id,
            new_from_balance,
            new_to_balance
        )

    def get_all_accounts(self):
        accounts = self.account_repository.get_all_accounts()
        if not accounts:
            print("No accounts available")
            return
        for index, account in enumerate(accounts, start=1):
            account.display(index)

    def get_account(self, account_id):
        return self.account_repository.get_account_by_id(account_id)

    def show_account(self, account_id):
        account = self.get_account(account_id)
        if account is None:
            raise AccountNotFoundError
        account.display(1)

def main():
    bank_service = BankService()
    while True:
        try:
            choice = int(input("1) Create account\n"
                               "2) Show all accounts\n"
                               "3) Deposit money\n"
                               "4) Withdraw money\n"
                               "5) Transfer money\n"
                               "6) Show account by ID\n"
                               "7) Exit\n"))
        except ValueError:
            print("Invalid choice! choose between 1 and 7.")
            continue
        match choice:
            case 1:
                account_id = input("Enter account ID: ").strip()
                owner_name = input("Enter owner name: ").strip()
                try:
                    starting_balance = float(input("Enter starting balance: "))
                    bank_service.create_account(account_id, owner_name, starting_balance)
                    print("Account created.")
                except ValueError:
                    print("Invalid account data")
                except InvalidAccountDataError:
                    print("Invalid account data")
                except DuplicateAccountError:
                    print("Account ID already exists")
            case 2:
                bank_service.get_all_accounts()
            case 3:
                account_id = input("Enter account ID: ").strip()
                try:
                    amount = float(input("Enter amount to deposit: "))
                    bank_service.deposit(account_id, amount)
                    print("Deposit completed.")
                except ValueError:
                    print("Invalid amount")
                except AccountNotFoundError:
                    print("Account not found")
                except InvalidAmountError:
                    print("Invalid amount")
            case 4:
                account_id = input("Enter account ID: ").strip()
                try:
                    amount = float(input("Enter amount to withdraw: "))
                    bank_service.withdraw(account_id, amount)
                    print("Withdrawal completed.")
                except ValueError:
                    print("Invalid amount")
                except AccountNotFoundError:
                    print("Account not found")
                except InvalidAmountError:
                    print("Invalid amount")
                except InsufficientFundsError:
                    print("Insufficient funds")
            case 5:
                from_account_id = input("Enter source account ID: ").strip()
                to_account_id = input("Enter destination account ID: ").strip()
                try:
                    amount = float(input("Enter amount to transfer: "))
                    bank_service.transfer(from_account_id, to_account_id, amount)
                    print("Transfer completed.")
                except ValueError:
                    print("Invalid amount")
                except SourceAccountNotFoundError:
                    print("Source account not found")
                except DestinationAccountNotFoundError:
                    print("Destination account not found")
                except InvalidAmountError:
                    print("Invalid amount")
                except InsufficientFundsError:
                    print("Insufficient funds")
            case 6:
                account_id = input("Enter account ID: ").strip()
                try:
                    bank_service.show_account(account_id)
                except AccountNotFoundError:
                    print("Account not found")
            case 7:
                print("Goodbye!")
                return
            case _:
                print("Invalid choice! choose between 1 and 7.")

if __name__ == "__main__":
    main()