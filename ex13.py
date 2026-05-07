# Log Analyzer with JSON Report

import datetime
import json

def parse_log_line(line):
    parts = line.split(" | ")
    if len(parts) != 3:
        return None

    timestamp_str = parts[0].strip()
    level = parts[1].strip()
    message = parts[2].strip()

    if level not in ["INFO", "WARNING", "ERROR"]:
        return None

    try:
        timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

    return timestamp, level, message

def analyze_logs(file_path, target_date):
    summary = {
        "total_valid_lines": 0,
        "skipped_lines": 0,
        "level_counts": {
            "INFO": 0,
            "WARNING": 0,
            "ERROR": 0
        },
        "earliest_timestamp": None,
        "latest_timestamp": None,
        "errors_on_target_date": 0
    }
    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parsed = parse_log_line(line)
                if not parsed:
                    summary["skipped_lines"] += 1
                    continue
                timestamp, level, message = parsed
                summary["total_valid_lines"] += 1
                summary["level_counts"][level] += 1
                if level == "ERROR" and timestamp.date() == target_date:
                    summary["errors_on_target_date"] += 1
                if not summary["earliest_timestamp"] or timestamp < summary["earliest_timestamp"]:
                    summary["earliest_timestamp"] = timestamp
                if not summary["latest_timestamp"] or timestamp > summary["latest_timestamp"]:
                    summary["latest_timestamp"] = timestamp
    except FileNotFoundError:
        print("File not found")
        return None
    except PermissionError:
        print("You do not have permission to read that file")
        return None
    if summary["earliest_timestamp"]:
        summary["earliest_timestamp"] = summary["earliest_timestamp"].strftime("%Y-%m-%d %H:%M:%S")

    if summary["latest_timestamp"]:
        summary["latest_timestamp"] = summary["latest_timestamp"].strftime("%Y-%m-%d %H:%M:%S")

    return summary

def save_summary(summary):
    output_path = "summary.json"
    try:
        with open(output_path, "w") as file:
            json.dump(summary, file, indent=4)
    except PermissionError:
        print("You do not have permission to write that file")

def main():
    file_path = input("Enter the file path: ")
    target_date_input = input("Enter your date: ")
    try:
        target_date = datetime.datetime.strptime(target_date_input, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date")
        return

    summary = analyze_logs(file_path, target_date)
    if not summary:
        return
    print(summary)
    save_summary(summary)

if __name__ == '__main__':

    main()
    