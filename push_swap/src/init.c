/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/12 11:08:18 by ccolnat           #+#    #+#             */
/*   Updated: 2026/04/18 13:50:22 by ccolnat          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static ssize_t	check_dup(char **list)
{
	ssize_t	i;
	ssize_t	j;

	j = 0;
	while (list[j] != NULL)
	{
		i = j + 1;
		while (list[i] != NULL)
		{
			if (ft_strcmp(list[i], list[j]) != -1)
				return (-1);
			i++;
		}
		j++;
	}
	return (1);
}

static ssize_t	check_list(char **list)
{
	ssize_t	i;
	ssize_t	nb;

	i = 0;
	if (check_dup(list) == -1)
		return (debugg(6));
	while (list[i] != NULL)
	{
		if (ft_strlen(list[i]) > 11)
			return (debugg(7));
		nb = ft_atoi(list[i]);
		if (nb > 2147483647 || nb < -2147483648)
			return (debugg(7));
		i++;
	}
	return (1);
}

static void	init_list(t_stack **stack_a, t_stack **stack_b, char **list)
{
	ssize_t	list_size;

	list_size = 0;
	while (list[list_size])
		list_size++;
	*stack_a = fill_value(list, list_size);
	*stack_b = NULL;
	fill_index(*stack_a, list_size);
	return ;
}

void	init(char	*raw_str, t_stack **stack_a, t_stack **stack_b)
{
	char	*clean_str;
	char	**list;
	ssize_t	i;

	i = 0;
	clean_str = clean_list(raw_str);
	list = split(clean_str, ' ');
	free(clean_str);
	if (check_list(list) == -1)
	{
		while (list[i] != NULL)
		{
			free(list[i]);
			i++;
		}
		free(list);
		exit(1);
	}
	init_list(stack_a, stack_b, list);
	while (list[i] != NULL)
	{
		free(list[i]);
		i++;
	}
	free(list);
}
