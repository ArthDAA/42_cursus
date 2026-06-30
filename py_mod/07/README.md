# Module 07 — Patterns de conception (Abstract Factory, Interfaces, Strategy)

> *DataDeck — Abstract Card Architecture*

Ce module ne porte pas sur une nouvelle syntaxe : il porte sur **l'architecture**. Tu connais déjà les classes abstraites et le polymorphisme (py_05) ; ici on les utilise comme briques pour construire trois *design patterns* classiques, chacun résolvant un problème d'extensibilité différent :

1. **Abstract Factory** (ex0) — créer des familles d'objets sans coupler le code aux classes concrètes.
2. **Interfaces / héritage multiple** (ex1) — ajouter des capacités orthogonales à un objet sans toucher sa hiérarchie principale.
3. **Strategy** (ex2) — injecter un comportement comme objet, pour que le code client n'ait pas à connaître chaque cas.

Le fil rouge des trois : le **principe Ouvert/Fermé** — un système ouvert à l'extension (ajouter des classes) mais fermé à la modification (ne pas réécrire le code existant). C'est ce que le sujet appelle « penser comme un architecte senior ».

---

## 0. La fondation : les classes abstraites comme contrats

Avant les patterns, le socle. Une classe abstraite (ABC) définit un **contrat** : « toute classe concrète qui hérite de moi *doit* implémenter ces méthodes ».

```python
from abc import ABC, abstractmethod


class Creature(ABC):
    def __init__(self, name: str, creature_type: str) -> None:
        self.name = name
        self.creature_type = creature_type

    @abstractmethod
    def attack(self) -> str:
        ...

    def describe(self) -> str:
        return f"{self.name} is a {self.creature_type} type Creature"
```

Deux points décisifs ici :

- **`@abstractmethod` rend l'instanciation impossible tant qu'elle n'est pas implémentée.** `Creature()` lève `TypeError: Can't instantiate abstract class Creature with abstract method attack`. Le contrat est vérifié par Python, pas par convention.
- **Abstrait et concret cohabitent.** `attack` est abstraite (chaque créature l'implémente à sa façon) ; `describe` est concrète (logique partagée, écrite une fois dans la base). C'est la force des ABC vs une simple interface : factoriser le commun *et* imposer le variable.

### Le frame C

Si tu viens du C, une ABC avec `@abstractmethod`, c'est exactement une **interface / méthode virtuelle pure**. En C tu l'émulerais avec une **struct de pointeurs de fonction** (une vtable) : la struct déclare les slots (`attack`, `describe`), et chaque « type » remplit les pointeurs. La classe abstraite Python fait pareil, mais le compilateur/runtime garantit que tu ne peux pas instancier une struct dont un pointeur obligatoire est `NULL`. Le polymorphisme qui suit (appeler `creature.attack()` sans connaître le type concret) = déréférencer le pointeur de fonction de la vtable. Garde cette image : les trois patterns ne sont que des manières d'organiser ces vtables.

```python
class Flameling(Creature):
    def __init__(self) -> None:
        super().__init__("Flameling", "Fire")

    def attack(self) -> str:
        return f"{self.name} uses Ember!"
```

---

## 1. Pattern I — Abstract Factory (ex0)

### Le problème

Tu veux créer des milliers de types de cartes regroupées en **familles** (Feu, Eau…), chacune avec une forme de base et une forme évoluée. Si `battle.py` fait `Flameling()`, `Pyrodon()`, etc. en dur, il est couplé à chaque classe concrète : ajouter une famille = modifier le code client partout. Mauvais.

### La structure

Une **factory abstraite** déclare *comment* créer une famille (méthodes abstraites) ; chaque **factory concrète** sait créer *une* famille précise.

```python
from abc import ABC, abstractmethod

from .creature import Creature
from .flame import Flameling, Pyrodon


class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> Creature:
        ...

    @abstractmethod
    def create_evolved(self) -> Creature:
        ...


class FlameFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Flameling()

    def create_evolved(self) -> Creature:
        return Pyrodon()
