/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_program_name.c                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/19 22:30:37 by arde-ass          #+#    #+#             */
/*   Updated: 2025/07/19 23:14:59 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_putchar(char c)
{
	write (1, &c, 1);
}

int	main(int argc, char **argv)
{
	int	i;

	i = argc;
	i = 0;
	while (argv[0][i] != '\0')
	{
		ft_putchar (argv[0][i]);
		i++;
	}
	ft_putchar('\n');
}
