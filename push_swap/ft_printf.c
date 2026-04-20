/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/14 08:28:44 by ccolnat           #+#    #+#             */
/*   Updated: 2026/04/10 08:11:47 by ccolnat          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	ft_printf(const char *input, ...)
{
	va_list	args;
	int		i;
	int		count;

	count = 0;
	i = 0;
	va_start(args, input);
	while (input[i])
	{
		if (input[i] == '%')
			count += ft_printf_parse(input[++i], args);
		else
			count += ft_putchar(input[i]);
		i++;
	}
	return (count);
}
