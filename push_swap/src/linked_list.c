/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   linked_list.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/04 07:25:24 by ccolnat           #+#    #+#             */
/*   Updated: 2026/04/18 14:07:08 by ccolnat          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_stack	*fill_value(char **list, ssize_t list_size)
{
	t_stack	*stack_a;
	ssize_t	nb;
	ssize_t	i;

	stack_a = NULL;
	i = 0;
	while (i < list_size)
	{
		nb = ft_atoi(list[i]);
		add_bottom(&stack_a, new_stack(nb));
		i++;
	}
	return (stack_a);
}

static t_stack	*get_highest_unindexed(t_stack *stack)
{
	t_stack	*ptr;
	t_stack	*highest;

	ptr = stack;
	highest = NULL;
	while (ptr)
	{
		if (ptr->index == 0)
		{
			if (highest == NULL || ptr->value > highest->value)
				highest = ptr;
		}
		ptr = ptr->next;
		if (ptr == stack)
			break ;
	}
	return (highest);
}

void	fill_index(t_stack *stack, ssize_t list_size)
{
	t_stack	*ptr;
	t_stack	*highest;
	ssize_t	current_idx;

	if (!stack)
		return ;
	current_idx = list_size - 1;
	while (list_size > 0)
	{
		highest = get_highest_unindexed(stack);
		if (highest != NULL)
			highest->index = current_idx + 1;
		current_idx--;
		list_size--;
	}
	ptr = stack;
	while (ptr)
	{
		ptr->index -= 1;
		ptr = ptr->next;
		if (ptr == stack)
			break ;
	}
}
