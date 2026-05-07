# store inventory manager

class Product:
    def __init__(self, name, product_id, price, quantity):
        self.name = name
        self.product_id = product_id #unique
        self.price = price
        self.quantity = quantity
    def __str__(self):
        return (f"Name: {self.name}, "
                f"ID: {self.product_id}, "
                f"Price: {self.price:.1f}, "
                f"Quantity: {self.quantity}")

class Store:
    def __init__(self):
        self.products = []

    def find_product(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None

    def add_product(self, name, product_id, price, quantity):
        self.products.append(Product(name, product_id, price, quantity))
        print("Product added.")

    def show_products(self):
        if not self.products:
            print("No products available")
            return
        for product in self.products:
            print(product)

    def restock_product(self, product_id, quantity):
        product = self.find_product(product_id)
        product.quantity += quantity
        print("Restock successful.")

    def sell_product(self, product_id, quantity):
        product = self.find_product(product_id)
        if product.quantity < quantity:
            print("Insufficient stock")
            return
        product.quantity -= quantity
        print("Sale successful.")

    def search_product(self, product_id):
        product = self.find_product(product_id)
        if not product:
            print("Product not found")
            return
        print(product)

    def total_inventory_value(self):
        total = 0
        for product in self.products:
            total += product.quantity * product.price
        print(f"Total inventory value: {total:.1f}")

def main():
    store = Store()
    while True:
        try:
            choice = int(input("1) Add product\n"
                               "2) Show all products\n"
                               "3) Restock product\n"
                               "4) Sell product\n"
                               "5) Search product by ID\n"
                               "6) Show total inventory value\n"
                               "7) Exit\n"))
        except ValueError:
            print("Please enter a number between 1 and 7")
            continue
        match choice:
            case 1:
                name = input("Enter product name: ").strip()
                if not name:
                    print("Invalid product data")
                    continue
                try:
                    product_id = int(input("Enter product ID: "))
                except ValueError:
                    print("Invalid product data")
                    continue
                if store.find_product(product_id):
                    print("Product ID already exists")
                    continue
                try:
                    price = float(input("Enter product price: "))
                except ValueError:
                    print("Invalid price")
                    continue
                if price <= 0:
                    print("Invalid price")
                    continue
                try:
                    quantity = int(input("Enter quantity: "))
                except ValueError:
                    print("Invalid quantity")
                    continue
                if quantity < 0:
                    print("Invalid quantity")
                    continue
                store.add_product(name, product_id, price, quantity)
            case 2:
                store.show_products()
            case 3:
                try:
                    product_id = int(input("Enter product ID: "))
                except ValueError:
                    print("Invalid product data")
                    continue
                if not store.find_product(product_id):
                    print("Product not found")
                    continue
                try:
                    quantity = int(input("Enter quantity: "))
                except ValueError:
                    print("Invalid quantity")
                    continue
                if quantity <= 0:
                    print("Invalid quantity")
                    continue
                store.restock_product(product_id, quantity)
            case 4:
                try:
                    product_id = int(input("Enter product ID: "))
                except ValueError:
                    print("Invalid product data")
                    continue
                if not store.find_product(product_id):
                    print("Product not found")
                    continue
                try:
                    quantity = int(input("Enter quantity: "))
                except ValueError:
                    print("Invalid quantity")
                    continue
                if quantity <= 0:
                    print("Invalid quantity")
                    continue
                store.sell_product(product_id, quantity)
            case 5:
                try:
                    product_id = int(input("Enter product ID: "))
                except ValueError:
                    print("Invalid product data")
                    continue
                store.search_product(product_id)
            case 6:
                store.total_inventory_value()
            case 7:
                print("Goodbye!")
                break
            case _:
                print("Please enter a number between 1 and 7")

if __name__ == '__main__':
    main()