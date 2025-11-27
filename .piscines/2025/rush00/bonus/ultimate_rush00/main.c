/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/13 22:45:05 by arde-ass          #+#    #+#             */
/*   Updated: 2025/07/13 22:58:04 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

void	rush(int x, int y, char *character);

void	ft_putchar(char c);

void	ft_putstr(char *str)
{
	int	i;

	i = 0;
	while (str[i] != '\0')
	{
		ft_putchar(str[i]);
		i++;
	}
}

int	main(int argc, char **argv)
{
	char	character[6];

	if (argc <= 6 || argc == 6)
	{
		ft_putstr("6 arguments svp!\nFormat: ./a.out 'A' 'B' 'C' 'D' 'E' 'F'\n");
		return (1);
	}
	character[0] = argv[1][0];
	character[1] = argv[2][0];
	character[2] = argv[3][0];
	character[3] = argv[4][0];
	character[4] = argv[5][0];
	character[5] = argv[6][0];
	rush(23, 42, character);
	return (0);
}
