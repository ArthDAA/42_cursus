/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_default_map.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <arde-ass@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/30 22:32:32 by arde-ass          #+#    #+#             */
/*   Updated: 2025/07/30 23:14:08 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ftlib.h"

void	set_line(char *arr, int *arr_int, char filled)
{
	if (*arr == filled)
		*arr_int = 0;
	else
		*arr_int = 1;
}

void	set_col(char *arr, int *arr_int, char filled)
{
	if (*arr == filled)
		*arr_int = 0;
	else
		*arr_int = 1;
}

void	ft_default_map(int **arr_int, char **arr, char filled)
{
	int	i;

	i = 0;
	while (arr[0][i])
	{
		set_line(&arr[0][i], &arr_int[0][i], filled);
		i++;
	}
	i = 1;
	while (arr[i])
	{
		set_col(&arr[i][0], &arr_int[i][0], filled);
		i++;
	}
}