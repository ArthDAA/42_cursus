/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_bzero.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <arde-ass@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/06 16:51:00 by arde-ass          #+#    #+#             */
/*   Updated: 2025/11/06 17:04:53 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void bzero(void *s, size_t n)
{
    size_t i;
    unsigned char *ptr;
    
    ptr = (unsigned char *)s;
    i = 0;
    while (i < n)
    {
        ptr[i] = '\0';
        i++;
    }
    return (s);
}