#!/usr/bin/env python3
from ex0.creatures import Creature
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex1.capabilities import HealCapability, TransformCapability


if __name__ == "__main__":
    print("Testing Creature with healing capability")
    heal_factory = HealingCreatureFactory()

    base: Creature = heal_factory.create_base()
    print("base:")
    print(base.describe())
    print(base.attack())
    hb: HealCapability = base  # type: ignore[assignment]
    print(hb.heal())

    evolved: Creature = heal_factory.create_evolved()
    print("evolved:")
    print(evolved.describe())
    print(evolved.attack())
    he: HealCapability = evolved  # type: ignore[assignment]
    print(he.heal())

    print()
    print("Testing Creature with transform capability")
    transform_factory = TransformCreatureFactory()

    base2: Creature = transform_factory.create_base()
    print("base:")
    print(base2.describe())
    print(base2.attack())
    tb: TransformCapability = base2  # type: ignore[assignment]
    print(tb.transform())
    print(base2.attack())
    print(tb.revert())

    evolved2: Creature = transform_factory.create_evolved()
    print("evolved:")
    print(evolved2.describe())
    print(evolved2.attack())
    te: TransformCapability = evolved2  # type: ignore[assignment]
    print(te.transform())
    print(evolved2.attack())
    print(te.revert())
