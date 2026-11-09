import os
import json
from abc import ABC, abstractmethod

class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.supplier_id = supplier_id
        self.name = name
        self.contact_email = contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self.supplier_id}")
        print(f"Supplier Name: {self.name}")
        print(f"Contact Email: {self.contact_email}")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_FILE = os.path.join(SCRIPT_DIR, "inventory.json")

class Product(ABC):
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier
    ):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.__supplier = supplier

    def get_product_id(self) -> str:
        return self.__product_id
    
    def get_product_name(self) -> str:
        return self.__name
    
    def get_product_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def to_dict(self) -> dict:
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": {
                "supplier_id": self.__supplier.supplier_id,
                "name": self.__supplier.name,
                "contact_email": self.__supplier.contact_email
            }
        }

    def update_stock(self, new_stock: int) -> None:
        self.__stock = new_stock

    def display_information(self) -> None:
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")

    def display_supplier_information(self) -> None:
        self.__supplier.display_information()

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass

class PhysicalProduct(Product, CanBeShipped):
    def __init__(
            self,
            product_id: str,
            name: str,
            price: float,
            stock: int,
            weight: float,
            supplier: Supplier
    ):
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight = weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.__weight} kg")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return self.__weight * 5 

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

class DigitalProduct(Product):
    def __init__(
            self,
            product_id: str,
            name: str,
            price: float,
            stock: int,
            download_size: float,
            supplier: Supplier
    ):
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size = download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self.__download_size} MB")

    def get_fulfilment_info(self) -> str:
        return "This product can be delivered digitally."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

class SubscriptionProduct(Product):
    def __init__(
            self,
            product_id: str,
            name: str,
            price: float,
            stock: int,
            duration: int,
            supplier: Supplier
    ):
        super().__init__(product_id, name, price, stock, supplier)
        self.__duration = duration

    def display_information(self) -> None:
        super().display_information()
        print(f"Subscription Duration: {self.__duration} months")

    def get_fulfilment_info(self) -> str:
        return "This product provides a subscription based access."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "subscription"
        data["duration"] = self.__duration
        return data

class Inventory:
    def __init__(self):
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    def remove_product(self, product_id: str) -> None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                self.__products.remove(product)
                return

        print(f"Product {product_id} not found.")

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self) -> None:
        print("Current Inventory")
        print("-" * 50)

        if len(self.__products) == 0:
            print("Inventory is empty.")
            return

        for product in self.__products:
            product.display_information()
            product.display_supplier_information()
            print(f"Fulfilment: {product.get_fulfilment_info()}")
            print("-" * 50)

    def get_products(self) -> list[Product]:
        return self.__products

class OrderLine:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

    def calculate_subtotal(self) -> float:
        return self.product.get_product_price() * self.quantity

class Order:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        total = 0.0

        for order_line in self.order_lines:
            total += order_line.calculate_subtotal()

        return total
    
def load_inventory():
    inventory = Inventory()

    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)

        for item in data:

            supplier_data = item.get("supplier")
            
            if supplier_data:
                supplier = Supplier(
                supplier_data["supplier_id"],
                supplier_data["name"],
                supplier_data["contact_email"]
                )
            else:
                supplier = Supplier(
                "S000",
                "Unknown Supplier",
                "unknown@example.com"
                )

            if item["type"] == "physical":
                product = PhysicalProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    item["weight"],
                    supplier
                )

            elif item["type"] == "digital":
                product = DigitalProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    item["download_size"],
                    supplier
                )

            elif item["type"] == "subscription":
                product = SubscriptionProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    item["duration"],
                    supplier
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

def show_product_details(product: Product) -> None:
    product.display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")

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
        print("6. Remove Product")
        print("7. Exit")
        print("----------------------------")

        choice = input("Enter your choice: ")

        if choice == "1":
            inventory.display_all()

        elif choice == "2":
            print("Add New Product")
            print("1. Physical Product")
            print("2. Digital Product")
            print("3. Subscription Product")

            product_type = input("Enter product type (1, 2, or 3): ")

            if product_type not in ["1", "2", "3"]:
                print("Invalid product type. Please try again.")
                continue

            product_id = input("Enter Product ID: ")

            if inventory.find_product(product_id) is not None:
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

                    supplier_id = input("Enter Supplier ID: ")
                    supplier_name = input("Enter Supplier Name: ")
                    supplier_email = input("Enter Supplier Email: ")
                    
                    supplier = Supplier(
                        supplier_id,
                        supplier_name,
                        supplier_email
                        )

                    product = PhysicalProduct(product_id, name, price, stock, weight, supplier)

                elif product_type == "2":
                    download_size = float(input("Enter Download Size (MB): "))

                    if download_size <= 0:
                        print("Download size must be greater than zero.")
                        continue

                    supplier_id = input("Enter Supplier ID: ")
                    supplier_name = input("Enter Supplier Name: ")
                    supplier_email = input("Enter Supplier Email: ")
                                        
                    supplier = Supplier(
                        supplier_id,
                        supplier_name,
                        supplier_email
                    )
                    

                    product = DigitalProduct(product_id, name, price, stock, download_size, supplier)

                elif product_type == "3":
                    duration = int(input("Enter Subscription Duration (months): "))

                    if duration <= 0:
                        print("Duration must be greater than zero.")
                        continue

                    supplier_id = input("Enter Supplier ID: ")
                    supplier_name = input("Enter Supplier Name: ")
                    supplier_email = input("Enter Supplier Email: ")
                                        
                    supplier = Supplier(
                        supplier_id,
                        supplier_name,
                        supplier_email
                    )

                    product = SubscriptionProduct(product_id, name, price, stock, duration, supplier)

                inventory.add_product(product)
                print("Product added successfully.")

            except ValueError:
                print("Invalid input. Please enter valid inputs.")

        elif choice == "3":
            print("Update Stock")
            product_id = input("Enter Product ID: ")

            product = inventory.find_product(product_id)

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

            product = inventory.find_product(product_id)

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
            product_id = input("Enter Product ID to remove: ")
            
            inventory.remove_product(product_id)

        elif choice == "7":
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