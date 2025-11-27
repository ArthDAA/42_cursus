/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_return_sqr.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <arde-ass@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/30 23:29:11 by arde-ass          #+#    #+#             */
/*   Updated: 2025/07/30 23:59:59 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ftlib.h"

void	ft_make_sqr(char **arr, int *best, char mark)
{
	int	i;
	int	j;

	i = best[2];
	while (i >= 0)
	{
		j = best[2];
		while (j >= 0)
		{
			arr[i + best[0]][j + best[1]] = mark;
			j--;
		}
		i--;
	}
}

int	mini(int left, int diag, int high)
{
	int	i;

	i = left;
	if (i > diag)
		i = diag;
	if (i > high)
		i = high;
	return (i + 1);
}

void	ft_set_best(int *best, int i, int j, int value)
{
	best[0] = i - value + 1;
	best[1] = j - value + 1;
	best[2] = value - 1;
}

char	**ft_return_sqr(int **arr_int, char **arr_char, char filled)
{
	int		i;
	int		j;
	int		max;
	int		best[3];

	i = 1;
	max = 0;
	while (arr_int[i])
	{
		j = 1;
		while (arr_int[i][j] || j == 1)
		{
			if (arr_char[i][j] != filled)
			{
				arr_int[i][j] = mini(arr_int[i - 1][j],
						arr_int[i - 1][j - 1], arr_int[i][j - 1]);
				if (max < arr_int[i][j])
				{
					max = arr_int[i][j];
					ft_set_best(best, i, j, arr_int[i][j]);
				}
			}
			else
				arr_int[i][j] = 0;
			j++;
		}
		i++;
	}
	ft_make_sqr(arr_char, best, filled);
	return (arr_char);
}
