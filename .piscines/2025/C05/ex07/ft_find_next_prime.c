/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_find_next_prime.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/17 22:56:31 by arde-ass          #+#    #+#             */
/*   Updated: 2025/07/17 22:58:37 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_find_next_prime(int nb)
{
	int	i;

	i = nb - 1;
	if (nb < 2)
		return (ft_find_next_prime(nb + 1));
	while (i > 1)
	{
		if (nb % i == 0)
			return (ft_find_next_prime(nb + 1));
		i--;
	}
	return (nb);
}