```

Le code client ne connaît que l'interface `CreatureFactory`. On lui passe une factory, il produit une famille cohérente, sans jamais nommer `Flameling` :

```python
def test_factory(factory: CreatureFactory) -> None:
    for creature in (factory.create_base(), factory.create_evolved()):
        print(creature.describe())
        print(creature.attack())
```

Ajouter une famille Plante ? Tu écris `PlantFactory(CreatureFactory)`. `test_factory` ne change pas d'une ligne. **Ouvert/Fermé en action.**

### L'encapsulation par le package

Le sujet impose : *« your ex0 package cannot expose concrete Creature directly, it must only expose factories »*. C'est la leçon du module 06 qui revient — `__init__.py` est une vitrine curatée :

```python
from .factory import CreatureFactory, FlameFactory, AquaFactory

__all__ = ["CreatureFactory", "FlameFactory", "AquaFactory"]
```

`Flameling`, `Pyrodon`, etc. ne sont **pas** dans `__all__`. Depuis l'extérieur, impossible de les instancier directement : la seule porte d'entrée est la factory. L'architecture *force* le bon usage au lieu de l'espérer.

> Nuance de défense : exposer la classe **abstraite** `CreatureFactory` (pour typer le paramètre) ne viole pas la règle — c'est le contrat, pas un produit concret. Et si un autre package a besoin du type `Creature` pour une annotation, il peut faire `from ex0.creature import Creature` : un import direct ignore `__all__` (qui ne contrôle que `import *`). La vitrine publique reste « factories only », l'accès interne reste possible.

### Factory Method vs Abstract Factory

Question piège classique : la différence ? Une *factory method* a **une** méthode de création (la sous-classe choisit le produit). Une *abstract factory* a **plusieurs** méthodes produisant une **famille** cohérente de produits liés. Ici `create_base` **et** `create_evolved` → c'est bien une abstract factory.

---

## 2. Pattern II — Interfaces et héritage multiple (ex1)

### Le problème

On veut ajouter des capacités (soigner, se transformer). Mais — point clé du sujet — *« capability abstract classes will not inherit from the Creature base class »*. Pourquoi ? Parce qu'une capacité de soin n'est **pas** propre aux créatures : un jour un objet, un sort, un terrain pourraient aussi soigner. On garde les capacités **orthogonales** à la hiérarchie Creature.

### La solution : interface + mixin via héritage multiple

Une capacité est une ABC indépendante. Une créature concrète hérite de **Creature ET d'une capacité** : elle *est* une créature et *possède* une capacité.

```python
from abc import ABC, abstractmethod


class HealCapability(ABC):
    @abstractmethod
    def heal(self) -> str:
        ...


class TransformCapability(ABC):
    @abstractmethod
    def transform(self) -> str:
        ...

    @abstractmethod
    def revert(self) -> str:
        ...
```

`TransformCapability` introduit un **état persistant** qui modifie le comportement de `attack`. C'est la combinaison capacité + état :

```python
class Shiftling(Creature, TransformCapability):
    def __init__(self) -> None:
        Creature.__init__(self, "Shiftling", "Normal")
        self.transformed = False

    def attack(self) -> str:
        if self.transformed:
            return f"{self.name} performs a boosted strike!"
        return f"{self.name} attacks normally."

    def transform(self) -> str:
        self.transformed = True
        return f"{self.name} shifts into a sharper form!"

    def revert(self) -> str:
        self.transformed = False
        return f"{self.name} returns to normal."
```

L'attribut `transformed` survit entre les appels : `attack` → normal, puis `transform`, puis `attack` → coup boosté, puis `revert`. Le comportement dépend de l'état interne, pas d'un paramètre.

Et les nouvelles familles passent par des factories qui héritent de **ex0** :

```python
class HealingCreatureFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Sproutling()

    def create_evolved(self) -> Creature:
        return Bloomelle()
