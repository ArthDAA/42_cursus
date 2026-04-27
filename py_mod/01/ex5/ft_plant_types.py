class Plant:
    def __init__(self, name: str, height: float, days: int,
                 growth_rate: float = 0.8) -> None:
        self._name = name
        self._height = height if height >= 0 else 0.0
        self._days = days if days >= 0 else 0
        self._growth_rate = growth_rate

    def show(self) -> None:
        print(f"{self._name}: {self._height:.1f}cm, {self._days} days old")

    def grow(self) -> None:
        self._height += self._growth_rate

    def age(self) -> None:
        self._days += 1

    def get_age(self) -> int:
        return (self._days)

    def get_height(self) -> float:
        return (self._height)

    def set_height(self, new_height: float) -> None:
        if (new_height < 0):
            print(f"{self._name}: Error, height can't be negative")
            print("Height update rejected")
        else:
            self._height = new_height
            print(f"Height updated: {self._height}cm")

    def set_age(self, new_age: int) -> None:
        if (new_age < 0):
            print(f"{self._name}: Error, age can't be negative")
            print("Age update rejected")
        else:
            self._days = new_age
            print(f"Age updated: {self._days} days")


class Flower(Plant):
    def __init__(self, name: str, height: float,
                 days: int, color: str) -> None:
        super().__init__(name, height, days)
        self._color = color
        self._blooming = False

    def _show(self) -> None:
        super().show()
        print(f" Color: {self._color}")

    def _bloom(self) -> None:
        self._blooming = True


class Tree(Plant):
    def __init__(self, name: str, height: float, days: int,
                 trunk_diameter: float) -> None:
        super().__init__(name, height, days)
        self._trunk_diameter = trunk_diameter

    def _show(self) -> None:
        super().show()
        print(f" Trunk diameter: {self._trunk_diameter:.1f}cm")

    def produce_shade(self) -> None:
        print(f"Tree {self._name} now produces a shade of "
              f"{self._height:.1f}cm long and "
              f"{self._trunk_diameter:.1f}cm wide.")


class Vegetable(Plant):
    def __init__(self, name: str, height: float, days: int,
                 harvest_season: str, growth_rate: float = 2.1) -> None:
        super().__init__(name, height, days, growth_rate)
        self._harvest_season = harvest_season
        self._nutritional_value = 0

    def _show(self) -> None:
        super().show()
        print(f" Harvest season: {self._harvest_season}")
        print(f" Nutritional value: {self._nutritional_value}")

    def grow(self) -> None:
        super().grow()
        self._nutritional_value += 1


if __name__ == "__main__":
    print("=== Garden Plant Types ===")
    rose = Flower("Rose", 15, 10, "red")
    oak = Tree("Oak", 200, 365, 5)
    tomato = Vegetable("Tomato", 5, 10, "April")
    print("=== Flower")
    rose._show()
    if (rose._blooming is False):
        print(f" {rose._name} has not bloomed yet")
        print(f"[asking the {rose._name.lower()} to bloom]")
        rose._bloom()
    rose._show()
    if (rose._blooming is True):
        print(f" {rose._name} is blooming beautifully!")

    print("\n=== Tree")
    oak._show()
    print(f"[asking the {oak._name.lower()} to produce shade]")
    oak.produce_shade()
    print("\n=== Vegetable")
    tomato._show()
    print(f"[make {tomato._name.lower()} grow and age for 20 days]")
    i = 0
    while (i != 20):
        tomato.grow()
        tomato.age()
        i += 1
    tomato._show()
