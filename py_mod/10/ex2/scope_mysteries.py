#!/usr/bin/env python3
from collections.abc import Callable


def mage_counter() -> Callable[[], int]:
    count: int = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    total: int = initial_power

    def accumulate(amount: int) -> int:
        nonlocal total
        total += amount
        return total

    return accumulate


def enchantment_factory(enchantment_type: str) -> Callable[[str], str]:
    def enchant(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"

    return enchant


def memory_vault() -> dict[str, Callable]:
    _storage: dict[str, object] = {}

    def store(key: str, value: object) -> None:
        _storage[key] = value

    def recall(key: str) -> object:
        return _storage.get(key, "Memory not found")

    return {"store": store, "recall": recall}


if __name__ == "__main__":
    print("Testing mage counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()
    print(f"counter_a call 1: {counter_a()}")
    print(f"counter_a call 2: {counter_a()}")
    print(f"counter_b call 1: {counter_b()}")

    print()
    print("Testing spell accumulator...")
    acc = spell_accumulator(100)
    print(f"Base 100, add 20: {acc(20)}")
    print(f"Base 100, add 30: {acc(30)}")

    print()
    print("Testing enchantment factory...")
    flaming = enchantment_factory("Flaming")
    frozen = enchantment_factory("Frozen")
    print(flaming("Sword"))
    print(frozen("Shield"))

    print()
    print("Testing memory vault...")
    vault = memory_vault()
    print("Store 'secret' = 42")
    vault["store"]("secret", 42)
    print(f"Recall 'secret': {vault['recall']('secret')}")
    print(f"Recall 'unknown': {vault['recall']('unknown')}")