```

> Continuité 06↔07 : ex1 **importe** depuis ex0 (`from ex0 import CreatureFactory`). C'est un import inter-package — exactement les chemins absolus du module précédent. Le sujet l'exige : *« use the content of ex0 and build upon it »*.

### `is-a` vs `has-a`, revisité

`Sproutling(Creature, HealCapability)` : Sproutling **EST** une Creature (relation d'héritage classique) **ET** une HealCapability (interface implémentée). L'héritage multiple ici n'est pas « hériter de deux parents pour réutiliser du code », c'est « être d'un type principal + remplir un ou plusieurs contrats ». C'est le sens propre d'un *mixin / interface*, pas du fourre-tout.

### Le MRO : ce qu'il faut savoir pour la défense

Avec `class Shiftling(Creature, TransformCapability)`, Python construit un **MRO** (Method Resolution Order) par linéarisation C3 :

```
Shiftling -> Creature -> TransformCapability -> ABC -> object
```

Trois choses à savoir expliquer :

- **Pas de conflit de métaclasse.** `Creature` et les capacités utilisent toutes `ABCMeta` (via `ABC`). Métaclasses compatibles → l'héritage multiple passe. Si tu mélangeais deux ABC avec des métaclasses incompatibles, tu aurais une `TypeError: metaclass conflict`.
- **`super().__init__()` ne remonte qu'un seul cran.** Dans une chaîne d'héritage multiple, `super().__init__()` appelle le **suivant dans le MRO**, pas tous les parents. Pour une vraie coopération il faudrait que *chaque* classe appelle `super().__init__()` et accepte `**kwargs`. Ici les deux hiérarchies sont indépendantes : j'appelle **explicitement** `Creature.__init__(self, ...)`. C'est sans ambiguïté et correct. (Si `TransformCapability` avait son propre `__init__` à état, je l'appellerais aussi explicitement.)
- **Pas de problème du diamant** ici : `Creature` et `TransformCapability` ne partagent que `ABC`/`object`. Le diamant n'apparaît que si deux parents ont un ancêtre commun *intermédiaire* ; le MRO le résout, mais sache nommer le concept.

---

## 3. Pattern III — Strategy (ex2)

### Le problème

Maintenant le tournoi : des créatures de familles variées s'affrontent, chacune se bat différemment (soigne après, ou transforme-attaque-revert). La tentation : un gros `if isinstance(...): ... elif ...` dans le tournoi. **C'est exactement ce qu'il faut éviter** — ça viole Ouvert/Fermé (chaque nouvelle capacité = modifier le tournoi).

### La solution : le comportement devient un objet

On encapsule chaque manière de combattre dans une **stratégie**. Le tournoi ne connaît plus les capacités : il délègue à `strategy.act(creature)`.

```python
from abc import ABC, abstractmethod

from ex0.creature import Creature


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        ...

    @abstractmethod
    def act(self, creature: Creature) -> None:
        ...
```

Deux méthodes, deux rôles : `is_valid` dit *si* la stratégie convient à une créature ; `act` exécute le combat (et refuse si le couple est invalide).

```python
class InvalidStrategyError(Exception):
    pass


class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> None:
        print(creature.attack())


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> None:
        if not isinstance(creature, TransformCapability):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}' "
                f"for this aggressive strategy"
            )
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())
```

### Le pont entre ex1 et ex2 : `isinstance` sur l'interface

Comment une stratégie sait-elle si une créature lui convient ? **Elle teste l'interface, pas la classe concrète** : `isinstance(creature, TransformCapability)`. C'est précisément à quoi servent les capacités-interfaces de l'ex1 — elles deviennent le critère de validité. `AggressiveStrategy` ↔ `TransformCapability`, `DefensiveStrategy` ↔ `HealCapability`, `NormalStrategy` ↔ tout le monde. Les deux patterns se branchent ici.

### Capacité (ex1) vs Stratégie (ex2) — la distinction à maîtriser

C'est *la* question de défense de ce module. Même si les deux décrivent du « comportement », ils sont opposés :

| | Capacité (ex1) | Stratégie (ex2) |
|---|---|---|
| Nature | Intrinsèque à la créature | Extrinsèque, injectée de l'extérieur |
| Mécanisme | Héritage (`is-a` / interface) | Composition (objet passé à côté) |
| Réponse à | « Que **peut** faire cette créature ? » | « **Comment** l'utiliser dans ce combat ? » |
| Couplage | Fixé à la création de la classe | Choisi à l'exécution, échangeable |

Une même créature transformante peut être jouée avec une `NormalStrategy` (juste attaquer) ou une `AggressiveStrategy` (transformer-attaquer-revert). La capacité est ce qu'elle a ; la stratégie est comment on s'en sert. **Composition over inheritance** : le comportement variable est un objet branché, pas une sous-classe de plus.

### Le tournoi délègue, point

```python
def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    roster = [(factory.create_base(), strategy)
              for factory, strategy in opponents]
    for index, (creature, strategy) in enumerate(roster):
        for other, other_strategy in roster[index + 1:]:
            run_fight(creature, strategy, other, other_strategy)
