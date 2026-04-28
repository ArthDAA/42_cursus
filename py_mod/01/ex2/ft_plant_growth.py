class Plant:
    def __init__(self) -> None:
        self.name: str = ""
        self.height: float = 0.0
        self.days: int = 0
        self.def_height: float = 0.0

    def show(self) -> None:
        print(f"{self.name}: {self.height:.1f}cm, {self.days} days old")

    def grow(self) -> None:
        self.height += 0.8

    def age(self) -> None:
        self.days += 1


if __name__ == "__main__":
    rose = Plant()
    rose.name = "Rose"
    rose.height = 25
    rose.days = 30
    rose.def_height = rose.height
    days = 1
    print("=== Garden Plant Growth ===")
    rose.show()
    while (days <= 7):
        print(f"=== Day {days} ===")
        rose.grow()
        rose.age()
        days += 1
        rose.show()
    print(f"Growth this week: {rose.height - rose.def_height:.1f}cm")
