#!/usr/bin/env python3


def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda a: a["power"], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda m: m["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda s: f"* {s} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    max_power: int = max(mages, key=lambda m: m["power"])["power"]
    min_power: int = min(mages, key=lambda m: m["power"])["power"]
    avg_power: float = round(
        sum(map(lambda m: m["power"], mages)) / len(mages), 2
    )
    return {"max_power": max_power, "min_power": min_power, "avg_power": avg_power}


if __name__ == "__main__":
    artifacts: list[dict] = [
        {"name": "Crystal Orb", "power": 85, "type": "magic"},
        {"name": "Fire Staff", "power": 92, "type": "fire"},
        {"name": "Shadow Dagger", "power": 70, "type": "dark"},
    ]

    print("Testing artifact sorter...")
    sorted_arts = artifact_sorter(artifacts)
    print(
        f"{sorted_arts[0]['name']} ({sorted_arts[0]['power']} power) "
        f"comes before {sorted_arts[1]['name']} ({sorted_arts[1]['power']} power)"
    )

    print()
    print("Testing spell transformer...")
    spells: list[str] = ["fireball", "heal", "shield"]
    transformed = spell_transformer(spells)
    print(" ".join(transformed))

    print()
    mages: list[dict] = [
        {"name": "Alex", "power": 80, "element": "fire"},
        {"name": "Jordan", "power": 55, "element": "water"},
        {"name": "Riley", "power": 95, "element": "lightning"},
    ]
    stats = mage_stats(mages)
    print(f"Stats: {stats}")

    print()
    print("Testing power filter (min_power=70)...")
    filtered = power_filter(mages, 70)
    print([m["name"] for m in filtered])
