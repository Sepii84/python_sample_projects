# SQLite Bank System v3: Customers, Multiple Accounts, and Statements

from dataclasses import dataclass
import sqlite3
import datetime

# Exceptions

class BankError(Exception):
    pass

class CustomerNotFoundError(BankError):
    pass

class DuplicateCustomerError(BankError):
    pass

class DuplicateEmailError(BankError):
    pass

class InvalidCustomerDataError(BankError):
    pass

class InvalidAccountTypeError(BankError):
    pass

class NoCustomersFoundError(BankError):
    pass

class NoCustomerAccountsFoundError(BankError):
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

@dataclass
class Customer:
    customer_id: str
    full_name: str
    email: str
    created_at: str

    def display(self, index):
        print(f"[{index}] "
              f"customer_id: {self.customer_id} | "
              f"full_name: {self.full_name} | "
              f"email: {self.email} | "
              f"created_at: {self.created_at}")

@dataclass
class Account:
    account_id: str
    customer_id: str
    account_type: str
    balance: float
    created_at: str

    def display(self, index):
        print(f"[{index}] "
              f"account_id: {self.account_id} | "
              f"customer_id: {self.customer_id} | "
              f"account_type: {self.account_type} | "
              f"balance: {self.balance:.2f} | "
              f"created_at: {self.created_at}")

@dataclass
class TransactionRecord:
    transaction_id: int
    transaction_type: str
    from_account_id: str
    to_account_id: str
    amount: float
    created_at: str

    def display(self, index):
        print(f"[{index}] "
              f"transaction_id: {self.transaction_id} | "
              f"transaction_type: {self.transaction_type} | "
              f"from_account_id: {self.from_account_id} | "
              f"to_account_id: {self.to_account_id} | "
              f"amount: {self.amount:.2f} | "
              f"created_at: {self.created_at}")

# DataBase connection

