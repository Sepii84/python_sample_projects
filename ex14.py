# expense tracker with CSV storage

import datetime
import csv

class Expense:
    def __init__(self, date, category, description, amount):
        self.date = date
        self.category = category
        self.description = description
        self.amount = amount
    def __str__(self):
        return (f"Date: {self.date}, "
                f"Category: {self.category}, "
                f"Description: {self.description}, "
                f"Amount: {self.amount:.2f}")

def validate_date(date_str):
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None
    return date

def add_expense(expenses):
    date_str = input("Enter date (in YYYY-MM-DD format please): ")
    date = validate_date(date_str)
    if not date:
        print("Invalid date")
        return None
    category = input("Enter the category: ").strip()
    if not category:
        print("Invalid expense data")
        return None
    description = input("Enter description: ").strip()
    if not description:
        print("Invalid expense data")
        return None
    try:
        amount = float(input("Enter the amount: "))
    except ValueError:
        print("Invalid amount")
        return None
    if amount <= 0:
        print("Invalid amount")
        return None
    print("Expense added.")
    expenses.append(Expense(date, category, description, amount))
    return True

def show_expenses(expenses):
    if not expenses:
        print("No expenses available")
        return
    for expense in expenses:
        print(expense)

def filter_by_category(expenses):
    category_input = input("Enter the category to search for: ")
    empty = True
    category = category_input.strip().lower()
    for expense in expenses:
        if expense.category.lower() == category:
            print(expense)
            empty = False
    if empty:
        print("No matching expenses")
        
def filter_by_date(expenses):
    date_str = input("Enter date to search for (in YYYY-MM-DD format please): ")
    date = validate_date(date_str)
    if not date:
        print("Invalid date")
        return
    empty = True
    for expense in expenses:
        if expense.date == date:
            print(expense)
            empty = False
    if empty:
        print("No matching expenses")

def total_spent(expenses):
    if not expenses:
        print(f"Total spent: 0.0")
        return
    total = 0
    for expense in expenses:
        total += expense.amount
    print(f"Total spent: {total:.2f}")

def total_by_category(expenses):
    category_input = input("Enter the category to search for: ")
    total = 0
    empty = True
    category = category_input.strip().lower()
    for expense in expenses:
        if expense.category.lower() == category:
            total += expense.amount
            empty = False
    if not expenses or empty:
        print(f"Total spent in category: 0.0")
        return
    print(f"Total spent in category: {total:.2f}")

def save_to_csv(expenses):
    output_file = "expenses.csv"
    try:
        with open(output_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "category",
                             "description", "amount"])
            for expense in expenses:
                writer.writerow([expense.date, expense.category,
                                expense.description, expense.amount])
    except PermissionError:
        print("Permission denied")
        return
    print("Expenses saved.")

def load_from_csv(expenses):
    input_file = "expenses.csv"
    expenses.clear()
    try:
        with open(input_file, "r") as file:
            reader = csv.reader(file)
            header = next(reader, None)
            for line in reader:
                if len(line) != 4:
                    continue
                date_str, category, description, amount_str = line
                date = validate_date(date_str)
                if not date:
                    continue
                try:
                    amount = float(amount_str)
                except ValueError:
                    continue
                if not category.strip() or not description.strip() or amount <= 0:
                    continue
                expenses.append(Expense(date, category, description, amount))
    except FileNotFoundError:
        print("File not found")
        return
    except PermissionError:
        print("Permission denied")
        return
    print("Expenses loaded.")

def main():
    expenses = []
    while True:
        try:
            choice = int(input("1) Add expense\n"
                               "2) Show all expenses\n"
                               "3) Show expenses by category\n"
                               "4) Show expenses by date\n"
                               "5) Show total spent\n"
                               "6) Show total spent by category\n"
                               "7) Save to CSV\n"
                               "8) Load from CSV\n"
                               "9) Exit\n"))
        except ValueError:
            print("Invalid choice")
            continue
        match choice:
            case 1:
                add_expense(expenses)
            case 2:
                show_expenses(expenses)
            case 3:
                filter_by_category(expenses)
            case 4:
                filter_by_date(expenses)
            case 5:
                total_spent(expenses)
            case 6:
                total_by_category(expenses)
            case 7:
                save_to_csv(expenses)
            case 8:
                load_from_csv(expenses)
            case 9:
                print("Goodbye!")
                break
            case _:
                print("Invalid choice")
                continue

if __name__ == '__main__':
    main()