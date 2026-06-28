#!/usr/bin/env python3
import sys
from typing import IO

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        sys.exit(1)

    filename: str = sys.argv[1]
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{filename}'")

    f: IO[str]
    try:
        f = open(filename)
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        sys.exit(1)

    content: str = f.read()
    f.close()

    print("---\n")
    print(content)
    print("---")
    print(f"File '{filename}' closed.")
