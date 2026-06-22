_ALLOWED: list[str] = ["earth", "air", "fire", "water"]


def validate_ingredients(ingredients: str) -> str:
    lower: str = ingredients.lower()
    valid: bool = any(item in lower for item in _ALLOWED)
    keyword: str = "VALID" if valid else "INVALID"
    return f"{ingredients} - {keyword}"
