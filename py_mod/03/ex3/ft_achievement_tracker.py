import random


ACHIEVEMENTS: list[str] = [
    "Crafting Genius", "Strategist", "World Savior", "Speed Runner",
    "Survivor", "Master Explorer", "Treasure Hunter", "Unstoppable",
    "First Steps", "Collector Supreme",
    "Untouchable", "Sharp Mind", "Boss Slayer", "Hidden Path Finder",
]


def gen_player_achievements() -> set[str]:
    count: int = random.randint(1, len(ACHIEVEMENTS))
    picked: list[str] = random.sample(ACHIEVEMENTS, count)
    return (set(picked))


def main() -> None:
    print("=== Achievement Tracker System ===")

    players: dict[str, set[str]] = {
        "Alice": gen_player_achievements(),
        "Bob": gen_player_achievements(),
        "Charlie": gen_player_achievements(),
        "Dylan": gen_player_achievements(),
    }

    for name, owned in players.items():
        print(f"Player {name}: {owned}")

    all_distinct: set[str] = set()
    for owned in players.values():
        all_distinct = all_distinct.union(owned)
    print(f"All distinct achievements: {all_distinct}")

    common: set[str] = set(ACHIEVEMENTS)
    for owned in players.values():
        common = common.intersection(owned)
    print(f"Common achievements: {common}")

    for name, owned in players.items():
        others: set[str] = set()
        for other_name, other_owned in players.items():
            if (other_name != name):
                others = others.union(other_owned)
        print(f"Only {name} has: {owned.difference(others)}")

    for name, owned in players.items():
        missing: set[str] = all_distinct.difference(owned)
        print(f"{name} is missing: {missing}")


if (__name__ == "__main__"):
    main()
