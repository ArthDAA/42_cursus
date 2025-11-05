/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   test.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <arde-ass@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/05 11:18:00 by arde-ass          #+#    #+#             */
/*   Updated: 2025/11/05 11:57:52 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <ctype.h>
#include <stdio.h>

int	ft_isdigit(int i)
{
	if (i >= '0' && i <= '9')
		return (2048);
	else
		return (0);
}

int main()
{
    int i;
    i = -1;
    while (i < 129)
    {
        if (isdigit(i) != ft_isdigit(i))
            printf("\n%c : %d - %d\n\n", i, isdigit(i), ft_isdigit(i));
        else
            printf("---\n");
        i++;
    }
}