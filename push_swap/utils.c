/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/12 11:08:07 by ccolnat           #+#    #+#             */
/*   Updated: 2026/04/16 13:17:20 by ccolnat          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

ssize_t	ft_strcmp(const char *s1, const char *s2)
{
	ssize_t	i;

	i = 0;
	if ((s1[0] == '\0') || (s2[0] == '\0'))
		return (-1);
	while ((s1[i] != '\0') || (s2[i] != '\0'))
	{
		if (s1[i] == s2[i])
			i++;
		else if (s1[i] != s2[i])
			return (-1);
	}
	if ((s1[i] == '\0') && (s2[i] == '\0'))
		return (1);
	else
		return (-1);
}

ssize_t	debugg(ssize_t nb)
{
	if (nb == 4)
		return (-1);
	else if (nb >= 0)
		ft_printf("Error\n");
	return (-1);
}

size_t	ft_strlen(char const *str)
{
	size_t	i;

	i = 0;
	while (str[i] != '\0')
	{
		i++;
	}
	return (i);
}

ssize_t	ft_atoi(const char *str)
{
	ssize_t	i;
	ssize_t	sign;
	ssize_t	nb;

	nb = 0;
	sign = 1;
	i = 0;
	if (str[i] == '+' || str[i] == '-')
	{
		if (str[i] == '-')
			sign = -sign;
		i++;
	}
	while (str[i] >= '0' && str[i] <= '9')
	{
		nb = (nb * 10) + (str[i] - '0');
		i++;
	}
	nb = (nb * sign);
	return (nb);
}

int	ft_putchar(char c)
{
	write(2, &c, 1);
	return (1);
}
/*
ssize_t	debugg(ssize_t nb)
{
	if (nb == 0)
		ft_printf("error : arg in list is not a number.\n");
	else if (nb == 1)
		ft_printf("error : instruct is invalid.\n");
	else if (nb == 2)
		ft_printf("error : not exactly one instruct.\n");
	else if (nb == 4)
		ft_printf("error : empty input.\n");
	else if (nb == 5)
		ft_printf("error : no space before '-'.\n");
	else if (nb == 6)
		ft_printf("error : same number found twice in the list\n");
	else if (nb == 7)
		ft_printf("error : number out of range\n");
	else if (nb == 8)
		ft_printf("error : not sorted\n");
	return (-1);
}*/
