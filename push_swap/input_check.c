/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   input_check.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/12 11:05:52 by ccolnat           #+#    #+#             */
/*   Updated: 2026/04/16 09:46:41 by ccolnat          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static ssize_t	find_nb_flag(char **argv)
{
	ssize_t	checker;
	ssize_t	i;

	checker = 0;
	i = 1;
	{
		while (argv[i] != NULL)
		{
			if ((argv[i][0] == '-') && (argv[i][1] == '-'))
				checker++;
			i++;
		}
		return (checker);
	}
}

ssize_t	find_flag(char **argv)
{
	ssize_t	i;

	i = 1;
	{
		while (argv[i] != NULL)
		{
			if ((argv[i][0] == '-') && (argv[i][1] == '-'))
				return (i);
			i++;
		}
		return (0);
	}
}

static ssize_t	parse_instruct(char **argv, ssize_t flag_index)
{
	if (ft_strcmp(argv[flag_index], "--simple") == 1)
		return (1);
	else if (ft_strcmp(argv[flag_index], "--medium") == 1)
		return (2);
	else if (ft_strcmp(argv[flag_index], "--complex") == 1)
		return (3);
	else if (ft_strcmp(argv[flag_index], "--adaptive") == 1)
		return (4);
	else
		return (debugg(1));
}

ssize_t	char_check(char *argv)
{
	int	i;

	i = 0;
	while (argv[i] != '\0')
	{
		if (argv[i] == '-')
			i++;
		else if (argv[i] == ' ')
			i++;
		else if ((argv[i] < '0') || (argv[i] > '9'))
			return (debugg(0));
		else
			i++;
	}
	return (0);
}

ssize_t	check_flags(int argc, char **argv)
{
	ssize_t	flag_index;
	ssize_t	strategy;

	strategy = 4;
	if (argc == 2)
		return (strategy);
	if (argc < 2)
		return (debugg(4));
	if (argc > 2)
	{
		if (find_nb_flag(argv) == 0)
			return (strategy);
		if (find_nb_flag(argv) > 1)
			return (debugg(2));
		flag_index = find_flag(argv);
		return (parse_instruct(argv, flag_index));
	}
	return (-1);
}
