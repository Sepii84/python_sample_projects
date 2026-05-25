# Multithreaded File Word Analyzer

import threading
import time
import json

class FileReport:
    def __init__(self, filename, line_count, word_count, character_count, most_common_word, status):
        self.filename = filename
        self.line_count = line_count
        self.word_count = word_count
        self.character_count = character_count
        self.most_common_word = most_common_word
        self.status = status

    def display(self):
        print(f"File: {self.filename}\n"
              f"Lines: {self.line_count}\n"
              f"Words: {self.word_count}\n"
              f"Characters: {self.character_count}\n"
              f"Most common word: {self.most_common_word}\n"
              f"Status: {self.status}")

    def to_dict(self):
        return {
            "filename": self.filename,
            "line_count": self.line_count,
            "word_count": self.word_count,
            "character_count": self.character_count,
            "most_common_word": self.most_common_word,
            "status": self.status
        }

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Analysis finished in {elapsed_time:.2f} seconds.")
        return result
    return wrapper

def clean_word(word):
    punctuation = ".,!?;:\"'()[]{}<>"
    word = word.strip(punctuation)
    word = word.lower()
    return word

def find_most_common_word(words):
    if not words:
        return None
    word_counts = {}
    for word in words:
        if word not in word_counts:
            word_counts[word] = 1
        else:
            word_counts[word] += 1
    most_common = None
    highest_count = 0
    for word, count in word_counts.items():
        if count > highest_count:
            highest_count = count
            most_common = word
    return most_common

def analyze_file(filename, reports, lock):
    try:
        with open(filename, "r") as file:
            content = file.read()
    except FileNotFoundError:
        report = FileReport(
            filename=filename,
            line_count=0,
            word_count=0,
            character_count=0,
            most_common_word=None,
            status="File not found"
        )
        with lock:
            reports.append(report)
        return
    except PermissionError:
        report = FileReport(
            filename=filename,
            line_count=0,
            word_count=0,
            character_count=0,
            most_common_word=None,
            status="Permission denied"
        )
        with lock:
            reports.append(report)
        return
    lines = content.splitlines()
    raw_words = content.split()
    words = []
    for word in raw_words:
        cleaned = clean_word(word)
        if cleaned:
            words.append(cleaned)
    line_count = len(lines)
    word_count = len(words)
    character_count = len(content)
    most_common_word = find_most_common_word(words)
    report = FileReport(
        filename=filename,
        line_count=line_count,
        word_count=word_count,
        character_count=character_count,
        most_common_word=most_common_word,
        status="Success"
    )
    with lock:
        reports.append(report)

@timer
def analyze_files(filenames):
    reports = []
    threads = []
    lock = threading.Lock()
    for filename in filenames:
        thread = threading.Thread(
            target=analyze_file,args=(filename, reports, lock))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
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
    output_file = "file_report.json"
    try:
        with open(output_file, "w") as file:
            data = []
            for report in reports:
                data.append(report.to_dict())
            json.dump(data, file, indent=4)
    except PermissionError:
        print("Permission denied")
        return
    print("Report saved.")

def get_filenames_from_user():
    try:
        file_count = int(input("How many files do you want to analyze? "))
    except ValueError:
        print("Invalid number")
        return None
    if file_count <= 0:
        print("Invalid number")
        return None
    filenames = []
    for i in range(file_count):
        while True:
            filename = input(f"Enter file name {i + 1}: ").strip()
            if not filename:
                print("Invalid filename")
                continue
            filenames.append(filename)
            break
    return filenames

def main():
    last_report = []
    while True:
        try:
            choice = int(input(
                "1) Analyze files\n"
                "2) Show last report\n"
                "3) Save last report to JSON\n"
                "4) Exit\n"
            ))
        except ValueError:
            print("Invalid choice")
            continue
        match choice:
            case 1:
                filenames = get_filenames_from_user()
                if filenames is None:
                    continue
                last_report = analyze_files(filenames)
                show_reports(last_report)
            case 2:
                show_reports(last_report)
            case 3:
                save_report(last_report)
            case 4:
                print("Goodbye!")
                break
            case _:
                print("Invalid choice")

if __name__ == "__main__":
    main()