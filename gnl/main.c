#include "get_next_line.h"
#include <fcntl.h>
#include <stdio.h>

int	main(void)
{
	int		fd;
	char	*line;

	// Ouvre un fichier (assure-toi d'avoir un fichier test.txt ou change le nom)
	// Tu peux aussi tester avec 0 pour l'entrée standard
	fd = open("test.txt", O_RDONLY);
	if (fd == -1)
	{
		printf("Erreur d'ouverture du fichier\n");
		return (1);
	}

	while (1)
	{
		line = get_next_line(fd);
		if (line == NULL)
			break ;
		printf("%s", line);
		free(line); // C'est ici qu'on vérifie si tu as bien tout free
	}
	close(fd);
	return (0);
}