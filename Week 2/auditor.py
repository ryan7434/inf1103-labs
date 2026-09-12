inventory = int(0)
failed_entries = int(0)

while True:
    entry = input("Enter stock quantity (enter quit to exit): ")

    if entry.lower() == "quit":
        break

    if not entry.isdigit():
        print("Invalid input. Please enter a valid number.")
        failed_entries += 1
        continue

    quantity = int(entry)

    if quantity < 0:
        print("Invalid input. Quantity cannot be negative.")
        failed_entries += 1
        continue

    inventory += quantity

    if inventory > 500:
        print("Inventory limit exceeded. Cannot add more stock.")
        break

print("Total units processed:", inventory)
print("Failed entries:", failed_entries)