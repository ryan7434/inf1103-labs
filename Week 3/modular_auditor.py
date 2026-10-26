#can do global constant for tax rate and max inventory limit
#Tax_rate = 0.10
#max_inventory_limit = 500

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
    tax = amount * 0.10
    return tax

def generate_reports(total_units,failed_attempts):
    print("Total units processed:", total_units)
    print("Failed entries:", failed_attempts)

def main():
    inventory = 0
    failed_entries = 0

    while True:
        result = get_valid_input()

        if result == "quit":
            break

        elif result is None:
            failed_entries += 1
            continue

        inventory = process_delivery(inventory, result)

        if inventory > 500:
            print("Inventory limit exceeded. Cannot add more stock.")
            break

    tax_amount = calculate_tax(inventory)
    print("Total tax on inventory:", tax_amount)

    generate_reports(inventory, failed_entries)

main()
#if __name__ == "__main__":
    #main()




