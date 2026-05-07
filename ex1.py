#simple ATM menu

def show_balance(balance):
    print(f"Balance: {balance:.2f}")
def deposit_money():
    try:
        amount = float(input("enter the amount you want to deposit: "))
    except ValueError:
        print("Invalid deposit amount.")
        return 0
    if amount <= 0:
        print("Invalid deposit amount.")
        return 0
    print(f"Deposited: {amount:.2f}")
    return amount
def withdraw_money(balance):
    try:
        amount = float(input("enter the amount you want to withdraw: "))
    except ValueError:
        print("Invalid withdrawal amount.")
        return 0
    if amount <= 0:
        print("Invalid withdrawal amount.")
        return 0
    if amount > balance:
        print("Insufficient funds.")
        return 0
    print(f"Withdrawn: {amount:.2f}")
    return amount
def main():
    balance = 1000
    is_running = True
    while True:
        print("-----------------------")
        choice = input("choose between:\n"
                       "1) show balance\n"
                       "2) deposit money\n"
                       "3) withdraw money\n"
                       "4) exit\n")
        match choice:
            case "1":
                show_balance(balance)
            case "2":
                balance += deposit_money() 
            case "3":
                balance -= withdraw_money(balance)
            case "4":
                print("Goodbye!")
                break
            case _:
                print("Invalid choice.")
if __name__ == '__main__':
    main()