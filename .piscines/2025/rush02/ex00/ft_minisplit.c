/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_minisplit.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/26 19:11:30 by arde-ass          #+#    #+#             */
/*   Updated: 2025/07/27 22:46:50 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

int	num_blocks(char *str)
{
	int	i;
	
	i = 0;
	while (str[i])
		i++;
	return (i + 2) / 3;
}

int     last_str_len(char *str)
{
        int     i;

        i = 0;
        while (str[i])
		i++;
	return (i % 3 == 0) ? 3 : i % 3;
}

char	**ft_minisplit(char *nbr)
{
	int	i;
	char	**arr;
	int	nb;
	int	len;
	int	j;
	int	k;
	int	first_block_size;
	int	pos;
	
	first_block_size = last_str_len(nbr);
	len = 0;
	nb = num_blocks(nbr);
	i = 0;
	j = 0;
	while (nbr[len])
		len++;
	arr = malloc(sizeof(char *) * num_blocks(nbr) * 1);
	while (i < nb - 1)
	{
		arr[i] = malloc(sizeof(char) * 4);
		i++;
	}
	arr[i] = malloc(sizeof(char) * last_str_len(nbr) + 1);
	while (j < first_block_size)
	{
		arr[0][j] = nbr[j];
		j++;
	}
	arr[0][first_block_size] = '\0';
	pos = first_block_size;
	i = 1;
	while (i < nb)
	{
		k = 0;
		while (k < 3)
		{
			if (pos < len)
				arr[i][k] = nbr[pos];
			pos++;
			k++;
		}
		arr[i][3] = '\0';
		i++;
	}
	return (arr);
}
