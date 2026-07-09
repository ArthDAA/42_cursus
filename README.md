# Module 09 — Cosmic Data : Validation de données avec Pydantic v2

---

## 🎯 Objectif

Valider des données structurées sans écrire de code de validation manuel : des types, des contraintes de champ, des enums, et des règles métier cross-champs déclarées directement sur la classe. Un générateur de données de test et un exporteur multi-format complètent le module pour te donner des données réalistes à valider.

---

## 🏗️ Architecture

| Fichier | Rôle |
|---------|------|
| `ex0/space_station.py` | `BaseModel` de base, `Field`, `Optional`, `datetime` |
| `ex1/alien_contact.py` | `Enum`, `@model_validator(mode='after')` |
| `ex2/space_crew.py` | Modèles imbriqués, règles métier complexes |
| `data_generator.py` | Génère des données réalistes pour les trois modèles |
| `data_exporter.py` | Exporte en JSON, CSV, Python |

---

## ⚙️ Exercice par exercice

### Ex0 — `space_station.py` : Le premier modèle Pydantic

`SpaceStation` valide les données d'une station spatiale : ID, nom, taille d'équipage, niveaux d'énergie et d'oxygène, date de maintenance. Elle rejette automatiquement tout ce qui viole ses contraintes — trop d'équipage, niveau hors plage, ID trop long — sans qu'on écrive une seule ligne de validation.

**Comment ça marche :**

> **`BaseModel`** — La classe de base Pydantic. Toute classe qui en hérite bénéficie automatiquement de : validation de type à l'instanciation, coercition (une string ISO devient un `datetime`), `ValidationError` si une contrainte est violée.

> **`Field()`** — Attache des contraintes à un champ. `ge` (greater or equal), `le` (less or equal), `gt`, `lt` pour les nombres. `min_length`, `max_length` pour les strings et les listes.

```python
class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime           # auto-converti depuis "2024-01-15T08:30:00"
    notes: Optional[str] = Field(default=None, max_length=200)
```

> **`Optional[str]`** — Équivalent à `str | None`. Si le champ n'est pas fourni, il prend la valeur `default`. Pydantic distingue "non fourni" (→ default) de "fourni explicitement à `None`".

> **`ValidationError`** — Pydantic ne s'arrête pas à la première erreur : il valide tous les champs et agrège tout dans une seule exception. `e.errors()` retourne la liste complète avec le champ concerné, le message, et le type d'erreur pour chacun.

```python
try:
    SpaceStation(station_id="BAD01", crew_size=99, ...)
except ValidationError as e:
    for err in e.errors():
        print(err["msg"])   # "Input should be less than or equal to 20"
```

---

### Ex1 — `alien_contact.py` : Enum et validation cross-champs

`AlienContact` ajoute deux mécanismes nouveaux : `ContactType` est un enum qui restreint les valeurs acceptées pour le type de contact, et `@model_validator` impose des règles qui impliquent plusieurs champs en même temps — ce qu'un `Field` seul ne peut pas exprimer.

**Comment ça marche :**

> **`class ContactType(str, Enum)`** — Hériter de `str` en plus d'`Enum` permet à Pydantic d'accepter la chaîne `"radio"` directement là où `ContactType` est attendu, et de la convertir automatiquement. `ContactType.radio == "radio"` est `True`. Une valeur hors enum lève `ValidationError`.

```python
class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"
```

> **`@model_validator(mode="after")`** — Méthode de classe décorée qui s'exécute **après** que tous les champs individuels ont été validés. Elle reçoit `self` avec tous les attributs déjà convertis et contraints. Elle doit retourner `self` ou lever `ValueError`.

```python
@model_validator(mode="after")
def validate_contact_rules(self) -> "AlienContact":
    if not self.contact_id.startswith("AC"):
        raise ValueError("Contact ID must start with 'AC'")
    if self.contact_type == ContactType.physical and not self.is_verified:
        raise ValueError("Physical contact reports must be verified")
    if self.contact_type == ContactType.telepathic and self.witness_count < 3:
        raise ValueError("Telepathic contact requires at least 3 witnesses")
    if self.signal_strength > 7.0 and self.message_received is None:
        raise ValueError("Strong signals (> 7.0) should include received messages")
    return self
```

Ces quatre règles croisent des champs différents — impossible à exprimer avec `Field`. C'est exactement le cas d'usage de `@model_validator`.

---

### Ex2 — `space_crew.py` : Modèles imbriqués et règles métier complexes

`SpaceMission` contient une liste de `CrewMember` — Pydantic valide chaque membre individuellement. Le `@model_validator` de `SpaceMission` agrège ensuite des informations sur l'ensemble de l'équipage pour vérifier des règles qui ne peuvent pas s'appliquer membre par membre.

**Comment ça marche :**

