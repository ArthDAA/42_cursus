/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rev_rotate.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/14 04:42:30 by arde-ass          #+#    #+#             */
/*   Updated: 2026/04/17 14:40:25 by ccolnat          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	rev_rotate(t_stack **head)
{
	if (!head || !*head || (*head)->next == *head)
		return ;
	*head = (*head)->prev;
}

void	rra(t_stack **a)
{
	rev_rotate(a);
	write_instruct(9, 0);
}

void	rrb(t_stack **b)
{
	rev_rotate(b);
	write_instruct(10, 0);
}

void	rrr(t_stack **a, t_stack **b)
{
	rev_rotate(a);
	rev_rotate(b);
	write_instruct(11, 0);
}
