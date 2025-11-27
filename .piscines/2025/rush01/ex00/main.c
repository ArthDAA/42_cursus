/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/19 15:20:33 by arde-ass          #+#    #+#             */
/*   Updated: 2025/07/20 23:27:37 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

int		solve(char *input);
int		ft_strlen(char *str);
int		ft_error(void);

int	main(int argc, char **argv)
{
	if (argc != 2 || ft_strlen(argv[1]) != 31)
		return (ft_error());
	if (!solve(argv[1]))
		return (ft_error());
	return (0);
}
