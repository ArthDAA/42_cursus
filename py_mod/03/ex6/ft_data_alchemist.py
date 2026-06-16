import random


def main() -> None:
    names: list[str] = [
        "alice",
        "bob",
        "charlie",
        "dylan",
        "emma",
        "gregory",
        "john",
        "kevin",
        "liam"
    ]

    count: int = random.randint(1, len(names))
    to_capitalize: list[str] = random.sample(names, count)

    players: list[str] = []
    for name in names:
        if (name in to_capitalize):
            players.append(name.capitalize())
        else:
            players.append(name)

    print(
        "=== Game Data Alchemist ===\n"
    )

    print(
        "Intial list of players: "
        f"{players}"
    )

    is_capitalized: list[str] = [name for name in players if name[0].isupper()]
    been_capitalized: list[str] = [name.capitalize() for name in players]

    print(
        "New list with all names capitalized: "
        f"{been_capitalized}"
    )

    print(
        "New list of capitalized names only: "
        f"{is_capitalized}\n"
    )

    stats:  dict(str, int) = {}
    for name in been_capitalized:
        stats[name] = random.randint(0, 1000)

    print(
        "Score dict: "
        f"{stats}"
    )

    average: int = sum(stats.values()) / len(stats)
    print(
        "Score average is "
        f"{average:.2f}"
    )

    high_scores: dict[str, int] = {}
    for name in stats:
        if (stats[name] > average):
            high_scores[name] = stats[name]

    print(
        f"High scores: {high_scores}"
    )


if __name__ == "__main__":
    main()
