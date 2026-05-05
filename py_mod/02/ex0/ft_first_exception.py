def input_temperature(temp_str: str) -> int:
	return int(temp_str)


def test_temperature(temp_str: str) -> None:
	print(f"Input data is '{temp_str}'")
	try:
		print(f"Temperature is now {input_temperature(temp_str)}°C\n")
	except Exception as e:
		print(f"Caught input_temperature error: {e}\n")

if __name__ == "__main__":
    print("=== Garden Temperature ===\n")
    test_temperature("25")
    test_temperature("abc")
    print("All tests completed - program didn't crash!")
