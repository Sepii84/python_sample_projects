# Multithreaded Notification Delivery System
# with Priority + Retry + Polymorphism

import csv
import json
import threading
import queue
from abc import ABC, abstractmethod
import time
import datetime

class DeliveryWorker:
    def __init__(self,
                 worker_id,
                 name,
                 processed_count,
                 success_count,
                 failed_count,
                 retried_count):
        self.worker_id = worker_id
        self.name = name
        self.processed_count = processed_count
        self.success_count = success_count
        self.failed_count = failed_count
        self.retried_count = retried_count

    def process_success(self):
        self.processed_count += 1
        self.success_count += 1

    def process_failure(self):
        self.processed_count += 1
        self.failed_count += 1

    def process_retry(self):
        self.retried_count += 1

    def display(self, index):
        print(f"[{index}] "
              f"Worker: {self.name} | "
              f"ID: {self.worker_id} | "
              f"Processed: {self.processed_count} | "
              f"Success: {self.success_count} | "
              f"Failed: {self.failed_count} | "
              f"Retried: {self.retried_count}")

    def to_dict(self):
        return {
            "worker_id": self.worker_id,
            "name": self.name,
            "processed_count": self.processed_count,
            "success_count": self.success_count,
            "failed_count": self.failed_count,
            "retried_count": self.retried_count
        }

class Notification(ABC):
    def __init__(self,
                 notification_id,
                 recipient,
                 priority,
                 message,
                 scheduled_at,
                 fail_until_attempt,
                 current_attempt):
        self.notification_id = notification_id
        self.recipient = recipient
        self.priority = priority
        self.message = message
        self.scheduled_at = scheduled_at
        self.fail_until_attempt = fail_until_attempt
        self.current_attempt = current_attempt

    @abstractmethod
    def send(self):
        pass

    def to_dict(self):
        return {
            "notification_id": self.notification_id,
            "recipient": self.recipient,
            "priority": self.priority,
            "message": self.message,
            "scheduled_at": self.scheduled_at.strftime("%Y-%m-%d %H:%M"),
            "fail_until_attempt": self.fail_until_attempt,
            "current_attempt": self.current_attempt
        }

class EmailNotification(Notification):
    def __init__(self,
                 notification_id,
                 recipient,
                 priority,
                 message,
                 scheduled_at,
                 fail_until_attempt,
                 current_attempt,
                 subject):
        super().__init__(notification_id,
                 recipient,
                 priority,
                 message,
                 scheduled_at,
                 fail_until_attempt,
                 current_attempt)
        self.subject = subject

    def send(self):
        return "Email sent"

class SMSNotification(Notification):
    def __init__(self,
                 notification_id,
                 recipient,
                 priority,
                 message,
                 scheduled_at,
                 fail_until_attempt,
                 current_attempt,
                 phone_number):
        super().__init__(notification_id,
                 recipient,
                 priority,
                 message,
                 scheduled_at,
                 fail_until_attempt,
                 current_attempt)
        self.phone_number = phone_number

    def send(self):
        return "SMS sent"

class PushNotification(Notification):
    def __init__(self,
                 notification_id,
                 recipient,
                 priority,
                 message,
                 scheduled_at,
                 fail_until_attempt,
                 current_attempt,
                 device_id):
        super().__init__(notification_id,
                         recipient,
                         priority,
                         message,
                         scheduled_at,
                         fail_until_attempt,
                         current_attempt)
        self.device_id = device_id

    def send(self):
        return "Push notification sent"

class DeliveryResult:
    def __init__(self,
                 notification_id,
                 notification_type,
                 recipient,
                 priority,
                 worker_id,
                 attempts_used,
                 scheduled_at,
                 completed_at,
                 status,
                 message):
        self.notification_id = notification_id
        self.notification_type = notification_type
        self.recipient = recipient
        self.priority = priority
        self.worker_id = worker_id
        self.attempts_used =attempts_used
        self.scheduled_at =scheduled_at
        self.completed_at =completed_at
        self.status =status
        self.message =message

    def display(self):
        print(f"Notification: {self.notification_id} | "
              f"Type: {self.notification_type} | "
              f"Recipient: {self.recipient} | "
              f"Priority: {self.priority} | "
              f"Worker: {self.worker_id} | "
              f"Attempts: {self.attempts_used} | "
              f"Status: {self.status} | "
              f"Message: {self.message}")

    def to_dict(self):
        return {
            "notification_id" : self.notification_id,
            "notification_type" : self.notification_type,
            "recipient" : self.recipient,
            "priority" : self.priority,
            "worker_id" : self.worker_id,
            "attempts_used" : self.attempts_used,
            "scheduled_at" : self.scheduled_at.strftime("%Y-%m-%d %H:%M"),
            "completed_at" : self.completed_at,
            "status" : self.status,
            "message" : self.message
        }

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        elapsed_time = end - start
        print(f"Processing finished in {elapsed_time:.2f} seconds.")
        return result
    return wrapper