```

`run_fight` se contente d'appeler `strategy.act(creature)` de chaque côté, en attrapant `InvalidStrategyError` pour interrompre proprement (cf. *« Battle error, aborting tournament »* dans l'exemple). Le tournoi n'a **aucune** connaissance de heal/transform. Ajoute une `BerserkStrategy` demain : zéro ligne touchée dans `battle`.

---

## 4. Les mécanismes Python en coulisses

### `abc` : `ABC` et `@abstractmethod`

`ABC` est une classe de base dont la métaclasse est `ABCMeta`. Le décorateur `@abstractmethod` marque une méthode comme obligatoire : `ABCMeta` empêche l'instanciation tant qu'une méthode abstraite n'est pas redéfinie. C'est un contrat **vérifié à l'instanciation**, pas à la déclaration.

### Le piège mypy de l'héritage multiple

Subtil mais important (le module exige mypy). Après `if not isinstance(creature, TransformCapability): raise`, mypy **réduit** `creature` au type `TransformCapability` — qui a `transform`/`revert` mais **pas** `name`/`attack` (définis sur `Creature`). Or à l'exécution la créature est bien les deux. Python n'a pas de type « intersection » natif (`Creature & TransformCapability`). La solution propre pour mypy : déclarer un `Protocol` qui réunit ce que la stratégie utilise.

```python
from typing import Protocol


class Transformable(Protocol):
    name: str

    def attack(self) -> str: ...
    def transform(self) -> str: ...
    def revert(self) -> str: ...
