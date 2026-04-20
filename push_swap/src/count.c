/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   count.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/17 09:13:02 by arde-ass          #+#    #+#             */
/*   Updated: 2026/04/17 17:13:03 by ccolnat          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

ssize_t	count_r(ssize_t instruct, ssize_t mode)
{
	static ssize_t	ra;
	static ssize_t	rb;
	static ssize_t	rr;

	if (mode == 0)
	{
		if (instruct == 6)
			ra++;
		else if (instruct == 7)
			rb++;
		else if (instruct == 8)
			rr++;
		return (0);
	}
	else if (mode == 1)
	{
		if (instruct == 6)
			return (ra);
		else if (instruct == 7)
			return (rb);
		else if (instruct == 8)
			return (rr);
	}
	return (0);
}

ssize_t	count_rr(ssize_t instruct, ssize_t mode)
{
	static ssize_t	rra;
	static ssize_t	rrb;
	static ssize_t	rrr;

	if (mode == 0)
	{
		if (instruct == 9)
			rra++;
		else if (instruct == 10)
			rrb++;
		else if (instruct == 11)
			rrr++;
		return (0);
	}
	else if (mode == 1)
	{
		if (instruct == 9)
			return (rra);
		else if (instruct == 10)
			return (rrb);
		else if (instruct == 11)
			return (rrr);
	}
	return (0);
}

ssize_t	count_s(ssize_t instruct, ssize_t mode)
{
	static ssize_t	sa;
	static ssize_t	sb;
	static ssize_t	ss;

	if (mode == 0)
	{
		if (instruct == 1)
			sa++;
		else if (instruct == 2)
			sb++;
		else if (instruct == 3)
			ss++;
		return (0);
	}
	else if (mode == 1)
	{
		if (instruct == 1)
			return (sa);
		else if (instruct == 2)
			return (sb);
		else if (instruct == 3)
			return (ss);
	}
	return (0);
}

ssize_t	count_p(ssize_t instruct, ssize_t mode)
{
	static ssize_t	pa;
	static ssize_t	pb;

	if (mode == 0)
	{
		if (instruct == 4)
			pa++;
		else if (instruct == 5)
			pb++;
		return (0);
	}
	else if (mode == 1)
	{
		if (instruct == 4)
			return (pa);
		else if (instruct == 5)
			return (pb);
	}
	return (0);
}

ssize_t	parse_count(ssize_t instruct, ssize_t mode)
{
	if ((instruct == 6) || (instruct == 7) || (instruct == 8))
		return (count_r(instruct, mode));
	else if ((instruct == 9) || (instruct == 10) || (instruct == 11))
		return (count_rr(instruct, mode));
	else if ((instruct == 1) || (instruct == 2) || (instruct == 3))
		return (count_s(instruct, mode));
	else if ((instruct == 4) || (instruct == 5))
		return (count_p(instruct, mode));
	return (0);
}
