#!/usr/bin/env python3
from ex0 import FlameFactory, AquaFactory, CreatureFactory
from ex0.creatures import Creature
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    BattleStrategy,
    NormalStrategy,
    AggressiveStrategy,
    DefensiveStrategy,
    BattleStrategyError,
)

Opponent = tuple[CreatureFactory, BattleStrategy]


def battle(opponents: list[Opponent]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    creatures: list[tuple[Creature, BattleStrategy]] = [
        (factory.create_base(), strategy)
        for factory, strategy in opponents
    ]

    for i in range(len(creatures)):
        for j in range(i + 1, len(creatures)):
            creature_a, strategy_a = creatures[i]
            creature_b, strategy_b = creatures[j]
            print()
            print("* Battle *")
            print(creature_a.describe())
            print("vs.")
            print(creature_b.describe())
            print("now fight!")
            try:
                strategy_a.act(creature_a)
                strategy_b.act(creature_b)
            except BattleStrategyError as e:
                print(f"Battle error, aborting tournament: {e}")
                return


if __name__ == "__main__":
    flame = FlameFactory()
    aqua = AquaFactory()
    heal = HealingCreatureFactory()
    transform = TransformCreatureFactory()

    normal = NormalStrategy()
    aggressive = AggressiveStrategy()
    defensive = DefensiveStrategy()

    print("Tournament 0 (basic)")
    print("[ (Flameling+Normal), (Healing+Defensive) ]")
    battle([(flame, normal), (heal, defensive)])

    print()
    print("Tournament 1 (error)")
    print("[ (Flameling+Aggressive), (Healing+Defensive) ]")
    battle([(flame, aggressive), (heal, defensive)])

    print()
    print("Tournament 2 (multiple)")
    print("[ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]")
    battle([(aqua, normal), (heal, defensive), (transform, aggressive)])
