/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_check_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <arde-ass@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/30 21:27:16 by arde-ass          #+#    #+#             */
/*   Updated: 2025/07/30 23:17:24 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ftlib.h"

int ft_check_line(char **str)
{
    int i;
    int len;
    int height;
    
    i = 2;
    len = ft_strlen(str[1]);
    height = ft_atoi(str[0]);
    printf("%s\n", str[0]);
    printf("%d\n", height);
    while (i <= height)
    {
        if (ft_strlen(str[i]) != len)
            return(0);
        i++;
    }
    return (height);
}