```

Tu annotes alors la variable réduite comme `Transformable` (typage structurel : « tout objet qui a ces membres »), et mypy est content sans rien casser au runtime. Sache au moins **expliquer pourquoi** le typage coince — c'est typiquement creusé en défense.

### `isinstance` vs duck typing

Deux façons de tester une capacité : `isinstance(creature, HealCapability)` (vérifie le type / l'interface déclarée) ou `hasattr(creature, "heal")` (duck typing : « si ça sait soigner, c'est bon »). Ici `isinstance` est préférable : les capacités sont des **interfaces explicites**, l'intention est claire et mypy la comprend. Le duck typing est plus souple mais moins lisible et invérifiable statiquement.

### Exceptions personnalisées

`InvalidStrategyError(Exception)` donne un type d'erreur **dédié** : le tournoi peut l'attraper spécifiquement (`except InvalidStrategyError`) sans masquer d'autres bugs. Le sujet demande de gérer les erreurs *gracefully* — une exception métier nommée vaut mieux qu'un `Exception` générique ou un `return None` silencieux.

---

## 5. Le fil rouge : trois leviers de flexibilité

Les trois patterns répondent au même besoin — **faire évoluer le système sans le casser** — mais sur trois axes différents :

- **Abstract Factory** → flexibilité de la **création**. *Quoi* instancier, décidé par une factory interchangeable.
- **Interfaces / mixins** → flexibilité des **capacités**. *Ce qu'un objet sait faire*, composé via héritage multiple.
- **Strategy** → flexibilité du **comportement**. *Comment un objet est utilisé*, injecté comme objet à l'exécution.

Principes SOLID en jeu, à citer en défense :

- **Open/Closed** (le cœur) : on étend par de nouvelles classes, jamais en modifiant l'existant.
- **Dependency Inversion** : le code client dépend des abstractions (`CreatureFactory`, `BattleStrategy`), pas des classes concrètes.
- **Interface Segregation** : des capacités petites et ciblées (`HealCapability`, `TransformCapability`) plutôt qu'une grosse classe Creature qui sait tout faire.
- **Separation of Concerns** : création / capacité / comportement vivent dans des hiérarchies séparées.

---

## 6. Préparation à la défense

*« You may be asked to explain the design patterns explored in this project. Focus on understanding the concepts, not just the implementation. »* Réponses prêtes :

**Q : Qu'est-ce qu'une classe abstraite et que garantit `@abstractmethod` ?**
Une classe-contrat non instanciable. `@abstractmethod` force toute sous-classe concrète à implémenter la méthode ; sinon `TypeError` à l'instanciation. Et abstrait + concret cohabitent (`attack` abstraite, `describe` concrète).

**Q : Pourquoi un abstract factory plutôt que `Flameling()` en dur ?**
Pour découpler la création de l'usage. Le client manipule `CreatureFactory` ; ajouter une famille = ajouter une factory, sans toucher au client. Et le package n'expose que les factories : impossible d'instancier une créature concrète par erreur.

**Q : Pourquoi les capacités n'héritent pas de Creature ?**
Parce qu'elles sont orthogonales : soigner/transformer pourrait un jour s'appliquer à autre chose qu'une créature. On les garde comme interfaces indépendantes, et une créature concrète les implémente par héritage multiple.

**Q : Différence entre une capacité et une stratégie ?**
La capacité est **intrinsèque** (ce que la créature *est/a*, par héritage) ; la stratégie est **extrinsèque** (comment on l'*utilise*, injectée par composition, échangeable à l'exécution). Une même créature peut tourner avec plusieurs stratégies.

**Q : Pourquoi Strategy plutôt qu'un `if/elif` sur le type dans le tournoi ?**
Le `if/elif` viole Ouvert/Fermé : chaque nouvelle capacité oblige à rouvrir le tournoi. Avec Strategy, le tournoi appelle `strategy.act(creature)` et ignore les détails ; une nouvelle stratégie = une nouvelle classe, zéro modification du tournoi.

**Q : Comment `is_valid` sait-il qu'une créature convient ?**
Par `isinstance(creature, CapabilityInterface)` : la stratégie teste l'**interface** (ex1), pas la classe concrète. C'est le point de jonction entre les deux patterns.

**Q : C'est quoi le MRO, et que se passe-t-il avec `class X(Creature, HealCapability)` ?**
L'ordre de résolution des méthodes par linéarisation C3 : `X → Creature → HealCapability → ABC → object`. Détermine quelle méthode/`super()` est appelée. Pas de conflit de métaclasse (toutes en `ABCMeta`). `super().__init__()` ne remonte qu'au suivant du MRO, d'où l'appel explicite des `__init__` parents ici.

**Q : Quel principe relie les trois patterns ?**
Ouvert/Fermé : étendre par ajout de classes (factories, capacités, stratégies), sans modifier le code existant.

---

## 7. Carte exercices → notions

| Exercice / script | Notion démontrée |
|---|---|
| `ex0` / `battle.py` | **Abstract Factory** : familles d'objets via une interface ; package qui n'expose que les factories ; polymorphisme sur `CreatureFactory` |
| `ex1` / `capacitor.py` | **Interfaces + héritage multiple** : capacités orthogonales (`heal`, `transform`), état persistant qui modifie `attack`, MRO, `is-a`/`has-a` ; réutilisation de ex0 (import inter-package) |
| `ex2` / `tournament.py` | **Strategy** : comportement de combat encapsulé en objet injecté, `is_valid`/`act`, `isinstance` sur l'interface comme critère, exception dédiée sur couple invalide |

---

## Les trois patterns en une phrase

1. **Abstract Factory** : une interface de création produit des familles d'objets cohérentes ; on échange la factory, pas le code client.
2. **Interfaces / héritage multiple** : une créature *est* d'un type et *implémente* des capacités-contrats indépendantes, branchées par héritage multiple.
3. **Strategy** : le comportement variable devient un objet injecté de l'extérieur, pour que le code client reste aveugle aux cas particuliers.

Et le tout sert une seule idée : **un système qui grandit par ajout, jamais par réécriture.**