`Rank` est un `str, Enum` comme `ContactType`. `CrewMember` est un `BaseModel` à part entière avec ses propres `Field`.

```python
class SpaceMission(BaseModel):
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
```

`list[CrewMember]` : Pydantic valide chaque dict ou objet de la liste comme un `CrewMember`. `min_length=1` sur la liste garantit au moins un membre. Si un membre a un `rank` invalide ou un `age` hors plage, l'erreur remonte dans `ValidationError` avec le chemin exact (`crew.0.rank`).

Le `@model_validator` de `SpaceMission` traverse ensuite tout l'équipage pour des règles globales :

```python
@model_validator(mode="after")
def validate_mission_rules(self) -> "SpaceMission":
    if not self.mission_id.startswith("M"):
        raise ValueError("Mission ID must start with 'M'")

    senior_ranks = {Rank.captain, Rank.commander}
    has_senior = any(m.rank in senior_ranks for m in self.crew)
    if not has_senior:
        raise ValueError("Mission must have at least one Commander or Captain")

    if self.duration_days > 365:
        experienced = sum(1 for m in self.crew if m.years_experience >= 5)
        if experienced / len(self.crew) < 0.5:
            raise ValueError("Long missions (> 365 days) need 50% experienced crew")

    inactive = [m.name for m in self.crew if not m.is_active]
    if inactive:
        raise ValueError(f"Inactive crew members not allowed: {', '.join(inactive)}")
    return self
```

`any(...)` et `sum(... for ...)` avec des compréhensions de générateur permettent de parcourir l'équipage en une ligne pour chaque règle.

---

### `data_generator.py` : Générer des données réalistes

Le générateur produit des données qui respectent les contraintes des modèles Pydantic — il connaît les règles. `AlienContactGenerator` s'assure que les contacts `telepathic` ont toujours au moins 3 témoins. `CrewMissionGenerator` s'assure que les missions longues ont 50% d'équipage expérimenté.

**Comment ça marche :**

> **`@dataclass`** — Décorateur qui génère automatiquement `__init__`, `__repr__` et `__eq__` depuis les annotations. Plus léger que `BaseModel` (pas de validation) — idéal pour un objet de configuration simple comme `DataConfig`.

```python
from dataclasses import dataclass

@dataclass
class DataConfig:
    seed: int = 42
    base_date: datetime = datetime(2024, 1, 1)
    date_range_days: int = 365
```

`random.seed(config.seed)` dans chaque générateur fixe le générateur de nombres aléatoires — le même seed produit toujours exactement les mêmes données, ce qui rend les tests reproductibles.

---

### `data_exporter.py` : Exporter en JSON, CSV, Python

`DataExporter` prend des données générées et les écrit dans des fichiers de différents formats. Il interagit avec `data_generator.py` pour récupérer les données et avec le système de fichiers pour les écrire.

**Comment ça marche :**

> **`pathlib.Path`** — Objet représentant un chemin de fichier. `Path("generated_data")` crée un objet chemin. `path.mkdir(exist_ok=True)` crée le répertoire sans erreur s'il existe déjà. L'opérateur `/` joint les segments : `output_dir / "stations.json"` donne `Path("generated_data/stations.json")`.

> **`json.dump(data, file, indent=2)`** — Sérialise un objet Python en JSON dans un fichier ouvert. `indent=2` formate avec indentation lisible.

> **`csv.DictWriter`** — Écrit des lignes CSV depuis des dicts. `writeheader()` écrit les noms de colonnes. `writerows(data)` écrit toutes les lignes.

```python
with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

with open(filepath, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
    writer.writeheader()
    writer.writerows(flat_data)
```

`_flatten_dict()` aplatit récursivement les dicts imbriqués pour le CSV — les membres d'équipage deviennent `crew_0_name`, `crew_0_rank`, etc.

`create_test_scenarios()` génère intentionnellement des données **invalides** (ID trop long, crew_size à 99, signal fort sans message) pour tester que les `ValidationError` se déclenchent bien.

---

## 🚀 Comment tester

```bash
pip install pydantic
cd module_09

python3 ex0/space_station.py
# Valid station created: ISS001, 6 crew, 85.5% power
# Expected validation error: Input should be less than or equal to 20

python3 ex1/alien_contact.py
# Valid: AC_2024_001, radio, signal 8.5, message reçu
# Expected error: Telepathic contact requires at least 3 witnesses

python3 ex2/space_crew.py
# Valid: Mars Colony, 900 days, 3 crew members
# Expected error: Mission must have at least one Commander or Captain

python3 data_generator.py
# 5 stations, 6 contacts, 3 missions générées avec statuts

python3 data_exporter.py
# Crée generated_data/ avec .json, .csv, .py
# + invalid_stations.json et invalid_contacts.json pour tester ValidationError
```
