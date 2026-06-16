def garden_operations(operation_number: int) -> None:
    if (operation_number == 0):
        int("abc")
    elif (operation_number == 1):
        42 / 0
    elif (operation_number == 2):
        open("/non/existent/file")
    elif (operation_number == 3):
        "hello" + 42  # type: ignore
    return


def test_operation(n: int) -> None:
    print(f"Testing operation {n}...")
    try:
        garden_operations(n)
        print("Operation completed successfully")
    except (
        ValueError, ZeroDivisionError,
        FileNotFoundError, TypeError
    ) as e:
        print(f"Caught {type(e).__name__}: {e}")


if __name__ == "__main__":
    print("=== Garden Error Types Demo ===")
    test_operation(0)
    test_operation(1)
    test_operation(2)
    test_operation(3)
    test_operation(4)
    print("\nAll error types tested successfully!")
