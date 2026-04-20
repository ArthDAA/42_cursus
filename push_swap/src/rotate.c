/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rotate.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/14 04:41:01 by arde-ass          #+#    #+#             */
/*   Updated: 2026/04/17 14:38:09 by ccolnat          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	rotate(t_stack **head)
{
	if (!head || !*head || (*head)->next == *head)
		return ;
	*head = (*head)->next;
}

void	ra(t_stack **a)
{
	rotate(a);
	write_instruct(6, 0);
}

void	rb(t_stack **b)
{
	rotate(b);
	write_instruct(7, 0);
}

void	rr(t_stack **a, t_stack **b)
{
	rotate(a);
	rotate(b);
	write_instruct(8, 0);
}
