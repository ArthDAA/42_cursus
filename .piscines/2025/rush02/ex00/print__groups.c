/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print__groups.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/27 21:16:49 by arde-ass          #+#    #+#             */
/*   Updated: 2025/07/27 22:15:40 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "main.h"

void	ft_print_groups(char *arr, t_dict_entry *dict)
{
	int	i;
	int	j;
	char 	temp[2];
	char 	temp_2[3];

	i = 0;
	j = 0;
	while (arr[i])
	{
		temp[0] = arr[i];
		if (arr[i] != '0')
		{
			while (ft_strcmp(temp, dict[j].nb) == 1)
				j++;
			ft_putstr(dict[j].value);
			j = 0;
			while (ft_strcmp("100", dict[j].nb) == 1)
                	       	j++;
               		ft_putstr(dict[j].value);
		}
		i++;
		j = 0;
		if (arr[i] != '0')
		{
			if (arr[i] == 1)
			{
				temp_2[0] = arr[i];
				temp_2[1] = arr[i + 1];
				while (ft_strcmp(temp_2, dict[j].nb) == 1)
					j++;
				ft_putstr(dict[j].value);
				return ;
			}
			else
			{
				temp_2[0] = arr[i];
				temp_2[1] = '0';
				while (ft_strcmp(temp_2, dict[j].nb) == 1)
                		        j++;
		                ft_putstr(dict[j].value);
			}
		}
		i++;
		j = 0;
		if (arr[i] != '0')
		{
			temp[0] = arr[i];
			while (ft_strcmp(temp, dict[j].nb) == 1)
                        	j++;
                	ft_putstr(dict[j].value);
		}
	}
}
