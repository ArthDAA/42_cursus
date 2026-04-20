/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/11 09:21:05 by ccolnat           #+#    #+#             */
/*   Updated: 2026/04/18 14:04:54 by ccolnat          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include <stdarg.h>
# include <stddef.h>
# include <stdlib.h>
# include <unistd.h>

typedef struct s_stack
{
	ssize_t			value;
	ssize_t			index;
	struct s_stack	*next;
	struct s_stack	*prev;
}					t_stack;

void				init(char *str, t_stack **stack_a, t_stack **stack_b);
void				push_swap(t_stack **stack_a, ssize_t strategy,
						ssize_t bench);
void				write_instruct(ssize_t instruct, ssize_t mode);
void				fill_index(t_stack *stack, ssize_t list_size);
void				add_bottom(t_stack **stack, t_stack *new);
void				push(t_stack **dest, t_stack **src);
void				pa(t_stack **a, t_stack **b);
void				pb(t_stack **a, t_stack **b);
void				rrr(t_stack **a, t_stack **b);
void				rr(t_stack **a, t_stack **b);
void				ss(t_stack **a, t_stack **b);
void				pa(t_stack **a, t_stack **b);
void				pb(t_stack **a, t_stack **b);
void				rev_rotate(t_stack **head);
void				rotate(t_stack **head);
void				swap(t_stack **head);
void				rrb(t_stack **b);
void				rra(t_stack **a);
void				ra(t_stack **a);
void				sa(t_stack **a);
void				sb(t_stack **b);
void				rb(t_stack **b);
void				put_bench(void);

ssize_t				check_flags(int argc, char **argv, ssize_t bench);
ssize_t				direction(t_stack *tmp, ssize_t val, ssize_t max);
ssize_t				parse_count(ssize_t instruct, ssize_t mode);
ssize_t				ft_strcmp(const char *s1, const char *s2);
ssize_t				find_flag(char **argv, ssize_t bench);
ssize_t				count_rr(ssize_t instruct, ssize_t mode);
ssize_t				count_p(ssize_t instruct, ssize_t mode);
ssize_t				count_r(ssize_t instruct, ssize_t mode);
ssize_t				count_s(ssize_t instruct, ssize_t mode);
ssize_t				get_stack_size(t_stack *head);
ssize_t				is_sorted(t_stack *head);
ssize_t				ft_atoi(const char *str);
ssize_t				char_check(char *str);
ssize_t				debugg(ssize_t nb);

int					ft_printf_parse(char arg_type, va_list args);
int					ft_printf(const char *input, ...);
int					ft_putchar(char c);

t_stack				*fill_value(char **list, ssize_t list_size);
t_stack				*get_min_node(t_stack *head);
t_stack				*get_max_node(t_stack *head);
t_stack				*complex_sort(t_stack *head);
t_stack				*medium_sort(t_stack *head);
t_stack				*simple_sort(t_stack *head);
t_stack				*new_stack(ssize_t value);

ssize_t				ft_strlen(char const *str);

char				*extract_str(int argc, char **argv, ssize_t bench);
char				**split(char *str, char c);
char				*clean_list(char *raw_str);

#endif