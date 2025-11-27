/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_iterative_factorial.c                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/17 02:29:09 by arde-ass          #+#    #+#             */
/*   Updated: 2025/07/21 17:59:03 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_iterative_factorial(int nb)
{
	int	total;
	int	index;

	total = 1;
	index = 1;
	if (nb < 0)
		return (0);
	if (nb == 0)
		return (1);
	while (index <= nb)
	{
		total = total * index;
		index++;
	}
	return (total);
}
