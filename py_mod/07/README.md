# Module 07 — DataDeck : Patterns de conception orientés objet

---

## 🎯 Objectif

Construire un système de combat de créatures en appliquant trois design patterns : **Abstract Factory** pour créer des familles de créatures cohérentes, **Capabilities** (Mixin) pour greffer des aptitudes optionnelles sur des créatures existantes via l'héritage multiple, et **Strategy** pour choisir un comportement de combat à l'exécution sans toucher aux créatures. Les trois exercices s'emboîtent — les classes des exercices précédents sont réutilisées directement.

---

## 🏗️ Architecture

```
ex0/
├── creatures.py   → Creature (ABC), Flameling, Pyrodon, Aquabub, Torragon
├── factories.py   → CreatureFactory (ABC), FlameFactory, AquaFactory
└── __init__.py    → expose FlameFactory, AquaFactory uniquement

ex1/
├── capabilities.py → HealCapability (ABC), TransformCapability (ABC)
├── creatures.py    → Sproutling, Bloomelle (Heal), Shiftling, Morphagon (Transform)
├── factories.py    → HealingCreatureFactory, TransformCreatureFactory
└── __init__.py     → expose les factories + HealCapability, TransformCapability

ex2/
├── strategies.py   → BattleStrategy (ABC), NormalStrategy, AggressiveStrategy,
│                     DefensiveStrategy, BattleStrategyError
└── __init__.py

battle.py      → teste ex0 : factories et créatures de base
capacitor.py   → teste ex1 : capabilities sur les créatures
tournament.py  → teste ex2 : stratégies appliquées au tournoi
```

---

## ⚙️ Exercice par exercice

### Ex0 — `creatures.py` et `factories.py` : Abstract Factory

`Creature` est une classe abstraite qui impose un contrat minimal : toute créature doit avoir un nom, un type, et une méthode `attack()`. `CreatureFactory` est une classe abstraite qui impose à chaque factory de pouvoir produire une créature de base et une créature évoluée. `FlameFactory` et `AquaFactory` implémentent ce contrat et créent chacune leur famille cohérente.

`battle.py` reçoit une `CreatureFactory` et crée des créatures sans jamais connaître leur type concret. Changer la factory change la famille entière.

**Comment ça marche :**

```python
class Creature(ABC):
    def __init__(self, name: str, creature_type: str) -> None:
        self._name: str = name
        self._type: str = creature_type

    @abstractmethod
    def attack(self) -> str: ...

    def describe(self) -> str:   # méthode concrète, partagée par tous
        return f"{self._name} is a {self._type} type Creature"
```

`describe()` est concrète dans `Creature` — toutes les créatures l'héritent directement. `attack()` est abstraite — chaque créature concrète doit fournir sa propre version.

> **Abstract Factory** — Le pattern résout le problème de la cohérence de famille. Sans factory, on pourrait accidentellement créer un `Flameling` avec un `Torragon` évolué. Avec `FlameFactory`, les deux créatures produites sont garanties d'appartenir à la même famille feu.

```python
class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> Creature: ...
    @abstractmethod
    def create_evolved(self) -> Creature: ...

class FlameFactory(CreatureFactory):
    def create_base(self) -> Creature: return Flameling()
    def create_evolved(self) -> Creature: return Pyrodon()
```

`__init__.py` n'expose que les factories — pas les créatures concrètes. Le code client crée des créatures uniquement via les factories, sans jamais importer `Flameling` ou `Aquabub` directement.

---

### Ex1 — `capabilities.py` et `creatures.py` : Capabilities (Mixin)

`HealCapability` et `TransformCapability` sont des classes abstraites qui représentent des **aptitudes**, pas des entités. Elles ne correspondent à rien dans le monde du jeu — elles expriment "peut faire X". `Sproutling` et `Bloomelle` sont des créatures herbacées qui peuvent se soigner. `Shiftling` et `Morphagon` sont des créatures qui peuvent se transformer.

`capacitor.py` reçoit les créatures depuis des factories, puis les downcast vers leur capability pour appeler `heal()` ou `transform()`.

**Comment ça marche :**

