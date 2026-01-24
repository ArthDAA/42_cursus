*This project has been created as part of the 42 curriculum by arde-ass.*

# get_next_line

## Description

The goal of this project is to implement the function `get_next_line`, which returns a line read from a file descriptor. Successive calls allow reading a file or standard input line by line.

The returned line includes the terminating `\n` character, except if the end of file is reached without it. If there is nothing left to read or if an error occurs, the function returns `NULL`.

## Instructions

### Files

* `get_next_line.c`
* `get_next_line_utils.c`
* `get_next_line.h`

### Compilation

The buffer size must be defined at compilation time:

```bash
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 get_next_line.c get_next_line_utils.c
```

The project must compile with or without the `-D BUFFER_SIZE` flag.

## Algorithm

The function uses a static variable to store unread data between calls.

* Data is read from the file descriptor using `read()` with a buffer of size `BUFFER_SIZE`.
* The read data is appended to the static storage until a newline is found or EOF is reached.
* Once a full line is available, it is extracted and returned.
* The remaining data is kept for the next call.
* When there is nothing left to read, the function returns `NULL`.

This approach avoids reading the whole file at once and ensures correct behavior for any `BUFFER_SIZE` value.

## Resources

* `man 2 read`
* `man 3 malloc`
* 42 subject: Get Next Line (v14)

### AI usage

AI was used only to help write this README. No code was generated using AI.
