# Multithreaded Support Ticket Processor with Priority Queue

import time
import csv
import json
import threading
import queue

class SupportAgent:
    def __init__(self, agent_id, name, processed_count):
        self.agent_id = agent_id
        self.name = name
        self.processed_count = processed_count

    def process_ticket(self):
        self.processed_count += 1

    def display(self, index):
        print(f"[{index}] "
              f"Agent: {self.name} | "
              f"ID: {self.agent_id} | "
              f"Processed tickets: {self.processed_count}")

    def to_dict(self):
        return{
            "id": self.agent_id,
            "agent": self.name,
            "processed tickets": self.processed_count
        }

class TicketResult:
    def __init__(self,
                 ticket_id,
                 customer_name,
                 priority,
                 issue,
                 agent_id,
                 status,
                 message):
        self.ticket_id = ticket_id
        self.customer_name = customer_name
        self.priority = priority
        self.issue = issue
        self.agent_id = agent_id
        self.status = status
        self.message = message

    def display(self):
        print(f"Ticket: {self.ticket_id} | "
              f"Customer: {self.customer_name} | "
              f"Priority: {self.priority} | "
              f"Agent: {self.agent_id} | "
              f"Status: {self.status} | "
              f"Message: {self.message}")

    def to_dict(self):
        return {
            "ticket_id": self.ticket_id,
            "customer_name": self.customer_name,
            "priority": self.priority,
            "issue": self.issue,
            "agent_id": self.agent_id,
            "status": self.status,
            "message": self.message
        }

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        time_elapsed = end - start
        print(f"Processing finished in {time_elapsed:.2f} seconds.")
        return result
    return wrapper

def find_agent(agents, agent_id):
    for agent in agents:
        if agent.agent_id == agent_id:
            return agent
    return None

def add_agent(agents):
    agent_id = input("Enter agent ID: ").strip()
    if not agent_id:
        print("Invalid agent data")
        return
    if find_agent(agents, agent_id):
        print("Agent ID already exists")
        return
    name = input("Enter agent name: ").strip()
    if not name:
        print("Invalid agent data")
        return
    agents.append(SupportAgent(agent_id, name, 0))
    print("Agent added.")

def show_agents(agents):
    if not agents:
        print("No agents available")
        return
    for index, agent in enumerate(agents, start=1):
        agent.display(index)

def load_tickets_from_csv():
    file_name = "tickets.csv"
    tickets = []
    try:
        with (open(file_name, "r") as file):
            reader = csv.reader(file)
            header = next(reader, None)
            for row in reader:
                if len(row) != 4:
                    continue
                if (not row[0].strip() or
                    not row[1].strip() or
                    not row[2].strip() or
                    not row[3].strip()):
                    continue
                if row[2].strip().lower() not in ("high", "medium", "low"):
                    continue
                tickets.append({
                    "ticket_id": row[0].strip(),
                    "customer_name": row[1].strip(),
                    "priority": row[2].strip().lower(),
                    "issue": row[3].strip()
                })
    except FileNotFoundError:
        print("File not found")
        return
    except PermissionError:
        print("Permission denied")
        return
    print("Tickets loaded.")
    return tickets

@timer
def process_all_tickets(tickets, agents):
    if not tickets:
        print("No tickets loaded")
        return
    if not agents:
        print("No agents available")
        return
    ticket_priority_queue = queue.PriorityQueue()
    priority_map = {
        "high": 1,
        "medium": 2,
        "low": 3
    }
    counter = {
        "high": 0,
        "medium": 0,
        "low": 0
    }
    for ticket in tickets:
        priority_name = ticket.get("priority")
        priority = priority_map.get(priority_name)
        counter[priority_name] += 1
        counter_ticket = counter[priority_name]
        ticket_priority_queue.put((priority, counter_ticket, ticket))
    threads = []
    lock = threading.Lock()
    results = []
    for _ in range(3):
        thread = threading.Thread(
            target=worker,
            args=(ticket_priority_queue, agents, results, lock)
        )
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print("Tickets processed.")
    return results

def worker(ticket_queue, agents, results, lock):
    while True:
        try:
            priority_number, counter, ticket = ticket_queue.get_nowait()
        except queue.Empty:
            break
        result = process_ticket(ticket, agents, lock)
        with lock:
            results.append(result)
        ticket_queue.task_done()

def find_least_busy_agent(agents):
    least_busy = agents[0]
    for agent in agents:
        if agent.processed_count < least_busy.processed_count:
            least_busy = agent
    return least_busy

def process_ticket(ticket, agents, lock):
    with lock:
        agent = find_least_busy_agent(agents)
        agent.process_ticket()
        agent_id = agent.agent_id
    return TicketResult(
        ticket.get("ticket_id"),
        ticket.get("customer_name"),
        ticket.get("priority"),
        ticket.get("issue"),
        agent_id,
        "Success",
        "Ticket resolved"
    )

def show_ticket_report(results):
    if not results:
        print("No report available")
        return
    for report in results:
        report.display()

def show_agent_statistics(agents):
    if not agents:
        print("No agents available")
        return
    for agent in agents:
        print(f"{agent.agent_id} processed {agent.processed_count} ticket(s)")

def save_report_to_json(results):
    if not results:
        print("No report available")
        return
    file_name = "ticket_report.json"
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
    agents = []
    tickets = []
    results = []
    while True:
        try:
            choice = int(input("1) Add support agent\n"
                               "2) Show agents\n"
                               "3) Load tickets from CSV\n"
                               "4) Process loaded tickets\n"
                               "5) Show ticket report\n"
                               "6) Show agent statistics\n"
                               "7) Save report to JSON\n"
                               "8) Exit\n"))
        except ValueError:
            print("Invalid choice. choose between 1 and 8.")
            continue
        match choice:
            case 1:
                add_agent(agents)
            case 2:
                show_agents(agents)
            case 3:
                loaded_tickets = load_tickets_from_csv()
                if loaded_tickets is not None:
                    tickets = loaded_tickets
            case 4:
                loaded_results = process_all_tickets(tickets, agents)
                if loaded_results is not None:
                    results = loaded_results
            case 5:
                show_ticket_report(results)
            case 6:
                show_agent_statistics(agents)
            case 7:
                save_report_to_json(results)
            case 8:
                print("Goodbye!")
                break
            case _:
                print("Invalid choice. choose between 1 and 8.")

if __name__ == "__main__":
    main()