def find_delivery_worker(delivery_workers, worker_id):
    for delivery_worker in delivery_workers:
        if delivery_worker.worker_id == worker_id:
            return delivery_worker
    return None

def add_delivery_worker(delivery_workers):
    worker_id = input("Enter worker ID: ").strip()
    if not worker_id:
        print("Invalid worker data")
        return
    if find_delivery_worker(delivery_workers, worker_id) is not None:
        print("Worker ID already exists")
        return
    name = input("Enter worker name: ").strip()
    if not name:
        print("Invalid worker data")
        return
    delivery_workers.append(DeliveryWorker(
        worker_id,
        name,
        0,
        0,
        0,
        0
    ))
    print("Worker added.")

def show_workers(delivery_workers):
    if not delivery_workers:
        print("No workers available")
        return
    for index, delivery_worker in enumerate(delivery_workers, start=1):
        delivery_worker.display(index)

def load_notifications_from_csv():
    file_name = "notifications.csv"
    valid_types = ("email", "sms", "push")
    valid_priorities = ("high", "medium", "low")
    notifications = []
    try:
        with open(file_name, "r") as file:
            reader = csv.reader(file)
            header = next(reader, None)
            for row in reader:
                if len(row) != 8:
                    continue
                if (not row[0].strip() or
                    not row[2].strip() or
                    not row[4].strip() or
                    not row[6].strip()):
                    continue
                notification_type = row[1].strip().lower()
                if notification_type not in valid_types:
                    continue
                priority = row[3].strip().lower()
                if priority not in valid_priorities:
                    continue
                try:
                    fail_until_attempt = int(row[7].strip())
                except ValueError:
                    continue
                if fail_until_attempt < 0:
                    continue
                try:
                    scheduled_at = datetime.datetime.strptime(
                        row[5].strip().lower(), "%Y-%m-%d %H:%M")
                except ValueError:
                    continue
                if notification_type == "email":
                    notifications.append(EmailNotification(
                        row[0].strip(),
                        row[2].strip(),
                        priority,
                        row[4].strip(),
                        scheduled_at,
                        fail_until_attempt,
                        0,
                        row[6].strip()
                    ))
                elif notification_type == "sms":
                     notifications.append(SMSNotification(
                        row[0].strip(),
                        row[2].strip(),
                        priority,
                        row[4].strip(),
                        scheduled_at,
                        fail_until_attempt,
                        0,
                        row[6].strip()
                    ))
                elif notification_type == "push":
                    notifications.append(PushNotification(
                        row[0].strip(),
                        row[2].strip(),
                        priority,
                        row[4].strip(),
                        scheduled_at,
                        fail_until_attempt,
                        0,
                        row[6].strip()
                    ))
    except FileNotFoundError:
        print("File not found")
        return None
    except PermissionError:
        print("Permission denied")
        return None
    print("Notifications loaded.")
    return notifications

def find_least_busy_worker(delivery_workers):
    least_busy = delivery_workers[0]
    for delivery_worker in delivery_workers:
        if delivery_worker.processed_count < least_busy.processed_count:
            least_busy = delivery_worker
    return least_busy

def put_in_queue(notification_queue, notification, priority_map, counter, lock):
    priority_number = priority_map.get(notification.priority)
    scheduled_timestamp = notification.scheduled_at
    with lock:
        counter["counter"] += 1
        notification_queue.put((priority_number, scheduled_timestamp, counter["counter"], notification))

def worker_in_queue(notification_queue, delivery_workers, results, priority_map, counter, lock):
    while True:
        try:
            priority_number, scheduled_timestamp, counter_value, notification = notification_queue.get_nowait()
        except queue.Empty:
            break
        process_notification(notification_queue, delivery_workers, notification, priority_map, counter, results, lock)
        notification_queue.task_done()

