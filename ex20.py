#Thread-Safe Bank Transaction Processor

import threading
import csv
import json

class Account:
    def __init__(self, account_id, owner_name, balance):
        self.account_id = account_id
        self.owner_name = owner_name
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def display(self, index):
        print(f"[{index}] "
              f"Account: {self.account_id} | "
              f"Owner: {self.owner_name} | "
              f"Balance: {self.balance:.2f}")

class TransactionResult:
    def __init__(self,
                 transaction_type,
                 from_account_id,
                 to_account_id,
                 amount,
                 status,
                 message):
        self.transaction_type = transaction_type
        self.from_account_id = from_account_id
        self.to_account_id = to_account_id
        self.amount = amount
        self.status = status
        self.message = message

    def display(self):
        print(f"Type: {self.transaction_type} | "
              f"From: {self.from_account_id} | "
              f"To: {self.to_account_id} | "
              f"Amount: {self.amount:.2f} | "
              f"Status: {self.status} | "
              f"Message: {self.message}")

    def to_dict(self):
        return {
            "transaction_type": self.transaction_type,
            "from_account_id": self.from_account_id,
            "to_account_id": self.to_account_id,
            "amount": self.amount,
            "status": self.status,
            "message": self.message
        }

def find_account(accounts, account_id):
    for account in accounts:
        if account.account_id == account_id:
            return account
    return None

def add_account(accounts):
    account_id = input("Enter the account ID: ").strip()
    if not account_id:
        print("Invalid account data")
        return
    if find_account(accounts, account_id):
        print("Account ID already exists")
        return
    owner_name = input("Enter the owner name: ").strip()
    if not owner_name:
        print("Invalid account data")
        return
    try:
        balance = float(input("Enter starting balance: "))
    except ValueError:
        print("Invalid account data")
        return
    if balance < 0:
        print("Invalid account data")
        return
    accounts.append(Account(account_id, owner_name, balance))
    print("Account added.")

def show_accounts(accounts):
    if not accounts:
        print("No accounts available")
        return
    for index, account in enumerate(accounts, start=1):
        account.display(index)

def deposit(accounts, from_acc, amount):
    account = find_account(accounts, from_acc)
    if not account:
        return TransactionResult(
            "deposit",
            from_acc,
            None,
            amount,
            "Failed",
            "Account not found"
        )
    if amount <= 0:
        return TransactionResult(
            "deposit",
            from_acc,
            None,
            amount,
            "Failed",
            "Amount must be greater than 0"
        )
    account.deposit(amount)
    return TransactionResult(
        "deposit",
        from_acc,
        None,
        amount,
        "Success",
        "Deposit completed"
    )

def withdraw(accounts, from_acc, amount):
    account = find_account(accounts, from_acc)
    if not account:
        return TransactionResult(
            "withdraw",
            from_acc,
            None,
            amount,
            "Failed",
            "Account not found"
        )
    if amount <= 0:
        return TransactionResult(
            "withdraw",
            from_acc,
            None,
            amount,
            "Failed",
            "Amount must be greater than 0"
        )
    if account.balance < amount:
        return TransactionResult(
            "withdraw",
            from_acc,
            None,
            amount,
            "Failed",
            "Insufficient funds"
        )
    account.withdraw(amount)
    return TransactionResult(
        "withdraw",
        from_acc,
        None,
        amount,
        "Success",
        "Withdrawal completed"
    )

def transfer(accounts, from_acc, to_acc, amount):
    from_account = find_account(accounts, from_acc)
    if not from_account:
        return TransactionResult(
            "transfer",
            from_acc,
            to_acc,
            amount,
            "Failed",
            "From account not found"
        )
    to_account = find_account(accounts, to_acc)
    if not to_account:
        return TransactionResult(
            "transfer",
            from_acc,
            to_acc,
            amount,
            "Failed",
            "To account not found"
        )
    if amount <= 0:
        return TransactionResult(
            "transfer",
            from_acc,
            to_acc,
            amount,
            "Failed",
            "Amount must be greater than 0"
        )
    if from_account.balance < amount:
        return TransactionResult(
            "transfer",
            from_acc,
            to_acc,
            amount,
            "Failed",
            "Insufficient funds"
        )
    from_account.withdraw(amount)
    to_account.deposit(amount)
    return TransactionResult(
        "transfer",
        from_acc,
        to_acc,
        amount,
        "Success",
        "Transfer completed"
    )

def load_from_csv():
    file_name = "transactions.csv"
    transactions = []
    try:
        with open(file_name, "r") as file:
            reader = csv.reader(file)
            header = next(reader, None)
            for row in reader:
                try:
                    if len(row) != 4:
                        continue
                    elif (row[0] == "deposit" or
                        row[0] == "withdraw" or
                        row[0] == "transfer"):
                        transactions.append(
                            {
                                "type": row[0],
                                "from_account_id": row[1],
                                "to_account_id": row[2],
                                "amount": float(row[3])
                            }
                        )
                    else:
                        continue
                except ValueError:
                    continue
    except FileNotFoundError:
        print("File not found")
        return None
    except PermissionError:
        print("Permission denied")
        return None
    print("Transactions loaded.")
    return transactions

def process_transactions(transactions, accounts):
    if not transactions:
        print("No transactions loaded")
        return None
    if not accounts:
        print("No accounts available")
        return None
    threads = []
    lock = threading.Lock()
    results = []
    for transaction in transactions:
        thread = threading.Thread(
            target=process_transaction,
            args=(transaction, accounts, results, lock)
        )
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print("Transactions processed.")
    return results

def process_transaction(transaction, accounts, results, lock):
    with lock:
        transaction_type = transaction.get("type")
        from_account_id = transaction.get("from_account_id")
        to_account_id = transaction.get("to_account_id")
        amount = transaction.get("amount")
        if transaction_type == "deposit":
            transaction_report = deposit(accounts, from_account_id, amount)
        elif transaction_type == "withdraw":
            transaction_report = withdraw(accounts, from_account_id, amount)
        elif transaction_type == "transfer":
            transaction_report = transfer(accounts, from_account_id, to_account_id, amount)
        else:
            return
        results.append(transaction_report)

def show_transaction_report(results):
    if not results:
        print("No report available")
        return
    for result in results:
        result.display()

def save_to_json(results):
    file_name = "transaction_report.json"
    if not results:
        print("No report available")
        return
    try:
        with open(file_name, "w") as file:
            data = []
            for result in results:
                data.append(result.to_dict())
            json.dump(data, file, indent=4)
    except PermissionError:
        print("Permission denied")
        return
    print("Report saved.")

def main():
    accounts = []
    transactions = []
    results = []
    while True:
        try:
            choice = int(input("1) Add account\n"
                               "2) Show all accounts\n"
                               "3) Load transactions from CSV\n" 
                               "4) Process loaded transactions\n"
                               "5) Show transaction report\n"
                               "6) Save report to JSON\n"
                               "7) Exit\n"))
        except ValueError:
            print("Invalid choice! choose between 1 and 7")
            continue
        match choice:
            case 1:
                add_account(accounts)
            case 2:
                show_accounts(accounts)
            case 3:
                loaded_transactions = load_from_csv()
                if loaded_transactions is not None:
                    transactions = loaded_transactions
            case 4:
                loaded_results = process_transactions(transactions, accounts)
                if loaded_results is not None:
                    results = loaded_results
            case 5:
                show_transaction_report(results)
            case 6:
                save_to_json(results)
            case 7:
                print("Goodbye!")
                break
            case _:
                print("Invalid choice! choose between 1 and 7")

if __name__ == "__main__":
    main()