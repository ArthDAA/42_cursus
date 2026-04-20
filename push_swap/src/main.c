/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/13 11:42:23 by ccolnat           #+#    #+#             */
/*   Updated: 2026/04/18 13:59:23 by ccolnat          ###   ########.fr       */
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

static ssize_t	is_bench(char **argv)
{
	ssize_t	i;
	ssize_t	j;
	ssize_t	checker;

	i = 1;
	checker = 0;
	{
		while (argv[i] != NULL)
		{
			if ((argv[i][0] == '-') && (argv[i][1] == '-'))
			{
				if (ft_strcmp(argv[i], "--bench") == 1)
				{
					j = i;
					checker++;
				}
			}
			i++;
		}
		if (checker > 1)
			return (debugg(2));
		else if (checker == 1)
			return (j);
		return (0);
	}
}

int	main(int argc, char **argv)
{
	ssize_t	strategy;
	ssize_t	bench;
	t_stack	*stack_a;
	t_stack	*stack_b;
	char	*raw_str;

	bench = is_bench(argv);
	if (bench == -1)
		return (1);
	strategy = check_flags(argc, argv, bench);
	if (strategy == -1)
		return (1);
	raw_str = extract_str(argc, argv, bench);
	if (char_check(raw_str) == -1)
	{
		free(raw_str);
		return (1);
	}
	init(raw_str, &stack_a, &stack_b);
	push_swap(&stack_a, strategy, bench);
	if (bench > 0)
		put_bench();
	free_stack(&stack_a);
	return (0);
}
