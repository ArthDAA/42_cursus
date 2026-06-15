import sys


def parse_inventory(args: list[str]) -> dict[str, int]:
    inventory: dict[str, int] = {}
    for arg in args:
        parts: list[str] = arg.split(":")
        if (len(parts) != 2):
            print(f"Error - invalid parameter '{arg}'")
            continue
        name: str = parts[0]
        qty_str: str = parts[1]
        if (name in inventory):
            print(f"Redundant item '{name}' - discarding")
            continue
        try:
            qty: int = int(qty_str)
        except ValueError as error:
            print(f"Quantity error for '{name}': {error}")
            continue
        inventory[name] = qty
    return (inventory)


def find_extremes(inventory: dict[str, int]) -> tuple[str, str]:
    item_list: list[str] = list(inventory.keys())
    most: str = item_list[0]
    least: str = item_list[0]
    for item in item_list:
        if (inventory[item] > inventory[most]):
            most = item
        if (inventory[item] < inventory[least]):
            least = item
    return ((most, least))


def display_analysis(inventory: dict[str, int]) -> None:
    item_list: list[str] = list(inventory.keys())
    total: int = sum(inventory.values())
    print(f"Got inventory: {inventory}")
    print(f"Item list: {item_list}")
    print(f"Total quantity of the {len(item_list)} items: {total}")
    for item in item_list:
        percent: float = round(inventory[item] / total * 100, 1)
        print(f"Item {item} represents {percent}%")
    most: str
    least: str
    most, least = find_extremes(inventory)
    print(f"Item most abundant: {most} with quantity {inventory[most]}")
    print(f"Item least abundant: {least} with quantity {inventory[least]}")


def main() -> None:
    args: list[str] = sys.argv[1:]
    print("=== Inventory System Analysis ===")
    inventory: dict[str, int] = parse_inventory(args)
    if (len(inventory) == 0):
        return
    display_analysis(inventory)
    inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")


if (__name__ == "__main__"):
    main()