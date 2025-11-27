/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   solve.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/19 15:39:58 by arde-ass          #+#    #+#             */
/*   Updated: 2025/07/20 23:27:56 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int		check_valid(int grid[4][4], int clues[16]);
void	print_grid(int grid[4][4]);
int		fill(int grid[4][4], int clues[16], int row, int col);

int	to_int(char c)
{
	if (c >= '1' && c <= '4')
		return (c - '0');
	return (0);
}

int	parse_clues(char *str, int clues[16])
{
	int	i;
	int	j;

	i = 0;
	j = 0;
	while (str[i])
	{
		if (str[i] >= '1' && str[i] <= '4')
			clues[j++] = str[i] - '0';
		else if (str[i] != ' ')
			return (0);
		i++;
	}
	return (j == 16);
}

int	solve(char *input)
{
	static int	grid[4][4];
	int	clues[16];
	int	i;
	int	j;

	i = 0;
	while (i < 4)
	{
		j = 0;
		while (j < 4)
			grid[i][j++] = 0;
		i++;
	}
	if (!parse_clues(input, clues))
		return (0);
	if (fill(grid, clues, 0, 0))
	{
		print_grid(grid);
		return (1);
	}
	return (0);
}
