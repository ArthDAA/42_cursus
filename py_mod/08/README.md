# Module 08 — The Matrix : Environnements virtuels, dépendances et configuration

---

## 🎯 Objectif

Comprendre l'écosystème Python autour du code : détecter si on tourne dans un environnement isolé, charger dynamiquement des bibliothèques tierces et les utiliser pour de l'analyse de données, et séparer la configuration sensible du code source via des variables d'environnement. Trois exercices indépendants qui couvrent les bonnes pratiques de mise en place d'un projet Python professionnel.

---

## 🏗️ Architecture

| Exercice | Fichier | Notion principale |
|----------|---------|------------------|
| ex0 | `construct.py` | `sys.prefix`, détection venv |
| ex1 | `loading.py` | `importlib.import_module`, numpy/pandas/matplotlib |
| ex2 | `oracle.py` | `os.environ.get()`, `python-dotenv`, `.env` |

---

## ⚙️ Exercice par exercice

### Ex0 — `construct.py` : Détection de l'environnement virtuel

`construct.py` inspecte l'environnement Python courant et informe l'utilisateur s'il tourne dans un venv ou dans le Python système. Si c'est le Python système, il affiche les instructions pour créer et activer un venv. Si c'est un venv, il affiche son nom et le chemin des packages installés.

**Comment ça marche :**

> **Environnement virtuel (`venv`)** — Un répertoire Python isolé avec son propre interpréteur et ses propres packages, indépendant du Python système. Chaque projet a le sien pour éviter les conflits de versions entre dépendances.

```bash
python -m venv matrix_env           # crée le venv
source matrix_env/bin/activate      # active (Unix/macOS)
matrix_env\Scripts\activate         # active (Windows)
deactivate                          # désactive
```

> **`sys.prefix` vs `sys.base_prefix`** — `sys.prefix` pointe vers le Python actif (le venv si activé). `sys.base_prefix` pointe toujours vers le Python système. S'ils diffèrent, on est dans un venv.

```python
def is_in_venv() -> bool:
    return sys.prefix != sys.base_prefix
```

`sys.executable` donne le chemin complet de l'interpréteur (`/home/user/matrix_env/bin/python3`). `os.path.basename(sys.prefix)` extrait juste le nom du venv (`"matrix_env"`). `site.getsitepackages()[0]` retourne le chemin où `pip install` installe les packages dans ce venv.

---

### Ex1 — `loading.py` : Import dynamique et analyse de données

`check_dependencies()` vérifie que les bibliothèques requises (`numpy`, `pandas`, `matplotlib`) sont installées, en tente l'import dynamiquement, et quitte proprement avec un message d'aide si l'une manque. Si tout est bon, `analyze_matrix_data()` génère 1000 données aléatoires, les analyse statistiquement, et sauvegarde un histogramme en PNG. `compare_pip_vs_poetry()` explique la différence entre les deux outils de gestion de dépendances.

**Comment ça marche :**

> **`importlib.import_module(name)`** — Importe un module dont le nom est une **chaîne de caractères**. Équivalent à `import pandas` mais utilisable dans une boucle ou avec un nom connu seulement à l'exécution. Lève `ImportError` si le module n'est pas installé.

```python
for pkg in ["pandas", "numpy", "matplotlib"]:
    try:
        mod = importlib.import_module(pkg)
        version: str = getattr(mod, "__version__", "unknown")
        loaded[pkg] = mod
    except ImportError:
        missing.append(pkg)
```

> **`getattr(obj, name, default)`** — Lit un attribut par son nom (string). `getattr(mod, "__version__", "unknown")` retourne la version du module si l'attribut `__version__` existe, sinon `"unknown"`.

> **`pip` vs `Poetry`** — `pip` + `requirements.txt` : simple, pas de lock file automatique. `Poetry` + `pyproject.toml` : génère un `poetry.lock` qui fixe les versions exactes de toutes les dépendances (directes et transitives). Le lock file garantit que tous les développeurs et la CI ont exactement les mêmes versions.

`analyze_matrix_data()` utilise les modules chargés dynamiquement via le dict `mods`. `np.random.randn(1000)` génère 1000 valeurs normalement distribuées. `pd.DataFrame({"signal": data})` crée un tableau avec une colonne. `plt.subplots()` crée une figure matplotlib, `ax.hist()` trace l'histogramme, `fig.savefig()` l'enregistre.

---

### Ex2 — `oracle.py` : Configuration via variables d'environnement

`load_config()` lit la configuration depuis les variables d'environnement, avec une valeur par défaut pour chacune si elle n'est pas définie. `display_config()` affiche la config de manière sécurisée — elle ne révèle pas la valeur brute de l'API key, juste si elle est définie ou non. `security_check()` vérifie si un fichier `.env` est présent.

**Comment ça marche :**

> **`os.environ`** — Dictionnaire des variables d'environnement du shell. `os.environ.get("DATABASE_URL", "sqlite:///local.db")` retourne la valeur si définie, sinon la valeur par défaut. **Les secrets ne doivent jamais être codés en dur dans le code source** — ils arrivent via l'environnement.

> **`python-dotenv`** — Package qui lit un fichier `.env` et injecte son contenu dans `os.environ`. `.env` contient des lignes `KEY=value`. `load_dotenv()` s'appelle au démarrage du programme, avant tout `os.environ.get()`.

```python
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed.")
```

L'import est dans un `try / except ImportError` : si `python-dotenv` n'est pas installé, le programme continue quand même en lisant uniquement les variables d'environnement système. C'est une **dégradation gracieuse**.

> **`.env` et `.gitignore`** — Le fichier `.env` contient les vraies valeurs (mots de passe, clés API) et ne doit **jamais** être commité. On versionne `.env.example` (template vide) pour documenter les variables requises. `.gitignore` contient `.env` pour éviter l'accident.

`MATRIX_MODE=production` vs `MATRIX_MODE=development` change le comportement affiché à la fin : logs verbeux en dev, settings stricts en prod.

---

## 🚀 Comment tester

```bash
cd module_08

# Ex0 — hors venv
python3 ex0/construct.py
# MATRIX STATUS: You're still plugged in
# WARNING: You're in the global environment!

# Ex0 — dans un venv
python -m venv matrix_env && source matrix_env/bin/activate
python3 ex0/construct.py
# MATRIX STATUS: Welcome to the construct
# Virtual Environment: matrix_env

# Ex1 — installer les dépendances puis analyser
pip install -r ex1/requirements.txt
python3 ex1/loading.py
# [OK] pandas / numpy / matplotlib
# Generates matrix_analysis.png

# Ex2 — sans .env (valeurs par défaut)
python3 ex2/oracle.py
# Mode: development / [WARN] No .env file found

# Ex2 — avec .env
cp ex2/.env.example ex2/.env
# Éditer .env avec de vraies valeurs, puis :
python3 ex2/oracle.py
# [OK] .env file properly configured
# Mode selon MATRIX_MODE dans .env
```
