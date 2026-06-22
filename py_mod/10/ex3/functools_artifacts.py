#!/usr/bin/env python3
import functools
import operator
from collections.abc import Callable
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0
    ops: dict[str, Callable] = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max,
        "min": min,
    }
    if operation not in ops:
        raise ValueError(f"Unknown operation: '{operation}'")
    if operation in ("max", "min"):
        return functools.reduce(ops[operation], spells)
    return functools.reduce(ops[operation], spells)


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    fire_enchant = functools.partial(base_enchantment, power=50, element="fire")
    ice_enchant = functools.partial(base_enchantment, power=50, element="ice")
    lightning_enchant = functools.partial(
        base_enchantment, power=50, element="lightning"
    )
    return {
        "fire": fire_enchant,
        "ice": ice_enchant,
        "lightning": lightning_enchant,
    }


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    @functools.singledispatch
    def dispatch(spell: Any) -> str:
        return "Unknown spell type"

    @dispatch.register(int)
    def _(spell: int) -> str:
        return f"{spell} damage"

    @dispatch.register(str)
    def _(spell: str) -> str:  # type: ignore[misc]
        return spell

    @dispatch.register(list)
    def _(spell: list) -> str:  # type: ignore[misc]
        return f"{len(spell)} spells"

    return dispatch


if __name__ == "__main__":
    print("Testing spell reducer...")
    spells: list[int] = [10, 20, 30, 40]
    print(f"Sum: {spell_reducer(spells, 'add')}")
    print(f"Product: {spell_reducer(spells, 'multiply')}")
    print(f"Max: {spell_reducer(spells, 'max')}")
    print()

    print("Testing memoized fibonacci...")
    for n in (0, 1, 10, 15):
        print(f"Fib({n}): {memoized_fibonacci(n)}")
    print(f"Cache info: {memoized_fibonacci.cache_info()}")
    print()

    def base_enchant(target: str, power: int, element: str) -> str:
        return f"{element.capitalize()} enchantment on {target} with {power} power"

    enchanters = partial_enchanter(base_enchant)
    print("Testing partial enchanter...")
    for elem, fn in enchanters.items():
        print(fn(target="Sword"))
    print()

    print("Testing spell dispatcher...")
    dispatch = spell_dispatcher()
    print(f"Damage spell: {dispatch(42)}")
    print(f"Enchantment: {dispatch('fireball')}")
    print(f"Multi-cast: {dispatch([1, 2, 3])}")
    print(f"Unknown: {dispatch(3.14)}")
