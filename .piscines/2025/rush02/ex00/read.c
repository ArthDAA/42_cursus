/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   read.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/27 16:28:06 by arde-ass          #+#    #+#             */
/*   Updated: 2025/07/27 20:47:30 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include "main.h"

int	allocate_data(char *str)
{
	int	i;

	i = 0;
	if (ft_is_number(str[i]) == 1)
	{
		while (ft_is_number(str[i]) == 1)
		{
			i++;
		}
		return (i);
	}
	else
	{
		while (ft_is_alpha(str[i]) == 1)
		{
			i++;
		}
		return (i);
	}
}

int	allocate_array(char *str)
{
	int	i;
	int	lines;

	i = 0;
	lines = 0;
	while (str[i] != '\0')
	{
		if (ft_is_number(str[i]) == 1 && ft_is_number(str[i + 1]))
		{
			lines++;
		}
		i++;
	}
	return(i);
}

t_dict_entry	*make_struct(char *str)
{
	int				i;
	int				j;
	t_dict_entry	*dictionary;

	i = 0;
	j = 0;
	i = 0;

	dictionary = malloc(sizeof(t_dict_entry) * allocate_array(str));
	while (str[i] != '\0')
	{
		if (ft_is_number(str[i] == 1))
		{
			dictionary[j].nb = malloc(sizeof(char) * allocate_data(&str[i]));
			ft_strcpy_nb(dictionary[j].nb, &str[i]);
		}
		if (ft_is_alpha(str[i] == 1))
		{
			dictionary[j].value = malloc(sizeof(char) * allocate_data(&str[i]));
			ft_strcpy_value(dictionary[j].value, &str[i]);
			j++;
		}
		i++;
	}
	return (dictionary);
}

t_dict_entry	*set_struct(char *file_to_parse)
{
	char	buffer[2000];
	int	nb_read;
	int	bytes;

	nb_read = open(file_to_parse, O_RDONLY);
	
	read(nb_read, buffer, 1999);
	buffer[2000] = '\0';
	return (make_struct(buffer));
}
