# Module 05 — Code Nexus : Classes abstraites, polymorphisme et Protocol

---

## 🎯 Objectif

Construire un pipeline de traitement de données extensible en appliquant le polymorphisme : des classes abstraites (`ABC`) forcent chaque processeur à implémenter un contrat, `DataStream` orchestre tous les processeurs sans connaître leurs types concrets, et `Protocol` permet aux plugins d'export de s'intégrer sans héritage explicite. Les trois exercices s'emboîtent — chacun ajoute une couche au-dessus du précédent.

---

## 🏗️ Architecture

| Exercice | Fichier | Notion principale |
|----------|---------|------------------|
| ex0 | `data_processor.py` | `ABC`, `@abstractmethod`, 3 processeurs concrets |
| ex1 | `data_stream.py` | `DataStream`, routage par `validate()`, stats |
| ex2 | `data_pipeline.py` | `Protocol`, `ExportPlugin`, `output_pipeline` |

---

## ⚙️ Exercice par exercice

### Ex0 — `data_processor.py`

`DataProcessor` est une classe abstraite qui définit le contrat : tout processeur doit savoir **valider** une donnée (`validate`) et **l'ingérer** (`ingest`). Elle fournit aussi des méthodes concrètes partagées par tous : `output()` pour extraire les données, `_store()` pour les ranger, `total_ingested()` et `remaining()` pour les statistiques. Les trois processeurs concrets implémentent chacun leur propre logique de validation et d'ingestion, mais héritent tout le reste de `DataProcessor` sans le réécrire.

**Comment ça marche :**

> **`ABC` et `@abstractmethod`** — Une classe qui hérite de `ABC` ne peut pas être instanciée directement. `@abstractmethod` marque une méthode comme **obligatoire** : toute sous-classe doit l'implémenter, sinon `TypeError` à l'instanciation. C'est un contrat imposé par le code.

```python
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    @abstractmethod
    def validate(self, data: Any) -> bool: ...

    @abstractmethod
    def ingest(self, data: Any) -> None: ...

DataProcessor()      # TypeError: Can't instantiate abstract class
NumericProcessor()   # OK : validate et ingest sont implémentés
```

> **FIFO avec `list.pop(0)`** — `self._storage.append(...)` ajoute en fin de liste (enqueue). `self._storage.pop(0)` retire et retourne le **premier** élément (dequeue). L'ordre d'ingestion est ainsi préservé à la sortie.

`NumericProcessor.validate()` vérifie `bool` avant `int` — parce que `bool` est une sous-classe de `int` en Python, donc `isinstance(True, int)` retourne `True`. Sans cette vérification en premier, `True` et `False` passeraient comme des nombres.

`LogProcessor.ingest()` formate chaque entrée en `"LEVEL: message"` avant de la stocker, en utilisant `.get()` avec des valeurs par défaut pour les clés manquantes.

---

### Ex1 — `data_stream.py`

`DataStream` est l'orchestrateur. Il maintient une liste de processeurs enregistrés et, quand on lui envoie un flux de données, il fait passer chaque élément devant chaque processeur jusqu'à en trouver un qui accepte de le traiter. Il ne connaît aucun processeur concret — il ne voit que l'interface `DataProcessor`.

**Comment ça marche :**

Le routage se fait par `validate()` : pour chaque élément du flux, `DataStream` interroge les processeurs dans l'ordre. Le premier qui retourne `True` prend en charge l'ingestion. Si aucun ne valide l'élément, un message d'erreur est affiché.

```python
def process_stream(self, stream: list[Any]) -> None:
    for element in stream:
        handled: bool = False
        for proc in self._processors:
            if proc.validate(element):
                proc.ingest(element)
                handled = True
                break
        if not handled:
            print(f"DataStream error - Can't process element: {element}")
```

`print_processors_stats()` appelle `proc.name()` sur chaque processeur — méthode concrète de `DataProcessor` qui retourne `self.__class__.__name__`. Ça permet d'afficher `"NumericProcessor"` dynamiquement sans hardcoder le nom.

---

### Ex2 — `data_pipeline.py`

`DataStream` gagne une méthode `output_pipeline` qui extrait des lots de données de chaque processeur et les passe à un **plugin d'export**. `CSVExportPlugin` et `JSONExportPlugin` n'héritent de rien — ils satisfont juste `ExportPlugin` parce qu'ils ont la bonne méthode. C'est le typage structurel.

**Comment ça marche :**

> **`Protocol`** — Définit une **interface implicite** : toute classe qui possède les méthodes déclarées dans le `Protocol`, avec les bonnes signatures, est automatiquement compatible. Pas besoin d'héritage explicite.

```python
from typing import Protocol

class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None: ...

class CSVExportPlugin:          # aucun héritage
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print(",".join(val for _, val in data))

class JSONExportPlugin:         # aucun héritage
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...
```

`mypy` vérifie statiquement que `CSVExportPlugin` satisfait `ExportPlugin` — si la méthode était absente ou avait la mauvaise signature, l'erreur serait signalée à la compilation, pas à l'exécution.

**Différence clé avec `ABC`** :

| | `ABC` | `Protocol` |
|-|-------|-----------|
| Héritage requis | Oui | Non |
| Vérification | À l'instanciation (runtime) | Par mypy (statique) |
| Cas d'usage | Hiérarchie interne | Interfaces avec du code tiers |

`output_pipeline(nb, plugin)` extrait jusqu'à `nb` éléments de chaque processeur et les accumule en lot avant de les passer au plugin — le plugin reçoit `list[tuple[int, str]]` et formate comme il veut.

---

## 🚀 Comment tester

```bash
cd module_05

python3 ex0/data_processor.py
# Testing Numeric Processor...
# Got exception: Improper numeric data
# Numeric value 0: 1

python3 ex1/data_stream.py
# Send first batch... (routage automatique par validate)
# DataStream error - Can't process element in stream: ...

python3 ex2/data_pipeline.py
# CSV Output: Hello world,3.14,-1,...
# JSON Output: {"item_0": "Hello world", ...}
```
