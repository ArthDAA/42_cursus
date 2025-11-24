/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <arde-ass@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/20 21:33:35 by arde-ass          #+#    #+#             */
/*   Updated: 2025/11/24 14:41:52 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strjoin(const char *s1, const char *s2)
{
	size_t	l1;
	size_t	l2;
	size_t	i;
	size_t	j;
	char	*r;

	l1 = ft_strlen(s1);
	l2 = ft_strlen(s2);
	r = (char *)malloc(l1 + l2 + 1);
	if (r == NULL)
		return (NULL);
	i = 0;
	while (i < l1)
	{
		r[i] = s1[i];
		i++;
	}
	j = 0;
	while (j < l2)
	{
		r[i + j] = s2[j];
		j++;
	}
	r[i + j] = '\0';
	return (r);
}
