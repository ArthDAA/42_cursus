
#include "ftlib.h"
#define BUF_SIZE 1000

char	*ft_get_map(char *map_address)
{
	int		fd;
	char	*buffer;
	int		bytes_read;

	if (map_address == NULL)
	{
		char	*filename = malloc(256);
		int		i = 0;
		char	c;

		if (!filename)
			return (NULL);
		while (read(0, &c, 1) > 0 && c != '\n' && i < 255)
			filename[i++] = c;
		filename[i] = '\0';
		map_address = filename;
		fd = open(map_address, O_RDONLY);
		free(filename);
	}
	else
		fd = open(map_address, O_RDONLY);

	if (fd < 0)
		return (NULL);

	buffer = malloc(BUF_SIZE + 1);
	if (!buffer)
		return (NULL);
	bytes_read = read(fd, buffer, BUF_SIZE);
	if (bytes_read <= 0)
	{
		free(buffer);
		return (NULL);
	}
	buffer[bytes_read] = '\0';
	close(fd);
	printf("%s\n", buffer);
	return (buffer);
}




