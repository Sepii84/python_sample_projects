# Multithreaded Background Job Processor with Retry Queue

import csv
import json
import threading
import queue
import time

class Worker:
    def __init__(self,
                 worker_id,
                 name,
                 processed_count,
                 success_count,
                 failed_count):
        self.worker_id = worker_id
        self.name = name
        self.processed_count = processed_count
        self.success_count = success_count
        self.failed_count = failed_count

    def process_success(self):
        self.processed_count += 1
        self.success_count += 1

    def process_failure(self):
        self.processed_count += 1
        self.failed_count += 1

    def display(self, index):
        print(f"[{index}] "
              f"Worker: {self.name} | "
              f"ID: {self.worker_id} | "
              f"Processed: {self.processed_count} | "
              f"Success: {self.success_count} | "
              f"Failed: {self.failed_count}")

    def to_dict(self):
        return {
            "worker_id": self.worker_id,
            "name": self.name,
            "processed_count": self.processed_count,
            "success_count": self.success_count,
            "failed_count": self.failed_count
        }

class JobResult:
    def __init__(self,
                 job_id,
                 job_type,
                 priority,
                 payload,
                 worker_id,
                 attempts_used,
                 status,
                 message
                 ):
        self.job_id = job_id
        self.job_type = job_type
        self.priority = priority
        self.payload = payload
        self.worker_id = worker_id
        self.attempts_used = attempts_used
        self.status = status
        self.message = message

    def display(self):
        print(f"Job: {self.job_id} | "
              f"Type: {self.job_type} | "
              f"Priority: {self.priority} | "
              f"Worker: {self.worker_id} | "
              f"Attempts: {self.attempts_used} | "
              f"Status: {self.status} | "
              f"Message: {self.message}")

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "job_type": self.job_type,
            "priority": self.priority,
            "payload": self.payload,
            "worker_id": self.worker_id,
            "attempts_used": self.attempts_used,
            "status": self.status,
            "message": self.message
        }

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        elapsed_time = end - start
        print(f"Processing finished in {elapsed_time:.2f} seconds")
        return result
    return wrapper

def find_worker(workers, worker_id):
    for worker in workers:
        if worker.worker_id == worker_id:
            return worker
    return None

def add_worker(workers):
    worker_id = input("Enter the worker id: ").strip()
    if not worker_id:
        print("Invalid worker data")
        return
    if find_worker(workers, worker_id) is not None:
        print("Worker ID already exists")
        return
    name = input("Enter the worker name: ").strip()
    if not name:
        print("Invalid worker data")
        return
    workers.append(Worker(worker_id, name, 0, 0, 0))
    print("Worker added.")

def show_all_workers(workers):
    if not workers:
        print("No workers available")
        return
    for index, worker in enumerate(workers, start=1):
        worker.display(index)

def load_from_csv():
    file_name = "jobs.csv"
    jobs = []
    try:
        with open(file_name, "r") as file:
            reader = csv.reader(file)
            header = next(reader, None)
            for row in reader:
                if len(row) != 5:
                    continue
                if (not row[0].strip() or
                not row[1].strip() or
                not row[2].strip() or
                not row[3].strip() or
                not row[4].isdigit()):
                    continue
                try:
                    if int(row[4]) < 0:
                        continue
                except ValueError:
                    continue
                if row[1].strip().lower() not in ("email", "export", "cleanup", "notification"):
                    continue
                if row[2].strip().lower() not in ("high", "medium", "low"):
                    continue
                jobs.append(
                    {
                        "job_id": row[0].strip(),
                        "job_type": row[1].strip().lower(),
                        "priority": row[2].strip().lower(),
                        "payload": row[3].strip(),
                        "fail_until_attempt": int(row[4]),
                        "current_attempt": 0
                    }
                )
    except FileNotFoundError:
        print("File not found")
        return None
    except PermissionError:
        print("Permission denied")
        return None
    print("Jobs loaded.")
    return jobs

