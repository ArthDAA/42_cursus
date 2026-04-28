class Plant:
    def __init__(self, name: str, height: float, days: int,
                 growth_rate: float = 0.8) -> None:
        self._name = name
        self._height = height if height >= 0 else 0.0
        self._days = days if days >= 0 else 0
        self._growth_rate = growth_rate
        self._stats = Plant._Stats()

    def show(self) -> None:
        print(f"{self._name}: {self._height:.1f}cm, {self._days} days old")
        self._stats._show_call += 1

    def grow(self) -> None:
        self._height = round(self._height + self._growth_rate, 1)
        self._stats._grow_call += 1

    def age(self, it: int = 1) -> None:
        self._days += it
        self._stats._age_call += 1

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

    class _Stats:
        def __init__(self) -> None:
            self._grow_call = 0
            self._age_call = 0
            self._show_call = 0

        def display(self) -> None:
            print(f"Stats: {self._grow_call} grow, "
                  f"{self._age_call} age, "
                  f"{self._show_call} show")

    @staticmethod
    def is_older_than_a_year(age: int) -> bool:
        return (age > 365)

    @classmethod
    def create_anonymous(cls) -> "Plant":
        return (cls("Unknown plant", 0.0, 0))


class Flower(Plant):
    def __init__(self, name: str, height: float,
                 days: int, color: str, growth_rate: float = 0.8) -> None:
        super().__init__(name, height, days, growth_rate)
        self._color = color
        self._blooming = False

    def show(self) -> None:
        super().show()
        print(f" Color: {self._color}")
        if (self._blooming is False):
            print(f" {self._name} has not bloomed yet")
        else:
            print(f" {self._name} is blooming beautifully!")

    def bloom(self) -> None:
        self._blooming = True


class Tree(Plant):
    def __init__(self, name: str, height: float, days: int,
                 trunk_diameter: float) -> None:
        super().__init__(name, height, days)
        self._trunk_diameter = trunk_diameter
        self._stats: Tree._TreeStats = Tree._TreeStats()

    def show(self) -> None:
        super().show()
        print(f" Trunk diameter: {self._trunk_diameter:.1f}cm")

    def produce_shade(self) -> None:
        print(f"Tree {self._name} now produces a shade of "
              f"{self._height:.1f}cm long and "
              f"{self._trunk_diameter:.1f}cm wide.")
        self._stats._shade_count += 1

    class _TreeStats(Plant._Stats):
        def __init__(self) -> None:
            super().__init__()
            self._shade_count = 0

        def display(self) -> None:
            super().display()
            print(f" {self._shade_count} shade")


class Vegetable(Plant):
    def __init__(self, name: str, height: float, days: int,
                 harvest_season: str, growth_rate: float = 0.8) -> None:
        super().__init__(name, height, days, growth_rate)
        self._harvest_season = harvest_season
        self._nutritional_value = 0

    def show(self) -> None:
        super().show()
        print(f" Harvest season: {self._harvest_season}")
        print(f" Nutritional value: {self._nutritional_value}")

    def grow(self) -> None:
        super().grow()
        self._nutritional_value += 1


class Seed(Flower):
    def __init__(self, name: str, height: float, days: int,
                 color: str, seeds: int, growth_rate: float = 0.8) -> None:
        super().__init__(name, height, days, color, growth_rate)
        self._seeds = seeds

    def show(self) -> None:
        super().show()
        print(f" Seeds: {self._seeds}")

    def bloom(self, new_seeds: int = 0) -> None:
        super().bloom()
        self._seeds = new_seeds


def display_stats(plant: Plant) -> None:
    print(f"[statistics for {plant._name}]")
    plant._stats.display()


if __name__ == "__main__":
    rose = Flower("Rose", 15, 10, "red", 8)
    oak = Tree("Oak", 200, 365, 5)
    sunflower = Seed("Sunflower", 80, 45, "yellow", 0, 30)
    print("=== Garden statistics ===")
    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> "
          f"{Plant.is_older_than_a_year(30)}")
    print(f"Is 400 days more than a year? -> "
          f"{Plant.is_older_than_a_year(400)}")
    print("\n=== Flower")
    rose.show()
    display_stats(rose)
    print("[asking the rose to grow and bloom]")
    rose.grow()
    rose.bloom()
    rose.show()
    display_stats(rose)
    print("\n=== Tree")
    oak.show()
    display_stats(oak)
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    display_stats(oak)
    print("\n=== Seed")
    sunflower.show()
    print("[make sunflower grow, age and bloom]")
    sunflower.grow()
    sunflower.age(20)
    sunflower.bloom(42)
    sunflower.show()
    display_stats(sunflower)
    print("\n=== Anonymous")
    john = Plant.create_anonymous()
    john.show()
    display_stats(john)
