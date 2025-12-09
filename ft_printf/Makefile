# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: arde-ass <arde-ass@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/12/09 06:40:50 by arde-ass          #+#    #+#              #
#    Updated: 2025/12/09 11:32:29 by arde-ass         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = libftprintf.a
CC = cc
CFLAGS = -Wall -Wextra -Werror

SRC_DIR = ./libftprintf
SRC = $(SRC_DIR)/convert_base.c \
      $(SRC_DIR)/ft_putchar.c \
      $(SRC_DIR)/ft_putnbr.c \
      $(SRC_DIR)/ft_putuns.c \
      $(SRC_DIR)/ft_strlen.c \
      $(SRC_DIR)/ft_strdup.c \
      $(SRC_DIR)/ft_putmem.c \
      $(SRC_DIR)/ft_putstr.c \
      $(SRC_DIR)/ft_puthexa.c \
      ft_printf.c

OBJ = $(SRC:.c=.o)

all: $(NAME)

$(NAME): $(OBJ)
	ar rcs $(NAME) $(OBJ)

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f $(NAME)

re: fclean all
