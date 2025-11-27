/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strstr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/14 15:34:03 by arde-ass          #+#    #+#             */
/*   Updated: 2025/07/14 19:54:52 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

char	*ft_strstr(char *str, char *to_find)
{
	int		i;
	int		j;
	char	index;

	i = 0;
	j = 0;
	index = 0;
	while (str[i] != '\0')
	{
		while (str[i] == to_find[j])
		{
			if (to_find[j + 1] == '\0')
				return (&str[index + 1]);
			else
			{
				i++;
				j++;
			}
		}
		index = i;
		j = 0;
		i++;
	}
	return (0);
}
