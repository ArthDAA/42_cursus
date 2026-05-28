import random

ACHIEVEMENTS = [
    'Crafting Genius', 'Strategist', 'World Savior', 'Speed Runner',
    'Survivor', 'Master Explorer', 'Treasure Hunter', 'Unstoppable',
    'First Steps', 'Collector Supreme',
    'Untouchable', 'Sharp Mind', 'Boss Slayer'
]


def gen_player_achievements():
    success = random.randint(1, len(ACHIEVEMENTS))
    return set(random.sample(ACHIEVEMENTS, success))


if __name__ == "__main__":
    print("=== Achievement Tracker System ===\n")
    Players = {
        'Epic': gen_player_achievements(),
        'Ice': gen_player_achievements(),
        'Bluekill33': gen_player_achievements(),
        'Boruto459': gen_player_achievements()
    }
    player_names = list(Players.keys())
    for i in range(len(player_names)):
        name = player_names[i]
        print(f"Player {name}: {Players[name]}")
    print(f"\nAll distinct achievements: {set(ACHIEVEMENTS)}\n")

    common_achievements = set.intersection(*Players.values())
    print(f"Common achievements: {common_achievements}\n")

    for name in player_names:
        diff_sets = [Players[diff] for diff in player_names if diff != name]
        diff = Players[name].difference(*diff_sets)
        print(f"Only {name} has: {diff}")

    print("\n")
    for name in player_names:
        all_achievements = set(ACHIEVEMENTS)
        diff_sets = [Players[diff] for diff in player_names if diff != name]
        diff = Players[name].difference(*diff_sets)
        missing = all_achievements - Players[name]
        print(f"{name} is missing: {missing}")
