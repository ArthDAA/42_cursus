from alchemy.elements import create_air
from ..potions import strength_potion
import elements


def lead_to_gold() -> str:
    air: str = create_air()
    sp: str = strength_potion()
    fire: str = elements.create_fire()
    return (
        f"Recipe transmuting Lead to Gold: "
        f"brew '{air}' and '{sp}' mixed with '{fire}'"
    )
