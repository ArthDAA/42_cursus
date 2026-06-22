#!/usr/bin/env python3
from ex0 import FlameFactory, AquaFactory, CreatureFactory
from ex0.creatures import Creature


def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    base: Creature = factory.create_base()
    evolved: Creature = factory.create_evolved()
    print(base.describe())
    print(base.attack())
    print(evolved.describe())
    print(evolved.attack())


def test_battle(factory_a: CreatureFactory, factory_b: CreatureFactory) -> None:
    print("Testing battle")
    a: Creature = factory_a.create_base()
    b: Creature = factory_b.create_base()
    print(a.describe())
    print("vs.")
    print(b.describe())
    print("fight!")
    print(a.attack())
    print(b.attack())


if __name__ == "__main__":
    flame = FlameFactory()
    aqua = AquaFactory()

    test_factory(flame)
    print()
    test_factory(aqua)
    print()
    test_battle(flame, aqua)
