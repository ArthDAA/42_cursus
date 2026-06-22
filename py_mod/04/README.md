# Module 04 — Data Archivist : Fichiers, flux et contextes

---

## 🎯 Objectif

Maîtriser les entrées/sorties en Python : lire et écrire des fichiers, manipuler les flux standards (`stdin`, `stdout`, `stderr`), et garantir la fermeture des ressources avec le gestionnaire de contexte `with`. Les quatre exercices montrent la même opération — lire un fichier et transformer son contenu — en variant progressivement le niveau d'abstraction et de robustesse.

---

## 🏗️ Architecture

| Exercice | Fichier | Notion principale |
|----------|---------|------------------|
| ex0 | `ft_ancient_text.py` | `open()`, `.read()`, `.close()`, `OSError` |
| ex1 | `ft_archive_creation.py` | Mode `"w"`, `.splitlines()`, écriture |
| ex2 | `ft_stream_management.py` | `sys.stdin`, `sys.stdout`, `sys.stderr` |
| ex3 | `ft_vault_security.py` | `with open(...) as f:`, retourner `tuple[bool, str]` |

---

## ⚙️ Exercice par exercice

### Ex0 — `ft_ancient_text`

Le programme prend un nom de fichier en argument de ligne de commande, l'ouvre, lit son contenu entier, l'affiche, et le ferme. Si le fichier n'existe pas ou n'est pas accessible, il affiche une erreur et quitte proprement.

**Comment ça marche :**

> **`open(filename)`** — Ouvre un fichier en lecture (mode `"r"` par défaut). Retourne un objet fichier de type `IO[str]`. Le fichier reste ouvert jusqu'à ce qu'on appelle `.close()` dessus — si on oublie, le descripteur de fichier reste occupé.

> **`f.read()`** — Lit tout le contenu du fichier en une seule chaîne.

> **`f.close()`** — Libère le descripteur de fichier. Obligatoire. Si une exception se produit entre `open()` et `close()`, le fichier reste ouvert — c'est le problème que `with` résout en ex3.

> **`OSError`** — Exception parente de `FileNotFoundError` et `PermissionError`. Attraper `OSError` couvre tous les problèmes d'accès fichier : fichier inexistant, droits insuffisants, chemin invalide.

```python
f: IO[str]
try:
    f = open(filename)
except OSError as e:
    print(f"Error opening file '{filename}': {e}")
    sys.exit(1)

content: str = f.read()
f.close()
```

> **`sys.exit(code)`** — Termine le programme avec un code de retour. `1` signale une erreur au shell. `echo $?` après l'exécution affiche ce code.

---

### Ex1 — `ft_archive_creation`

Reprend la logique d'ex0 (lire un fichier), y ajoute une transformation (un `#` à la fin de chaque ligne), puis propose à l'utilisateur de sauvegarder le résultat dans un nouveau fichier. Deux fichiers sont impliqués : un en lecture, un en écriture.

**Comment ça marche :**

> **Mode `"w"`** — `open(filename, "w")` ouvre en écriture. Si le fichier existe, son contenu est **écrasé**. Si il n'existe pas, il est créé.

> **`.splitlines()`** — Découpe une chaîne en liste de lignes. Gère proprement tous les styles de fins de ligne (`\n`, `\r\n`, `\r`). Préférable à `.split("\n")` qui peut laisser des éléments vides.

```python
lines: list[str] = content.splitlines()
new_content: str = "\n".join(line + "#" for line in lines) + "\n"
```

`"\n".join(...)` recolle les lignes transformées avec un saut de ligne entre chacune. Le `+ "\n"` final garantit que le fichier se termine par un retour à la ligne.

```python
f_out: IO[str] = open(new_name, "w")
f_out.write(new_content)
f_out.close()
```

---

### Ex2 — `ft_stream_management`

Fonctionnellement identique à ex1. La différence : toutes les sorties passent explicitement par `sys.stdout.write()`, les erreurs par `sys.stderr.write()`, et la saisie par `sys.stdin.readline()`. Cet exercice montre les flux standards bruts, sans l'abstraction de `print()` et `input()`.

**Comment ça marche :**

> **`sys.stdout` / `sys.stderr` / `sys.stdin`** — Les trois flux standards Unix. `stdout` : sortie normale, redirigeable avec `> fichier.txt`. `stderr` : erreurs, toujours visible même si `stdout` est redirigé. `stdin` : entrée, par défaut le clavier.

> **`sys.stdout.flush()`** — Force l'envoi du buffer vers le terminal immédiatement. Nécessaire avant une saisie `readline()` pour que le prompt s'affiche avant que le programme n'attende.

> **`sys.stdin.readline().rstrip("\n")`** — Lit une ligne depuis l'entrée standard. Contrairement à `input()`, elle inclut le `\n` final — `.rstrip("\n")` l'enlève.

```python
sys.stdout.write("Enter new file name (or empty): ")
sys.stdout.flush()
new_name: str = sys.stdin.readline().rstrip("\n")
```

**Pourquoi distinguer stdout et stderr ?** Si tu fais `python3 ex2.py fichier.txt > résultat.txt`, la sortie normale va dans `résultat.txt` mais les messages d'erreur restent visibles dans le terminal — parce qu'ils passent par `stderr`, non redirigé.

---

### Ex3 — `ft_vault_security`

`secure_archive` encapsule les opérations fichier dans une fonction réutilisable qui ne lève jamais d'exception vers l'appelant — elle retourne toujours un tuple `(succès, données_ou_message)`. Elle utilise `with` pour garantir la fermeture du fichier dans tous les cas.

**Comment ça marche :**

> **`with open(...) as f:`** — Le **gestionnaire de contexte**. À la sortie du bloc `with` — qu'il soit normal ou qu'une exception se produise — Python appelle automatiquement `f.close()`. C'est la façon recommandée de gérer les fichiers : on ne peut plus oublier de fermer.

```python
# Avant (ex0 style) — risqué si une exception se produit entre open et close
f = open(filename)
content = f.read()   # si ça plante ici, f.close() n'est jamais appelé
f.close()

# Après (with) — fermeture garantie
with open(filename) as f:
    content = f.read()   # même si ça plante, f est fermé en sortant du with
```

> **`tuple[bool, str]`** — Type de retour qui encode succès/échec dans la valeur elle-même, sans lever d'exception. L'appelant peut déstructurer : `success, data = secure_archive(filename)`.

```python
def secure_archive(filename: str, action: int = 0, content: str = "") -> tuple[bool, str]:
    if action == 0:
        try:
            with open(filename) as f:
                data: str = f.read()
            return (True, data)
        except OSError as e:
            return (False, str(e))
    else:
        try:
            with open(filename, "w") as f:
                f.write(content)
            return (True, "Content successfully written to file")
        except OSError as e:
            return (False, str(e))
```

---

## 🚀 Comment tester

```bash
cd module_04
echo -e "Ligne 1\nLigne 2\nLigne 3" > test.txt

python3 ex0/ft_ancient_text.py test.txt
# Affiche le contenu entre ---

python3 ex0/ft_ancient_text.py inexistant.txt
# Error opening file 'inexistant.txt': ...  (exit code 1)

python3 ex1/ft_archive_creation.py test.txt
# Affiche contenu + version avec # en fin de ligne, propose de sauvegarder

python3 ex2/ft_stream_management.py test.txt 2>erreurs.txt
# stdout normal, stderr redirigé vers erreurs.txt

python3 ex3/ft_vault_security.py
# (False, "No such file or directory")
# (True, contenu du fichier)
# (True, "Content successfully written to file")
```
