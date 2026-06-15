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
    




















if __name__ == "__main__":
    main()