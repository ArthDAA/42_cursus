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

#ifndef MAIN_H
# define MAIN_H

char	**ft_minisplit(char *nbr);
int	ft_is_alpha(char str);
int	ft_is_number(char str);
char	*ft_strcpy_nb(char *dest, char *src);
char	*ft_strcpy_value(char *dest, char *src);
void	ft_putstr(char *str);
int     ft_strcmp(char *s1, char *s2);

typedef struct s_dict
	{
		char *nb;
		char *value;
	} t_dict_entry;

void	ft_print_groups(char *arr, t_dict_entry *dict);
t_dict_entry    *set_struct(char *file_to_parse);
#endif
