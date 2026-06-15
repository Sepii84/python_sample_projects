# SQLite Bank System v4: Debit Cards, Foreign Keys, and JOIN Reports

from dataclasses import dataclass
import sqlite3
import datetime

# Exceptions
class Exceptions:
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

    class CardNotFoundError(BankError):
        pass

    class DuplicateCardError(BankError):
        pass

    class InvalidCardDataError(BankError):
        pass

    class CardFrozenError(BankError):
        pass

    class CardCancelledError(BankError):
        pass

    class CardLimitExceededError(BankError):
        pass

    class NoCardsFoundError(BankError):
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
class Card:
    card_id: str
    account_id: str
    card_holder_name: str
    card_status: str
    daily_limit: float
    daily_spent: float
    created_at: str

    def display(self, index):
        print(f"[{index}] "
              f"card_id: {self.card_id} | "
              f"account_id: {self.account_id} | "
              f"card_holder_name: {self.card_holder_name} | "
              f"card_status: {self.card_status} | "
              f"daily_limit: {self.daily_limit:.2f} | "
              f"daily_spent: {self.daily_spent:.2f} | "
              f"created_at: {self.created_at}")

@dataclass
class TransactionRecord:
    transaction_id: int
    transaction_type: str
    from_account_id: str
    to_account_id: str
    amount: float
    description: str
    created_at: str

    def display(self, index):
        print(f"[{index}] "
              f"transaction_id: {self.transaction_id} | "
              f"transaction_type: {self.transaction_type} | "
              f"from_account_id: {self.from_account_id} | "
              f"to_account_id: {self.to_account_id} | "
              f"amount: {self.amount:.2f} | "
              f"description: {self.description} | "
              f"created_at: {self.created_at}")

# Database connection

