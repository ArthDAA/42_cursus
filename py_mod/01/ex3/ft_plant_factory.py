class Plant:
    def __init__(self, name: str, height: float, days: int) -> None:
        self.name = name
        self.height = height
        self.days = days
    def show(self) -> None:
        print(f"{self.name}: {self.height:.1f}cm, {self.days} days old")
    def grow(self) -> None:
        self.height += 0.8
    def age(self) -> None:
        self.days += 1

if __name__ == "__main__":
    rose = Plant("Rose", 25, 30)
    oak = Plant("Oak", 200, 365)
    cactus = Plant("Cactus", 5, 90)
    sunflower = Plant("Sunflower", 80, 45)
    fern = Plant("Fern", 15, 120)
    print("=== Plant Factory Output ===")
    print(f"Created: ", end = "")
    rose.show()
    print(f"Created: ", end = "")
    oak.show()
    print(f"Created: ", end = "")
    cactus.show()
    print(f"Created: ", end = "")
    sunflower.show()
    print(f"Created: ", end = "")
    fern.show()
