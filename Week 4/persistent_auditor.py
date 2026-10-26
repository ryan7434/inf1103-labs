import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_FILE = os.path.join(SCRIPT_DIR, "inventory.txt")

#can do global constant for tax rate and max inventory limit
Tax_rate = float(0.10)
Max_inventory_limit = int(500)

def get_valid_input():
        entry = input("Enter stock quantity (enter quit to exit): ")

        if entry.lower() == "quit":
            return "quit"

        if not entry.isdigit():
            print("Invalid input. Please enter a valid number.")
            return None

        quantity = int(entry)

        if quantity < 0:
            print("Invalid input. Quantity cannot be negative.")
            return None

        return quantity

def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total

def calculate_tax(amount):
    tax = amount * Tax_rate
    return tax

def generate_reports(total_units,failed_attempts):
    print("Total units processed:", total_units)
    print("Failed entries:", failed_attempts)

def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as file:
            lines = file.readlines()
            inventory = int(lines[0])  
            history = [int(line.strip()) for line in lines[1:]]
            return inventory, history
    except FileNotFoundError:
        return 0, []
    except ValueError:
        print("Invalid data in inventory file. Starting with zero inventory.")
        return 0, []

def save_inventory(inventory, history):
    with open(INVENTORY_FILE, "w") as file:
        file.write(str(inventory) + "\n")
        for entry in history:
            file.write(str(entry) + "\n")

def main():
    inventory, history = load_inventory()
    failed_entries = 0

    while True:
        result = get_valid_input()

        if result == "quit":
            break

        elif result is None:
            failed_entries += 1
            continue

        inventory = process_delivery(inventory, result)

        history.append(result)

        if inventory > Max_inventory_limit:
            print("Inventory limit exceeded. Cannot add more stock.")
            break

    save_inventory(inventory, history)
    tax_amount = calculate_tax(inventory)
    print("Total tax on inventory:", tax_amount)

    generate_reports(inventory, failed_entries)

#main()
if __name__ == "__main__":
    main()