class BankRepository:
    def __init__(self, db_name = "bank.db"):
        self.db_name = db_name
        self.create_tables()

    def get_connection(self):
        connection = sqlite3.connect(self.db_name)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def create_tables(self):
        with self.get_connection() as connection:
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
                            CREATE TABLE IF NOT EXISTS cards(
                                card_id TEXT PRIMARY KEY,
                                account_id TEXT NOT NULL REFERENCES accounts(account_id),
                                card_holder_name TEXT NOT NULL,
                                card_status TEXT NOT NULL CHECK(card_status IN ('active', 'frozen', 'cancelled')),
                                daily_limit REAL NOT NULL,
                                daily_spent REAL NOT NULL,
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
                                description TEXT,
                                created_at TEXT NOT NULL
                            )
            """)

    def add_customer(self, customer):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            INSERT INTO customers (customer_id, full_name, email, created_at)
                            VALUES (?, ?, ?, ?)
            """,(customer.customer_id,
                           customer.full_name,
                           customer.email,
                           customer.created_at))

    def get_customer_by_id(self, customer_id):
        with self.get_connection() as connection:
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
        with self.get_connection() as connection:
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
        with self.get_connection() as connection:
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
        with self.get_connection() as connection:
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
        with self.get_connection() as connection:
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
        with self.get_connection() as connection:
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
        with self.get_connection() as connection:
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

    def add_card(self, card):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            INSERT INTO cards 
                                (card_id, account_id, card_holder_name, card_status, daily_limit, daily_spent, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                card.card_id,
                card.account_id,
                card.card_holder_name,
                card.card_status,
                card.daily_limit,
                card.daily_spent,
                card.created_at
                  ))

    def get_card_by_id(self, card_id):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT 
                    card_id, 
                    account_id, 
                    card_holder_name, 
                    card_status, 
                    daily_limit, 
                    daily_spent, 
                    created_at
                FROM cards 
                WHERE card_id = ?
            """, (card_id, ))
            row = cursor.fetchone()
        if not row:
            return None
        return Card(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6]
        )

    def get_cards_by_account(self, account_id):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT 
                    card_id, 
                    account_id, 
                    card_holder_name, 
                    card_status, 
                    daily_limit, 
                    daily_spent, 
                    created_at
                FROM cards 
                WHERE account_id = ?
            """, (account_id,))
            rows = cursor.fetchall()
        if not rows:
            return None
        cards = []
        for row in rows:
            cards.append(Card(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6]
            ))
        return cards

    def get_cards_by_customer(self, customer_id):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT 
                    c.card_id, 
                    c.account_id, 
                    c.card_holder_name, 
                    c.card_status, 
                    c.daily_limit, 
                    c.daily_spent, 
                    c.created_at
                FROM cards c
                INNER JOIN accounts a
                ON c.account_id = a.account_id
                WHERE a.customer_id = ?
            """, (customer_id,))
            rows = cursor.fetchall()
        if not rows:
            return None
        cards = []
        for row in rows:
            cards.append(Card(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6]
            ))
        return cards

    def update_card_status(self, card_id, new_status):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE cards
                SET card_status = ?
                WHERE card_id = ?
            """, (new_status, card_id))

    def deposit_with_transaction(self, account_id, new_balance, amount, description, created_at):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            UPDATE accounts
                            SET balance = ?
                            WHERE account_id = ?
            """, (new_balance, account_id))
            cursor.execute("""
                            INSERT INTO transactions 
                                (transaction_type, from_account_id, to_account_id, amount, description, created_at)
                            VALUES (?, ?, ?, ?, ?, ?)
            """, ("deposit", None, account_id, amount, description, created_at))

    def withdraw_with_transaction(self, account_id, new_balance, amount, description, created_at):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            UPDATE accounts
                            SET balance = ?
                            WHERE account_id = ?
            """, (new_balance, account_id))
            cursor.execute("""
                            INSERT INTO transactions 
                                (transaction_type, from_account_id, to_account_id, amount, description, created_at)
                            VALUES (?, ?, ?, ?, ?, ?)
            """, ("withdraw", account_id, None, amount, description, created_at))

    def card_payment_with_transaction(
            self,
            card_id,
            account_id,
            new_balance,
            new_daily_spent,
            amount,
            description,
            created_at):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            UPDATE cards
                            SET daily_spent = ?
                            WHERE card_id = ?
            """, (new_daily_spent, card_id))
            cursor.execute("""
                            UPDATE accounts
                            SET balance = ?
                            WHERE account_id = ?
            """, (new_balance, account_id))
            cursor.execute("""
                            INSERT INTO transactions 
                                (transaction_type, from_account_id, to_account_id, amount, description, created_at)
                            VALUES (?, ?, ?, ?, ?, ?)
            """, ("card_payment", account_id, None, amount, description, created_at))


    def transfer_with_transaction(self,
                                  from_account_id,
                                  to_account_id,
                                  new_from_balance,
                                  new_to_balance,
                                  amount,
                                  description,
                                  created_at):
        with self.get_connection() as connection:
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
                                (transaction_type, from_account_id, to_account_id, amount, description, created_at)
                            VALUES (?, ?, ?, ?, ?, ?)
            """, ("transfer", from_account_id, to_account_id, amount, description, created_at))

    def get_all_transactions(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            SELECT 
                                transaction_id, 
                                transaction_type, 
                                from_account_id, 
                                to_account_id, 
                                amount, 
                                description, 
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
                row[6]
            ))
        return transactions

    def get_transactions_for_account(self, account_id):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            SELECT 
                                transaction_id, 
                                transaction_type, 
                                from_account_id, 
                                to_account_id, 
                                amount, 
                                description,
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
                row[6]
            ))
        return transactions

    def get_transactions_for_customer(self, customer_id):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            SELECT 
                                transaction_id, 
                                transaction_type, 
                                from_account_id, 
                                to_account_id, 
                                amount, 
                                description,
                                created_at
                            FROM transactions t
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
                row[6]
            ))
        return transactions

    def get_joined_account_report(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    a.account_id,
                    c.full_name,
                    c.email,
                    a.account_type,
                    a.balance
                FROM accounts a
                JOIN customers c
                    ON a.customer_id = c.customer_id
                ORDER BY a.account_id
            """)
            rows = cursor.fetchall()
        if not rows:
            return None
        return rows

    def get_joined_card_report(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    ca.card_id,
                    ca.card_status,
                    ca.daily_limit,
                    ca.daily_spent,
                    a.account_id,
                    cu.full_name,
                    a.balance
                FROM cards ca
                JOIN accounts a
                    ON ca.account_id = a.account_id
                JOIN customers cu
                    ON a.customer_id = cu.customer_id
                ORDER BY ca.card_id
            """)
            rows = cursor.fetchall()
        if not rows:
            return None
        return rows

# Bridge of Database connection and main

