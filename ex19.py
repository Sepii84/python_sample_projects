#multithreaded keyword scanner

import threading
import json
import time

class ScanReport:
    def __init__(self,
                 filename,
                 line_count,
                 word_count,
                 keyword_count,
                 lines_with_keyword,
                 status):
        self.filename = filename
        self.line_count = line_count
        self.word_count = word_count
        self.keyword_count = keyword_count
        self.lines_with_keyword = lines_with_keyword
        self.status = status

    def display(self):
        print(f"filename: {self.filename}\n"
              f"line_count: {self.line_count}\n"
              f"word_count: {self.word_count}\n"
              f"keyword count: {self.keyword_count}\n"
              f"lines with keyword: {self.lines_with_keyword}\n"
              f"status: {self.status}")

    def to_dict(self):
        return {
            "filename": self.filename,
            "line_count": self.line_count,
            "word_count": self.word_count,
            "keyword_count": self.keyword_count,
            "lines_with_keyword": self.lines_with_keyword,
            "status": self.status
        }

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        data = func(*args, **kwargs)
        end = time.time()
        time_passed = end - start
        print(f"Scan finished in {time_passed:.2f} seconds.")
        return data
    return wrapper

def clean_word(word):
    strip_items = ",./;'[]!@#$^&*()<>?:\"{}|`~"
    return word.strip(strip_items).lower()

def get_number_of_files():
    number = 0
    while True:
        try:
            number = int(input("How many files do you want to scan? "))
        except ValueError:
            print("Invalid number")
            continue
        if number <= 0:
            print("Invalid number")
            continue
        break
    return number
def get_file_names(number):
    filenames = []
    for i in range(number):
        while True:
            name = input(f"Enter file name {i+1}: ").strip()
            if not name:
                print("Invalid filename")
                continue
            filenames.append(name)
            break
    return filenames

def get_keyword():
    while True:
        keyword = input("Enter keyword to search: ").strip().lower()
        if not keyword:
            print("Invalid keyword")
            continue
        break
    return keyword

@timer
def scan_files(filenames, keyword):
    reports = []
    threads = []
    lock = threading.Lock()
    for filename in filenames:
        thread = threading.Thread(
            target=scan_file, args=(filename, keyword, reports, lock))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return reports

def scan_file(filename, keyword, reports, lock):
    try:
        with open(filename, "r") as file:
            context = file.read()
    except FileNotFoundError:
        report = ScanReport(
            filename=filename,
            line_count=0,
            word_count=0,
            keyword_count=0,
            lines_with_keyword=0,
            status="File not found"
        )
        with lock:
            reports.append(report)
        return
    except PermissionError:
        report = ScanReport(
            filename=filename,
            line_count=0,
            word_count=0,
            keyword_count=0,
            lines_with_keyword=0,
            status="Permission denied"
        )
        with lock:
            reports.append(report)
        return
    lines = context.splitlines()
    words = context.split()
    keyword_count = 0
    lines_with_keyword = 0
    for word in words:
        if clean_word(word) == keyword:
            keyword_count += 1
    for line in lines:
        words_in_line = line.split()
        for word in words_in_line:
            if clean_word(word) == keyword:
                lines_with_keyword += 1
                break
    report = ScanReport(
        filename=filename,
        line_count=len(lines),
        word_count=len(words),
        keyword_count=keyword_count,
        lines_with_keyword=lines_with_keyword,
        status="Success"
    )
    with lock:
        reports.append(report)

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
    file_name = "keyword_report.json"
    try:
        with open(file_name, "w") as file:
            data = []
            for report in reports:
                data.append(report.to_dict())
            json.dump(data, file, indent=4)
    except PermissionError:
        print("Permission denied")
        return
    print("Report saved.")

def main():
    last_report = []
    while True:
        try:
            choice  = int(input("1) Scan files\n"
                                "2) Show last scan report\n"
                                "3) Save last report to JSON\n"
                                "4) Exit\n"))
        except ValueError:
            print("Invalid choice! choose between 1 and 4.")
            continue
        match choice:
            case 1:
                filenames = get_file_names(get_number_of_files())
                keyword = get_keyword()
                last_report = scan_files(filenames, keyword)
                show_reports(last_report)
            case 2:
                show_reports(last_report)
            case 3:
                save_report(last_report)
            case 4:
                print("Goodbye!")
                break
            case _:
                print("Invalid choice! choose between 1 and 4")

if __name__ == "__main__":
    main()
