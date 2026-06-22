# Module 06 — The Codex : Système d'imports et packages Python

---

## 🎯 Objectif

Comprendre en profondeur comment Python résout les noms de modules : la différence entre un module racine et un sous-module de package, les trois formes d'import, le rôle de `__init__.py` comme porte d'entrée d'un package, le contrôle de l'interface publique avec `__all__`, les imports relatifs depuis l'intérieur d'un package, et pourquoi une dépendance circulaire entre deux modules fait tout planter.

---

## 🏗️ Architecture

```
module_06/
├── elements.py                         ← module racine (create_fire, create_water)
├── alchemy/
│   ├── __init__.py                     ← API publique du package
│   ├── elements.py                     ← create_earth, create_air
│   ├── potions.py                      ← healing_potion, strength_potion
│   ├── transmutation/
│   │   ├── __init__.py
│   │   └── recipes.py                  ← 3 styles d'import en un fichier
│   └── grimoire/
│       ├── __init__.py
│       ├── light_spellbook.py          ← importe light_validator → OK
│       ├── light_validator.py          ← pas d'import → pas de circularité
│       ├── dark_spellbook.py           ← importe dark_validator → CIRCULAIRE
│       └── dark_validator.py           ← importe dark_spellbook → CIRCULAIRE
├── ft_alembic_0.py  →  ft_alembic_5.py
├── ft_distillation_0.py, ft_distillation_1.py
├── ft_transmutation_0.py → ft_transmutation_2.py
├── ft_kaboom_0.py  (fonctionne)
└── ft_kaboom_1.py  (plante : dépendance circulaire)
```

| Fichier | Ce qu'il démontre |
|---------|------------------|
| `ft_alembic_0` | `import elements` (module racine, forme courte) |
| `ft_alembic_1` | `from elements import create_water` |
| `ft_alembic_2` | `import alchemy.elements` (sous-module de package) |
| `ft_alembic_3` | `from alchemy.elements import create_air` |
| `ft_alembic_4` | `import alchemy` → `alchemy.create_earth()` → `AttributeError` |
| `ft_alembic_5` | `from alchemy import create_air` (via `__init__.py`) |
| `ft_distillation_0` | `from alchemy.potions import ...` (accès direct au sous-module) |
| `ft_distillation_1` | `import alchemy` → `alchemy.strength_potion()`, `alchemy.heal()` (alias) |
| `ft_transmutation_0` | `import alchemy.transmutation.recipes` (chemin complet) |
| `ft_transmutation_1` | `import alchemy.transmutation` (via `__init__` du sous-package) |
| `ft_transmutation_2` | `import alchemy` → `alchemy.lead_to_gold()` (remonté dans `__init__`) |
| `ft_kaboom_0` | Import du grimoire light → fonctionne |
| `ft_kaboom_1` | Import du grimoire dark → `ImportError` (circulaire) |

---

## ⚙️ Exercice par exercice

### `ft_alembic_0` et `ft_alembic_1` — Le module racine `elements.py`

`elements.py` est un simple fichier Python à la racine du projet (pas dans un sous-dossier). `ft_alembic_0` l'importe avec `import elements` et appelle `elements.create_fire()`. `ft_alembic_1` l'importe avec `from elements import create_water` et appelle `create_water()` directement.

**Comment ça marche :**

> **`import module`** — Charge le module et le rend disponible sous son nom. On accède aux membres via la notation pointée : `elements.create_fire()`.

> **`from module import nom`** — Importe uniquement `nom` dans l'espace de noms courant. On l'appelle directement : `create_water()`. Plus pratique, mais si deux modules exportent un même nom, il faut faire attention aux collisions.

Ces deux formes s'appliquent à n'importe quel module — la différence est juste dans la façon d'y accéder ensuite.

---

### `ft_alembic_2` et `ft_alembic_3` — Le sous-module `alchemy/elements.py`

Il existe **deux fichiers `elements.py`** dans ce projet : un à la racine (`elements.py`) et un dans le package (`alchemy/elements.py`). Ils cohabitent sans conflit parce que Python les distingue par leur chemin. `ft_alembic_2` accède à celui du package avec `import alchemy.elements`, `ft_alembic_3` avec `from alchemy.elements import create_air`.

**Comment ça marche :**

> **Package** — Un répertoire qui contient un fichier `__init__.py`. Ce fichier est exécuté automatiquement quand le package est importé. `alchemy/` est un package, donc `import alchemy.elements` charge `alchemy/__init__.py` puis `alchemy/elements.py`.

`alchemy/elements.py` contient `create_earth` et `create_air`. `elements.py` (racine) contient `create_fire` et `create_water`. Ce découpage est intentionnel pour montrer qu'un même nom de fichier peut désigner des modules différents.

---

### `ft_alembic_4` — Ce que `__init__.py` choisit d'exposer

`ft_alembic_4` importe le package avec `import alchemy` et appelle `alchemy.create_air()` (ça marche), puis `alchemy.create_earth()` (ça plante). Les deux fonctions existent dans `alchemy/elements.py` — pourquoi l'une est accessible et pas l'autre ?

**Comment ça marche :**

`alchemy/__init__.py` importe explicitement `create_air` mais pas `create_earth` :

```python
# alchemy/__init__.py
from alchemy.elements import create_air   # create_air est dans l'espace de noms d'alchemy
# create_earth n'est pas importée ici → pas accessible via alchemy.create_earth
```

