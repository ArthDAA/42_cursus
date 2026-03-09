/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <arde-ass@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/14 03:57:15 by arde-ass          #+#    #+#             */
/*   Updated: 2025/12/09 11:51:01 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include <stdlib.h>
# include <unistd.h>

# define LOW_HEX		"0123456789abcdef"
# define UP_HEX 		"0123456789ABCDEF"

size_t	ft_strlen(const char *s);
char	*convert_base(unsigned long long value, char *table);
int		ft_printf(const char *format, ...);
int		ft_putchar(char c);
int		ft_putmem(void *ptr);
int		ft_putstr(char *str);
int		ft_putuns(unsigned int nbr);
int		ft_putnbr(int nbr);
char	*ft_strdup(const char *s1);
int		ft_puthexa(unsigned int nbr, char *base);

#endif
