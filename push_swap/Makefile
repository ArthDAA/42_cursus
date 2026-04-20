# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/04/11 09:21:05 by ccolnat           #+#    #+#              #
#    Updated: 2026/04/18 14:14:34 by ccolnat          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME    =   push_swap

CFLAGS  =   -Wall -Wextra -Werror

CC      =   gcc

S       =   src/main.c \
            src/init.c \
            src/input_check.c \
            src/input_clean.c \
            src/linked_list.c \
            src/linked_list_utils.c \
            src/push_swap.c \
            src/push.c \
            src/rotate.c \
            src/rev_rotate.c \
            src/swap.c \
            src/simple_sort.c \
            src/medium_sort.c \
            src/complex_sort.c \
            src/sorts_utils.c \
            src/split.c \
            src/utils.c \
            src/ft_printf.c \
            src/ft_printf_utils.c \
            src/count.c \
            src/print_moves.c \

OBJS	=	$(S:.c=.o)

all:	$(NAME)

$(NAME):	$(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

clean:
	rm -f $(OBJS)

fclean:        clean
	rm -f $(NAME)

re:	fclean all

.PHONY:	all clean fclean re
