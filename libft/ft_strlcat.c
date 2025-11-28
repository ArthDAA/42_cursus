/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <arde-ass@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/14 05:02:34 by arde-ass          #+#    #+#             */
/*   Updated: 2025/11/28 11:42:53 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t	ft_strlcat(char *dst, const char *src, size_t dstsize)
{
	size_t	dst_len;
	size_t	src_len;
	size_t	i;

	if (!src)
		return (0);
	src_len = ft_strlen(src);
	if (!dst && dstsize == 0)
		return (src_len);
	if (!dst)
		return (0);
	dst_len = 0;
	while (dst_len < dstsize && dst[dst_len] != '\0')
		dst_len++;
	if (dst_len == dstsize)
		return (dstsize + src_len);
	i = 0;
	while (dst_len + i + 1 < dstsize && src[i] != '\0')
	{
		dst[dst_len + i] = src[i];
		i++;
	}
	dst[dst_len + i] = '\0';
	return (dst_len + src_len);
}
