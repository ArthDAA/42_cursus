class GardenError(Exception):
    def __init__(
            self,
            message: str = "Unknown garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    def __init__(
            self,
            message: str = "Unknown plant error") -> None:
        super().__init__(message)


class WaterError(GardenError):
    def __init__(
            self,
            message: str = "Unknown water error") -> None:
        super().__init__(message)


def raise_plant_error() -> None:
    raise PlantError("The tomato plant is wilting!")


def raise_water_error() -> None:
    raise WaterError("Not enough water in the tank!")


def test_specific_errors() -> None:
    print("Testing PlantError...")
    try:
        raise_plant_error()
    except PlantError as e:
        print(f"Caught PlantError: {e}")
    print("\nTesting WaterError...")
    try:
        raise_water_error()
    except WaterError as e:
        print(f"Caught WaterError: {e}")


def test_catch_all() -> None:
    print("\nTesting catching all garden errors...")
    try:
        raise_plant_error()
    except GardenError as e:
        print(f"Caught GardenError: {e}")
    try:
        raise_water_error()
    except GardenError as e:
        print(f"Caught GardenError: {e}")


if __name__ == "__main__":
    print("=== Custom Garden Errors Demo ===\n")
    test_specific_errors()
    test_catch_all()
    print("\nAll custom error types work correctly!")
