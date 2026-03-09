/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   convert_base.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <arde-ass@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/04 05:15:06 by arde-ass          #+#    #+#             */
/*   Updated: 2025/12/09 11:13:12 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../ft_printf.h"

int	length(unsigned long long value, int base)
{
	int	len;

	len = 0;
	if (value == 0)
		return (1);
	while (value > 0)
	{
		value /= base;
		len++;
	}
	return (len);
}

char	*convert_base(unsigned long long value, char *table)
{
	int		i;
	char	*out;
	int		base;

	base = ft_strlen(table);
	if (value == 0)
		return (ft_strdup("0"));
	i = length(value, base);
	out = malloc(sizeof(char) * (i + 1));
	if (!out)
		return (NULL);
	out[i--] = '\0';
	while (value > 0)
	{
		out[i] = table[value % base];
		value /= base;
		i--;
	}
	return (out);
}
