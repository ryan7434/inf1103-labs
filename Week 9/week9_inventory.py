import os
import json
from abc import ABC, abstractmethod
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_FILE = os.path.join(SCRIPT_DIR, "inventory.json")

class Product(ABC):
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_product_id(self):
        return self.__product_id
    
    def get_product_name(self):
        return self.__name
    
    def get_product_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def to_dict(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }

    def update_stock(self, new_stock):
        self.__stock = new_stock

    def display_information(self):
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")

    @abstractmethod
    def get_fulfilment_info(self):
        pass

class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self):
        pass

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight} kg")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        return self.__weight * 5 

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size

    def display_information(self):
        super().display_information()
        print(f"Download Size: {self.__download_size} MB")

    def get_fulfilment_info(self):
        return "This product can be delivered digitally."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        self.__products.append(product)

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product

        return None

    def display_all(self):
        print("Current Inventory")
        print("-" * 50)

        if len(self.__products) == 0:
            print("Inventory is empty.")
            return

        for product in self.__products:
            product.display_information()
            print(f"Fulfilment: {product.get_fulfilment_info()}")
            print("-" * 50)

    def get_products(self):
        return self.__products

    
def load_inventory():
    inventory = Inventory()

    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)

        for item in data:

            if item["type"] == "physical":
                product = PhysicalProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    item["weight"]
                )

            elif item["type"] == "digital":
                product = DigitalProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    item["download_size"]
                )

            else:
                print("Unknown product type. Skipping item.")
                continue    

            inventory.add_product(product)

        print("Inventory loaded successfully.")
        return inventory

    except FileNotFoundError:
        print("Inventory file not found. Starting with empty inventory.")
        return inventory
    
    except json.JSONDecodeError:
        print("Invalid data in inventory file. Starting with empty inventory.")
        return inventory

    except KeyError:
        print("Inventory file uses an old or invalid format.")
        print("Please back up or remove the old inventory.json file.")
        return inventory


def save_inventory(inventory):
    data = []

    for product in inventory.get_products():
        data.append(product.to_dict())

    with open(INVENTORY_FILE, "w") as file:
        json.dump(data, file, indent=4)

    print("Inventory saved successfully to inventory.json.")



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
            inventory.display_all()

        elif choice == "2":
            print("Add New Product")
            print("1. Physical Product")
            print("2. Digital Product")

            product_type = input("Enter product type (1 or 2): ")

            if product_type not in ["1", "2"]:
                print("Invalid product type. Please try again.")
                continue

            product_id = input("Enter Product ID: ")

            if inventory.search_product(product_id) is not None:
                print("Product ID already exists.")
                continue

            name = input("Enter Product Name: ")

            try:
                price = float(input("Enter Product Price: "))
                stock = int(input("Enter Product Stock: "))

                if price < 0 or stock < 0:
                    print("Price and stock cannot be negative.")
                    continue

                if product_type == "1":
                    weight = float(input("Enter Product Weight (kg): "))

                    if weight < 0:
                        print("Weight must be greater than zero.")
                        continue

                    product = PhysicalProduct(product_id, name, price, stock, weight)

                else:
                    download_size = float(input("Enter Download Size (MB): "))

                    if download_size <= 0:
                        print("Download size must be greater than zero.")
                        continue

                    product = DigitalProduct(product_id, name, price, stock, download_size)

                inventory.add_product(product)
                print("Product added successfully.")

            except ValueError:
                print("Invalid input. Please enter valid inputs.")

        elif choice == "3":
            print("Update Stock")
            product_id = input("Enter Product ID: ")

            product = inventory.search_product(product_id)

            if product is not None:
                print("Product found:")
                print(f"Name: {product.get_product_name()}")
                print(f"Current Stock: {product.get_stock()}")

                try:
                    new_stock = int(
                        input("Enter new stock: ")
                    )

                    if new_stock < 0:
                        print("Stock cannot be negative.")
                    else:
                        product.update_stock(new_stock)
                        print("Stock updated successfully.")

                except ValueError:
                    print("Invalid stock. Please enter a whole number.")

            else:
                print("Product not found.")

        elif choice == "4":
            print("Search Product")
            product_id = input("Enter Product ID: ")

            product = inventory.search_product(product_id)

            if product is not None:
                print("Product Found")
                print("-" * 50)
                product.display_information()
                print("-" * 50)
            else:
                print("Product not found.")

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