> **Héritage multiple** — En Python, une classe peut hériter de plusieurs parents. `class Shiftling(Creature, TransformCapability):` hérite des attributs et méthodes des deux.

```python
class Shiftling(Creature, TransformCapability):
    def __init__(self) -> None:
        Creature.__init__(self, "Shiftling", "Normal")
        TransformCapability.__init__(self)   # initialise self._transformed
```

On appelle les `__init__` **explicitement** (sans `super()`) parce que les deux parents ont des `__init__` distincts avec des signatures différentes. `Creature.__init__` a besoin de `name` et `type`. `TransformCapability.__init__` initialise `_transformed`. L'appel explicite garantit que les deux sont appelés dans l'ordre voulu.

> **MRO (Method Resolution Order)** — Python calcule un ordre linéaire pour résoudre les méthodes en héritage multiple (algorithme C3). `Shiftling.__mro__` serait `[Shiftling, Creature, TransformCapability, ABC, object]`. Quand on appelle une méthode, Python la cherche dans cet ordre et s'arrête au premier qui la définit.

`Shiftling.attack()` vérifie `self._transformed` — attribut initialisé par `TransformCapability.__init__` — pour varier son message selon l'état. Cet état est partagé entre `attack()` (définie dans `Shiftling`) et `transform()`/`revert()` (dont la signature est imposée par `TransformCapability`).

`capacitor.py` fait un downcast typé pour appeler les capabilities :

```python
tb: TransformCapability = base2  # type: ignore[assignment]
print(tb.transform())
```

`base2` est de type `Creature` (retourné par la factory), mais on sait à l'exécution que c'est un `Shiftling` avec `TransformCapability`. Le `type: ignore` dit à mypy d'accepter cette assertion.

---

### Ex2 — `strategies.py` : Strategy Pattern

`BattleStrategy` est une classe abstraite avec deux méthodes : `is_valid` (la créature supporte-t-elle cette stratégie ?) et `act` (exécute la stratégie). `NormalStrategy` convient à toutes les créatures. `AggressiveStrategy` nécessite `TransformCapability`. `DefensiveStrategy` nécessite `HealCapability`. Si on applique une stratégie incompatible, `BattleStrategyError` est levée.

`tournament.py` combine les exercices précédents : des créatures créées par les factories d'ex0 et ex1, avec des stratégies d'ex2, s'affrontent. Si une stratégie est incompatible, le tournoi s'interrompt proprement.

**Comment ça marche :**

> **`isinstance()` pour tester une capability** — `isinstance(creature, TransformCapability)` retourne `True` si la créature hérite de `TransformCapability`, peu importe son type principal. C'est la vérification runtime des mixins.

```python
class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise BattleStrategyError(
                f"Invalid Creature '{creature._name}' for this aggressive strategy"
            )
        tc: TransformCapability = creature  # type: ignore[assignment]
        print(tc.transform())
        print(creature.attack())
        print(tc.revert())
```

`AggressiveStrategy` d'abord vérifie, puis downcast pour accéder à `transform()` et `revert()`. Un `Flameling` (sans `TransformCapability`) fait lever `BattleStrategyError` immédiatement.

> **Strategy Pattern** — Encapsule un algorithme dans un objet. Le code de combat ne connaît que `BattleStrategy` — changer la stratégie passée change le comportement sans modifier ni la créature ni le code de tournoi.

`tournament.py` illustre les trois scénarios : tournoi normal (toutes stratégies compatibles), tournoi avec erreur (Flameling + AggressiveStrategy → interrompu), et tournoi mixte (plusieurs créatures et stratégies différentes).

---

## 🚀 Comment tester

```bash
cd module_07

python3 battle.py
# Flameling uses Ember!
# Aquabub uses Water Gun!
# (battle entre les deux)

python3 capacitor.py
# Sproutling heals itself for a small amount
# Shiftling shifts into a sharper form!
# Shiftling performs a boosted strike!
# Shiftling returns to normal.

python3 tournament.py
# Tournament 0 (basic) → fonctionne
# Tournament 1 (error) → BattleStrategyError : Flameling incompatible avec AggressiveStrategy
# Tournament 2 (multiple) → 3 créatures, stratégies mixtes
```
