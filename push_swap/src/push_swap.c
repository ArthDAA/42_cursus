/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/02 07:34:00 by ccolnat           #+#    #+#             */
/*   Updated: 2026/04/17 15:54:56 by ccolnat          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	print_strat(ssize_t strategy)
{
	if (strategy == 4)
		ft_printf("[bench] strategy: Adaptive");
	else if (strategy == 1)
		ft_printf("[bench] strategy: Simple");
	else if (strategy == 2)
		ft_printf("[bench] strategy: Medium");
	else if (strategy == 3)
		ft_printf("[bench] strategy: Complex");
}

static ssize_t	get_strategy(ssize_t mistakes, ssize_t pairs, ssize_t bench)
{
	float	disorder;
	float	disorder_decimal;

	disorder_decimal = (float)mistakes / (float)pairs;
	disorder = disorder_decimal * 100;
	disorder_decimal = disorder - (ssize_t)disorder;
	disorder_decimal = disorder_decimal * 100;
	if (bench > 0)
	{
		ft_printf("[bench] disorder: %d,%d", (ssize_t)disorder,
			(ssize_t)disorder_decimal);
		write(2, "%\n", 2);
	}
	if ((ssize_t)disorder < 20)
		return (1);
	if ((ssize_t)disorder >= 50)
		return (3);
	return (2);
}

static ssize_t	disorder_level(t_stack *head, ssize_t bench)
{
	ssize_t	mistakes;
	ssize_t	pairs;
	t_stack	*current;
	t_stack	*compare;

	mistakes = 0;
	pairs = 0;
	if (!head || head->next == head)
		return (1);
	current = head;
	while (current->next != head)
	{
		compare = current->next;
		while (compare != head)
		{
			pairs++;
			if (current->value > compare->value)
				mistakes++;
			compare = compare->next;
		}
		current = current->next;
	}
	return (get_strategy(mistakes, pairs, bench));
}

void	push_swap(t_stack **stack_a, ssize_t strategy, ssize_t bench)
{
	if (bench > 0)
	{
		write_instruct(0, -1);
		print_strat(strategy);
	}
	if (strategy == 4)
		strategy = disorder_level(*stack_a, 0);
	if (strategy == 1 && bench > 0)
		ft_printf(" / O(n²)\n");
	if (strategy == 2 && bench > 0)
		ft_printf(" / O(n√n)\n");
	if (strategy == 3 && bench > 0)
		ft_printf(" / O(n log n)\n");
	disorder_level(*stack_a, bench);
	if (is_sorted(*stack_a) != 1)
	{
		if (strategy == 1)
			*stack_a = simple_sort(*stack_a);
		if (strategy == 2)
			*stack_a = medium_sort(*stack_a);
		if (strategy == 3)
			*stack_a = complex_sort(*stack_a);
	}
	if (is_sorted(*stack_a) != 1)
		debugg(8);
}
