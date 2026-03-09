/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_puthexa.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <arde-ass@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/09 11:27:50 by arde-ass          #+#    #+#             */
/*   Updated: 2025/12/09 11:51:30 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../ft_printf.h"

int	ft_puthexa(unsigned int nbr, char *base)
{
	char	*hexa;
	int		len;

	hexa = convert_base((unsigned long long)nbr, base);
	if (!hexa)
		return (-1);
	len = ft_putstr(hexa);
	free(hexa);
	return (len);
}
