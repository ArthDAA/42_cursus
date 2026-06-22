#!/usr/bin/env python3


def secure_archive(
    filename: str,
    action: int = 0,
    content: str = "",
) -> tuple[bool, str]:
    if action == 0:
        try:
            with open(filename) as f:
                data: str = f.read()
            return (True, data)
        except OSError as e:
            return (False, str(e))
    else:
        try:
            with open(filename, "w") as f:
                f.write(content)
            return (True, "Content successfully written to file")
        except OSError as e:
            return (False, str(e))


if __name__ == "__main__":
    print("=== Cyber Archives Security ===\n")

    print("Using 'secure_archive' to read from a nonexistent file:")
    result = secure_archive("/not/existing/file")
    print(result)
    print()

    print("Using 'secure_archive' to read from an inaccessible file:")
    result = secure_archive("/etc/shadow")
    print(result)
    print()

    print("Using 'secure_archive' to read from a regular file:")
    success, data = secure_archive("ancient_fragment.txt")
    print((success, data))
    print()

    if success:
        print("Using 'secure_archive' to write previous content to a new file:")
        result2 = secure_archive("vault_copy.txt", action=1, content=data)
        print(result2)
