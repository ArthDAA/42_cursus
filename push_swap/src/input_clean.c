/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   input_clean.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/12 11:05:52 by ccolnat           #+#    #+#             */
/*   Updated: 2026/04/18 13:57:51 by ccolnat          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static ssize_t	clean_string(char *clean_list, const char *list)
{
	ssize_t	i;
	ssize_t	j;

	i = 0;
	j = 0;
	while (list[i] == ' ')
		i++;
	while (list[i] != '\0')
	{
		if (list[i] != ' ' && list[i + 1] == '-')
			return (-1);
		if ((list[i] == '-' && list[i + 1] == '\0') || (list[i] == '-' && list[i
					+ 1] == ' ') || (list[i] == ' ' && list[i + 1] == ' ')
			|| (list[i] == ' ' && list[i + 1] == '\0'))
			i++;
		else
		{
			clean_list[j] = list[i];
			j++;
			i++;
		}
	}
	clean_list[j] = '\0';
	return (j);
}

char	*clean_list(char *raw_str)
{
	char	*tmp;
	char	*clean_str;
	ssize_t	len;

	len = ft_strlen(raw_str);
	tmp = malloc(sizeof(char) * len + 1);
	tmp[len] = '\0';
	len = clean_string(tmp, raw_str);
	if (len == -1)
	{
		free(tmp);
		free(raw_str);
		debugg(5);
		exit(1);
	}
	clean_str = malloc(sizeof(char) * len + 1);
	clean_string(clean_str, tmp);
	free(tmp);
	free(raw_str);
	return (clean_str);
}

static void	ft_strcpy(char *dest, const char *src)
{
	ssize_t	i;
	ssize_t	j;

	j = 0;
	i = 0;
	while (dest[j] != '\0')
		j++;
	while ((src[i] != '\0'))
	{
		dest[j] = src[i];
		i++;
		j++;
	}
	dest[j] = ' ';
	j++;
	dest[j] = '\0';
}

static	ssize_t	total_size(char **argv)
{
	ssize_t	i;
	ssize_t	j;
	ssize_t	total_len;

	j = 1;
	total_len = 0;
	while (argv[j])
	{
		i = 0;
		while (argv[j][i])
		{
			total_len++;
			i++;
		}
		j++;
		total_len++;
	}
	return (total_len);
}

char	*extract_str(int argc, char **argv, ssize_t	bench)
{
	ssize_t	flag_index;
	ssize_t	i;
	ssize_t	total_len;
	char	*raw_str;

	i = 1;
	flag_index = find_flag(argv, bench);
	total_len = total_size(argv);
	raw_str = malloc(sizeof(char) * total_len + argc + 1);
	raw_str[0] = '\0';
	raw_str[total_len + argc] = '\0';
	while (argv[i] != NULL)
	{
		if ((i == flag_index) || (i == bench))
			i++;
		else
		{
			ft_strcpy(raw_str, argv[i]);
			i++;
		}
	}
	return (raw_str);
}
