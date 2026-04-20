/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   simple_sort.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/24 07:15:57 by arde-ass          #+#    #+#             */
/*   Updated: 2026/04/16 11:33:49 by ccolnat          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	sort_three(t_stack **head)
{
	t_stack	*max_node;

	if (!head || !*head || (*head)->next == *head
		|| (*head)->next->next == *head)
		return ;
	max_node = get_max_node(*head);
	if (*head == max_node)
		ra(head);
	else if ((*head)->next == max_node)
		rra(head);
	if ((*head)->index > (*head)->next->index)
		sa(head);
}

static void	push_to_b(t_stack **a, t_stack **b, int target, int size)
{
	if (direction(*a, target, size / 2))
	{
		while ((*a)->index != (ssize_t)target)
			ra(a);
	}
	else
	{
		while ((*a)->index != (ssize_t)target)
			rra(a);
	}
	pb(a, b);
}

t_stack	*simple_sort(t_stack *head)
{
	t_stack	*stack_b;
	int		size;
	int		target;

	stack_b = NULL;
	target = 0;
	size = get_stack_size(head);
	if (size == 2 && head->index > head->next->index)
		sa(&head);
	if (size <= 2)
		return (head);
	while (size > 3)
	{
		push_to_b(&head, &stack_b, target++, size--);
	}
	sort_three(&head);
	while (stack_b)
		pa(&head, &stack_b);
	return (head);
}
