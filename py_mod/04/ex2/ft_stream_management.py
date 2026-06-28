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
        sys.stderr.write(f"[STDERR] Error opening file '{filename}': {e}\n")
        sys.exit(1)

    content: str = f_in.read()
    f_in.close()

    sys.stdout.write("---\n\n")
    sys.stdout.write(content)
    sys.stdout.write("\n---\n")
    sys.stdout.write(f"File '{filename}' closed.\n\n")
    sys.stdout.flush()

    lines: list[str] = content.splitlines()
    new_content: str = "\n".join(line + "#" for line in lines) + "\n"

    sys.stdout.write("Transform data:\n---\n\n")
    sys.stdout.write(new_content)
    sys.stdout.write("\n---\n")
    sys.stdout.flush()

    sys.stdout.write("Enter new file name (or empty): ")
    sys.stdout.flush()
    new_name: str = sys.stdin.readline().rstrip("\n")

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
            sys.stderr.write(
                f"[STDERR] Error opening file '{new_name}': {e}\n"
            )
            print("Data not saved.")