class BankService:
    def __init__(self):
        self.repository = BankRepository()

    def create_customer(self, customer_id, full_name, email):
        if not customer_id or not full_name or not email:
            raise Exceptions.InvalidCustomerDataError
        if self.get_customer(customer_id) is not None:
            raise Exceptions.DuplicateCustomerError
        if self.get_customer_by_email(email) is not None:
            raise Exceptions.DuplicateEmailError
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
            raise Exceptions.NoCustomersFoundError
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
            raise Exceptions.InvalidAccountDataError
        if self.repository.get_customer_by_id(customer_id) is None:
            raise Exceptions.CustomerNotFoundError
        if self.get_account(account_id) is not None:
            raise Exceptions.DuplicateAccountError
        if account_type not in ("checking", "savings", "business"):
            raise Exceptions.InvalidAccountTypeError
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
            raise Exceptions.NoAccountsFoundError
        return accounts

    def get_accounts_by_customer(self, customer_id):
        if self.get_customer(customer_id) is None:
            raise Exceptions.CustomerNotFoundError
        accounts = self.repository.get_accounts_by_customer(customer_id)
        if accounts is None:
            raise Exceptions.NoCustomerAccountsFoundError
        return accounts

    def get_account(self, account_id):
        account = self.repository.get_account_by_id(account_id)
        if account is None:
            return None
        return account

    def issue_card(self, card_id, account_id, daily_limit):
        if not card_id or daily_limit <= 0:
            raise Exceptions.InvalidCardDataError
        account = self.get_account(account_id)
        if account is None:
            raise Exceptions.AccountNotFoundError
        if self.get_card(card_id) is not None:
            raise Exceptions.DuplicateCardError
        card_status = "active"
        daily_spent = 0
        card_holder_name = self.get_customer(account.customer_id).full_name
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.repository.add_card(Card(
            card_id,
            account_id,
            card_holder_name,
            card_status,
            daily_limit,
            daily_spent,
            created_at
        ))

    def get_card(self, card_id):
        return self.repository.get_card_by_id(card_id)

    def get_cards_by_account(self, account_id):
        if self.get_account(account_id) is None:
            raise Exceptions.AccountNotFoundError
        cards = self.repository.get_cards_by_account(account_id)
        if cards is None:
            raise Exceptions.NoCardsFoundError
        return cards

    def get_cards_by_customer(self, customer_id):
        if self.get_customer(customer_id) is None:
            raise Exceptions.CustomerNotFoundError
        cards = self.repository.get_cards_by_customer(customer_id)
        if cards is None:
            raise Exceptions.NoCardsFoundError
        return cards

    def freeze_card(self, card_id):
        card = self.get_card(card_id)
        if card is None:
            raise Exceptions.CardNotFoundError
        if card.card_status == "cancelled":
            raise Exceptions.CardCancelledError
        self.repository.update_card_status(card_id, "frozen")

    def unfreeze_card(self, card_id):
        card = self.get_card(card_id)
        if card is None:
            raise Exceptions.CardNotFoundError
        if card.card_status == "cancelled":
            raise Exceptions.CardCancelledError
        self.repository.update_card_status(card_id, "active")

    def pay_with_card(self, card_id, merchant_name, amount):
        card = self.get_card(card_id)
        if card is None:
            raise Exceptions.CardNotFoundError
        if card.card_status == "cancelled":
            raise Exceptions.CardCancelledError
        if card.card_status == "frozen":
            raise Exceptions.CardFrozenError
        if amount <= 0:
            raise Exceptions.InvalidAmountError
        if not merchant_name:
            raise Exceptions.InvalidCardDataError
        account = self.get_account(card.account_id)
        if account is None:
            raise Exceptions.AccountNotFoundError
        if account.balance < amount:
            raise Exceptions.InsufficientFundsError
        if card.daily_spent + amount > card.daily_limit:
            raise Exceptions.CardLimitExceededError
        new_balance = account.balance - amount
        new_daily_spent = card.daily_spent + amount
        description = f"Card payment at {merchant_name} with card {card_id}"
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.repository.card_payment_with_transaction(
            card_id,
            account.account_id,
            new_balance,
            new_daily_spent,
            amount,
            description,
            created_at
        )

    def deposit(self, account_id, description, amount):
        account = self.get_account(account_id)
        if account is None:
            raise Exceptions.AccountNotFoundError
        if amount <= 0:
            raise Exceptions.InvalidAmountError
        new_balance = account.balance + amount
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.repository.deposit_with_transaction(account_id, new_balance, amount, description, created_at)

    def withdraw(self, account_id, description, amount):
        account = self.get_account(account_id)
        if account is None:
            raise Exceptions.AccountNotFoundError
        if amount <= 0:
            raise Exceptions.InvalidAmountError
        if account.balance < amount:
            raise Exceptions.InsufficientFundsError
        new_balance = account.balance - amount
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.repository.withdraw_with_transaction(account_id, new_balance, amount, description, created_at)

    def transfer(self, from_account_id, to_account_id, description, amount):
        from_account = self.get_account(from_account_id)
        to_account = self.get_account(to_account_id)
        if from_account is None:
            raise Exceptions.SourceAccountNotFoundError
        if to_account is None:
            raise Exceptions.DestinationAccountNotFoundError
        if amount <= 0:
            raise Exceptions.InvalidAmountError
        if from_account.balance < amount:
            raise Exceptions.InsufficientFundsError
        new_from_balance = from_account.balance - amount
        new_to_balance = to_account.balance + amount
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.repository.transfer_with_transaction(
            from_account_id,
            to_account_id,
            new_from_balance,
            new_to_balance,
            amount,
            description,
            created_at
        )

    def get_all_transactions(self):
        transactions = self.repository.get_all_transactions()
        if transactions is None:
            raise Exceptions.NoTransactionsFoundError
        return transactions

    def get_transactions_for_account(self, account_id):
        if self.get_account(account_id) is None:
            raise Exceptions.AccountNotFoundError
        transactions = self.repository.get_transactions_for_account(account_id)
        if transactions is None:
            raise Exceptions.NoTransactionsFoundError
        return transactions

    def get_customer_statement(self, customer_id):
        customer = self.get_customer(customer_id)
        if customer is None:
            raise Exceptions.CustomerNotFoundError
        accounts = self.repository.get_accounts_by_customer(customer_id)
        total_balance = 0
        if accounts is not None:
            for account in accounts:
                total_balance += account.balance
        transactions = self.repository.get_transactions_for_customer(customer_id)
        return customer, accounts, total_balance, transactions

    def get_joined_account_report(self):
        rows = self.repository.get_joined_account_report()
        if not rows:
            raise Exceptions.NoAccountsFoundError
        accounts = []
        for row in rows:
            accounts.append({
                "account_id": row[0],
                "full_name": row[1],
                "email": row[2],
                "account_type": row[3],
                "balance": row[4]
            })
        return accounts

    def get_joined_card_report(self):
        rows = self.repository.get_joined_card_report()
        if not rows:
            raise Exceptions.NoCardsFoundError
        cards = []
        for row in rows:
            cards.append({
                "card_id": row[0],
                "card_status": row[1],
                "daily_limit": row[2],
                "daily_spent": row[3],
                "account_id": row[4],
                "full_name": row[5],
                "balance": row[6]

            })
        return cards

