/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/14 04:40:19 by arde-ass          #+#    #+#             */
/*   Updated: 2026/04/13 08:22:59 by ccolnat          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	push_to_dest(t_stack **dest, t_stack *node)
{
	if (!dest || !*dest)
	{
		*dest = node;
		(*dest)->next = *dest;
		(*dest)->prev = *dest;
	}
	else
	{
		node->prev = (*dest)->prev;
		node->next = *dest;
		(*dest)->prev->next = node;
		(*dest)->prev = node;
		*dest = node;
	}
}

void	push(t_stack **dest, t_stack **src)
{
	t_stack	*tmp;

	if (!src || !*src)
		return ;
	tmp = *src;
	if (tmp->next == tmp)
		*src = NULL;
	else
	{
		tmp->prev->next = tmp->next;
		tmp->next->prev = tmp->prev;
		*src = tmp->next;
	}
	push_to_dest(dest, tmp);
}

void	pa(t_stack **a, t_stack **b)
{
	push(a, b);
	write(1, "pa\n", 3);
}

void	pb(t_stack **a, t_stack **b)
{
	push(b, a);
	write(1, "pb\n", 3);
}
