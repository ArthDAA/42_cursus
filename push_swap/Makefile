# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ccolnat <ccolnat@student.42nice.fr>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/11 09:21:05 by ccolnat           #+#    #+#              #
#    Updated: 2026/04/16 15:38:04 by ccolnat          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME    =   push_swap

CC  =   cc

SRCS    =   main.c \
            init.c \
            input_check.c \
            input_clean.c \
            linked_list.c \
            linked_list_utils.c \
            push_swap.c \
            push.c \
            rotate.c \
            rev_rotate.c \
            swap.c \
            simple_sort.c \
            medium_sort.c \
            complex_sort.c \
            sorts_utils.c \
            split.c \
            utils.c \
            ft_printf.c \
            ft_printf_utils.c

OBJS	=	$(SRCS:.c=.o)

all:	$(NAME)

$(NAME):	$(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

clean:
	rm -f $(OBJS)

fclean:        clean
	rm -f $(NAME)

re:	fclean all

.PHONY:	all clean fclean re
