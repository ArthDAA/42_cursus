# Get Next Line

**Get Next Line** est un projet de programmation en C (cursus 42) dont l'objectif est de développer une fonction capable de lire le contenu d'un fichier (via un *file descriptor*) ligne par ligne, quelle que soit la taille du tampon de lecture.

## Fonctionnalités

* **Lecture ligne par ligne :** Retourne une ligne complète terminée par `\n` à chaque appel.
* **Gestion de buffer dynamique :** La taille du tampon de lecture est définie à la compilation via `-D BUFFER_SIZE=n`.
* **Persistance des données :** Utilise une variable statique pour conserver les caractères lus mais non encore retournés entre deux appels.
* **Gestion de la mémoire :** Assure la libération propre de la mémoire en cas d'erreur ou de fin de fichier.

## Architecture & Logique

Le fonctionnement de la fonction repose sur trois étapes principales orchestrées autour d'une variable **statique** (`stash`).

### 1. La Variable Statique (`stash`)
Contrairement aux variables locales standard, la variable `static char *stash` conserve son contenu entre les appels successifs de la fonction. Elle sert de "mémoire" pour stocker les fragments de texte lus qui dépassent la ligne actuelle (le reste après le `\n`).

### 2. La Boucle de Lecture
La fonction `get_next_line` commence par vérifier si la `stash` contient déjà un saut de ligne. Si ce n'est pas le cas, elle entre dans une boucle de lecture :
1.  Un tampon temporaire (`buf`) est alloué selon `BUFFER_SIZE`.
2.  La fonction `read()` récupère un bloc de données du fichier.
3.  Ce bloc est immédiatement fusionné avec la `stash` existante via `gnl_strjoin`.
    * *Note technique :* `gnl_strjoin` dans ce projet est conçu pour libérer automatiquement la mémoire de l'ancienne `stash` (`s1`) après la fusion, évitant ainsi les fuites de mémoire dans la boucle.
4.  La boucle s'interrompt dès qu'un `\n` est détecté dans la `stash` ou que la fin du fichier (EOF) est atteinte.

### 3. L'Extraction de la Ligne
Une fois la lecture terminée (ou si la `stash` contenait déjà un `\n`), la fonction `extract_line` est appelée :
1.  Elle localise le premier `\n`.
2.  Elle copie tout ce qui précède le `\n` (inclus) dans la variable de retour (`line`).
3.  Elle sauvegarde tout ce qui suit le `\n` dans une nouvelle chaîne (`rest`) qui remplace l'ancienne `stash`.
4.  Si aucun `\n` n'est trouvé (fin de fichier sans saut de ligne), tout le contenu de la `stash` est retourné.

## Structure des Fichiers

* **`get_next_line.c`** : Contient la fonction principale `get_next_line`, la boucle de lecture et la logique d'extraction de ligne.
* **`get_next_line_utils.c`** : Contient les fonctions utilitaires nécessaires à la manipulation des chaînes (`gnl_strlen`, `gnl_strdup`, `gnl_strjoin`, `gnl_substr`).
* **`get_next_line.h`** : Fichier d'en-tête contenant les prototypes des fonctions et la définition de la macro `BUFFER_SIZE`.

## Utilisation

### Compilation

Pour utiliser `get_next_line` dans votre projet, compilez vos fichiers avec l'option `-D BUFFER_SIZE=xx` (où xx est la taille du tampon souhaitée). Si omis, la taille par défaut est 10.

```bash
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 main.c get_next_line.c get_next_line_utils.c -o gnl
```

Voici également joint un main de démonstration pour tester ce projet.

```c
#include "get_next_line.h"
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int     fd;
    char    *line;

    fd = open("fichier.txt", O_RDONLY);
    if (fd == -1)
        return (1);
    
    while ((line = get_next_line(fd)))
    {
        printf("%s", line);
        free(line);
    }
    
    close(fd);
    return (0);
}
```