/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   medium_sort.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/03 13:48:57 by arde-ass          #+#    #+#             */
/*   Updated: 2026/04/16 10:01:10 by ccolnat          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static ssize_t	ft_sqrt(ssize_t number)
{
	ssize_t	i;

	if (number < 0)
		return (0);
	i = 1;
	while (i * i <= number)
		i++;
	return (i - 1);
}

static void	push_chunks_to_b(t_stack **a, t_stack **b, ssize_t size)
{
	ssize_t	chunk;
	ssize_t	i;

	chunk = ft_sqrt(size) + (size / 100);
	i = 0;
	while (*a)
	{
		if ((*a)->index <= i)
		{
			pb(a, b);
			rb(b);
			i++;
		}
		else if ((*a)->index <= i + chunk)
		{
			pb(a, b);
			i++;
		}
		else
		{
			ra(a);
		}
	}
}

t_stack	*medium_sort(t_stack *head)
{
	t_stack	*stack_b;
	t_stack	*max_node;
	ssize_t	size;

	stack_b = NULL;
	size = get_stack_size(head);
	push_chunks_to_b(&head, &stack_b, size);
	while (stack_b)
	{
		size = get_stack_size(stack_b);
		max_node = get_max_node(stack_b);
		if (direction(stack_b, max_node->index, size / 2))
			while (stack_b != max_node)
				rb(&stack_b);
		else
			while (stack_b != max_node)
				rrb(&stack_b);
		pa(&head, &stack_b);
	}
	return (head);
}
