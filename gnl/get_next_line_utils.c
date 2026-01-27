/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <arde-ass@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/10 02:19:30 by arde-ass          #+#    #+#             */
/*   Updated: 2026/01/21 10:39:26 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

size_t	gnl_strlen(const char *s)
{
	size_t	i;

	i = 0;
	while (s && s[i])
		i++;
	return (i);
}

char	*gnl_strdup(const char *s)
{
	size_t	i;
	char	*dup;

	dup = malloc(gnl_strlen(s) + 1);
	if (!dup)
		return (NULL);
	i = 0;
	while (s[i])
	{
		dup[i] = s[i];
		i++;
	}
	dup[i] = 0;
	return (dup);
}

char	*gnl_strjoin(char *s1, char *s2)
{
	size_t	i;
	size_t	j;
	char	*res;

	if (!s1 && s2)
		return (gnl_strdup(s2));
	res = malloc(gnl_strlen(s1) + gnl_strlen(s2) + 1);
	if (!res)
	{
		free(s1);
		return (NULL);
	}
	i = -1;
	j = 0;
	while (s1 && s1[++i])
		res[j++] = s1[i];
	i = -1;
	while (s2 && s2[++i])
		res[j++] = s2[i];
	res[j] = 0;
	free(s1);
	return (res);
}

char	*gnl_substr(char *s, size_t start, size_t len)
{
	size_t	i;
	char	*out;

	if (!s || start >= gnl_strlen(s))
		return (NULL);
	if (len > gnl_strlen(s + start))
		len = gnl_strlen(s + start);
	out = malloc(len + 1);
	if (!out)
		return (NULL);
	i = 0;
	while (i < len)
	{
		out[i] = s[start + i];
		i++;
	}
	out[i] = 0;
	return (out);
}