# Printer functions

def display_customers(customers):
    for index, customer in enumerate(customers, start=1):
        customer.display(index)

def display_accounts(accounts):
    for index, account in enumerate(accounts, start=1):
        account.display(index)

def display_transactions(transactions):
    for index, transaction in enumerate(transactions, start=1):
        transaction.display(index)

def display_cards(cards):
    for index, card in enumerate(cards, start=1):
        card.display(index)

def display_joined_accounts(accounts):
    for index, account in enumerate(accounts, start=1):
        account_id = account["account_id"]
        full_name = account["full_name"]
        email = account["email"]
        account_type = account["account_type"]
        balance = account["balance"]
        print(f"[{index}] {account_id} | {full_name} | {email} | {account_type} | {balance:.2f}")

def display_joined_cards(cards):
    for index, card in enumerate(cards, start=1):
        card_id = card["card_id"]
        card_status = card["card_status"]
        daily_limit = card["daily_limit"]
        daily_spent = card["daily_spent"]
        account_id = card["account_id"]
        full_name = card["full_name"]
        balance = card["balance"]
        print(f"[{index}] {card_id} | "
              f"{card_status} | "
              f"{daily_limit:.2f} | "
              f"{daily_spent:.2f} | "
              f"{account_id} | "
              f"{full_name} | "
              f"{balance:.2f}")

# Main

