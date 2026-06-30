from abc import ABC, abstractmethod
from ex0.creatures import Creature
from ex1.capabilities import HealCapability, TransformCapability


class BattleStrategyError(Exception):
    pass


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: Creature) -> bool: ...

    @abstractmethod
    def act(self, creature: Creature) -> None: ...


class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> None:
        print(creature.attack())


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise BattleStrategyError(
                "Invalid Creature '"
                f"{creature._name}' for this aggressive strategy"
            )
        tc: TransformCapability = creature  # type: ignore[assignment]
        print(tc.transform())
        print(creature.attack())
        print(tc.revert())


class DefensiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise BattleStrategyError(
                "Invalid Creature '"
                f"{creature._name}' for this defensive strategy"
            )
        print(creature.attack())
        hc: HealCapability = creature  # type: ignore[assignment]
        print(hc.heal())
