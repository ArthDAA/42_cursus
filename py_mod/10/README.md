# Module 10 — FuncMage : Programmation fonctionnelle

---

## 🎯 Objectif

Explorer la programmation fonctionnelle en Python : fonctions lambda, fonctions d'ordre supérieur, fermetures et état capturé, module `functools`, et décorateurs. Les cinq exercices sont indépendants — chacun explore un aspect différent. Un générateur de données de test interactif accompagne le tout.

---

## 🏗️ Architecture

| Fichier | Notion principale |
|---------|------------------|
| `ex0/lambda_spells.py` | `lambda`, `sorted`, `filter`, `map`, `max`, `min` |
| `ex1/higher_magic.py` | Fonctions d'ordre supérieur, `Callable`, composition |
| `ex2/scope_mysteries.py` | Fermetures, `nonlocal`, état partagé entre closures |
| `ex3/functools_artifacts.py` | `reduce`, `partial`, `lru_cache`, `singledispatch` |
| `ex4/decorator_mastery.py` | Décorateurs, `@wraps`, décorateur paramétré, méthode décorée |
| `data_generator.py` | Utility class `@classmethod`, menu interactif |

---

## ⚙️ Exercice par exercice

### Ex0 — `lambda_spells.py` : Lambda et fonctions built-in

Quatre fonctions utilitaires sur des listes de mages et d'artefacts. Toutes utilisent des lambdas comme argument à des fonctions built-in — pas de boucle `for` explicite, pas d'accumulateur.

**Comment ça marche :**

> **`lambda`** — Fonction anonyme d'une seule expression. `lambda a: a["power"]` est équivalent à `def f(a): return a["power"]`. Idéale pour passer une logique simple comme argument sans définir une fonction nommée.

`artifact_sorter` trie par puissance décroissante :

```python
def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda a: a["power"], reverse=True)
```

`sorted(iterable, key=func)` crée une nouvelle liste triée. `key` est une fonction appelée sur chaque élément pour extraire la valeur de comparaison. `reverse=True` inverse l'ordre.

`power_filter` filtre les mages au-dessus d'un seuil :

```python
def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda m: m["power"] >= min_power, mages))
```

> **`filter(func, iterable)`** — Retourne un itérateur lazy qui ne garde que les éléments pour lesquels `func` retourne `True`. `list(...)` le matérialise en liste.

`spell_transformer` préfixe et suffixe chaque spell avec `*` :

```python
def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda s: f"* {s} *", spells))
```

> **`map(func, iterable)`** — Retourne un itérateur lazy qui applique `func` à chaque élément. Lazy comme `filter` — à matérialiser avec `list()`.

`mage_stats` combine `max`, `min` et `sum` avec des lambdas pour extraire des statistiques sans boucle explicite :

```python
max_power: int = max(mages, key=lambda m: m["power"])["power"]
avg: float = round(sum(map(lambda m: m["power"], mages)) / len(mages), 2)
```

`max(mages, key=...)` retourne le **dict** du mage le plus puissant. `["power"]` extrait ensuite la valeur. `sum(map(...))` : `map` extrait les puissances, `sum` les additionne.

---

### Ex1 — `higher_magic.py` : Fonctions d'ordre supérieur

Quatre fonctions qui prennent d'autres fonctions en argument et/ou en retournent. Elles ne savent pas ce que font les fonctions passées — elles s'occupent uniquement de la structure (combiner, amplifier, conditionner, séquencer).

**Comment ça marche :**

> **`Callable`** — Type hint pour "une fonction". `from collections.abc import Callable`. `Callable` seul pour une fonction quelconque, `Callable[[arg1, arg2], retour]` pour une signature précise.

> **Fonction d'ordre supérieur (HOF)** — Reçoit une fonction comme argument et/ou en retourne une. C'est la composition fonctionnelle.

`spell_combiner` prend deux fonctions et retourne une closure qui les appelle toutes les deux :

```python
def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combined(target: str, power: int) -> tuple[str, str]:
        return (spell1(target, power), spell2(target, power))
    return combined
```

`power_amplifier` retourne une closure qui multiplie `power` avant d'appeler la fonction de base — sans modifier la fonction de base :

```python
def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return amplified

mega = power_amplifier(damage_spell, 3)
mega("Dragon", 10)   # → "Deals 30 damage to Dragon"
```

`conditional_caster` ajoute un garde-fou : si la condition n'est pas satisfaite, le sort fizzle sans appeler la fonction :

```python
def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def cast(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"
    return cast
```

`spell_sequence` retourne une closure qui applique une liste de sorts dans l'ordre et retourne tous les résultats :

