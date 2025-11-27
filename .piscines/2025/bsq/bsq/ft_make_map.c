/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_make_map.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <arde-ass@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/30 22:18:06 by arde-ass          #+#    #+#             */
/*   Updated: 2025/07/30 23:14:06 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ftlib.h"

int	**ft_make_map(int height, int width)
{
    int **arr;
    int i;
    int j;
    
    i = 0;
    j = 0;
    *arr = malloc(sizeof(int *) * height);
    while (i < height)
    {
        arr[i] = malloc(sizeof(int) * height);
        i++;
    }
    i = 0;
    while (arr[i])
	{
		while (arr[i][j])
		{
			arr[i][j] = 0;
			j++;
		}
        j = 0;
		i++;
	}
    return(arr);
}