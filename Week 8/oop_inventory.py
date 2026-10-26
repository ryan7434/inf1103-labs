import os
import json
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_FILE = os.path.join(SCRIPT_DIR, "inventory.json")

class Product:
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_product_id(self):
            return self.__product_id

    def update_stock(self, new_stock):
        self.__stock = new_stock

    def display_information(self):
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")


class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        self.__products.append(product)
        print("Product added successfully.")

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product

        return None

    def display_all(self):
        print("Current Inventory")
        print("-" * 50)

        for product in self.__products:
            product.display_information()
            print("-" * 50)



inventory = [
    {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
    {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
]

def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as file:
            inventory = json.load(file)
            print("inventory.json found")
            print("Inventory loaded successfully.")
            return inventory
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Invalid data in inventory file. Starting with zero inventory.")
        return []

def save_inventory(inventory):
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory, file, indent=4)
        print("Inventory saved successfully to inventory.json.")

def display_all(inventory):
    print("Current Inventory")
    print("-" * 50)
    for product in inventory:
        print(f"ID: {product['id']} | Name: {product['name']} | Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print("-" * 50)

def add_product(inventory):
    print("Add New Product")
    product_id = input("Product ID : ")
    name = input("Product Name : ")
    price = float(input("Product Price : "))
    stock = int(input("Product Stock : "))
    new_product = {"id": product_id, "name": name, "price": price, "stock": stock}
    inventory.append(new_product)
    print("Product added successfully.")

def update_stock(inventory):
    print("Update Stock")
    search_id = input("Enter Product ID: ")

    for product in inventory:
        if product["id"] == search_id:
            print("Product found: ")
            print(f"Name: {product['name']}")
            print(f"Current Stock: {product['stock']}")
            new_stock = int(input(f"Enter new stock for {product['name']}: "))
            product["stock"] = new_stock
            print("Stock updated successfully.")
            return
    print("Product not found.")

def search_product(inventory):
    print("Search Product")
    search_id = input("Enter Product ID: ")

    for product in inventory:
        if product["id"] == search_id:
            print("Product Found")
            print("-" * 50)
            print(f"ID: {product['id']}")
            print(f"Name: {product['name']}")
            print(f"Price: ${product['price']:.2f}")
            print(f"Stock: {product['stock']}")
            print("-" * 50)
            return
    print("Product not found.")

def main():
    inventory = load_inventory()

    while True:
        print() 
        print("========================================") 
        print(" INVENTORY MANAGEMENT SYSTEM") 
        print("========================================") 
        print("----------- MENU -----------") 
        print("1. Display All Products") 
        print("2. Add Product") 
        print("3. Update Stock") 
        print("4. Search Product") 
        print("5. Save Inventory") 
        print("6. Exit") 
        print("----------------------------")

        choice = input("Enter your choice: ")

        if choice == "1":
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            print("Saving inventory to inventory.json...")
            save_inventory(inventory)
        elif choice == "6":
            print("Saving inventory to inventory.json...")
            save_inventory(inventory)
            print("Thank you for using the Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid choice. Please try again.")
#main()
if __name__ == "__main__":
    main()