def putting_jobs_in_queue(job_queue, job, priority_map, lock):
    with lock:
        priority_map["value"] += 1
        counter = priority_map["value"]
    priority_number = priority_map[job["priority"]]
    job_queue.put((priority_number, counter, job))

@timer
def process_all_jobs(jobs, workers):
    if not jobs:
        print("No jobs loaded")
        return
    if not workers:
        print("No workers available")
        return
    priority_map = {
        "high": 1,
        "medium": 2,
        "low": 3,
        "value": 0
    }
    job_queue = queue.PriorityQueue()
    lock = threading.Lock()
    for job in jobs:
        putting_jobs_in_queue(job_queue, job, priority_map, lock)
    threads = []
    results = []
    for _ in range(3):
        thread = threading.Thread(
            target=worker_processing,
            args=(job_queue, workers, results, priority_map, lock)
        )
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print("Jobs processed.")
    return results

def find_least_busy_worker(workers):
    least = workers[0]
    for worker in workers:
        if worker.processed_count < least.processed_count:
            least = worker
    return least

def worker_processing(job_queue, workers, results, priority_map, lock):
    while True:
        try:
            priority, counter, job = job_queue.get_nowait()
        except queue.Empty:
            break
        process_job(job, workers, job_queue, results, priority_map, lock)
        job_queue.task_done()

def process_job(job, workers, job_queue, results, priority_map, lock):
    job["current_attempt"] += 1
    current_attempt = job["current_attempt"]
    job_id = job.get("job_id")
    job_type = job.get("job_type")
    priority = job.get("priority")
    payload = job.get("payload")
    fail_until_attempt = job["fail_until_attempt"]
    if current_attempt <= fail_until_attempt:
        if current_attempt >= 3:
            with lock:
                worker = find_least_busy_worker(workers)
                worker.process_failure()
                worker_id = worker.worker_id
                results.append(JobResult(
                    job_id,
                    job_type,
                    priority,
                    payload,
                    worker_id,
                    current_attempt,
                    "Failed",
                    "Max retries reached"
                ))
        else:
            putting_jobs_in_queue(job_queue, job, priority_map, lock)
    else:
        with lock:
            worker = find_least_busy_worker(workers)
            worker.process_success()
            worker_id = worker.worker_id
            results.append(JobResult(
                job_id,
                job_type,
                priority,
                payload,
                worker_id,
                current_attempt,
                "Success",
                "Job completed"
            ))

def show_report(results):
    if not results:
        print("No report available")
        return
    for result in results:
        result.display()

def show_worker_statistics(workers):
    if not workers:
        print("No workers available")
        return
    for worker in workers:
        print(f"{worker.worker_id} processed {worker.processed_count} jobs in total.\n"
              f"{worker.failed_count} failures and {worker.success_count} successes.\n")

def save_to_json(results):
    if not results:
        print("No report available")
        return
    file_name = "job_report.json"
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
    workers = []
    jobs = []
    results = []
    while True:
        try:
            choice = int(input("1) Add worker\n"
                               "2) Show workers\n"
                               "3) Load jobs from CSV\n"
                               "4) Process loaded jobs\n"
                               "5) Show job report\n"
                               "6) Show worker statistics\n"
                               "7) Save report to JSON\n"
                               "8) Exit\n"))
        except ValueError:
            print("Invalid choice! choose between 1 and 8.")
            continue
        match choice:
            case 1:
                add_worker(workers)
            case 2:
                show_all_workers(workers)
            case 3:
                loaded_jobs = load_from_csv()
                if loaded_jobs is not None:
                    jobs = loaded_jobs
            case 4:
                loaded_results = process_all_jobs(jobs, workers)
                if loaded_results is not None:
                    results = loaded_results
            case 5:
                show_report(results)
            case 6:
                show_worker_statistics(workers)
            case 7:
                save_to_json(results)
            case 8:
                print("Goodbye!")
                break
            case _:
                print("Invalid choice! choose between 1 and 8.")

if __name__ == "__main__":
    main()