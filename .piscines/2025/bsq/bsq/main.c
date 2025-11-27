/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <arde-ass@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/30 21:18:23 by arde-ass          #+#    #+#             */
/*   Updated: 2025/07/31 00:52:02 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ftlib.h"

int	main(int argc, char **argv)
{
	t_values	infos;
	char		*buffer;
	int			i;

	i = 1;
	if (argv[1])
		buffer = ft_get_map(argv[1]);
	else
		buffer = ft_get_map(NULL);
	free(buffer);
	infos.input = ft_split(buffer, '\n');
	infos.h = ft_check_line(infos.input);
	if (infos.h == 0)
	{
		ft_putstr("map error");
		return (0);
	}
	infos.w = ft_strlen(infos.input[1]);
	infos.map = ft_make_map(infos.h, infos.w);
	ft_default_map(infos.map, &infos.input[1], infos.input[0][2]);
	infos.input = ft_return_sqr(infos.map, &infos.input[1], infos.input[0][2]);
	while (infos.input[i])
	{
		ft_putstr(infos.input[i]);
		i++;
	}
	return (0);
}
