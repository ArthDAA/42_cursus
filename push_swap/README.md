# *This project was created as part of the 42 curriculum by ccolnat and arde-ass.*

## DESCRIPTION
Push_swap is the first group project of the 42 curriculum.
The objective is to create a program which takes as input a series of numbers within the int range, and an optional flag (see more below).

The program then sorts the numbers by swapping them between two stacks, A and B. There is a restricted list of movements allowed within and between the stacks (sa, sb, ss, pa, pb, ra, rb, rr, rra, rrb, rrr); see details in the Resources section.

If no flag is provided, the program will measure the disorder and the length of the given list, and choose between 3 different algorithms to minimize the number of operations required to sort the array. The algorithms are detailed in the Resources section.

The program also handles errors, returning "Error" and freeing memory.

This push_swap implementation does not handle the bonus part of the subject.

## INSTRUCTIONS
To compile this project, you must run the command `make`.

Regarding inputs, our program allows for some flexibility: it tolerates and corrects multiple spaces, and/or stray "-" characters between spaces.

Regarding flags, you can use 4 different types: 
`--simple` / `--medium` / `--complex` / `--adaptive`

Flags are limited to only one per call. These flags can be placed anywhere in the input, except inside quotation marks in specific cases.

See examples below:
./push_swap 3 2 1 "--flag 6 5 4"     ->  Error
./push_swap 3 2 1 "--simple" 6 5 4   ->  Ok, forces the simple sorting strategy
./push_swap 3 2 1 --medium "6 5 4"   ->  Ok, forces the medium sorting strategy

You can check the Norm with this command in the terminal:
`norminette`

And use Valgrind to check for leaks:
`valgrind ./push_swap 3 2 1`

Testers are available online, though most do not allow for testing with custom flags.

Additionally, you can find a commented-out version of the `debug()` function in the `utils.c` file, which provides detailed error messages.

## RESOURCES

This push_swap follows the new subject of the 42_next cursus, version 1.1.

Here is the detailed list of movements allowed:

* **sa (swap a):** Swap the first two elements at the top of stack a. Do nothing if there is only one or no elements.
* **sb (swap b):** Swap the first two elements at the top of stack b. Do nothing if there is only one or no elements.
* **ss:** sa and sb at the same time.
* **pa (push a):** Take the first element at the top of b and put it at the top of a. Do nothing if b is empty.
* **pb (push b):** Take the first element at the top of a and put it at the top of b. Do nothing if a is empty.
* **ra (rotate a):** Shift up all elements of stack a by one. The first element becomes the last one.
* **rb (rotate b):** Shift up all elements of stack b by one. The first element becomes the last one.
* **rr:** ra and rb at the same time.
* **rra (reverse rotate a):** Shift down all elements of stack a by one. The last element becomes the first one.
* **rrb (reverse rotate b):** Shift down all elements of stack b by one. The last element becomes the first one.
* **rrr:** rra and rrb at the same time.

The structure we use for manipulating the nodes contains 4 components:

* **The next node**: As it is a linked list, it contains the next node's address.
* **The prev node**: In our implementation, every node contains a pointer to the next AND the previous node (a doubly linked list).
* **The index**: Another specificity is that our program defines every node's final position beforehand. This is especially useful in the complex algorithm (Radix sort), where negative values are harder to handle.
* **The value**: Finally, the actual value or content of the node.

1. Simple Sort (Small Sets)
The Simple Sort is used for stacks with 5 or fewer elements. It identifies the smallest index and pushes it to Stack B until only 3 elements remain in Stack A. A specific `sort_three` logic is then applied to Stack A using a maximum of 2-3 instructions, after which the elements from Stack B are pushed back to complete the sort.

2. Medium Sort (K-Sort / Chunk Sort)
The Medium Sort uses a "chunk" strategy based on the square root of the stack size. It moves elements to Stack B in a pre-sorted range, effectively creating a "butterfly" or hourglass shape. Once Stack A is empty, it repeatedly finds the maximum element in Stack B and pushes it back to Stack A in the correct order.

3. Complex Sort (Radix Sort)
The Complex Sort implements a binary Radix Sort for large datasets. It iterates through the bits of the pre-calculated indices (from the least significant to the most significant bit).

* If the current bit of an index is 0, the node is pushed to Stack B.
* If the current bit is 1, the node is rotated to the bottom of Stack A.

After each bit iteration, all elements from Stack B are pushed back to Stack A.

We used Claude code to help with some of the debugging, and Google Gemini as a learning tool, with strict permanent instructions, which you can see below :

*When the subject is programming, you must act as a teacher, so, you must not give the code directly, when you ask a question, do not give any obvious hint that respond to the question you are asking, and when your explaining something, give details, explain why and how things work, and if you show any simplified typos for coding, explain it.*