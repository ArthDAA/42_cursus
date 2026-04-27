class Plant:
    def __init__(self, name: str, height: float, days: int) -> None:
        self._name = name
        self._height = height if height >= 0 else 0.0
        self._days = days if days >= 0 else 0.0
    def show(self) -> None:
        print(f"{self._name}: {self._height:.1f}cm, {self._days} days old")
    def grow(self) -> None:
        self._height += 0.8
    def age(self) -> None:
        self._days += 1
    def get_age(self) -> int:
        return(self._days)
    def get_height(self) -> float:
        return(self._height)
    def set_height(self, new_height: float) -> None:
        if (new_height < 0):
            print(f"{self._name}: Error, height can't be negative")
            print("Height update rejected")
        else:
            self._height = new_height
            print(f"Height updated: {self._height}cm")
    def set_age(self, new_age: int) -> None:
        if(new_age < 0):
            print(f"{self._name}: Error, age can't be negative")
            print("Age update rejected")
        else:
            self._days = new_age
            print(f"Age updated: {self._days} days")

if __name__ == "__main__":
    rose = Plant("Rose", 15, 10)
    print("=== Garden Security System ===")
    print("Plant created: ", end = "")
    rose.show()
    print("")
    rose.set_height(25)
    rose.set_age(30)
    print("")
    rose.set_height(-1)
    rose.set_age(-1)
    print("\nCurrent state: ", end = "")
    rose.show()
