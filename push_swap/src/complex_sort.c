/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   complex_sort.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/01 17:12:48 by arde-ass          #+#    #+#             */
/*   Updated: 2026/04/16 10:01:01 by ccolnat          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static ssize_t	get_max_bits(t_stack *head)
{
	ssize_t	max_idx;
	ssize_t	max_bits;

	max_idx = get_stack_size(head) - 1;
	max_bits = 0;
	while ((max_idx >> max_bits) != 0)
	{
		max_bits++;
	}
	return (max_bits);
}

static void	process_bit(t_stack **head, t_stack **b, ssize_t s, ssize_t bit)
{
	ssize_t	j;

	j = 0;
	while (j < s)
	{
		if ((((*head)->index >> bit) & 1) == 1)
			ra(head);
		else
			pb(head, b);
		j++;
	}
}

t_stack	*complex_sort(t_stack *head)
{
	t_stack	*stack_b;
	ssize_t	size;
	ssize_t	max_bits;
	ssize_t	i;

	stack_b = NULL;
	size = get_stack_size(head);
	max_bits = get_max_bits(head);
	i = 0;
	while (i < max_bits)
	{
		process_bit(&head, &stack_b, size, i);
		while (stack_b)
			pa(&head, &stack_b);
		i++;
	}
	return (head);
}
