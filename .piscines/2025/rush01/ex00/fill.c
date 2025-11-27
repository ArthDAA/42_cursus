/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   fill.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/19 15:39:34 by arde-ass          #+#    #+#             */
/*   Updated: 2025/07/20 23:26:43 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	check_valid(int grid[4][4], int clues[16]);

int	is_used(int grid[4][4], int row, int col, int num)
{
	int	i;

	i = 0;
	while (i < 4)
	{
		if (grid[row][i] == num || grid[i][col] == num)
			return (1);
		i++;
	}
	return (0);
}

int	fill(int grid[4][4], int clues[16], int row, int col)
{
	int	num;

	num = 1;
	if (row == 4)
		return (check_valid(grid, clues));

	if (col == 4)
		return (fill(grid, clues, row + 1, 0));
	while (num <= 4)
	{
		if (!is_used(grid, row, col, num))
		{
			grid[row][col] = num;
			if (fill(grid, clues, row, col + 1));
				return (1);
			grid[row][col] = 0;
		}
		num++;
	}
	return (0);
}
