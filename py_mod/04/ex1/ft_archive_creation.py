#!/usr/bin/env python3
import sys
from typing import IO

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        sys.exit(1)

    filename: str = sys.argv[1]
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{filename}'")

    f_in: IO[str]
    try:
        f_in = open(filename)
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        sys.exit(1)

    content: str = f_in.read()
    f_in.close()

    print("---\n")
    print(content)
    print("---")
    print(f"File '{filename}' closed.")
    print()

    lines: list[str] = content.splitlines()
    new_content: str = "\n".join(line + "#" for line in lines) + "\n"

    print("Transform data:")
    print("---\n")
    print(new_content)
    print("---")

    new_name: str = input("Enter new file name (or empty): ")
    if not new_name:
        print("Not saving data.")
    else:
        print(f"Saving data to '{new_name}'")
        f_out: IO[str]
        try:
            f_out = open(new_name, "w")
            f_out.write(new_content)
            f_out.close()
            print(f"Data saved in file '{new_name}'.")
        except OSError as e:
            print(f"Error opening file '{new_name}': {e}")
