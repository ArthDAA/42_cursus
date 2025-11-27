/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rush0X.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/13 22:45:10 by arde-ass          #+#    #+#             */
/*   Updated: 2025/07/13 22:56:46 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

typedef struct pos
{
	int	x;
	int	y;
}	t_pos;

void	ft_putchar(char c);

void	ft_print(t_pos p, int i, int j, char *character)
{
	if (i == 0 && j == 0)
		ft_putchar(character[0]);
	else if (i == 0 && j == p.y - 1)
		ft_putchar(character[1]);
	else if (i == p.x - 1 && j == 0)
		ft_putchar(character[2]);
	else if (i == p.x - 1 && j == p.y - 1)
		ft_putchar(character[3]);
	else if (i == 0 || i == p.x - 1)
		ft_putchar(character[4]);
	else if (j == 0 || j == p.y - 1)
		ft_putchar(character[5]);
	else
		ft_putchar(' ');
}

void	rush(int x, int y, char *character)
{
	int		i;
	int		j;
	t_pos			p;

	i = 0;
	j = 0;
	p.x = x;
	p.y = y;
	if (p.x <= 0 || p.y <= 0)
		return ;
	while (i < x)
	{
		while (j < p.y)
		{
			ft_print(p, i, j, character);
			j++;
		}
		ft_putchar('\n');
		j = 0;
		i++;
	}
}
