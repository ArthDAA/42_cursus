#!/usr/bin/env python3
from collections.abc import Callable


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combined(target: str, power: int) -> tuple[str, str]:
        return (spell1(target, power), spell2(target, power))
    return combined


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return amplified


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def cast(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"
    return cast


def spell_sequence(spells: list[Callable]) -> Callable:
    def sequence(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]
    return sequence


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target}"


def heal(target: str, power: int) -> str:
    return f"Heals {target}"


def is_alive(target: str, power: int) -> bool:
    return power > 0


if __name__ == "__main__":
    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    result = combined("Dragon", 50)
    print(f"Combined spell result: {result[0]}, {result[1]}")

    print()
    print("Testing power amplifier...")

    def damage_spell(target: str, power: int) -> str:
        return f"Deals {power} damage to {target}"

    original_power = 10
    mega = power_amplifier(damage_spell, 3)
    print(f"Original: {original_power}, Amplified: {original_power * 3}")
    print(mega("Dragon", original_power))

    print()
    print("Testing conditional caster...")
    cond_spell = conditional_caster(is_alive, fireball)
    print(cond_spell("Dragon", 50))
    print(cond_spell("Dragon", 0))

    print()
    print("Testing spell sequence...")
    sequence = spell_sequence([fireball, heal, damage_spell])
    results = sequence("Enemy", 30)
    for r in results:
        print(r)

    print()
    print(f"callable(fireball): {callable(fireball)}")
    print(f"callable(42): {callable(42)}")
