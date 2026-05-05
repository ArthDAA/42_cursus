class InvalidTemperatureError(ValueError):
	pass

class OverTemperatureError(ValueError):
	pass

class UnderTemperatureError(ValueError):
	pass


def input_temperature(temp_str: str) -> int:
	try:
		temp = int(temp_str)
	except ValueError:
		raise InvalidTemperatureError(f"invalid literal for int() with base 10: '{temp_str}'")
	if (temp >= 40):
		raise OverTemperatureError(f"{temp}°C is too hot for plants (max 40°C)")
	if (temp <= 0):
		raise UnderTemperatureError(f"{temp}°C is too cold for pants (min 0°C)")
	return temp


def test_temperature(temp_str: str) -> None:
	print(f"Input data is '{temp_str}'")
	try:
		print(f"Temperature is now {input_temperature(temp_str)}°C\n")
	except (InvalidTemperatureError, OverTemperatureError, UnderTemperatureError) as e:
		print(f"Caught input_temperature error: {e}\n")


if __name__ == "__main__":
	print("=== Garden Temperature ===\n")
	test_temperature("25")
	test_temperature("abc")
	test_temperature("100")
	test_temperature("-50")
	print("All tests completed - program didn't crash!")
