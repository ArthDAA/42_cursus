from .dark_spellbook import dark_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    allowed: list[str] = dark_spell_allowed_ingredients()
    lower: str = ingredients.lower()
    valid: bool = any(item in lower for item in allowed)
    keyword: str = "VALID" if valid else "INVALID"
    return f"{ingredients} - {keyword}"