class BankRepository:
    def __init__(self, db_name = "bank.db"):
        self.db_name = db_name
        self.create_tables()

    def create_tables(self):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS customers(
                                customer_id TEXT PRIMARY KEY,
                                full_name TEXT NOT NULL,
                                email TEXT NOT NULL UNIQUE,
                                created_at TEXT NOT NULL
                            )
                        """)
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS accounts(
                                account_id TEXT PRIMARY KEY,
                                customer_id TEXT NOT NULL REFERENCES customers(customer_id),
                                account_type TEXT NOT NULL CHECK(account_type IN ("checking", "savings", "business")),
                                balance REAL NOT NULL,
                                created_at TEXT NOT NULL
                            )
                        """)
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

    def add_customer(self, customer):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            INSERT INTO customers (customer_id, full_name, email, created_at)
                            VALUES (?, ?, ?, ?)
            """,(customer.customer_id,
                           customer.full_name,
                           customer.email,
                           customer.created_at))

    def get_customer_by_id(self, customer_id):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            SELECT customer_id, full_name, email, created_at
                            FROM customers
                            WHERE customer_id = ?
            """, (customer_id, ))
            row = cursor.fetchone()
        if not row:
            return None
        return Customer(
            row[0],
            row[1],
            row[2],
            row[3]
        )

    def get_customer_by_email(self, email):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            SELECT customer_id, full_name, email, created_at
                            FROM customers
                            WHERE email = ?
            """, (email,))
            row = cursor.fetchone()
        if not row:
            return None
        return Customer(
            row[0],
            row[1],
            row[2],
            row[3]
        )

    def get_all_customers(self):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            SELECT customer_id, full_name, email, created_at
                            FROM customers
                            ORDER BY customer_id
            """)
            rows = cursor.fetchall()
        if not rows:
            return None
        customers = []
        for row in rows:
            customers.append(Customer(
                row[0],
                row[1],
                row[2],
                row[3]
        ))
        return customers

    def add_account(self, account):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            INSERT INTO accounts (account_id, customer_id, account_type, balance, created_at)
                            VALUES (?, ?, ?, ?, ?)
            """, (account.account_id,
                  account.customer_id,
                  account.account_type,
                  account.balance,
                  account.created_at))

    def get_account_by_id(self, account_id):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            SELECT account_id, customer_id, account_type, balance, created_at
                            FROM accounts
                            WHERE account_id = ?
            """, (account_id, ))
            row = cursor.fetchone()
        if not row:
            return None
        return Account(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4]
        )

    def get_all_accounts(self):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            SELECT account_id, customer_id, account_type, balance, created_at
                            FROM accounts
                            ORDER BY account_id
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
                row[3],
                row[4]
            ))
        return accounts

    def get_accounts_by_customer(self, customer_id):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            SELECT account_id, customer_id, account_type, balance, created_at
                            FROM accounts
                            WHERE customer_id = ?
            """, (customer_id, ))
            rows = cursor.fetchall()
        if not rows:
            return None
        accounts = []
        for row in rows:
            accounts.append(Account(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4]
            ))
        return accounts

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
            """, ("deposit", None, account_id, amount, created_at))

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
            """, ("withdraw", account_id, None, amount, created_at))

    def transfer_with_transaction(self,
                                  from_account_id,
                                  to_account_id,
                                  new_from_balance,
                                  new_to_balance,
                                  amount,
                                  created_at):
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
            """, ("transfer", from_account_id, to_account_id, amount, created_at))

    def get_all_transactions(self):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            SELECT 
                                transaction_id, 
                                transaction_type, 
                                from_account_id, 
                                to_account_id, 
                                amount, 
                                created_at
                            FROM transactions
                            ORDER BY transaction_id
            """)
            rows = cursor.fetchall()
        if not rows:
            return None
        transactions = []
        for row in rows:
            transactions.append(TransactionRecord(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
            ))
        return transactions

    def get_transactions_for_account(self, account_id):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            SELECT 
                                transaction_id, 
                                transaction_type, 
                                from_account_id, 
                                to_account_id, 
                                amount, 
                                created_at
                            FROM transactions
                            WHERE from_account_id = ? OR to_account_id = ?
                            ORDER BY transaction_id
            """, (account_id, account_id))
            rows = cursor.fetchall()
        if not rows:
            return None
        transactions = []
        for row in rows:
            transactions.append(TransactionRecord(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
            ))
        return transactions

    def get_transactions_for_customer(self, customer_id):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            SELECT 
                                transaction_id, 
                                transaction_type, 
                                from_account_id, 
                                to_account_id, 
                                amount, 
                                created_at
                            FROM transactions
                            WHERE from_account_id IN (
                                SELECT account_id 
                                FROM accounts
                                WHERE customer_id = ?
                            )
                            OR to_account_id IN (
                                SELECT account_id 
                                FROM accounts
                                WHERE customer_id = ?
                            )
                            ORDER BY transaction_id
            """, (customer_id, customer_id))
            rows = cursor.fetchall()
        if not rows:
            return None
        transactions = []
        for row in rows:
            transactions.append(TransactionRecord(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
            ))
        return transactions

class BankService:
    def __init__(self):
        self.repository = BankRepository()

    def create_customer(self, customer_id, full_name, email):
        if not customer_id or not full_name or not email:
            raise InvalidCustomerDataError
        if self.get_customer(customer_id) is not None:
            raise DuplicateCustomerError
        if self.get_customer_by_email(email) is not None:
            raise DuplicateEmailError
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.repository.add_customer(Customer(
            customer_id,
            full_name,
            email,
            created_at
        ))

    def get_all_customers(self):
        customers = self.repository.get_all_customers()
        if not customers:
            raise NoCustomersFoundError
        return customers

    def get_customer(self, customer_id):
        customer = self.repository.get_customer_by_id(customer_id)
        if customer is None:
            return None
        return customer

    def get_customer_by_email(self, email):
        customer = self.repository.get_customer_by_email(email)
        if customer is None:
            return None
        return customer

    def create_account(self, account_id, customer_id, account_type, starting_balance):
        if not account_id or not customer_id or starting_balance < 0:
            raise InvalidAccountDataError
        if self.repository.get_customer_by_id(customer_id) is None:
            raise CustomerNotFoundError
        if self.get_account(account_id) is not None:
            raise DuplicateAccountError
        if account_type not in ("checking", "savings", "business"):
            raise InvalidAccountTypeError
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.repository.add_account(Account(
            account_id,
            customer_id,
            account_type,
            starting_balance,
            created_at
        ))

    def get_all_accounts(self):
        accounts = self.repository.get_all_accounts()
        if accounts is None:
            raise NoAccountsFoundError
        return accounts

    def get_accounts_by_customer(self, customer_id):
        if self.get_customer(customer_id) is None:
            raise CustomerNotFoundError
        accounts = self.repository.get_accounts_by_customer(customer_id)
        if accounts is None:
            raise NoCustomerAccountsFoundError
        return accounts

    def get_account(self, account_id):
        account = self.repository.get_account_by_id(account_id)
        if account is None:
            return None
        return account

    def deposit(self, account_id, amount):
        account = self.get_account(account_id)
        if account is None:
            raise AccountNotFoundError
        if amount <= 0:
            raise InvalidAmountError
        new_balance = account.balance + amount
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.repository.deposit_with_transaction(account_id, new_balance, amount, created_at)

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
        self.repository.withdraw_with_transaction(account_id, new_balance, amount, created_at)

    def transfer(self, from_account_id, to_account_id, amount):
        from_account = self.get_account(from_account_id)
        to_account = self.get_account(to_account_id)
        if from_account is None:
            raise SourceAccountNotFoundError
        if to_account is None:
            raise DestinationAccountNotFoundError
        if amount <= 0:
            raise InvalidAmountError
        if from_account.balance < amount:
            raise InsufficientFundsError
        new_from_balance = from_account.balance - amount
        new_to_balance = to_account.balance + amount
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.repository.transfer_with_transaction(
            from_account_id,
            to_account_id,
            new_from_balance,
            new_to_balance,
            amount,
            created_at
        )

    def get_all_transactions(self):
        transactions = self.repository.get_all_transactions()
        if transactions is None:
            raise NoTransactionsFoundError
        return transactions

    def get_transactions_for_account(self, account_id):
        if self.get_account(account_id) is None:
            raise AccountNotFoundError
        transactions = self.repository.get_transactions_for_account(account_id)
        if transactions is None:
            raise NoTransactionsFoundError
        return transactions

    def get_customer_statement(self, customer_id):
        customer = self.get_customer(customer_id)
        if customer is None:
            raise CustomerNotFoundError
        accounts = self.repository.get_accounts_by_customer(customer_id)
        total_balance = 0
        if accounts is not None:
            for account in accounts:
                total_balance += account.balance
        transactions = self.repository.get_transactions_for_customer(customer_id)
        return customer, accounts, total_balance, transactions

def display_customers(customers):
    for index, customer in enumerate(customers, start=1):
        customer.display(index)

def display_accounts(accounts):
    for index, account in enumerate(accounts, start=1):
        account.display(index)

def display_transactions(transactions):
    for index, transaction in enumerate(transactions, start=1):
        transaction.display(index)

def main():
    bank_service = BankService()
    while True:
        try:
            choice = int(input("1) Create customer\n"
                               "2) Show all customers\n"
                               "3) Create account for customer\n"
                               "4) Show accounts of a customer\n"
                               "5) Show all accounts\n"
                               "6) Deposit money\n"
                               "7) Withdraw money\n"
                               "8) Transfer money\n"
                               "9) Show all transactions\n"
                               "10) Show transactions for one account\n"
                               "11) Show customer statement\n"
                               "12) Exit\n"))
        except ValueError:
            print("Invalid choice! enter a number between 1 and 12.")
            continue
        match choice:
            case 1:
                customer_id = input("Enter customer id: ").strip()
                full_name = input("Enter full name: ").strip()
                email = input("Enter email: ").strip()
                try:
                    bank_service.create_customer(customer_id, full_name, email)
                except InvalidCustomerDataError:
                    print("Invalid customer data")
                    continue
                except DuplicateCustomerError:
                    print("Customer ID already exists")
                    continue
                except DuplicateEmailError:
                    print("Email already exists")
                    continue
                print("Customer created.")
            case 2:
                try:
                    customers = bank_service.get_all_customers()
                except NoCustomersFoundError:
                    print("No customers found")
                    continue
                display_customers(customers)
            case 3:
                account_id = input("Enter account id: ").strip()
                customer_id = input("Enter customer id: ").strip()
                account_type = input("Enter account type. must be checking, savings or business: ").strip().lower()
                try:
                    starting_balance = float(input("Enter starting balance: "))
                    bank_service.create_account(account_id, customer_id, account_type, starting_balance)
                except ValueError:
                    print("Invalid account data")
                    continue
                except InvalidAccountDataError:
                    print("Invalid account data")
                    continue
                except CustomerNotFoundError:
                    print("Customer not found")
                    continue
                except DuplicateAccountError:
                    print("Account ID already exists")
                    continue
                except InvalidAccountTypeError:
                    print("Invalid account type")
                    continue
                print("Account created.")
            case 4:
                customer_id = input("Enter customer id: ").strip()
                try:
                    accounts = bank_service.get_accounts_by_customer(customer_id)
                except CustomerNotFoundError:
                    print("Customer not found")
                    continue
                except NoCustomerAccountsFoundError:
                    print("No accounts found for this customer")
                    continue
                display_accounts(accounts)
            case 5:
                try:
                    accounts = bank_service.get_all_accounts()
                except NoAccountsFoundError:
                    print("No accounts found")
                    continue
                display_accounts(accounts)
            case 6:
                account_id = input("Enter account id: ").strip()
                try:
                    amount = float(input("Enter the amount to deposit: "))
                    bank_service.deposit(account_id, amount)
                except ValueError:
                    print("Invalid amount")
                    continue
                except AccountNotFoundError:
                    print("Account not found")
                    continue
                except InvalidAmountError:
                    print("Invalid amount")
                    continue
                print(f"{amount:.2f} deposited into {account_id}.")
            case 7:
                account_id = input("Enter account id: ").strip()
                try:
                    amount = float(input("Enter the amount to withdraw: "))
                    bank_service.withdraw(account_id, amount)
                except ValueError:
                    print("Invalid amount")
                    continue
                except AccountNotFoundError:
                    print("Account not found")
                    continue
                except InvalidAmountError:
                    print("Invalid amount")
                    continue
                except InsufficientFundsError:
                    print("Insufficient funds")
                    continue
                print(f"{amount:.2f} withdrawn from {account_id}.")
            case 8:
                from_account_id = input("Enter the source account: ").strip()
                to_account_id = input("Enter the destination account: ").strip()
                try:
                    amount = float(input("Enter the amount to transfer: "))
                    bank_service.transfer(from_account_id, to_account_id, amount)
                except ValueError:
                    print("Invalid amount")
                    continue
                except SourceAccountNotFoundError:
                    print("Source account not found")
                    continue
                except DestinationAccountNotFoundError:
                    print("Destination account not found")
                    continue
                except InvalidAmountError:
                    print("Invalid amount")
                    continue
                except InsufficientFundsError:
                    print("Insufficient funds")
                    continue
                print(f"{amount:.2f} transferred from {from_account_id} to {to_account_id}.")
            case 9:
                try:
                    transactions = bank_service.get_all_transactions()
                except NoTransactionsFoundError:
                    print("No transactions found")
                    continue
                display_transactions(transactions)
            case 10:
                account_id = input("Enter account id: ").strip()
                try:
                    transactions = bank_service.get_transactions_for_account(account_id)
                except AccountNotFoundError:
                    print("Account not found")
                    continue
                except NoTransactionsFoundError:
                    print("No transactions found")
                    continue
                print(f"Transactions for account id {account_id}: ")
                display_transactions(transactions)
            case 11:
                customer_id = input("Enter customer id: ").strip()
                try:
                    customer, accounts, total_balance, transactions = (
                        bank_service.get_customer_statement(customer_id))
                except CustomerNotFoundError:
                    print("Customer not found")
                    continue
                print("Customer ", end="")
                customer.display(1)
                print("\nAccounts:")
                if accounts is None:
                    print("No accounts found for this customer")
                else:
                    display_accounts(accounts)
                print(f"\nTotal balance: {total_balance:.2f}")
                print("\nTransactions")
                if transactions is None:
                    print("This customer does not have any transactions")
                else:
                    display_transactions(transactions)
            case 12:
                print("Goodbye!")
                break
            case _:
                print("Invalid choice! enter a number between 1 and 12.")

if __name__ == "__main__":
    main()