```python
def spell_sequence(spells: list[Callable]) -> Callable:
    def sequence(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]
    return sequence
```

`callable(obj)` retourne `True` si `obj` peut être appelé comme une fonction — `callable(fireball)` → `True`, `callable(42)` → `False`.

---

### Ex2 — `scope_mysteries.py` : Fermetures et `nonlocal`

Quatre fonctions qui renvoient des fonctions ou des dicts de fonctions. Chacune démontre un aspect différent des fermetures : état privé partagé avec l'extérieur uniquement via la fonction retournée.

**Comment ça marche :**

> **Fermeture (closure)** — Une fonction interne qui **capture** des variables de son environnement extérieur, même après que cet environnement a fini de s'exécuter. La variable capturée reste en vie tant que la closure existe.

> **`nonlocal`** — Déclare qu'une variable dans la fonction interne **référence** la variable du scope englobant (pas une nouvelle variable locale). Sans `nonlocal`, `count += 1` créerait une nouvelle variable locale `count` → `UnboundLocalError`.

`mage_counter` retourne un compteur encapsulé — chaque appel à la closure incrémente **son propre** compteur :

```python
def mage_counter() -> Callable[[], int]:
    count: int = 0
    def counter() -> int:
        nonlocal count
        count += 1
        return count
    return counter

a = mage_counter()
b = mage_counter()
a()  # → 1
a()  # → 2
b()  # → 1  (état indépendant de a)
```

`spell_accumulator` retourne une closure dont l'état interne (`total`) s'accumule à chaque appel :

```python
def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    total: int = initial_power
    def accumulate(amount: int) -> int:
        nonlocal total
        total += amount
        return total
    return accumulate
```

`enchantment_factory` est l'exemple le plus simple : la closure capture `enchantment_type` au moment de sa création. Deux appels à `enchantment_factory` avec des types différents créent deux closures indépendantes avec leur propre copie capturée :

```python
flaming = enchantment_factory("Flaming")
frozen  = enchantment_factory("Frozen")
flaming("Sword")  # → "Flaming Sword"
frozen("Shield")  # → "Frozen Shield"
```

`memory_vault` retourne un **dict de deux closures** qui partagent le même `_storage`. `store` et `recall` peuvent accéder et modifier `_storage` — c'est un état partagé uniquement accessible via ces deux fonctions, inaccessible de l'extérieur :

```python
def memory_vault() -> dict[str, Callable]:
    _storage: dict[str, object] = {}
    def store(key: str, value: object) -> None:
        _storage[key] = value
    def recall(key: str) -> object:
        return _storage.get(key, "Memory not found")
    return {"store": store, "recall": recall}
```

---

### Ex3 — `functools_artifacts.py` : Le module functools

Quatre fonctions qui utilisent des outils de `functools` : réduction, application partielle, mémoïsation, et dispatch par type.

**Comment ça marche :**

`spell_reducer` utilise `functools.reduce` pour appliquer une opération cumulative sur une liste :

> **`functools.reduce(func, iterable)`** — Applique `func` cumulativement : `reduce(f, [a,b,c,d])` → `f(f(f(a,b),c),d)`. `operator.add` et `operator.mul` sont les fonctions correspondant à `+` et `*`.

```python
functools.reduce(operator.add, [10, 20, 30, 40])   # → 100
functools.reduce(operator.mul, [10, 20, 30, 40])   # → 240000
```

`partial_enchanter` crée des spécialisations d'une fonction générique en fixant certains arguments à l'avance :

> **`functools.partial(func, **kwargs)`** — Retourne une nouvelle fonction avec certains arguments pré-remplis. Appeler la fonction partielle ne demande que les arguments restants.

```python
fire_enchant = functools.partial(base_enchantment, power=50, element="fire")
fire_enchant(target="Sword")   # → "fire enchantment on Sword with 50 power"
```

`memoized_fibonacci` utilise `@functools.lru_cache` pour éviter de recalculer les mêmes valeurs :

> **`@functools.lru_cache(maxsize=None)`** — Mémoïse les résultats de la fonction. Si on appelle `memoized_fibonacci(10)` deux fois, le deuxième appel retourne immédiatement la valeur en cache. `cache_info()` montre les hits et misses.

```python
@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n <= 1: return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)
```

`spell_dispatcher` utilise `@functools.singledispatch` pour choisir l'implémentation selon le type du premier argument :

> **`@functools.singledispatch`** — Dispatch multiple : la fonction appelée dépend du type de l'argument à l'exécution. Chaque variante est enregistrée avec `@dispatch.register(Type)`.

