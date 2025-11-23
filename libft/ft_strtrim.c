/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <arde-ass@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/20 21:29:39 by arde-ass          #+#    #+#             */
/*   Updated: 2025/11/20 21:29:40 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	in_set(char c, const char *set)
{
	size_t	i;

	i = 0;
	while (set[i] != '\0')
	{
		if (set[i] == c)
			return (1);
		i++;
	}
	return (0);
}

char	*ft_strtrim(const char *s1, const char *set)
{
	size_t	start;
	size_t	end;

	start = 0;
	while (s1[start] != '\0' && in_set(s1[start], set))
		start++;
	end = 0;
	while (s1[end] != '\0')
		end++;
	while (end > start && in_set(s1[end - 1], set))
		end--;
	return (ft_substr(s1, start, end - start));
}
