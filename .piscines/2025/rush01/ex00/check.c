/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   check.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/19 15:39:27 by arde-ass          #+#    #+#             */
/*   Updated: 2025/07/19 19:31:28 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	visible_count(int *line)
{
	int	max;
	int	count;
	int	i;

	max = 0;
	count = 0;
	i = 0;
	while (i < 4)
	{
		if (line[i] > max)
		{
			max = line[i];
			count++;
		}
		i++;
	}
	return (count);
}

void	reverse(int *in, int *out)
{
	int	i;

	i = 0;
	while (i < 4)
	{
		out[i] = in[3 - i];
		i++;
	}
}

int	check_line_col(int grid[4][4], int *clues, int i)
{
	int	tmp[4];
	int	rev[4];

	tmp[0] = grid[0][i];
	tmp[1] = grid[1][i];
	tmp[2] = grid[2][i];
	tmp[3] = grid[3][i];
	if (visible_count(tmp) != clues[i])
		return (0);
	reverse(tmp, rev);
	if (visible_count(rev) != clues[i + 4])
		return (0);
	return (1);
}

int	check_row(int grid[4][4], int *clues, int i)
{
	int	tmp[4];
	int	rev[4];

	tmp[0] = grid[i][0];
	tmp[1] = grid[i][1];
	tmp[2] = grid[i][2];
	tmp[3] = grid[i][3];
	if (visible_count(tmp) != clues[i + 8])
		return (0);
	reverse(tmp, rev);
	if (visible_count(rev) != clues[i + 12])
		return (0);
	return (1);
}

int	check_valid(int grid[4][4], int clues[16])
{
	int	i;

	i = 0;
	while (i < 4)
	{
		if (!check_line_col(grid, clues, i) || !check_row(grid, clues, i))
			return (0);
		i++;
	}
	return (1);
}
