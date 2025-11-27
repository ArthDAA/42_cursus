/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.h                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: epesnel <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/27 11:49:59 by epesnel           #+#    #+#             */
/*   Updated: 2025/07/27 22:39:01 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FTLIB_H
# define FTLIB_H

#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>

typedef struct s_values
{
	char	**input;
	int		**map;
	int		w;
	int		h;
}	t_values;

int	ft_atoi(char *str);
int ft_check_line(char **str);
void	ft_default_map(int **arr_int, char **arr, char filled);
char	*ft_get_map(char *map_adress);
int	**ft_make_map(int height, int width);
void    ft_putstr(char *str);
char	**ft_return_sqr(int **arr_int, char **arr_char, char filled);
int	ft_strlen(char *str);
char **ft_split(char *str, char c);
char	*ft_strcpy(char *dest, char *src);

#endif