Quand on fait `import alchemy`, Python exécute `__init__.py`. Seuls les noms qui y ont été importés (ou définis) sont accessibles via `alchemy.xxx`. `create_earth` vit dans `alchemy/elements.py` mais n'a pas été remontée dans `__init__.py` → `AttributeError`.

> **`__init__.py` comme porte d'entrée** — Il décide ce que le package expose publiquement. Tout ce qui n'y est pas importé est un détail interne inaccessible via le nom du package.

---

### `ft_alembic_5` — `__all__` et `from alchemy import *`

`ft_alembic_5` utilise `from alchemy import create_air` — il passe par `__init__.py` pour récupérer `create_air` directement dans son espace de noms. `alchemy/__init__.py` déclare aussi `__all__`.

**Comment ça marche :**

> **`__all__`** — Liste de chaînes qui définit exactement ce qu'un `from module import *` exporte. Sans `__all__`, `import *` prendrait tout ce qui est dans l'espace de noms du module, y compris les noms importés pour usage interne.

```python
# alchemy/__init__.py
from alchemy.elements import create_air
from alchemy.potions import healing_potion, strength_potion
from alchemy.transmutation.recipes import lead_to_gold

heal = healing_potion   # alias

__all__ = ["create_air", "strength_potion", "heal", "lead_to_gold"]
```

`heal` est un simple alias : `alchemy.heal()` appelle `healing_potion()`. C'est une façon de renommer une fonction à la frontière du package sans modifier son code.

---

### `ft_distillation_0` et `ft_distillation_1` — Accéder aux potions

`ft_distillation_0` accède directement à `alchemy/potions.py` avec `from alchemy.potions import strength_potion, healing_potion`. `ft_distillation_1` passe par le package avec `import alchemy` et utilise `alchemy.strength_potion()` et `alchemy.heal()` (l'alias).

`alchemy/potions.py` lui-même utilise les deux types d'imports : il importe depuis le package (`from alchemy.elements import create_earth, create_air`) et depuis le module racine (`from elements import create_fire, create_water`). C'est possible parce que les deux sont dans le `sys.path`.

---

### `ft_transmutation_0`, `ft_transmutation_1`, `ft_transmutation_2` — Trois chemins vers `lead_to_gold`

`recipes.py` est le fichier le plus riche du module en termes d'imports : il utilise les trois styles en même temps pour démontrer leur cohabitation.

**Comment ça marche :**

```python
# alchemy/transmutation/recipes.py
from alchemy.elements import create_air    # import absolu : depuis la racine du projet
from ..potions import strength_potion      # import relatif : monte d'un niveau (→ alchemy/)
import elements                            # module racine
```

> **Import absolu** — Chemin depuis la racine du projet. Fonctionne partout, toujours lisible.

> **Import relatif** — `.` = répertoire courant, `..` = répertoire parent. `from ..potions` depuis `alchemy/transmutation/` remonte à `alchemy/` puis accède à `potions.py`. Ne fonctionne que depuis l'intérieur d'un package.

Les trois fichiers `ft_transmutation` accèdent à la même fonction via trois niveaux d'indirection différents : chemin complet (`alchemy.transmutation.recipes`), sous-package (`alchemy.transmutation`), ou package racine (`alchemy`).

---

### `ft_kaboom_0` et `ft_kaboom_1` — Quand le grimoire s'embrase

`ft_kaboom_0` importe `light_spellbook` depuis le grimoire — ça fonctionne. `ft_kaboom_1` importe `dark_spellbook` depuis le grimoire — ça plante avec `ImportError`.

**Comment ça marche :**

`light_spellbook.py` importe `light_validator.py`. `light_validator.py` n'importe rien du grimoire — il définit sa propre liste `_ALLOWED` localement. Pas de cycle.

`dark_spellbook.py` importe `dark_validator.py`. `dark_validator.py` importe `dark_spellbook.py`. Cycle fermé.

> **Dépendance circulaire** — Quand A importe B et B importe A, Python charge A, commence à charger B, qui essaie de charger A — mais A n'est pas encore complètement chargé. Résultat : `ImportError: cannot import name 'X' from partially initialized module`.

```
dark_spellbook  →  from .dark_validator import validate_ingredients
dark_validator  →  from .dark_spellbook import dark_spell_allowed_ingredients
```

La solution appliquée dans le grimoire de lumière : `light_validator.py` ne dépend de personne. Il redéfinit localement ce dont il a besoin plutôt que de l'importer depuis `light_spellbook`.

---

## 🚀 Comment tester

```bash
cd module_06

# Styles d'import sur le module racine
python3 ft_alembic_0.py   # import elements
python3 ft_alembic_1.py   # from elements import create_water

# Styles d'import sur le package
python3 ft_alembic_2.py   # import alchemy.elements
python3 ft_alembic_3.py   # from alchemy.elements import create_air
python3 ft_alembic_5.py   # from alchemy import create_air

# Ce que __init__.py expose (et ce qu'il cache)
python3 ft_alembic_4.py
# AttributeError: module 'alchemy' has no attribute 'create_earth'

# Alias et potions
python3 ft_distillation_0.py
python3 ft_distillation_1.py   # alchemy.heal() = alias de healing_potion

# Trois chemins vers recipes.py
python3 ft_transmutation_0.py
python3 ft_transmutation_1.py
python3 ft_transmutation_2.py

# Grimoire
python3 ft_kaboom_0.py   # OK : light, pas de circularité
python3 ft_kaboom_1.py   # ImportError : dark, dépendance circulaire
```