def process_notification(notification_queue, delivery_workers, notification, priority_map, counter, results, lock):
    notification_id = notification.notification_id
    if isinstance(notification, EmailNotification):
        notification_type = "email"
    elif isinstance(notification, SMSNotification):
        notification_type = "sms"
    else:
        notification_type = "push"
    recipient = notification.recipient
    priority = notification.priority
    with lock:
        notification.current_attempt += 1
    attempts_used = notification.current_attempt
    scheduled_at = notification.scheduled_at
    fail_until_attempt = notification.fail_until_attempt
    if attempts_used <= fail_until_attempt:
        if attempts_used < 3:
            with lock:
                delivery_worker = find_least_busy_worker(delivery_workers)
                delivery_worker.process_retry()
            put_in_queue(notification_queue, notification, priority_map, counter, lock)
        else:
            with lock:
                delivery_worker = find_least_busy_worker(delivery_workers)
                worker_id = delivery_worker.worker_id
                results.append(DeliveryResult(
                    notification_id,
                    notification_type,
                    recipient,
                    priority,
                    worker_id,
                    attempts_used,
                    scheduled_at,
                    completed_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    status="Failed",
                    message="Max retries reached"
                ))
                delivery_worker.process_failure()
    else:
        with lock:
            delivery_worker = find_least_busy_worker(delivery_workers)
            worker_id = delivery_worker.worker_id
            results.append(DeliveryResult(
                notification_id,
                notification_type,
                recipient,
                priority,
                worker_id,
                attempts_used,
                scheduled_at,
                completed_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                status="Success",
                message=notification.send()
            ))
            delivery_worker.process_success()

@timer
def process_all_notifications(notifications, delivery_workers):
    if not notifications:
        print("No notifications loaded")
        return None
    if not delivery_workers:
        print("No workers available")
        return None
    results = []
    notification_queue = queue.PriorityQueue()
    priority_map = {
        "high": 1,
        "medium": 2,
        "low": 3
    }
    counter = {"counter": 0}
    threads = []
    lock = threading.Lock()
    for notification in notifications:
        put_in_queue(notification_queue, notification, priority_map, counter, lock)
    for _ in range(3):
        thread = threading.Thread(
            target=worker_in_queue,
            args=(notification_queue, delivery_workers, results, priority_map, counter, lock)
        )
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print("Notifications processed.")
    return results

def show_delivery_report(results):
    if not results:
        print("No report available")
        return
    for result in results:
        result.display()

def show_worker_statistics(delivery_workers):
    if not delivery_workers:
        print("No workers available")
        return
    for delivery_worker in delivery_workers:
        print(f"{delivery_worker.worker_id} Processed {delivery_worker.processed_count} notifications\n"
              f"{delivery_worker.success_count} success\n"
              f"{delivery_worker.failed_count} failed\n"
              f"{delivery_worker.retried_count} retried\n")

def save_to_json(results):
    file_name = "delivery_report.json"
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
    delivery_workers = []
    notifications = []
    results = []
    while True:
        try:
            choice = int(input("1) Add delivery worker\n"
                               "2) Show workers\n"
                               "3) Load notifications from CSV\n"
                               "4) Process loaded notifications\n"
                               "5) Show delivery report\n"
                               "6) Show worker statistics\n"
                               "7) Save report to JSON\n"
                               "8) Exit\n"))
        except ValueError:
            print("Invalid choice! choose between 1 and 8.")
            continue
        match choice:
            case 1:
                add_delivery_worker(delivery_workers)
            case 2:
                show_workers(delivery_workers)
            case 3:
                loaded_notifications = load_notifications_from_csv()
                if loaded_notifications is not None:
                    notifications = loaded_notifications
            case 4:
                processed_results = process_all_notifications(notifications, delivery_workers)
                if processed_results is not None:
                    results = processed_results
            case 5:
                show_delivery_report(results)
            case 6:
                show_worker_statistics(delivery_workers)
            case 7:
                save_to_json(results)
            case 8:
                print("Goodbye!")
                return
            case _:
                print("Invalid choice! choose between 1 and 8.")

if __name__ == "__main__":
    main()