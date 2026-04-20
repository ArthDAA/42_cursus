/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_moves.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/17 15:22:21 by arde-ass          #+#    #+#             */
/*   Updated: 2026/04/17 17:15:12 by ccolnat          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	parse_write(ssize_t instruct)
{
	if (instruct == 1)
		write(1, "sa\n", 3);
	if (instruct == 2)
		write(1, "sb\n", 3);
	if (instruct == 3)
		write(1, "ss\n", 3);
	if (instruct == 4)
		write(1, "pa\n", 3);
	if (instruct == 5)
		write(1, "pb\n", 3);
	if (instruct == 6)
		write(1, "ra\n", 3);
	if (instruct == 7)
		write(1, "rb\n", 3);
	if (instruct == 8)
		write(1, "rr\n", 3);
	if (instruct == 9)
		write(1, "rra\n", 4);
	if (instruct == 10)
		write(1, "rrb\n", 4);
	if (instruct == 11)
		write(1, "rrr\n", 4);
}

void	write_instruct(ssize_t instruct, ssize_t mode)
{
	static ssize_t	count_state;

	if (mode == -1)
	{
		count_state = 1;
		return ;
	}
	parse_write(instruct);
	if (count_state == 1)
		parse_count(instruct, mode);
}

void	put_bench(void)
{
	ssize_t	arr[11];
	ssize_t	total;
	ssize_t	i;

	total = 0;
	i = 1;
	while (i <= 11)
	{
		arr[i - 1] = parse_count(i, 1);
		total += arr[i - 1];
		i++;
	}
	ft_printf("[bench] total_ops: %d\n", total);
	ft_printf("[bench] sa: %d sb: %d ss: %d pa: %d pb: %d\n", arr[0], arr[1],
		arr[2], arr[3], arr[4]);
	ft_printf("[bench] ra: %d rb: %d rr: %d rra: %d rrb: %d rrr: %d\n", arr[5],
		arr[6], arr[7], arr[8], arr[9], arr[10]);
}
