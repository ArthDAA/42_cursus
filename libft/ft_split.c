/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <arde-ass@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/20 21:30:13 by arde-ass          #+#    #+#             */
/*   Updated: 2025/11/23 18:45:11 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static size_t	skip_sep(const char *s, char c, size_t i)
{
	while (s[i] != '\0' && s[i] == c)
		i++;
	return (i);
}

static size_t	word_len(const char *s, char c, size_t i)
{
	size_t	len;

	len = 0;
	while (s[i + len] != '\0' && s[i + len] != c)
		len++;
	return (len);
}

static void	free_tab(char **tab, size_t n)
{
	while (n > 0)
	{
		n--;
		free(tab[n]);
	}
	free(tab);
}

char	**ft_split(const char *s, char c)
{
	char	**tab;
	size_t	i;
	size_t	j;
	size_t	len;

	tab = (char **)malloc((ft_strlen(s) + 1) * sizeof(char *));
	if (tab == NULL)
		return (NULL);
	i = 0;
	j = 0;
	while (s[i] != '\0')
	{
		i = skip_sep(s, c, i);
		if (s[i] != '\0')
		{
			len = word_len(s, c, i);
			tab[j] = ft_substr(s, i, len);
			if (tab[j] == NULL)
				return (free_tab(tab, j), NULL);
			j++;
			i += len;
		}
	}
	tab[j] = NULL;
	return (tab);
}
