#!/usr/bin/env python3
from alchemy.grimoire import light_spellbook

if __name__ == "__main__":
    print("=== Kaboom 0 ===")
    print("Using grimoire module directly")
    record = light_spellbook.light_spell_record(
        "Fantasy", "Earth, wind and fire"
    )
    print(f"Testing record light spell: {record}")