def main():
    bank_service = BankService()
    while True:
        try:
            choice = int(input("1) Create customer\n"
                               "2) Show all customers\n"
                               "3) Create account for customer\n"
                               "4) Show accounts of customer\n"
                               "5) Show all accounts\n"
                               "6) Issue card for account\n"
                               "7) Show cards of account\n"
                               "8) Show cards of customer\n"
                               "9) Freeze card\n"
                               "10) Unfreeze card\n"
                               "11) Pay with card\n"
                               "12) Deposit money\n"
                               "13) Withdraw money\n"
                               "14) Transfer money\n"
                               "15) Show all transactions\n"
                               "16) Show transactions for one account\n"
                               "17) Show customer statement\n"
                               "18) Show joined account report\n"
                               "19) Show joined card report\n"
                               "20) Exit\n"))
        except ValueError:
            print("Invalid choice! enter a number between 1 and 20.")
            continue
        match choice:
            case 1:
                customer_id = input("Enter customer id: ").strip()
                full_name = input("Enter full name: ").strip()
                email = input("Enter email: ").strip()
                try:
                    bank_service.create_customer(customer_id, full_name, email)
                except Exceptions.InvalidCustomerDataError:
                    print("Invalid customer data")
                    continue
                except Exceptions.DuplicateCustomerError:
                    print("Customer ID already exists")
                    continue
                except Exceptions.DuplicateEmailError:
                    print("Email already exists")
                    continue
                print("Customer created.")
            case 2:
                try:
                    customers = bank_service.get_all_customers()
                except Exceptions.NoCustomersFoundError:
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
                except Exceptions.InvalidAccountDataError:
                    print("Invalid account data")
                    continue
                except Exceptions.CustomerNotFoundError:
                    print("Customer not found")
                    continue
                except Exceptions.DuplicateAccountError:
                    print("Account ID already exists")
                    continue
                except Exceptions.InvalidAccountTypeError:
                    print("Invalid account type")
                    continue
                print("Account created.")
            case 4:
                customer_id = input("Enter customer id: ").strip()
                try:
                    accounts = bank_service.get_accounts_by_customer(customer_id)
                except Exceptions.CustomerNotFoundError:
                    print("Customer not found")
                    continue
                except Exceptions.NoCustomerAccountsFoundError:
                    print("No accounts found for this customer")
                    continue
                display_accounts(accounts)
            case 5:
                try:
                    accounts = bank_service.get_all_accounts()
                except Exceptions.NoAccountsFoundError:
                    print("No accounts found")
                    continue
                display_accounts(accounts)
            case 6:
                card_id = input("Enter card id: ").strip()
                account_id = input("Enter account id: ").strip()
                try:
                    daily_limit = float(input("Enter daily limit: "))
                    bank_service.issue_card(card_id, account_id, daily_limit)
                except ValueError:
                    print("Invalid card data")
                    continue
                except Exceptions.InvalidCardDataError:
                    print("Invalid card data")
                    continue
                except Exceptions.AccountNotFoundError:
                    print("Account not found")
                    continue
                except Exceptions.DuplicateCardError:
                    print("Card ID already exists")
                    continue
                print("Card issued.")
            case 7:
                account_id = input("Enter account id: ").strip()
                try:
                    cards = bank_service.get_cards_by_account(account_id)
                except Exceptions.AccountNotFoundError:
                    print("Account not found")
                    continue
                except Exceptions.NoCardsFoundError:
                    print("No cards found")
                    continue
                print(f"Cards for the account {account_id}: ")
                display_cards(cards)
            case 8:
                customer_id = input("Enter customer id: ").strip()
                try:
                    cards = bank_service.get_cards_by_customer(customer_id)
                except Exceptions.CustomerNotFoundError:
                    print("Customer not found")
                    continue
                except Exceptions.NoCardsFoundError:
                    print("No cards found")
                    continue
                print(f"Cards for the customer {customer_id}: ")
                display_cards(cards)
            case 9:
                card_id = input("Enter card id: ").strip()
                try:
                    bank_service.freeze_card(card_id)
                except Exceptions.CardNotFoundError:
                    print("Card not found")
                    continue
                except Exceptions.CardCancelledError:
                    print("Card is cancelled")
                    continue
                print("Card frozen.")
            case 10:
                card_id = input("Enter card id: ").strip()
                try:
                    bank_service.unfreeze_card(card_id)
                except Exceptions.CardNotFoundError:
                    print("Card not found")
                    continue
                except Exceptions.CardCancelledError:
                    print("Card is cancelled")
                    continue
                print("Card unfrozen.")
            case 11:
                card_id = input("Enter card id: ").strip()
                merchant_name = input("Enter merchant name: ").strip()
                try:
                    amount = float(input("Enter amount: "))
                    bank_service.pay_with_card(card_id, merchant_name, amount)
                except ValueError:
                    print("Invalid amount")
                    continue
                except Exceptions.CardNotFoundError:
                    print("Card not found")
                    continue
                except Exceptions.CardFrozenError:
                    print("Card is frozen")
                    continue
                except Exceptions.CardCancelledError:
                    print("Card is cancelled")
                    continue
                except Exceptions.InvalidAmountError:
                    print("Invalid amount")
                    continue
                except Exceptions.InvalidCardDataError:
                    print("Invalid card data")
                    continue
                except Exceptions.AccountNotFoundError:
                    print("Account not found")
                    continue
                except Exceptions.InsufficientFundsError:
                    print("Insufficient funds")
                    continue
                except Exceptions.CardLimitExceededError:
                    print("Card daily limit exceeded")
                    continue
                print("Payment completed")
            case 12:
                account_id = input("Enter account id: ").strip()
                try:
                    amount = float(input("Enter the amount to deposit: "))
                    description = input("Enter description: ").strip()
                    bank_service.deposit(account_id, description, amount)
                except ValueError:
                    print("Invalid amount")
                    continue
                except Exceptions.AccountNotFoundError:
                    print("Account not found")
                    continue
                except Exceptions.InvalidAmountError:
                    print("Invalid amount")
                    continue
                print(f"{amount:.2f} deposited into {account_id}.")
            case 13:
                account_id = input("Enter account id: ").strip()
                try:
                    amount = float(input("Enter the amount to withdraw: "))
                    description = input("Enter description: ").strip()
                    bank_service.withdraw(account_id, description, amount)
                except ValueError:
                    print("Invalid amount")
                    continue
                except Exceptions.AccountNotFoundError:
                    print("Account not found")
                    continue
                except Exceptions.InvalidAmountError:
                    print("Invalid amount")
                    continue
                except Exceptions.InsufficientFundsError:
                    print("Insufficient funds")
                    continue
                print(f"{amount:.2f} withdrawn from {account_id}.")
            case 14:
                from_account_id = input("Enter the source account: ").strip()
                to_account_id = input("Enter the destination account: ").strip()
                try:
                    amount = float(input("Enter the amount to transfer: "))
                    description = input("Enter description: ").strip()
                    bank_service.transfer(from_account_id, to_account_id, description, amount)
                except ValueError:
                    print("Invalid amount")
                    continue
                except Exceptions.SourceAccountNotFoundError:
                    print("Source account not found")
                    continue
                except Exceptions.DestinationAccountNotFoundError:
                    print("Destination account not found")
                    continue
                except Exceptions.InvalidAmountError:
                    print("Invalid amount")
                    continue
                except Exceptions.InsufficientFundsError:
                    print("Insufficient funds")
                    continue
                print(f"{amount:.2f} transferred from {from_account_id} to {to_account_id}.")
            case 15:
                try:
                    transactions = bank_service.get_all_transactions()
                except Exceptions.NoTransactionsFoundError:
                    print("No transactions found")
                    continue
                display_transactions(transactions)
            case 16:
                account_id = input("Enter account id: ").strip()
                try:
                    transactions = bank_service.get_transactions_for_account(account_id)
                except Exceptions.AccountNotFoundError:
                    print("Account not found")
                    continue
                except Exceptions.NoTransactionsFoundError:
                    print("No transactions found")
                    continue
                print(f"Transactions for account id {account_id}: ")
                display_transactions(transactions)
            case 17:
                customer_id = input("Enter customer id: ").strip()
                try:
                    customer, accounts, total_balance, transactions = (
                        bank_service.get_customer_statement(customer_id))
                except Exceptions.CustomerNotFoundError:
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
            case 18:
                try:
                    accounts = bank_service.get_joined_account_report()
                except Exceptions.NoAccountsFoundError:
                    print("No accounts found")
                    continue
                display_joined_accounts(accounts)
            case 19:
                try:
                    cards = bank_service.get_joined_card_report()
                except Exceptions.NoCardsFoundError:
                    print("No cards found")
                    continue
                display_joined_cards(cards)
            case 20:
                print("Goodbye!")
                break
            case _:
                print("Invalid choice! enter a number between 1 and 20.")

if __name__ == "__main__":
    main()