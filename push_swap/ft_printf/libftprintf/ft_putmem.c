/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putmem.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <arde-ass@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/04 05:15:06 by arde-ass          #+#    #+#             */
/*   Updated: 2025/12/09 09:56:41 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../ft_printf.h"

int	ft_putmem(void *ptr)
{
	char	*hexa;
	int		len;

	if (!ptr)
		return (ft_putstr("(nil)"));
	hexa = convert_base((unsigned long long)ptr, LOW_HEX);
	if (!hexa)
		return (-1);
	ft_putstr("0x");
	len = 2 + ft_putstr(hexa);
	free(hexa);
	return (len);
}