```python
@functools.singledispatch
def dispatch(spell: Any) -> str:
    return "Unknown spell type"

@dispatch.register(int)
def _(spell: int) -> str: return f"{spell} damage"

@dispatch.register(str)
def _(spell: str) -> str: return spell
```

---

### Ex4 — `decorator_mastery.py` : Décorateurs

Trois décorateurs génériques réutilisables, et une classe `MageGuild` dont une méthode est décorée au niveau de la définition de classe.

**Comment ça marche :**

> **Décorateur** — Une fonction qui prend une fonction et retourne une nouvelle fonction enrichie. `@spell_timer` avant une `def` est équivalent à `fireball = spell_timer(fireball)`.

> **`@functools.wraps(func)`** — Copie les métadonnées (`__name__`, `__doc__`) de la fonction originale vers le wrapper. Sans ça, `fireball.__name__` retournerait `"wrapper"` après décoration.

`spell_timer` mesure et affiche le temps d'exécution :

```python
def spell_timer(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        start: float = time.time()
        result: Any = func(*args, **kwargs)
        elapsed: float = time.time() - start
        print(f"Spell completed in {elapsed:.3f} seconds")
        return result
    return wrapper
```

`power_validator` est un **décorateur paramétré** — c'est une factory qui retourne un décorateur. L'usage de `*args` dans `wrapper` lui permet de fonctionner aussi bien sur une fonction ordinaire `(power, ...)` que sur une méthode d'instance `(self, power, ...)` :

```python
def power_validator(min_power: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            power: int = args[0] if isinstance(args[0], int) else args[1]
            if power < min_power:
                return "Insufficient power for this spell"
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

`retry_spell` boucle jusqu'à `max_attempts` fois et absorbe toute exception — utile pour des opérations instables :

```python
def retry_spell(max_attempts: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print(f"Spell failed, retrying... (attempt {attempt}/{max_attempts})")
            return f"Spell casting failed after {max_attempts} attempts"
        return wrapper
    return decorator
```

`MageGuild.cast_spell` est décorée avec `@power_validator(min_power=10)` directement dans la définition de la classe. La décoration se produit une fois à la définition, pas à l'instanciation.

---

### `data_generator.py` : Utility class et menu interactif

`FuncMageDataGenerator` n'est jamais instanciée — toutes ses méthodes sont `@classmethod`. Elle regroupe des générateurs de données thématiques sous un même namespace. `print_exercise_data(n)` dispatche selon le numéro d'exercice et affiche les données adaptées. `main()` expose un menu interactif en boucle.

**Comment ça marche :**

> **Utility class avec `@classmethod`** — Une classe dont toutes les méthodes sont `@classmethod` fonctionne comme un namespace de fonctions liées. `cls` donne accès aux attributs de classe (`MAGE_NAMES`, `SPELL_NAMES`) sans instanciation.

```python
@classmethod
def generate_mages(cls, count: int = 5) -> List[Dict[str, Any]]:
    return [{'name': random.choice(cls.MAGE_NAMES), 'power': random.randint(50, 100), ...}
            for _ in range(count)]
```

`main()` tourne dans une boucle `while True` et lit le choix de l'utilisateur avec `input()`. `break` sur `'q'` est le seul moyen d'en sortir. `int(input(...) or 5)` utilise le `or` de Python : si l'utilisateur tape Entrée sans rien, `input()` retourne `""` (falsy), donc `or 5` s'évalue à `5`.

---

## 🚀 Comment tester

```bash
cd module_10

python3 ex0/lambda_spells.py
# Fire Staff (92 power) comes before Crystal Orb (85 power)
# * fireball * * heal * * shield *

python3 ex1/higher_magic.py
# Combined spell result: Fireball hits Dragon, Heals Dragon
# Deals 30 damage to Dragon

python3 ex2/scope_mysteries.py
# counter_a: 1, 2 / counter_b: 1  (états indépendants)
# Base 100, add 20: 120 / add 30: 150  (accumulation)
# Recall 'secret': 42 / Recall 'unknown': Memory not found

python3 ex3/functools_artifacts.py
# Sum: 100 / Product: 240000 / Max: 40
# Fib(15): 610 / Cache info: hits=16, misses=16
# Fire/Ice/Lightning enchantment on Sword with 50 power

python3 ex4/decorator_mastery.py
# Casting fireball... / Spell completed in 0.100 seconds
# Spell failed, retrying... x3 / Spell casting failed after 3 attempts
# Successfully cast Lightning with 15 power
# Insufficient power for this spell

python3 data_generator.py
# Menu interactif : choisir 0-4 pour les données par exercice
```
