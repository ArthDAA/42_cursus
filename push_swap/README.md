*This project was created as part of the 42 curriculum by ccolnat, arde-ass.*

## DESCRIPTION
Push_swap is the first group project of the 42 curriculum.
The objective is to create a program which takes as input a series of numbers within the integer range, and an optional flag (see more below).

The program then sorts the numbers by swapping them between two stacks, A and B. There is a restricted list of movements allowed within and between the stacks (sa, sb, ss, pa, pb, ra, rb, rr, rra, rrb, rrr); see details in the Resources section.

If no flag is provided, the program will measure the disorder and the length of the given list, and choose between 3 different algorithms to minimize the number of operations required to sort the array. The algorithms are detailed in the Resources section.

The program also handles errors, returning "Error" and freeing memory.

This push_swap implementation does not handle the bonus part of the subject.

ccolnat wrote all the input-related code up to the initialization of the linked list, which connected our functions and was therefore coded together. arde-ass implemented the majority of the algorithms (see headers).

## INSTRUCTIONS
To compile this project, you must run the command `make`.

###  INPUTS
Our program allows for some flexibility: it tolerates and corrects multiple spaces, and/or stray "-" characters between spaces.

### FLAGS
Using one of 4 flags below will change the sorting behavior (only one at a time): 
`--simple` / `--medium` / `--complex` / `--adaptive`
Additionally, you can activate the benchmark mode with:
`--bench`
More about `Benchmark Mode` in Resources.

Flags can be placed mostly anywhere in the input.
See exceptions below:
./push_swap 3 2 1 "--flag 6 5 4"    ->  Error.
./push_swap 3 2 1 "--simple" 6 5 4  ->  Ok, forces the simple sorting strategy.
./push_swap 3 2 1 --bench "6 5 4"   ->  Ok, activates benchmark mode.

You can check the Norm with this command in the terminal:
`norminette`

And use Valgrind to check for leaks:
`valgrind ./push_swap 3 2 1`

Testers are available online, though most do not allow for testing with custom flags.

Additionally, you can find below both version of the `debugg`
The second version will provide more useful error messages.

##### DEBUGG FUNCTION V1
    ssize_t	debugg(ssize_t nb)
    {
    	if (nb == 4)
    		return (-1);
    	else if (nb >= 0)
    		ft_printf("Error\n");
    	return (-1);
    }

##### DEBUGG FUNCTION V2
    ssize_t	debugg(ssize_t nb)
    {
    	if (nb == 0)
    		ft_printf("Error: arg in list is not a number.\n");
	    else if (nb == 1)
	    	ft_printf("Error: instruct is invalid.\n");
	    else if (nb == 2)
	    	ft_printf("Error: instruct count invalid.\n");
	    else if (nb == 4)
	    	ft_printf("Error: empty input.\n");
	    else if (nb == 5)
	    	ft_printf("Error: no space before '-'.\n");
	    else if (nb == 6)
	    	ft_printf("Error: same number found twice in the list\n");
	    else if (nb == 7)
	    	ft_printf("Error: number out of range\n");
	    else if (nb == 8)
	    	ft_printf("Error: not sorted\n");
	    return (-1);
    }

## RESOURCES

This push_swap follows the new subject of the 42_next cursus, version 1.1.

### BENCHMARK MODE

This mode will provide information about : 
* The computed Complexity
* The selected algorithm and strategy
* The total number of operations
* The count of each operation

### MOVEMENT LIST

#### sa (swap a):
*    Swap the first two elements at the top of stack a.
*    Do nothing if there is only one or no elements.
#### sb (swap b): 
*    Swap the first two elements at the top of stack b.
*    Do nothing if there is only one or no elements.
#### ss:
*    Do sa and sb at the same time.
#### pa (push a): 
*    Take the first element at the top of b and put it at the top of a.
*    Do nothing if b is empty.
#### pb (push b): 
*    Take the first element at the top of a and put it at the top of b.
*    Do nothing if a is empty.
#### ra (rotate a): 
*    Shift up all elements of stack a by one.
*    The first element becomes the last one.
#### rb (rotate b): 
*    Shift up all elements of stack b by one.
*    The first element becomes the last one.
#### rr:
*    Do ra and rb at the same time.
#### rra (reverse rotate a): 
*    Shift down all elements of stack a by one.
*    The last element becomes the first one.
#### rrb (reverse rotate b): 
*    Shift down all elements of stack b by one.
*    The last element becomes the first one.
#### rrr:
*    Do rra and rrb at the same time.

The structure we use for manipulating the nodes contains 4 components:

* **The next node**: As it is a linked list, it contains the next node's address.
* **The prev node**: In our implementation, every node contains a pointer to the next AND the previous node (a doubly linked list).
* **The index**: Another specificity is that our program defines every node's final position beforehand. This is especially useful in the complex algorithm (Radix sort), where negative values are harder to handle.
* **The value**: Finally, the actual value or content of the node.

###  SORTS TYPES

#### Simple Sort (Small Sets)

**Used for:** Low disorder inputs.

The Simple Sort is used for stacks with 5 or fewer elements. It identifies the smallest index and pushes it to Stack B until only 3 elements remain in Stack A.
A specific `sort_three` logic is then applied to Stack A using a maximum of 2-3 instructions, after which the elements from Stack B are pushed back to complete the sort.

#### Medium Sort (K-Sort / Chunk Sort)

**Used for:** medium disorder inputs.

The Medium Sort uses a "chunk" strategy based on the square root of the stack size.
It moves elements to Stack B in a pre-sorted range, effectively creating a "butterfly" or hourglass shape.
Once Stack A is empty, it repeatedly finds the maximum element in Stack B and pushes it back to Stack A in the correct order.

#### Complex Sort (Radix Sort)

**Used for:** high disorder inputs.

The Complex Sort implements a binary Radix Sort for large datasets.
It iterates through the bits of the pre-calculated indices (from the least significant to the most significant bit).

* If the current bit of an index is 0, the node is pushed to Stack B.
* If the current bit is 1, the node is rotated to the bottom of Stack A.

After each bit iteration, all elements from Stack B are pushed back to Stack A.

### Adaptive Sort Algorithm

The adaptive strategy measures the disorder of the input, then dispatches to one of the three strategies above based on thresholds.

**Disorder metric:**

```
disorder = (number of inverted pairs) / (total pairs)
         = mistakes / (n * (n-1) / 2)
```

| Disorder       | Strategy selected | Complexity    |
|----------------|-------------------|---------------|
| < 20%          | Simple            | O(n²)         |
| 20% – 49%      | Medium            | O(n√n)        |
| ≥ 50%          | Complex           | O(n log n)    |

**Claude** was used for debugging specific functions we had already written: tracing pointer logic in linked list operations, identifying a stale-pointer bug after sort operations invalidated a cached head pointer, and finding signed/unsigned type mismatches in index comparisons. No algorithm, architecture, or complete function was generated by AI.

**Google Gemini** was used as a learning tool throughout the project, with the following permanent instruction: *"When the subject is programming, you must act as a teacher — do not give code directly, do not give obvious hints in response to a question, and when explaining something give details about why and how things work."*