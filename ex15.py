# personal task manager with JSON persistence

import datetime
import json

class Task:
    def __init__(self, title, description, completed, created_at):
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = created_at

    def display(self, index):
        completed_text = "Yes" if self.completed else "No"
        print (f"[{index}] Title: {self.title} | "
                f"Completed: {completed_text} | "
                f"Created: {self.created_at}\n"
                f"Description: {self.description}")

    def to_dict(self):
        return {"type": "normal",
                "title": self.title,
                "description": self.description,
                "completed": self.completed,
                "created_at": self.created_at}

class DeadlineTask(Task):
    def __init__(self, title, description, completed, created_at, deadline):
        super().__init__(title, description, completed, created_at)
        self.deadline = deadline

    def display(self, index):
        super().display(index)
        print(f"Deadline: {self.deadline}")

    def to_dict(self):
        data =  super().to_dict()
        data.update({"type": "deadline", "deadline": str(self.deadline)})
        return data

def log_action(func):
    def wrapper(*args, **kwargs):
        print("Action started...")
        return func(*args, **kwargs)
    return wrapper

def add_task(tasks):
    title = input("Enter the title: ").strip()
    if not title:
        print("Invalid task data")
        return
    description = input("enter the description of the task: ").strip()
    if not description:
        print("Invalid task data")
        return
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    tasks.append(Task(title, description, False, date))
    print("Task added.")

def add_deadline_task(tasks):
    title = input("Enter the title: ").strip()
    if not title:
        print("Invalid task data")
        return
    description = input("enter the description of the task: ").strip()
    if not description:
        print("Invalid task data")
        return
    deadline_str = input("please enter the deadline (in format YYYY-MM-DD): ")
    try:
        deadline = datetime.datetime.strptime(deadline_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid deadline")
        return
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    tasks.append(DeadlineTask(title, description, False, date, deadline))
    print("Deadline task added.")

def show_tasks(tasks):
    if not tasks:
        print("No tasks available")
        return
    for index, task in enumerate(tasks, start=1):
        task.display(index)

def mark_completed(tasks):
    incomplete_tasks = []
    for task in tasks:
        if not task.completed:
            incomplete_tasks.append(task)
    if not incomplete_tasks:
        print("No incomplete tasks")
        return
    show_tasks(incomplete_tasks)
    try:
        task_num = int(input("Enter the task number to mark as complete: "))
    except ValueError:
        print("Invalid task number")
        return
    if task_num < 1 or task_num > len(incomplete_tasks):
        print("Invalid task number")
        return
    incomplete_tasks[task_num-1].completed = True
    print("Task completed.")

def delete_task(tasks):
    if not tasks:
        print("No tasks available")
        return
    show_tasks(tasks)
    try:
        task_num = int(input("Enter the task number to delete: "))
    except ValueError:
        print("Invalid task number")
        return
    if task_num < 1 or task_num > len(tasks):
        print("Invalid task number")
        return
    tasks.pop(task_num-1)
    print("Task deleted.")

def search_tasks(tasks):
    keyword = input("Enter the keyword to search: ").strip().lower()
    search_result = []
    for task in tasks:
        if keyword in task.title.lower() or keyword in task.description.lower():
            search_result.append(task)
    if not search_result:
        print("No matching tasks")
        return
    print(f"Search results with the keyword {keyword}: ")
    show_tasks(search_result)

def show_overdue_tasks(tasks):
    overdue_tasks = []
    today = datetime.datetime.now().date()
    for task in tasks:
        if isinstance(task, DeadlineTask):
            deadline = task.deadline
            if isinstance(deadline, str):
                try:
                    deadline = datetime.datetime.strptime(task.deadline, "%Y-%m-%d").date()
                except ValueError:
                    continue
            if not task.completed and deadline < today:
                overdue_tasks.append(task)
    if not overdue_tasks:
        print("No overdue tasks")
        return
    show_tasks(overdue_tasks)

@log_action
def save_tasks(tasks):
    output_file = "tasks.json"
    try:
        with open(output_file, "w") as file:
            data = []
            for task in tasks:
                data.append(task.to_dict())
            json.dump(data, file, indent=4)
    except PermissionError:
        print("Permission denied")
        return
    print("Tasks saved.")

@log_action
def load_tasks():
    tasks = []
    input_file = "tasks.json"
    try:
        with open(input_file, "r") as file:
            data = json.load(file)
            for task in data:
                try:
                    if task["type"] == "normal":
                        tasks.append(Task(
                            task["title"],
                            task["description"],
                            task["completed"],
                            task["created_at"]))
                    elif task["type"] == "deadline":
                        tasks.append(DeadlineTask(
                            task["title"],
                            task["description"],
                            task["completed"],
                            task["created_at"],
                            task["deadline"]))
                except KeyError:
                    continue
    except FileNotFoundError:
        print("File not found")
        return
    except PermissionError:
        print("Permission denied")
        return
    print("Tasks loaded.")
    return tasks

def main():
    tasks = []
    while True:
        try:
            choice = int(input("1) Add normal task\n"
                               "2) Add deadline task\n"
                               "3) Show all tasks\n"
                               "4) Show incomplete tasks\n"
                               "5) Mark task as completed\n"
                               "6) Delete task\n"
                               "7) Search tasks by keyword\n"
                               "8) Show overdue tasks\n"
                               "9) Save tasks to JSON\n"
                               "10) Load tasks from JSON\n"
                               "11) Exit\n"))
        except ValueError:
            print("Invalid choice")
            continue
        match choice:
            case 1:
                add_task(tasks)
            case 2:
                add_deadline_task(tasks)
            case 3:
                show_tasks(tasks)
            case 4:
                incomplete_tasks = []
                for task in tasks:
                    if not task.completed:
                        incomplete_tasks.append(task)
                if not incomplete_tasks:
                    print("No incomplete tasks")
                else:
                    show_tasks(incomplete_tasks)
            case 5:
                mark_completed(tasks)
            case 6:
                delete_task(tasks)
            case 7:
                search_tasks(tasks)
            case 8:
                show_overdue_tasks(tasks)
            case 9:
                save_tasks(tasks)
            case 10:
                loaded_tasks = load_tasks()
                if loaded_tasks is not None:
                    tasks = loaded_tasks
            case 11:
                print("Goodbye!")
                break
            case _:
                print("Invalid choice")
                continue

if __name__ == '__main__':
    main()