/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/13 11:42:23 by ccolnat           #+#    #+#             */
/*   Updated: 2026/04/16 09:45:20 by ccolnat          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	free_stack(t_stack **stack)
{
	t_stack	*tmp;
	t_stack	*next;

	if (!stack || !*stack)
		return ;
	tmp = *stack;
	(*stack)->prev->next = NULL;
	while (tmp)
	{
		next = tmp->next;
		free(tmp);
		tmp = next;
	}
	*stack = NULL;
}

int	main(int argc, char **argv)
{
	ssize_t	strategy;
	t_stack	*stack_a;
	t_stack	*stack_b;
	char	*raw_str;

	strategy = check_flags(argc, argv);
	if (strategy == -1)
		return (1);
	raw_str = extract_str(argc, argv);
	if (char_check(raw_str) == -1)
	{
		free(raw_str);
		return (1);
	}
	init(raw_str, &stack_a, &stack_b);
	push_swap(&stack_a, strategy);
	free_stack(&stack_a);
	return (0);
}
