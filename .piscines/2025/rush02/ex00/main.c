/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: arde-ass <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/26 22:16:50 by arde-ass          #+#    #+#             */
/*   Updated: 2025/07/27 22:53:35 by arde-ass         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "main.h"
#include <unistd.h>
t_dict_entry    *set_struct(char *file_to_parse);

int	main(int argc, char **argv)
{
	char	**arr;
	char	*dictionary = "numbers.dict";
	t_dict_entry *parse;

//	if (argc > 2 || argc < 3)
//		write(1, "Error\n", 6);
	if (argc == 2)
	{
		arr = ft_minisplit(argv[1]);
		parse = set_struct("numbers.dict");
		ft_print_groups(arr[0], parse);
	}
	else
	{
		arr = ft_minisplit(argv[2]);
		//PARSING(argv[1], arr) - CAS 2
	}
}
