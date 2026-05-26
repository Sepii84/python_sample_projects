#Multithreaded Inventory Order processor

import csv
import json
import threading
import queue

class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def reduce_stock(self, quantity):
        self.stock -= quantity

    def display(self, index):
        print(
            f"[{index}] "
            f"Product: {self.name} | "
            f"ID: {self.product_id} | "
            f"Price: {self.price:.2f} | "
            f"Stock: {self.stock}"
        )

    def to_dict(self):
        return {
            "Product": self.name,
            "ID": self.product_id,
            "Price": self.price,
            "Stock": self.stock
        }

class OrderResult:
    def __init__(self,
                 order_id,
                 customer_name,
                 product_id,
                 quantity,
                 status,
                 message,
                 total_price):
        self.order_id = order_id
        self.customer_name = customer_name
        self.product_id = product_id
        self.quantity = quantity
        self.status = status
        self.message = message
        self.total_price = total_price

    def display(self):
        print(
            f"Order: {self.order_id} | "
            f"Customer: {self.customer_name} | "
            f"Product: {self.product_id} | "
            f"Quantity: {self.quantity} | "
            f"Status: {self.status} | "
            f"Total: {self.total_price:.2f} | "
            f"Message: {self.message}"
        )

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_name": self.customer_name,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "status": self.status,
            "message": self.message,
            "total_price": self.total_price
        }

def find_product(products, product_id):
    for product in products:
        if product.product_id == product_id:
            return product
    return None

def add_product(products):
    product_id = input("Enter the product ID: ").strip()
    if not product_id:
        print("Invalid product data")
        return
    if find_product(products, product_id) is not None:
        print("Product ID already exists")
        return
    name = input("Enter the product name: ").strip()
    if not name:
        print("Invalid product data")
        return
    try:
        price = float(input("Enter the product price: "))
    except ValueError:
        print("Invalid product data")
        return
    if price <= 0:
        print("Invalid product data")
        return
    try:
        stock = int(input("Enter the product stock: "))
    except ValueError:
        print("Invalid product data")
        return
    if stock < 0:
        print("Invalid product data")
        return
    products.append(Product(product_id, name, price, stock))
    print("Product added.")

def show_products(products):
    if not products:
        print("No products available")
        return
    for index, product in enumerate(products, start=1):
        product.display(index)

def load_orders_from_csv():
    file_name = "orders.csv"
    orders = []
    try:
        with open(file_name, "r") as file:
            reader = csv.reader(file)
            header = next(reader, None)
            for row in reader:
                if len(row) != 4:
                    continue
                try:
                    orders.append(
                        {
                            "order_id": row[0],
                            "customer_name": row[1],
                            "product_id": row[2],
                            "quantity": int(row[3])
                        }
                    )
                except ValueError:
                    continue
    except FileNotFoundError:
        print("File not found")
        return None
    except PermissionError:
        print("Permission denied")
        return None
    print("Orders loaded.")
    return orders

def process_all_orders(orders, products):
    if not orders:
        print("No orders loaded")
        return
    if not products:
        print("No products available")
        return
    results = []
    order_queue = queue.Queue()
    for order in orders:
        order_queue.put(order)
    threads = []
    lock = threading.Lock()
    for _ in range(3):
        thread = threading.Thread(
            target=worker,
            args=(order_queue, products, results, lock)
        )
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print("Orders processed.")
    return results

def process_order(order, products, lock):
    order_id = order.get("order_id")
    customer_name = order.get("customer_name")
    product_id = order.get("product_id")
    quantity = order.get("quantity")
    status = "Failed"
    total_price = 0
    with lock:
        product = find_product(products, product_id)
        if product is None:
            message = "Product not found"
        elif quantity <= 0:
            message = "Invalid quantity"
        elif product.stock < quantity:
            message = "Not enough stock"
        else:
            status = "Success"
            message = "Order completed"
            total_price = quantity * product.price
            product.reduce_stock(quantity)
    return OrderResult(
        order_id,
        customer_name,
        product_id,
        quantity,
        status,
        message,
        total_price
    )

def worker(order_queue, products, results, lock):
    while True:
        try:
            order = order_queue.get_nowait()
        except queue.Empty:
            break
        result = process_order(order, products, lock)
        with lock:
            results.append(result)
        order_queue.task_done()

def show_order_report(results):
    if not results:
        print("No report available")
        return
    for result in results:
        result.display()

def save_report_to_json(results):
    if not results:
        print("No report available")
        return
    file_name = "order_report.json"
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
    products = []
    orders = []
    results = []
    while True:
        try:
            choice = int(input("1) Add product\n"
                               "2) Show all products\n"
                               "3) Load orders from CSV\n"
                               "4) Process loaded orders\n"
                               "5) Show order report\n"
                               "6) Save report to JSON\n"
                               "7) Exit\n"))
        except ValueError:
            print("Invalid choice! choose between 1 and 7")
            continue
        match choice:
            case 1:
                add_product(products)
            case 2:
                show_products(products)
            case 3:
                loaded_orders = load_orders_from_csv()
                if loaded_orders is not None:
                    orders = loaded_orders
            case 4:
                loaded_results = process_all_orders(orders, products)
                if loaded_results is not None:
                    results = loaded_results
            case 5:
                show_order_report(results)
            case 6:
                save_report_to_json(results)
            case 7:
                print("Goodbye!")
                break
            case _:
                print("Invalid choice! choose between 1 and 7")

if __name__ == "__main__":
    main()