/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putuns.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <arde-ass@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/08 10:36:58 by arde-ass          #+#    #+#             */
/*   Updated: 2025/12/09 08:28:58 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ftprintf.h"

int	ft_putuns(unsigned int nbr)
{
	int	count;

	count = 0;
	if (nbr >= 10)
		count += ft_putuns(nbr / 10);
	count += ft_putchar((nbr % 10) + '0');
	return (count);
}
