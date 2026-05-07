# bank account manager

class BankAccount:
    def __init__(self, owner, account_number, balance):
        self.owner = owner
        self.account_number = account_number
        self.balance = balance
    def __str__(self):
        return (f"Owner: {self.owner}, "
                f"Account Number: {self.account_number}, "
                f"Balance: {self.balance:.1f}")

class Bank:
    def __init__(self):
        self.accounts =[]

    def find_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        return None

    def create_account(self, owner, account_number, balance):
        self.accounts.append(BankAccount(owner, account_number, balance))
        print("Account created.")

    def show_accounts(self):
        if not self.accounts:
            print("No accounts available")
            return
        for account in self.accounts:
            print(account)

    def deposit(self, account_number, amount):
        account = self.find_account(account_number)
        account.balance += amount
        print("Deposit successful.")

    def withdraw(self, account_number, amount):
        account = self.find_account(account_number)
        if account.balance < amount:
            print("Insufficient funds")
            return
        account.balance -= amount
        print("Withdraw successful.")

    def transfer(self, from_acc, to_acc, amount):
        sender = self.find_account(from_acc)
        reciever = self.find_account(to_acc)

        if sender.balance < amount:
            print("Insufficient funds")
            return
        sender.balance -= amount
        reciever.balance += amount
        print("Transfer successful.")

    def search_account(self, account_number):
        account = self.find_account(account_number)
        if not account:
            print("Account not found")
            return
        print(account)

def main():
    bank = Bank()
    while True:
        print("-----------------------------")
        try:
            choice = int(input("1) Create account\n"
                               "2) Show all accounts\n"
                               "3) Deposit money\n"
                               "4) Withdraw money\n"
                               "5) Transfer money\n"
                               "6) Search account by account number\n"
                               "7) Exit\n"))
        except ValueError:
            print("Please enter a number between 1 and 7")
            continue
        match choice:
            case 1:
                owner = input("Enter owner name: ").strip()
                if not owner:
                    print("Invalid account data")
                    continue
                try:
                    acc_num = int(input("Enter account number: "))
                except ValueError:
                    print("Invalid account data")
                    continue
                if bank.find_account(acc_num):
                    print("Account number already exists")
                    continue
                try:
                    initial_balance = float(input("Enter the initial balance you want to deposit: "))
                except ValueError:
                    print("Invalid amount")
                    continue
                if initial_balance < 0:
                    print("Invalid amount")
                    continue
                bank.create_account(owner, acc_num, initial_balance)
            case 2:
                bank.show_accounts()
            case 3:
                try:
                    acc_num = int(input("Enter account number: "))
                except ValueError:
                    print("Invalid account data")
                    continue
                if not bank.find_account(acc_num):
                    print("Account not found")
                    continue
                try:
                    amount = float(input("Enter the amount you want to deposit: "))
                except ValueError:
                    print("Invalid amount")
                    continue
                if amount <= 0:
                    print("Invalid amount")
                    continue
                bank.deposit(acc_num, amount)
            case 4:
                try:
                    acc_num = int(input("Enter account number: "))
                except ValueError:
                    print("Invalid account data")
                    continue
                if not bank.find_account(acc_num):
                    print("Account not found")
                    continue
                try:
                    amount = float(input("Enter the amount you want to withdraw: "))
                except ValueError:
                    print("Invalid amount")
                    continue
                if amount <= 0:
                    print("Invalid amount")
                    continue
                bank.withdraw(acc_num, amount)
            case 5:
                try:
                    sender_acc_num = int(input("Enter sender account number: "))
                except ValueError:
                    print("Invalid account data")
                    continue
                if not bank.find_account(sender_acc_num):
                    print("Account not found")
                    continue
                try:
                    receiver_acc_num = int(input("Enter recienver account number: "))
                except ValueError:
                    print("Invalid account data")
                    continue
                if not bank.find_account(receiver_acc_num):
                    print("Account not found")
                    continue
                try:
                    amount = float(input("Enter the amount you want to transfer: "))
                except ValueError:
                    print("Invalid amount")
                    continue
                if amount <= 0:
                    print("Invalid amount")
                    continue
                bank.transfer(sender_acc_num, receiver_acc_num, amount)
            case 6:
                try:
                    acc_num = int(input("Enter account number: "))
                except ValueError:
                    print("Invalid account data")
                    continue
                bank.search_account(acc_num)
            case 7:
                print("Goodbye!")
                break
            case _:
                print("Please enter a number between 1 and 7")

if __name__ == '__main__':
    main()