# multithreaded file word analyzer
import json

import threading
import time

class FileReport:
    def __init__(self, filename, line_count, word_count,
                 character_count, most_common_word, status):
        self.filename = filename
        self.line_count = line_count
        self.word_count = word_count
        self.character_count = character_count
        self.most_common_word = most_common_word
        self.status = status

    def display(self):
        if status == "Success":
            print(f"File: {self.filename}\n"
                  f"Lines: {self.line_count}\n"
                  f"Words: {self.word_count}\n"
                  f"Characters: {self.character_count}\n"
                  f"Most common word: {self.most_common_word}\n"
                  f"Status: {self.status}\n")
        else:
            print(f"File: {self.filename}\n"
                  f"Lines: 0\n"
                  f"Words: 0\n"
                  f"Characters: 0\n"
                  f"Most common word: None\n"
                  f"Status: {self.status}\n")

    def to_dict(self):
        pass

def timer(func):
    def wrapper(*args, **kwargs):
        print(f"Analysis finished in {time.thread_time()} seconds.")
        return func(*args, **kwargs)
    return wrapper

def clean_word(word):
    clean_word = word.strip().lower()
    return clean_word

def analyze_file(filename, reports, lock):
    pass

@timer
def analyze_files(filenames):
    reports = []
    try:
        num = int(input("How many files do you want to analyze? "))
    except ValueError:
        print("Invalid number")
        return None
    if num <= 0:
        print("Invalid number")
        return None
    for i in range(num):
        file_name = input(f"Enter file name {i+1}").strip()
        if not file_name:
            i -= 1
            continue
        thread = threading.Thread(target=analyze_file, args=(file_name, reports, lock))
        thread.start()

    thread.join()

    lock = threading.Lock()

    with lock:
        reports.append(report)

    return reports

def show_reports(reports):
    if not reports:
        print("No report available")
        return
    for report in reports:
        report.display()

def save_report(reports):
    if not reports:
        print("No report available")
        return
    file_name = "file_report.json"
    try:
        with open(file_name, "w") as file:
            data = []
            for report in reports:
                data.append(report.to_dict())
            json.dump(data, file)
    except PermissionError:
        print("Permission denied")


def main():
    filenames = []
    reports = []
    while True:
        try:
            choice = int(input("1) Analyze files\n"
                               "2) Show last report\n"
                               "3) Save last report to JSON\n"
                               "4) Exit"))
        except ValueError:
            print("Invalid choice")
            continue
        match choice:
            case 1:
                data = analyze_files(filenames)
                if data is not None:
                    reports = data
            case 2:
                show_reports(reports)
            case 3:
                pass
            case 4:
                print("Goodbye!")
                break
            case _:
                print("Invalid choice")
                continue

if __init__ == '__main__':
    main()