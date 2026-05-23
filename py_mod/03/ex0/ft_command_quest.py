import sys

if (__name__ == "__main__"):
    argc = len(sys.argv)
    print(
        f"=== Command Quest ===\n"
        f"Program name: {sys.argv[0]}"
    )
    if (argc > 1):
        i = 1
        print(f"Arguments received: {argc - 1}")
        while (i < argc):
            print(f"Argument {i}: {sys.argv[i]}")
            i += 1
    else:
        print("No arguments provided!")
    print(f"Total arguments: {argc}\n")