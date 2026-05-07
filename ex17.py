# employee payroll system with CSV persistence:

from abc import ABC, abstractmethod
import csv

class Employee(ABC):
    def __init__(self, name, employee_id):
        self.name = name
        self.employee_id = employee_id

    def display(self, index):
        print(f"[{index}] Employee: {self.name} | ID: {self.employee_id}")
    
    @abstractmethod
    def calculate_pay(self):
        pass
    
    @abstractmethod
    def to_csv_row(self):
        pass

class HourlyEmployee(Employee):
    def __init__(self, name, employee_id, hourly_rate, hours_worked):
        super().__init__(name, employee_id)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked
        self.pay = hourly_rate * hours_worked

    def display(self, index):
        print(f"[{index}] "
              f"Hourly Employee: {self.name} | "
              f"ID: {self.employee_id} | "
              f"Rate: {self.hourly_rate:.1f} | "
              f"Hours: {self.hours_worked} | "
              f"Pay: {self.pay:.2f}")

    def calculate_pay(self):
        return self.pay

    def to_csv_row(self):
        return ["hourly",
                self.name,
                self.employee_id,
                self.hourly_rate,
                self.hours_worked,
                ""]

class SalariedEmployee(Employee):
    def __init__(self, name, employee_id, monthly_salary):
        super().__init__(name, employee_id)
        self.monthly_salary = monthly_salary
        self.pay = monthly_salary

    def display(self, index):
        print(f"[{index}] "
              f"Salaried Employee: {self.name} | "
              f"ID: {self.employee_id} | "
              f"Salary: {self.monthly_salary:.1f} | "
              f"Pay: {self.pay:.2f}")

    def calculate_pay(self):
        return self.pay

    def to_csv_row(self):
        return ["salaried",
                self.name,
                self.employee_id,
                "",
                "",
                self.monthly_salary]

def employee_id_exists(employees, employee_id):
    for employee in employees:
        if employee.employee_id == employee_id:
            return True
    return False

def get_common_employee_data(employees):
    name = input("Enter the name of the employee: ").strip()
    if not name:
        print("Invalid employee data")
        return None
    employee_id = input("Enter employee ID: ").strip()
    if not employee_id:
        print("Invalid employee data")
        return None
    if employee_id_exists(employees, employee_id):
        print("Employee ID already exists")
        return None
    return name, employee_id

def add_hourly_employee(employees):
    data = get_common_employee_data(employees)
    if not data:
        return
    name, employee_id = data
    try:
        hourly_rate = float(input("Enter employee's hourly rate: "))
    except ValueError:
        print("Invalid hourly data")
        return
    if hourly_rate <= 0:
        print("Invalid hourly data")
        return
    try:
        hours_worked = float(input("Enter the hours the employee has worked: "))
    except ValueError:
        print("Invalid hourly data")
        return
    if hours_worked < 0:
        print("Invalid hourly data")
        return
    employees.append(HourlyEmployee(name, employee_id, hourly_rate, hours_worked))
    print("Hourly employee added.")

def add_salaried_employee(employees):
    data = get_common_employee_data(employees)
    if not data:
        return
    name, employee_id = data
    try:
        monthly_salary = float(input("Enter employee's monthly salary: "))
    except ValueError:
        print("Invalid salary")
        return
    if monthly_salary <= 0:
        print("Invalid salary")
        return
    employees.append(SalariedEmployee(name, employee_id, monthly_salary))
    print("Salaried employee added.")

def show_employees(employees):
    if not employees:
        print("No employees available")
        return
    for index, employee in enumerate(employees, start=1):
        employee.display(index)

def search_employee(employees):
    if not employees:
        print("No employees available")
        return
    keyword = input("Enter the keyword to search").strip().lower()
    found = False
    for index, employee in enumerate(employees, start=1):
        if keyword in employee.name.lower():
            employee.display(index)
            found = True
    if not found:
        print("No matching employees")

def total_payroll(employees):
    if not employees:
        print("Total payroll: 0.00")
        return
    total = 0
    for employee in employees:
        total += employee.calculate_pay()
    print(f"Total payroll: {total:.2f}")

def delete_employee(employees):
    if not employees:
        print("No employees available")
        return
    show_employees(employees)

    try:
        num = int(input("Enter the number of employee to be deleted: "))
    except ValueError:
        print("Invalid employee number")
        return
    if num < 1 or num > len(employees):
        print("Invalid employee number")
        return
    employees.pop(num - 1)
    print("Employee deleted.")

def save_to_csv(employees):
    output_file = "employees.csv"
    try:
        with open(output_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["type", "name", "employee_id",
                             "hourly_rate", "hours_worked", "monthly_salary"])
            for employee in employees:
                writer.writerow(employee.to_csv_row())
    except PermissionError:
        print("Permission denied")
        return
    print("Employees saved.")

def load_from_csv():
    input_file = "employees.csv"
    employees = []
    try:
        with open(input_file, "r", newline="") as file:
            reader = csv.reader(file)
            header = next(reader, None)
            for row in reader:
                try:
                    if len(row) != 6:
                        continue
                    elif row[0] == "hourly":
                        employees.append(HourlyEmployee(
                            row[1],
                            row[2],
                            float(row[3]),
                            float(row[4])
                        ))
                    elif row[0] == "salaried":
                        employees.append(SalariedEmployee(
                            row[1],
                            row[2],
                            float(row[5])
                        ))
                except ValueError:
                    continue
    except FileNotFoundError:
        print("File not found")
        return
    except PermissionError:
        print("Permission denied")
        return
    print("Employees loaded.")
    return employees

def main():
    employees = []
    while True:
        try:
            choice = int(input("1) Add hourly employee\n"
                               "2) Add salaried employee\n"
                               "3) Show all employees\n"
                               "4) Search employee by name\n"
                               "5) Calculate total payroll\n"
                               "6) Delete employee\n"
                               "7) Save to CSV\n"
                               "8) Load from CSV\n"
                               "9) Exit\n"))
        except ValueError:
            print("Invalid choice")
            continue
        match choice:
            case 1:
                add_hourly_employee(employees)
            case 2:
                add_salaried_employee(employees)
            case 3:
                show_employees(employees)
            case 4:
                search_employee(employees)
            case 5:
                total_payroll(employees)
            case 6:
                delete_employee(employees)
            case 7:
                save_to_csv(employees)
            case 8:
                data = load_from_csv()
                if data is not None:
                    employees = data
            case 9:
                print("Goodbye!")
                break
            case _:
                print("Invalid choice")

if __name__ == '__main__':
    main()