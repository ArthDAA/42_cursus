/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   split.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/13 10:24:46 by ccolnat           #+#    #+#             */
/*   Updated: 2026/04/10 08:12:27 by ccolnat          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	ft_count_words(const char *str, char c)
{
	int	nb_word;
	int	new_word;
	int	i;

	nb_word = 0;
	i = 0;
	new_word = 0;
	while (str[i] != '\0')
	{
		if (str[i] != c && new_word == 0)
		{
			new_word = 1;
			nb_word++;
		}
		else if (str[i] == c)
			new_word = 0;
		i++;
	}
	return (nb_word);
}

static char	*ft_alloc_word(char const *str, char c)
{
	int		len;
	char	*word;
	int		i;

	len = 0;
	while (str[len] != '\0' && str[len] != c)
		len++;
	word = (char *)malloc(sizeof(char) * (len + 1));
	if (word == NULL)
		return (NULL);
	i = 0;
	while (i < len)
	{
		word[i] = str[i];
		i++;
	}
	word[len] = '\0';
	return (word);
}

static int	ft_add_word(char **tab, int i, char const *str, char c)
{
	tab[i] = ft_alloc_word(str, c);
	if (tab[i] == NULL)
	{
		i--;
		while (i >= 0)
		{
			free(tab[i]);
			i--;
		}
		free(tab);
		return (0);
	}
	return (1);
}

static void	go_to_next(const char *str, int *j, char c)
{
	while (str[*j] != '\0' && str[*j] != c)
		(*j)++;
}

char	**split(char *str, char c)
{
	char	**tab;
	int		i;
	int		j;

	j = 0;
	if (str == NULL)
		return (NULL);
	tab = (char **)malloc(sizeof(char *) * (ft_count_words(str, c) + 1));
	if (tab == NULL)
		return (NULL);
	i = 0;
	while (str[j] != '\0')
	{
		while (str[j] != '\0' && str[j] == c)
			j++;
		if (str[j] != '\0')
		{
			if (ft_add_word(tab, i, &str[j], c) == 0)
				return (NULL);
			i++;
			go_to_next(str, &j, c);
		}
	}
	tab[i] = NULL;
	return (tab);
}
