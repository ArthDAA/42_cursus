import sys

print("=== Inventory System Analysis ===")

inventory: dict[str, int] = {}
arguments: list[str] = sys.argv[1:]

for arg in arguments:
    parts: list[str] = arg.split(":")

    if len(parts) != 2:
        print(f"Error - invalid parameter '{arg}'")
        continue

    item_name: str = parts[0]
    qty_str: str = parts[1]

    try:
        qty: int = int(qty_str)
    except ValueError as e:
        print(f"Quantity error for '{item_name}': {e}")
        continue

    if item_name in inventory:
        print(f"Redundant item '{item_name}' - discarding")
        continue

    inventory.update({item_name: qty})

print(f"Got inventory: {inventory}")

item_list: list[str] = list(inventory.keys())
print(f"Item list: {item_list}")

total_qty: int = sum(list(inventory.values()))
print(f"Total quantity of the {len(item_list)} items: {total_qty}")

for item in item_list:
    current_qty: int = inventory[item]
    percentage: float = round((current_qty / total_qty) * 100, 1)
    print(f"Item {item} represents {percentage}%")

if len(item_list) > 0:
    most_abundant_item: str = item_list[0]
    most_abundant_qty: int = inventory[most_abundant_item]

    least_abundant_item: str = item_list[0]
    least_abundant_qty: int = inventory[least_abundant_item]

    for item in item_list:
        loop_qty: int = inventory[item]

        if loop_qty > most_abundant_qty:
            most_abundant_qty = loop_qty
            most_abundant_item = item

        if loop_qty < least_abundant_qty:
            least_abundant_qty = loop_qty
            least_abundant_item = item

    print(f"Item most abundant: {most_abundant_item} "
          f"with quantity {most_abundant_qty}\n"
          f"Item least abundant: {least_abundant_item} "
          f"with quantity {least_abundant_qty}")

inventory.update({"magic_item": 1})
print(f"Updated inventory: {inventory}")
