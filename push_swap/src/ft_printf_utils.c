/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf_utils.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/14 08:28:44 by ccolnat           #+#    #+#             */
/*   Updated: 2026/04/17 15:52:38 by ccolnat          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	ft_putstr(char *str)
{
	int	i;

	if (!str)
		return (ft_putstr("(null)"));
	i = 0;
	while (str[i] != '\0')
	{
		write(2, &str[i], 1);
		i++;
	}
	return (i);
}

static int	ft_putnbr(int n)
{
	int		count;
	long	nb;

	count = 0;
	nb = n;
	if (nb < 0)
	{
		count += ft_putchar('-');
		nb = -nb;
	}
	if (nb > 9)
		count += ft_putnbr(nb / 10);
	count += ft_putchar((nb % 10) + '0');
	return (count);
}

static int	ft_putunbr(unsigned int n)
{
	int	count;

	count = 0;
	if (n > 9)
		count += ft_putunbr(n / 10);
	count += ft_putchar((n % 10) + '0');
	return (count);
}

int	ft_putchar(char c)
{
	write(2, &c, 1);
	return (1);
}

int	ft_printf_parse(char arg_type, va_list args)
{
	int	count;

	count = 0;
	if (arg_type == '%')
		count += ft_putchar('%');
	else if (arg_type == 'c')
		count += ft_putchar(va_arg(args, int));
	else if (arg_type == 's')
		count += ft_putstr(va_arg(args, char *));
	else if (arg_type == 'd')
		count += ft_putnbr(va_arg(args, int));
	else if (arg_type == 'i')
		count += ft_putnbr(va_arg(args, int));
	else if (arg_type == 'u')
		count += ft_putunbr(va_arg(args, unsigned int));
	return (count);
}
