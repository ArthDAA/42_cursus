/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <arde-ass@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/10 02:19:32 by arde-ass          #+#    #+#             */
/*   Updated: 2026/01/23 15:39:41 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

static int	find_nl(char *s)
{
	int	i;

	i = 0;
	while (s && s[i])
	{
		if (s[i] == '\n')
			return (i);
		i++;
	}
	return (-1);
}

static char	*extract_line(char **stash)
{
	int		nl;
	char	*line;
	char	*rest;

	if (!*stash || **stash == 0)
	{
		if (*stash)
			free(*stash);
		*stash = NULL;
		return (NULL);
	}
	nl = find_nl(*stash);
	if (nl >= 0)
	{
		line = gnl_substr(*stash, 0, nl + 1);
		rest = gnl_strdup(*stash + nl + 1);
		free(*stash);
		*stash = rest;
		return (line);
	}
	line = gnl_strdup(*stash);
	free(*stash);
	*stash = NULL;
	return (line);
}

char	*get_next_line(int fd)
{
	char		*buf;
	static char	*stash = NULL;
	int			r;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (NULL);
	buf = malloc(sizeof(char) * (BUFFER_SIZE + 1));
	if (!buf)
		return (NULL);
	r = read(fd, buf, BUFFER_SIZE);
	while (r > 0)
	{
		buf[r] = 0;
		stash = gnl_strjoin(stash, buf);
		if (find_nl(stash) >= 0)
			break ;
		r = read(fd, buf, BUFFER_SIZE);
	}
	free(buf);
	if (r < 0)
		return (free(stash), stash = NULL, NULL);
	return (extract_line(&stash));
}
